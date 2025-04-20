# 专利权利要求检查工具

这是一个基于Web的专利权利要求检查工具，用于自动分析专利权利要求书中的常见问题。

## 功能特点

- DOCX到Markdown的转换
- 使用pix2text识别文档中的数学公式
- 支持多种AI API进行智能分析（DeepSeek、Moonshot、百川等）
- 可自定义API配置参数（API密钥、基础URL、模型）
- 实时进度显示
- 美观的用户界面

## 主要检查项目

1. 权利要求引用关系检查
2. 公式符号定义检查
3. 句号使用检查
4. 多项从属权利要求引用检查
5. 非择一情形检查
6. 引用基础分析
7. 附图标记一致性检查
8. 附图标记括号检查

## 安装说明

1. 克隆项目
```bash
git clone [项目地址]
cd [项目目录]
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
python run.py
```

## 使用说明

1. 访问 http://localhost:5000
2. 点击右上角的齿轮图标，打开设置面板
3. 填写API密钥、API基础URL和模型（已提供常用选项）
4. 点击“保存设置”按钮
5. 上传权利要求文件（DOCX格式）
6. 点击“开始分析”按钮
7. 等待分析结果
8. 查看分析报告，包括问题统计和详细分析

## 技术栈

- 后端：Flask
- 前端：Alpine.js + Tailwind CSS
- 文档处理：python-docx + pix2text
- AI分析：支持多种OpenAI兼容的API（DeepSeek、Moonshot、百川等）

## 注意事项

- 需要有效的API密钥（支持多种API源）
- 仅支持DOCX格式文件
- 建议使用Chrome或Firefox浏览器

## 支持的API源

工具默认支持以下中国可访问的API源：

- https://ark.cn-beijing.volces.com/api/v3（默认）
- https://api.moonshot.cn/v1（Moonshot AI）
- https://api.baichuan-ai.com/v1（百川）
- https://api.minimax.chat/v1（MiniMax）

## 常用模型

工具支持以下常用模型：
- doubao-1.5-pro-256k-250115（默认）
- doubao-1-5-pro-32k-250115
- deepseek-chat
- moonshot-v1-8k
- Baichuan3-Turbo

## 作者

- 乐乐
- 微信：lidaen_
- GitHub：[lidaen001](https://github.com/lidaen001)