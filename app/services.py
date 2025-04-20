import os
import logging
from docx import Document
from pix2text import Pix2Text
from openai import OpenAI
import json
import re
import zipfile
import shutil
from pathlib import Path
import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_images_from_docx(docx_path, extract_path):
    """
    从DOCX文件中提取图片
    """
    try:
        # 创建临时目录
        os.makedirs(extract_path, exist_ok=True)

        # 将.docx文件复制到一个临时文件
        temp_docx = os.path.join(extract_path, 'temp.docx')
        shutil.copy2(docx_path, temp_docx)

        # 将.docx文件当作zip文件打开
        with zipfile.ZipFile(temp_docx, 'r') as zip_ref:
            # 提取所有图片文件
            for file in zip_ref.namelist():
                if file.startswith('word/media/'):
                    zip_ref.extract(file, extract_path)

        # 删除临时docx文件
        os.remove(temp_docx)

        # 返回提取的图片目录
        return os.path.join(extract_path, 'word/media')
    except Exception as e:
        logger.error(f"提取图片时出错: {str(e)}")
        raise

def process_docx(filepath):
    """
    处理DOCX文件，提取文本和图片，转换为Markdown格式

    使用中间结构来保持文档元素的顺序和关系：
    - 文本块直接存储其内容
    - 图片块存储其引用ID，以便后续处理
    """
    try:
        logger.info(f"开始处理文件: {filepath}")
        doc = Document(filepath)
        p2t = Pix2Text.from_config()

        # 创建临时目录用于存储提取的图片
        temp_dir = os.path.join(os.path.dirname(filepath), 'temp_images')

        try:
            # 提取图片
            logger.info("从DOCX中提取图片")
            media_path = extract_images_from_docx(filepath, temp_dir)

            # 创建中间结构来存储文档内容
            document_structure = []

            # 创建图片引用映射，用于快速查找图片信息
            image_refs = {}
            for rel in doc.part.rels.values():
                if "image" in rel.reltype:
                    image_refs[rel.rId] = {
                        'filename': os.path.basename(rel.target_ref),
                        'processed': False
                    }

            logger.info("构建文档结构")
            for para in doc.paragraphs:
                # 检查段落中是否包含图片
                has_image = False
                para_content = []

                for run in para.runs:
                    # 检查run中的所有图片引用
                    for element in run._element:
                        if element.tag.endswith('drawing'):
                            # 提取图片的rId
                            rId = None
                            for inline in element.findall('.//a:blip', {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}):
                                rId = inline.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                                if rId:
                                    has_image = True
                                    para_content.append({
                                        'type': 'image',
                                        'rId': rId
                                    })

                    # 添加文本内容
                    if run.text.strip():
                        para_content.append({
                            'type': 'text',
                            'content': run.text
                        })

                # 如果段落不为空，添加到文档结构中
                if para_content:
                    document_structure.append(para_content)

            logger.info("处理文档中的图片")
            # 处理所有图片并更新文档结构
            markdown_parts = []
            for para_content in document_structure:
                para_parts = []
                for element in para_content:
                    if element['type'] == 'text':
                        para_parts.append(element['content'])
                    elif element['type'] == 'image':
                        rId = element['rId']
                        if rId in image_refs and not image_refs[rId]['processed']:
                            image_filename = image_refs[rId]['filename']
                            image_path = os.path.join(media_path, image_filename)

                            if os.path.exists(image_path):
                                logger.info(f"处理图片: {image_path}")
                                try:
                                    # 使用pix2text识别图片中的公式
                                    formula_result = p2t.recognize_formula(image_path)
                                    if formula_result:
                                        para_parts.append(f"$${formula_result}$$")
                                    image_refs[rId]['processed'] = True
                                except Exception as e:
                                    logger.error(f"处理图片时出错: {str(e)}")
                            else:
                                logger.warning(f"图片文件不存在: {image_path}")

                if para_parts:
                    markdown_parts.append("".join(para_parts))

            return "\n".join(markdown_parts)

        finally:
            # 清理临时文件
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    except Exception as e:
        logger.error(f"处理DOCX文件时出错: {str(e)}")
        raise Exception(f"处理文件时出错: {str(e)}")

def analyze_claims(markdown_text, api_key, base_url="https://ark.cn-beijing.volces.com/api/v3", model="doubao-1.5-pro-256k-250115", debug=True):
    """
    使用DeepSeek API分析权利要求

    Args:
        markdown_text (str): 要分析的markdown文本
        api_key (str): DeepSeek API密钥
        base_url (str): API的基础URL，默认为"https://ark.cn-beijing.volces.com/api/v3"
        model (str): 使用的模型，默认为"doubao-1.5-pro-256k-250115"
        debug (bool): 是否开启调试模式，开启后会保存中间文件
    """
    try:
        logger.info("初始化DeepSeek API客户端")
        # 创建 OpenAI 客户端，使用用户指定的参数
        import httpx
        http_client = httpx.Client()
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=http_client
        )
        logger.info(f"使用API基础URL: {base_url}")
        logger.info(f"使用模型: {model}")
        # 如果是调试模式，保存输入的markdown文本
        if debug:
            debug_dir = "debug_output"
            os.makedirs(debug_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # 保存输入的markdown文本
            with open(os.path.join(debug_dir, f"{timestamp}_input.md"), "w", encoding="utf-8") as f:
                f.write(markdown_text)

        system_prompt = """
        你是一个专业的专利权利要求文本分析助手。请分析以下权利要求文本，并按照JSON格式返回分析结果。

        在分析过程中，请注意：
        1. 所有数学符号和公式必须使用LaTeX格式表示，例如：
           - 希腊字母：\\alpha, \\beta, \\gamma 等
           - 上标：x^2, y^{n+1}
           - 下标：x_1, y_{i,j}
           - 分数：\\frac{a}{b}
           - 求和：\\sum_{i=1}^n
           - 积分：\\int_{a}^b
        2. 在描述问题时，如果涉及数学符号，应该使用 $ 符号包裹LaTeX表达式，例如：
           "符号 $\\alpha$ 在权利要求2及其引用的权利要求中未定义"
        3. 符号定义检查需满足：
           (a) 检查范围包含文本描述和数学公式中的所有符号，包括但不限于变量、参数
           (b) 必须追溯当前权利要求的全部引用链（直接引用和间接引用）
           (c) 若符号在多个权利要求中重复出现，定义必须一致


        对于每一项权利要求，需要检查的问题包括：
        1. 权利要求引用关系，检查权利要求引用了自身或者引用了序号比自身大的权利要求的错误，如果出现，则认为该权利要求引用错误，如果此项出现问题，则以下第7、8项检查忽略
        2. 出现多余句号，每项权利要求中只允许一个句号且在句尾，检查权利要求中是否出现多余句号，如果出现，则认为该权利要求出现多余句号错误
        3. 多项从属权利要求引用，检查是否出现多项从属权利要求引用多项从属权利要求的情况，如果出现，则认为该权利要求出现多引多错误
        4. 非择一情形，检查是否出现非择一情形，如果出现，则认为该权利要求出现非择一错误
        5. 附图标记一致性，检查相同的特征对应不同的附图标记，以及相同的附图标记对应了不同的特征的错误，如果出现，则认为该权利要求出现附图标记一致性错误
        6. 附图标记括号，检查附图标记是否有被括号包裹，如果出现，则认为该权利要求出现附图标记括号错误
        7. 引用基础，如果有权利要求引用错误，此项忽略，否则检查带"所述"或者“所述的”前缀的技术特征是否在其前面或其引用的权利要求中出现过，如果没有引用基础，则认为该技术特征没有引用基础
        8. 公式符号定义，如果有权利要求引用错误，此项忽略，否则检查所有公式中的符号在当前权利要求或其引用的权利要求是否有被定义，如果出现没有被定义的符号，则认为该符号没有被定义
        
        请确保返回的JSON格式如下：
        {
            "claims_analysis": [
                {
                    "claim_number": "权利要求编号",
                    "issues": [
                        {
                            "type": "问题类型",
                            "description": "问题描述（如涉及数学符号，请在此处直接包含相关符号信息）",
                            "location": "问题位置"
                        }
                    ]
                }
            ],
            "summary": {
                "total_issues": "总问题数",
                "issue_types": {
                    "type1": "数量",
                    "type2": "数量"
                }
            }
        }
        """

        logger.info("发送API请求")
        response = client.chat.completions.create(
            model=model,
            # 可选模型示例：
            # doubao-1-5-pro-32k-250115
            # deepseek-chat
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": markdown_text}
            ],
            temperature=0.2,
            top_p=0.3
            # 设置temperature参数，取值范围通常为0到2之间
            # response_format 参数在当前版本不支持，已移除
        )

        logger.info("解析API响应")
        raw_response = response.choices[0].message.content

        # 如果是调试模式，先保存原始API响应，无论解析是否成功
        if debug:
            # 保存原始API响应
            with open(os.path.join(debug_dir, f"{timestamp}_raw_response.txt"), "w", encoding="utf-8") as f:
                f.write(raw_response)

        # 预处理JSON字符串，处理LaTeX转义序列
        # 在JSON中，反斜杠是转义字符，需要将LaTeX命令中的反斜杠转义
        processed_response = raw_response

        # 如果是调试模式，保存处理前的原始响应
        if debug:
            with open(os.path.join(debug_dir, f"{timestamp}_raw_response_before_process.txt"), "w", encoding="utf-8") as f:
                f.write(raw_response)

        # 尝试解析JSON
        try:
            # 先尝试直接解析
            try:
                result = json.loads(processed_response)
            except json.JSONDecodeError:
                # 如果直接解析失败，尝试处理LaTeX转义序列
                # 采用更简单的方法：将所有反斜杠都变成双反斜杠
                processed_response = processed_response.replace('\\', '\\\\')

                # 如果是调试模式，保存处理后的响应
                if debug:
                    with open(os.path.join(debug_dir, f"{timestamp}_processed_response.txt"), "w", encoding="utf-8") as f:
                        f.write(processed_response)

                # 尝试解析处理后的JSON
                result = json.loads(processed_response)

            # 如果解析成功且是调试模式，保存格式化后的结果
            if debug:
                with open(os.path.join(debug_dir, f"{timestamp}_parsed_result.json"), "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {str(e)}")
            # 如果是调试模式，保存错误信息
            if debug:
                with open(os.path.join(debug_dir, f"{timestamp}_json_error.txt"), "w", encoding="utf-8") as f:
                    f.write(f"JSON解析错误: {str(e)}\n\n原始响应:\n{raw_response}")
            raise

        logger.info(f"分析完成，发现 {result['summary']['total_issues']} 个问题")
        return result

    except json.JSONDecodeError as e:
        error_msg = f"API响应解析失败: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)
    except Exception as e:
        logger.error(f"分析权利要求时出错: {str(e)}")
        raise Exception(f"分析权利要求时出错: {str(e)}")