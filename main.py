from tkinter import *
import random

class Tile():


    def __init__(self, x, y, num):

        self.x = x
        self.y = y
        self.winSize = winSize
        self.num = num
        self.marked = False

        startx = x*tileSize + offset
        starty = y*tileSize + offset
        endx = (x+1)*tileSize + offset
        endy = (y+1)*tileSize + offset

        self.tile = canvas.create_rectangle(startx, starty, endx, endy, fill="white")
        self.number = canvas.create_text(startx+tileSize/2, starty+tileSize/2,
        font="Times 20 bold", text=str(self.num))

    def getPos(self):
        return self.x, self.y

    def setPos(self, x, y):

        dx = tileSize*(x-self.x)
        dy = tileSize*(y-self.y)

        canvas.move(self.tile, dx, dy)
        canvas.move(self.number, dx, dy)

        self.x = x
        self.y = y



    def setMarked(self, bo):
        self.marked = bo
        if self.marked:
            canvas.itemconfig(self.tile, fill="gray")
        else:
            canvas.itemconfig(self.tile, fill="white")


def numberOfInv(tiles):
    inv = 0
    for i in range(0, len(tiles)-1):
        if tiles[i].num > tiles[i+1].num:
            inv+=1

    return inv

def isSolvable(tiles):

    if tiles == []: return False

    inv = numberOfInv(tiles)
    print(inv)
    if inv % 2 == 0:
        return True
    else:
        return False

root = Tk()
root.title("Fifteen")
root.resizable(False, False)

winSize = 600

canvas = Canvas(root, width=winSize, height=winSize)
canvas.config(background='black')
canvas.pack()


tileSize = 100
offset = (winSize-4*tileSize)/2


while True:
    n = 1
    tiles = []
    numbers = random.sample(range(1, 16), 15)

    for j in range(4):
        for i in range(4):
            if n==16: break

            tiles.append(Tile(i, j, numbers[n-1]))

            n+=1

    if isSolvable(tiles): break


def correctList(cM):
    global tiles

    temp = []
    n = 0
    for j in range(4):
        for i in range(4):
            if [i, j] != cM:
                for obj in tiles:
                    if obj.x == i and obj.y == j:
                        temp.append(obj)
    tiles = temp


cM = [3, 3]
markedTile=None

def leftClick(event):

    global cM
    global markedTile

    insideTest1 = event.x>=offset and event.y>=offset
    insideTest2 = event.x<(winSize-offset) and event.y<(winSize-offset)

    if insideTest1 and insideTest2:

        currentX = int((event.x-offset)/tileSize)
        currentY =int((event.y-offset)/tileSize)

        currentTile=None
        for obj in tiles:
            if obj.x==currentX and obj.y==currentY:
                currentTile = obj
                break

        if markedTile==None and currentTile !=None: #Markera
            x = currentTile.x
            y = currentTile.y
            xTest = x-1==cM[0] or x==cM[0] or x+1==cM[0]
            yTest = y-1==cM[1] or y==cM[1] or y+1==cM[1]

            cornerTest = [[x+1, y-1]==cM, [x-1, y+1]==cM]
            cornerTest.append([x+1, y+1]==cM)
            cornerTest.append([x-1, y-1]==cM)

            if xTest and yTest and not any(cornerTest):
                if currentTile.marked:
                    currentTile.setMarked(False)
                    markedTile = None
                else:
                    currentTile.setMarked(True)
                    markedTile = currentTile
        elif markedTile!=None and currentTile==None: #Flytta
            cM = [markedTile.x, markedTile.y]
            markedTile.setPos(currentX, currentY)
            markedTile.setMarked(False)
            markedTile = None

            correctList(cM)

        elif markedTile!=None and currentTile!=None: #Avmarkera
            markedTile.setMarked(False)
            markedTile=None


canvas.bind("<Button-1>", leftClick)
root.mainloop()
