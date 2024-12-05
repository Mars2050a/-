from PIL import Image

# 打开PNG文件
png_path = 'D:/PyCharm/Py_projects/Python GUI设计/hsd.ico'
ico_path = 'output_icon.ico'

# 使用Pillow打开图像
img = Image.open(png_path)

# 保存为ICO格式，同时指定图标的尺寸
img.save(ico_path, format='ICO', sizes=[(200, 200), (200, 200), (400, 400)])