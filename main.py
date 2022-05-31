import png
from tqdm import tqdm
import colorsys
import json

with open("config.json") as config_file: #open the config file and import settings
    config = json.load(config_file)

thres = config["thres"]
max_ittr = config["max_ittr"]
hue_offset = config["hue_offset"]

equationMax = config["equationMax"]
equationMin = config["equationMin"]

greyscale = config["greyscale"]

cnvs_x_start = config["cnvs_x_start"]
cnvs_x_end = config["cnvs_x_end"]

cnvs_y_start = config["cnvs_y_start"]
cnvs_y_end = config["cnvs_y_end"]

cnvs_ittr = config["cnvs_ittr"]

thres_squared = thres**2 #used later, saves time and reducec repeated calculations

def z(c): #returns the number of times taken for complex number [c] to go unbounded (exceed thres)
    z = 0
    for i in range(max_ittr):
        y_squared = z.real**2 + z.imag**2
        if y_squared > thres_squared:
            return i
        z = z ** 2 + c
    return 0 #if after all the itterations the number is still below the thres, return 0. this means it is inside the set

if greyscale == False:
    hueMax = 1 #the hue in colorsys goes from 0 to 1
else:
    hueMax = 255

hueMin = 0

def calculate_pxl(c): #calculates pixel shade/hue
    x = z(c)
    
    equationSpan = equationMax - equationMin
    shadeSpan = hueMax - hueMin

    # Convert the equation range into a 0-1 range (float)
    valueScaled = float(x - equationMin) / float(equationSpan)

    # Convert the 0-1 range into a value in the shade range.
    return hueMin + (valueScaled * shadeSpan)
    
list = [] #init canvas list

y = cnvs_y_start #init x,y complex plane pointers
x = cnvs_x_start

#used as ints to stop floating point error
num_rows = int((cnvs_y_end - cnvs_y_start)/cnvs_ittr) 
num_cols = int((cnvs_x_end - cnvs_x_start)/cnvs_ittr)

print("Starting render of mandelbrot") #print info
print("Resolution: {} x {}\n".format(num_cols, num_rows))

while __name__ == "__main__":
    with tqdm(total=(cnvs_y_end-cnvs_y_start)/cnvs_ittr, desc="Progress", bar_format="{l_bar}{bar}| Col {n_fmt} of {total_fmt} [{elapsed}<{remaining}]", leave=False) as pbar: #start progress bar
        if greyscale == True:
            row = 0
            while row < num_rows:
                list.append([])
                col = 0
                while col < num_cols:
                    outside_set = 1
                    h = calculate_pxl(complex(x, y))
                    if h == 0:
                        outside_set = 0
                    h += hue_offset
    
                    list[row].append(int(h))
        
                    x += cnvs_ittr
                    col += 1
                x = cnvs_x_start
                y += cnvs_ittr
                pbar.update(1)
                row += 1
    
    
        if greyscale == False:
            row = 0
            while row < num_rows:
                list.append([])
                col = 0
                while col < num_cols:
                    outside_set = 1
                    h = calculate_pxl(complex(x, y))
                    if h == 0:
                        outside_set = 0
                    h += hue_offset
                    (r, g, b) = colorsys.hsv_to_rgb(h, 1, outside_set)
                    (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
        
                    list[row].append(r)
                    list[row].append(g)
                    list[row].append(b)
        
                    x += cnvs_ittr
                    col += 1
                x = cnvs_x_start
                y += cnvs_ittr
                pbar.update(1)
                row += 1
    
    print("MANDELBROT RENDER COMPLETE IN {} (MM:SS)".format(pbar.format_interval(pbar.format_dict["elapsed"])))
    
    if greyscale == True:
        cnvs_width = int(len(list[0]))
    else:
        cnvs_width = int(len(list[0])/3)
    
    cnvs_height = int(len(list))
    
    f = open("output.png", "wb") # binary mode is important
    w = png.Writer(cnvs_width, cnvs_height, greyscale = greyscale)
    w.write(f, list)
    f.close()
