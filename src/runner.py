from PIL import Image, ImageDraw
import matplotlib.pyplot as plt # plt 用于显示图片

scale = 10
width = 101*scale
height = 101*scale

def make_pip(lister):
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    for u in lister.values():
        if u.flag==0:
            if u.Get_unit_type()==4 or u.Get_unit_type()==0:
                draw.rectangle((u.position[0]*scale, u.position[1]*scale, u.position[0]*scale+9, u.position[1]*scale+9),fill ="blue")
            else:
                draw.rectangle((u.position[0]*scale, u.position[1]*scale, u.position[0]*scale + 9, u.position[1]*scale + 9), outline="blue")
        if u.flag == 1:
            if u.Get_unit_type() == 4 or u.Get_unit_type()==0:
                draw.rectangle((u.position[0]*scale, u.position[1]*scale, u.position[0]*scale + 9, u.position[1]*scale + 9), fill="red")
            else:
                draw.rectangle((u.position[0]*scale, u.position[1]*scale, u.position[0]*scale + 9, u.position[1]*scale + 9), outline="red")
        if u.flag == -1:
            if u.Get_unit_type() == 4 or u.Get_unit_type()==0:
                draw.rectangle((u.position[0]*scale, u.position[1]*scale, u.position[0]*scale + 9, u.position[1]*scale + 9), fill="grey")
            else:
                draw.rectangle((u.position[0]*scale, u.position[1]*scale, u.position[0]*scale + 9, u.position[1]*scale + 9), outline="grey")
    plt.imshow(image)  # 显示图片
    plt.axis('off')  # 不显示坐标轴
    plt.show()