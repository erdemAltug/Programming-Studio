import PIL.Image
from PIL import Image
from tkinter.colorchooser import askcolor
import PIL.ImageTk
from PIL import *
from tkinter import *
import tkinter.filedialog
from tkinter.colorchooser import askcolor
import glob
from tkinter import Menu,scrolledtext,messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import colorchooser

choosenColor=(0,0,0)
root= Tk()

def main():
    global root

    root.title("Online Coloring")
    root.geometry("1000x800")

    root.config(bg="purple")
    menu_bar = Menu(root)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Add Image!", command=openFile)
    file_menu.add_command(label="Save Image!", command=AskSaveasFilename)
    file_menu.add_command(label="End!", command=root.destroy)
    file_menu.add_command(label="Change Colour",command=change_colour)
    menu_bar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu_bar)
    file_menu.config(bg="green")

    pickColor = Button(root, text='Pick Color', command=getColor)
    pickColor.grid(row=300, column=300)
    pickColor.config(bg="gray")

    root.mainloop()
    
def getColor():
    color = askcolor()
    color = str(color)
    top = color.index("((")
    end = color.index("),")
    color = color[(top):end]
    color = color[2:len(color)]
    r, g, b = color.split(",")
    global choosenColor
    choosenColor = float(r),float(g),float(b)
    choosenColor = int(float(r)), int(float(g)), int(float(b))
    print("choosenColor is :", choosenColor)

def openFile():
    file_path_string = tkinter.filedialog.askopenfilename()
    # drawingImage=Image.open(file_path_string)
    fp = open(file_path_string, 'rb')
    global drawingImage
    drawingImage = PIL.Image.open(fp)
    global pix
    pix = drawingImage.load()
    global rowSize, columnSize
    rowSize,columnSize = drawingImage.size

    for i in range(rowSize):
        for j in range(columnSize):
            pix[i, j] = vanishNoisesFromPixel(pix[i, j])

    pixelValues = [[0 for x in range(columnSize)] for y in range(rowSize)]
    for i in range(rowSize):
        for j in range(columnSize):
            pixelValues[i][j] = converToBinaryValue(pix[i, j])

    for i in range(rowSize):
        for j in range(columnSize):
            if i == 0 or j == 0 or i == rowSize - 1 or j == columnSize - 1:
                pixelValues[i][j] = 0

    print("\n\n\n\nbefore labeling pixelValues matrix look like")

    for j in range(columnSize):
        for i in range(rowSize):
            print(pixelValues[i][j], )
        print("  ")
    global labelValues
    labelValues = [[0 for x in range(columnSize)] for y in range(rowSize)]

    for i in range(rowSize):
        for j in range(columnSize):
            labelValues[i][j] = 0
    labelCounter = 2

    for i in range(1, rowSize - 1):
        for j in range(1, columnSize - 1):
            if pixelValues[i][j] == 1:
                if pixelValues[i - 1][j] == 1 and pixelValues[i][j - 1] == 1:
                    if labelValues[i - 1][j] == labelValues[i][j - 1]:
                        labelValues[i][j] = labelValues[i][j - 1]
                    else:
                        labelValues[i][j] = labelValues[i - 1][j]
                        for t in range(0, i + 1):
                            for k in range(0, j + 1):
                                if labelValues[t][k] == labelValues[i][j - 1]:
                                    labelValues[t][k] = labelValues[i - 1][j]
                elif pixelValues[i - 1][j] == 1 or pixelValues[i][j - 1] == 1:
                    if pixelValues[i - 1][j] == 1:
                        labelValues[i][j] = labelValues[i - 1][j]
                    else:
                        labelValues[i][j] = labelValues[i][j - 1]
                else:
                    labelValues[i][j] = labelCounter
                    labelCounter += 1
            else:
                labelValues[i][j] = 1  # means blacks labels is one
    print("**********")
    print("After labelling")
    for j in range(columnSize):
        for i in range(rowSize):
            print(labelValues[i][j])
        print(" ")

    for i in range(rowSize):
        for j in range(columnSize):
            pix[i, j] = vanishNoisesFromPixel(pix[i, j])

    addToScreen(drawingImage)

def AskSaveasFilename():
    drawingImage.save("D:\\EagleGet\\saved.png")


def addToScreen(Img):
    render = ImageTk.PhotoImage(Img)
    img = Label(root, image=render)
    img.image = render
    img.place(x=150, y=50)
    img.bind("<Button-1>", printCoords)

def printCoords(event):
    paintReagion(event.x,event.y)

def paintReagion(x,y):
    global choosenColor
    print("coordinate is", (x,y))

    for i in range(rowSize):
        for j in range(columnSize):
            if labelValues[i][j] == labelValues[x][y]:
                pix[i,j] = choosenColor
    render=ImageTk.PhotoImage(drawingImage)
    img=Label(root,image=render)
    img.image=render
    img.place(x=150,y=50)
    img.bind("<Button-1>",printcoords)

def vanishNoisesFromPixel(rgbValues):
    # some pictures has another information that's the blur affect r,g,b,and F
    # but we are interested in only R,G,B values to clean noise
    if len(rgbValues) == 4:
        r, g, b, f = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average > 200:
        return 255, 255, 255
    return 0, 0, 0

def converToBinaryValue(rgbValues):
    if len(rgbValues) == 4:
        r, g, b, f = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average == 255:
        return 1  # means white
    return 0  # means black


if __name__ == '__main__':
    main()
