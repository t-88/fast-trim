#!/usr/bin/env python3
from PIL import Image
import sys


width, height = -1, -1
pixels  = []

def addPadding(im,padding):
    if padding["left"] == padding["right"] == padding["top"] == padding["bottom"] == 0:
        return im
    out = Image.new("RGBA",(im.width + padding["right"]+padding["left"],im.height + padding["bottom"]+padding["top"]),(0,0,0,0))
    out.paste(im,(padding["left"],padding["right"]))
    return out

def topBound():
    for y in range(height):
        for x in range(width):
            if pixels[y * width + x] != 0:
                return y
def bottomBound():
    for y in range(height-1,-1,-1):
        for x in range(width):
            if pixels[y * width + x] != 0:
                return y  
def leftBound():
    left = width
    for y in range(height):
        for x in range(0,left):
            pixel_alpha = pixels[y * width + x]
            if pixel_alpha != 0 and left > x: 
                left = x
                break
    return left
def rightBound():
    right = 0
    for y in range(height):
        for x in range(width - 1, right - 1 , -1):
            pixel_alpha = pixels[y * width + x]
            if pixel_alpha != 0 and right <= x: 
                right = x
                break
    return right

def trim(in_fn,out_fn,padding):
    global width, height
    global pixels

    im = Image.open(in_fn, 'r')

    im_alpha = im.split()[-1]
    width, height = im_alpha.size
    pixels = list(im_alpha.getdata())

    # get bounds
    top = topBound()
    bottom = bottomBound()
    left = leftBound()
    right = rightBound()


    cropped = addPadding(im.crop((left,top,right,bottom)),padding)
    cropped.save(out_fn)



def help():
    print("help:")
    print(" help: prints help")
    print(" [input] [output] [-padding=top,right,bottom,left]: trims img with optional padding")
def main():

    args = sys.argv
    args.pop(0) # remove file name arg

    if len(args) == 1 and args[0] == "help":
        help()
    elif len(args) < 2:
       print("Error: missing params, you need at least input and output file names") 
       help()
    else:
        padding = {"left":0,"right": 0,"top":0,"bottom": 0}
        for  idx, arg in enumerate(args): 
            if arg.find("-padding=") == 0:
                data = arg.removeprefix("-padding=").strip().split(",")
                if len(data) != 4: 
                    print("Error: expected top,left,bottom,right got less or more then that")
                    help()
                    return
                padding["top"] = int(data[0])
                padding["right"] = int(data[1])
                padding["bottom"] = int(data[2])
                padding["left"] = int(data[3])
                args.pop(idx)
                break
        in_fn = sys.argv[0]
        out_fn = sys.argv[1]
        trim(in_fn,out_fn,padding)


if __name__ == "__main__":
    main()