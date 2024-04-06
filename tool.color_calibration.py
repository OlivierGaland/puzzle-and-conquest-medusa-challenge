from PIL import Image,ImageDraw
from enum import Enum

class Color(Enum):
    Purple = ([123, 39, 202],[169, 84, 248])
    DarkGreen = ([2, 85, 84],[46, 132, 133])
    LightBlue = ([71, 152, 218],[116, 197, 265])
    Orange = ([222, 124, 24],[267, 172, 83])
    Blue = ([-5, 80, 204],[40, 127, 253])
    Yellow = ([219, 169, -10],[265, 216, 50])
    Pink = ([205, 134, 209],[252, 187, 259])
    Cream = ([233, 193, 165],[275, 240, 217])
    Red = ([166, 7, -2],[212, 52, 45])
    DarkRed = ([84, 8, 34],[131, 51, 80])
    Green = ([54, 169, 23],[108, 217, 80])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Garbage Program to check manually pictures and extract color boundaries to setup Color Enum
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


image = Image.open("./img/pic001.orig.jpg")  # 1080 x 2400
image_rgb = image.convert("RGB")
red = (255,0,0)

#rect = ((140,520),(180,560)) #purple
#rect = ((140,605),(180,645)) #dark green
#rect = ((140,690),(180,730)) #light blue
#rect = ((140,775),(180,815)) #orange
#rect = ((300,520),(340,560)) #blue
#rect = ((460,520),(500,560)) #yellow
#rect = ((460,690),(500,730)) #pink
#rect = ((460,775),(500,815)) #cream
#rect = ((610,605),(650,645)) #red
#rect = ((610,690),(650,730)) #dark red

#rect = ((760,775),(800,815)) #green

#rect = ((325,510),(340,525)) #darkblue
rect = ((636,592),(651,607)) #Grey


# Check graphically if rectangle is correctly placed on the pic for scan
if False:
    draw = ImageDraw.Draw(image_rgb)
    draw.rectangle(rect,fill=(255,0,0))
    image_rgb.show()
    exit(0)

min_rgb = [255,255,255]
max_rgb = [0,0,0]
for i in range(rect[0][0],rect[1][0]):
    for j in range(rect[0][1],rect[1][1]):
        rgb = image_rgb.getpixel((i,j))
        if min_rgb[0] > rgb[0]: min_rgb[0] = rgb[0]
        if max_rgb[0] < rgb[0]: max_rgb[0] = rgb[0]
        if min_rgb[1] > rgb[1]: min_rgb[1] = rgb[1]
        if max_rgb[1] < rgb[1]: max_rgb[1] = rgb[1]
        if min_rgb[2] > rgb[2]: min_rgb[2] = rgb[2]
        if max_rgb[2] < rgb[2]: max_rgb[2] = rgb[2]

#rgb_pixel_value = image_rgb.getpixel((10,15))

tol=20   # tolerance : 10 is too little, 20 seems correct

min_rgb = [min_rgb[0]-tol,min_rgb[1]-tol,min_rgb[2]-tol]
max_rgb = [max_rgb[0]+tol,max_rgb[1]+tol,max_rgb[2]+tol]

print("("+str(min_rgb) + "," + str(max_rgb)+")")

for x in range(image.size[0]):
    for y in range(image.size[1]):
        rgb = image_rgb.getpixel((x,y))
        if rgb[0] >= min_rgb[0] and rgb[1] >= min_rgb[1] and rgb[2] >= min_rgb[2]:
            if rgb[0] <= max_rgb[0] and rgb[1] <= max_rgb[1] and rgb[2] <= max_rgb[2]:
                image_rgb.putpixel((x,y),red)

image_rgb.show()