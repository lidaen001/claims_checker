from flask import Blueprint, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from .services import process_docx, analyze_claims

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static/images'), filename)

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400

    file = request.files['file']
    api_key = request.form.get('api_key')
    base_url = request.form.get('base_url', 'https://ark.cn-beijing.volces.com/api/v3')
    model = request.form.get('model', 'doubao-1-5-pro-32k-250115')

    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    if not api_key:
        return jsonify({'error': '缺少API密钥'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # 确保上传目录存在
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # 处理文档并分析权利要求
            markdown_text = process_docx(filepath)
            analysis_results = analyze_claims(markdown_text, api_key, base_url, model)

            # 清理临时文件
            os.remove(filepath)

            return jsonify(analysis_results)

        except Exception as e:
            # 确保即使发生错误也清理临时文件
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': '不支持的文件类型'}), 400