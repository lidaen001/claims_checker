from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 注册蓝图
    from .routes import main
    app.register_blueprint(main)
    
    return app 