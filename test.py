from pix2text import Pix2Text

# 初始化 Pix2Text 实例
p2t = Pix2Text.from_config()

# 定义待识别的图片路径
img_fp = '/Users/lidaen/权利要求 2_副本/word/media/image7.jpeg'

# 调用 recognize_text 函数进行识别
try:
    result1 = p2t.recognize_text_formula(img_fp)
    print("识别结果如下:")
    print(result1)
    print("--------------------------------")
    result2 = p2t.recognize_text(img_fp)
    print("识别结果如下:")
    print(result2)
except Exception as e:
    print(f"识别过程中出现错误: {e}")