from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from urllib.request import urlopen
import io
import json
from mergesort import sortTree, merge
import time
from operator import itemgetter

IMG_SIZE = 'normal'
TYPELINE_WIDTH = 35
NAME_WIDTH = 50 
MANA_WIDTH = 15
URL = 'https://c1.scryfall.com/file/scryfall-cards/png/front/b/7/b768efa2-e56b-4a7e-ace8-d673f10e0714.png?1562880960'

# Load full card list from scryfall dump
oracleFile = open('JSON\oracle-cards.json', 'r', encoding="utf8")
oracleDB = json.load(oracleFile)
oracleDB = sorted(oracleDB, key=itemgetter('name')) 


# Initialize Tkinter Window
root = Tk()
root.resizable(width = 1, height = 1)
root.title("QuickSilver")

import tkinter as tk
from tkinter import ttk

#Paned Window to store frames
pWin = ttk.PanedWindow(root, orient = HORIZONTAL)
pWin.pack(fill = BOTH, expand = True)

style = ttk.Style()
style.theme_use('classic')
style.configure("pWin")

# Paned Window to store decklist and cardimg
rightFrame = ttk.Frame(pWin)
rightFrame.pack(side = RIGHT, fill = BOTH, expand = True)
pWin.add(rightFrame)

pRight = ttk.PanedWindow(rightFrame, orient = VERTICAL)
pRight.pack(fill = BOTH, expand = True, side = RIGHT)

style = ttk.Style()
style.theme_use('classic')
style.configure("pWin")

# Initialize Card Viewer Window
cardViewer = ttk.Frame(pRight)
cardViewer.pack(side = TOP, fill = BOTH, expand = True)
pRight.add(cardViewer)

# Store Current Card Name
cardName = StringVar()

def searchDB(cardName):
    for card in oracleDB:
        if card["name"].upper() == cardName.upper():
            return card
    print('Card not found')
    return -1

# Check all listboxes for selected card
def select(*args):
    widget = root.focus_get()
    if type(widget) is ttk.Treeview:
        iid = widget.focus()
        if widget.item(iid)["values"]:
            displayCard(searchDB(widget.item(iid)["values"][0]))
    elif type(widget) is ttk.Entry:
        iid = dbTree.focus()
        if dbTree.item(iid)["values"]:
            displayCard(searchDB(dbTree.item(iid)["values"][0]))

# Initialize decklist
deck = []

# Return position in deck, -1 if not in deck
def inDeck(name):
    cursor = 0
    for card in deck:
        if card["CO"]["name"].upper() == name.upper():
            return cursor
        cursor = cursor + 1
    return -1

# Reload List Into Display
def reload(*args):
    cat1List.delete(*cat1List.get_children())
    cat12List.delete(0, END)
    cat13List.delete(0, END)
    cat2List.delete(0, END)
    cat23List.delete(0, END)
    cat3List.delete(0, END)
    catAllList.delete(0, END)
    for card in deck:
        addToDeck(card)

# Define function to add card to decklist
def addCard(*args):
    name = cardName.get()
    # Fetch card location
    locus = inDeck(name)
    # If card not in deck, add
    if locus == -1:
        CO = searchDB(name)
        if CO == -1:
            return -1
        print(CO)
        deck.append({"CO": CO, "n": 1, "cat1": cat1.get(), "cat2": cat2.get(), "cat3": cat3.get()})
        displayCard(CO)
    # If card is in deck, increase quantity
    else:
        current = deck.pop(locus)
        current["n"] = current["n"] + 1
        current["cat1"] = cat1.get()
        current["cat2"] = cat2.get()
        current["cat3"] = cat3.get()
        deck.append(current)
        displayCard(current["CO"])
    reload()

cardView = ttk.Label(cardViewer)
cardView.pack(fill = BOTH, expand = True)

imgOn = BooleanVar()
imgOn.set(True)

imgMode = ttk.Checkbutton(cardViewer, text = "Display Images?", variable = imgOn, onvalue = True, offvalue = False)
imgMode.pack(side = TOP)


def convertImg(imgURL):
    page = urlopen(imgURL)
    img = io.BytesIO(page.read())
    pilImg = Image.open(img)
    return pilImg

def updateImg(pilImg, w, h):
    img = pilImg.resize((w, h))
    tkImg = ImageTk.PhotoImage(img)
    cardView.configure(image = tkImg)
    cardView.image = tkImg

#Display image with new updated width and height
def displayImg():
    root.update() # refresh widget info
    
    w = cardViewer.winfo_width()
    h = cardViewer.winfo_height()
        
    if w*1.4 < h:
        h = w*1.4
    else:
        w = h*0.71
    
    updateImg(curPil, int(w), int(h))

curPil = convertImg(URL)

lastID = ''

def displayCard(card):
    if imgOn.get() == False:
        print("imgOn no!")
        return
    
    global lastID
    global curPil
    
    ID = card["id"]

    if lastID != ID:
        if "card_faces" in card:
            curPil = convertImg(card["card_faces"][0]["image_uris"][IMG_SIZE])
        else:
            curPil = convertImg(card["image_uris"][IMG_SIZE])
    displayImg()
    lastID = ID

displayImg()

#Frame for all card list browsing
listFrame = ttk.Frame(pWin, padding = 10)
listFrame.pack(expand = True, fill = BOTH, side = LEFT)
pWin.add(listFrame)

#Frame for decklist
deckFrame = ttk.Frame(pRight, padding = 10)
deckFrame.pack(expand = True, fill = BOTH)
pRight.add(deckFrame)

# Create a frame to store input widgets in
inFrame = ttk.Frame(listFrame, padding = 10)
inFrame.pack(side = TOP, fill = X)


## Create a frame to store cards in
#listFrame = ttk.Frame(root, padding = 10)
#listFrame.grid(column = 1, row = 1)

# Create a frame to store full card list in
dbFrame = ttk.Frame(listFrame, padding = 10)
dbFrame.pack(side = BOTTOM, fill = BOTH, expand = True)

# Full card list display
dbTree = ttk.Treeview(dbFrame, columns = ('name', 't', 'mc'), show='headings', selectmode = 'browse')
dbTree.heading('name', text='Name')
dbTree.heading('t', text='Type')
dbTree.heading('mc', text='Mana Cost')
dbTree.pack(side = LEFT, fill = BOTH, expand = True)

dbScroll = ttk.Scrollbar(dbFrame,
                         orient = "vertical",
                         command = dbTree.yview)
dbScroll.pack(side = RIGHT, fill = BOTH)
dbTree.configure(yscrollcommand = dbScroll.set)

# Deck list display
deckTree = ttk.Treeview(deckFrame, columns = ('q', 'name'), show='headings', selectmode = 'browse')
deckTree.heading('q', text='#')
deckTree.heading('name', text='Name')
deckTree.pack(side = LEFT, fill = BOTH, expand = True)

deckScroll = ttk.Scrollbar(deckFrame,
                         orient = "vertical",
                         command = deckTree.yview)
deckScroll.pack(side = RIGHT, fill = BOTH)
deckTree.configure(yscrollcommand = deckScroll.set)


# Load Card DB
for card in oracleDB:
    item = [card["name"], card["type_line"]]
    if "mana_cost" in card:
        item.append(card["mana_cost"])
    else:
        item.append('None')
    dbTree.insert('', END, values=item)
"""
t = time.time()
sortedIid = sortTree(dbTree, dbTree.get_children(), 0)
print(time.time() - t)


cursor = 0
for iid in sortedIid:
    dbTree.move(iid, dbTree.parent(iid), cursor)
    cursor = cursor + 1
"""

def filterByName(*args):
    dbTree.delete(*dbTree.get_children())
    for card in oracleDB:
        item = [card["name"], card["type_line"]]
        if "mana_cost" in card:
            item.append(card["mana_cost"])
        else:
            item.append('None')
        if cardName.get().upper() in card["name"].upper():
            dbTree.insert('', END, values=item)
    
    treeChildren = dbTree.get_children()
    if treeChildren:
        top_child = treeChildren[0]
        dbTree.focus(top_child)
        dbTree.selection_set(top_child)

# Card Input
cin = ttk.Entry(inFrame, textvariable=cardName) # Card Name Input
cin.pack(side = TOP)

#add = ttk.Button(inFrame, text="Add", command=addCard) # Add To List
#add.pack(side = LEFT)

# Key Binds
root.bind('<Key>', lambda *args: [filterByName(), select()])
root.bind('<Expose>', select)
root.bind('<Button-1>', select)

# Run Event Loop
#cardViewer.mainloop()
root.mainloop()
