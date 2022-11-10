from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from urllib.request import urlopen, Request
import urllib.parse
import io
import json
from mergesort import sortTree, merge
import time
from operator import itemgetter
from collections import deque
import requests

IMG_SIZE = 'normal'
TYPELINE_WIDTH = 35
NAME_WIDTH = 50 
MANA_WIDTH = 15
URL = 'https://cards.scryfall.io/small/front/8/6/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012.jpg?1562242171'
CI_PADDING = 10
INPUT_BREAK = 4

# Load full card list from scryfall dump
oracleFile = open('JSON\oracle-cards.json', 'r', encoding="utf8")
oracleDB = json.load(oracleFile)
oracleDB = sorted(oracleDB, key=itemgetter('name')) 

# Initialize Tkinter Window
root = Tk()
root.resizable(width = 1, height = 1)
root.minsize(500,300)
root.title("QuickSilver")
root.iconbitmap('misc/icon.ico')
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
root.state('zoomed')

import tkinter as tk
from tkinter import ttk

#Paned Window to store frames
pWin = ttk.PanedWindow(root, orient = HORIZONTAL)
pWin.grid(column = 0, row = 0, sticky = (N, S, E, W))
pWin.columnconfigure(0, weight = 8, minsize = 800)
pWin.rowconfigure(0, weight = 1)
pWin.columnconfigure(1, weight = 1)


style = ttk.Style()
style.theme_use('classic')
style.configure("pWin")

# Paned Window to store decklist and cardimg
rightFrame = ttk.Frame(pWin)
rightFrame.grid(column = 1, row = 0, sticky = (N, S, E, W))
rightFrame.columnconfigure(0, weight = 1)
rightFrame.rowconfigure(0, weight = 1)

pRight = ttk.PanedWindow(rightFrame, orient = VERTICAL)
pRight.grid(column = 0, row = 0, sticky = (N, S, E, W))
pRight.columnconfigure(0, weight = 1)
pRight.rowconfigure(0, weight = 1)
pRight.rowconfigure(1, weight = 3)

style = ttk.Style()
style.theme_use('classic')
style.configure("pWin")

# Initialize Card Viewer Window
cardViewer = ttk.Frame(pRight)
cardViewer.grid(column = 0, row = 1, sticky = (N, S, E, W))
cardViewer.columnconfigure(0, weight = 1)
cardViewer.rowconfigure(0, weight = 1)
cardViewer.rowconfigure(1, weight = 1)
pRight.add(cardViewer)

# Store Current Card Name
cardName = StringVar()

# Create a buffer to store most recent 10 Images
imgBuff = deque([])

# Bool to switch between simple and scryfall search
simpleSearch = BooleanVar()
simpleSearch.set(True)

def searchDB(cardName = False, ID = False):
    if ID:
        for card in oracleDB:
            if card["id"] == ID:
                return card
    if cardName:
        for card in oracleDB:
            if card["name"].upper() == cardName.upper():
                return card
    print('Card not found')
    return -1

lastCard = searchDB(cardName = "Birthing Pod")

# Check all listboxes for selected card
def select(event):
    global lastCard
    if event is None:
        return
    widget = event.widget
    if type(widget) is ttk.Treeview:
        iid = widget.focus()
        if widget.item(iid)["values"]:
            card = searchDB(ID = widget.item(iid)["values"][0])
            displayCard(card)
            lastCard = card
    else:
        displayCard(lastCard)

# Initialize decklist
deck = []

# Return position in deck, -1 if not in deck
def inDeck(ID):
    cursor = 0
    for card in deck:
        if card['CO']['id'] == ID:
            return cursor
        cursor = cursor + 1
    return -1

# Define function to add card to decklist
def addCard(*args):
    if "values" not in dbTree.item(dbTree.focus()):
        print(f'Failed to add card: {dbTree.item(dbTree.focus())}')
        return -1
    
    cardID = dbTree.item(dbTree.focus())["values"][0]
    # Fetch card location
    locus = inDeck(cardID)
    # If card not in deck, add
    if locus == -1:
        CO = searchDB(ID = cardID)
        if CO == -1:
            return -1
        deck.append({'CO': CO, 'n': 1})
    # If card is in deck, increase quantity
    else:
        current = deck.pop(locus)
        current["n"] = current["n"] + 1
        deck.append(current)
    reload()

# Reload decklist tree
def reload():
    deckTree.delete(*deckTree.get_children())
    for card in deck:
        deckTree.insert('', END, values=(card['CO']['id'], card['n'], card['CO']['name']))

cardView = ttk.Label(cardViewer)
cardView.grid(column = 0, row = 0, sticky = (N, S, E, W))

""" Image enable / disable (temporarily deprecated)
imgOn = BooleanVar()
imgOn.set(True)

imgMode = ttk.Checkbutton(cardViewer, text = "Display Images?", variable = imgOn, onvalue = True, offvalue = False)
imgMode.grid(column = 0, row = 1)
"""

def convertImg(imgURL):
    head = {'User-Agent': 'Mozilla/5.0'}
    page = urlopen(Request(imgURL, headers=head))
    img = io.BytesIO(page.read())
    pilImg = Image.open(img)
    return pilImg

# Store current width and height to abort pointless re-renders
curW = 0
curH = 0
curPil = convertImg(URL)

def updateImg(pilImg, w, h, resize = False, cardObj = cardView):
    global curW, curH
    if (w == curW) and (h == curH) and resize:
        return
    
    img = pilImg.resize((int(w), int(h)))
    curW = w
    curH = h
    tkImg = ImageTk.PhotoImage(img)
    cardObj.configure(image = tkImg)
    cardObj.image = tkImg

#Display image with new updated width and height
def displayImg(resize = False):
    root.update() # refresh widget info
    
    w = cardViewer.winfo_width()
    h = cardViewer.winfo_height()
        
    if w*1.4 < h:
        h = w*1.4
    else:
        w = h*0.71
    
    updateImg(curPil, int(w), int(h), resize)

# Update card display
def displayCard(card):
    global lastID
    global curPil
    
    resize = False
    
    ID = card["id"]

    # only fetch new image if it's not stored in the buffer
    if not (ID in imgBuff):
        if len(imgBuff) != 0:
            imgBuff.popleft()
        imgBuff.append(ID)
        
        if "card_faces" in card:
            curPil = convertImg(card["card_faces"][0]["image_uris"][IMG_SIZE])
        else:
            curPil = convertImg(card["image_uris"][IMG_SIZE])
    else:
        resize = True
    
    displayImg(resize)

displayImg()

#Frame for all card list browsing
listFrame = ttk.Frame(pWin, padding = 10)
listFrame.grid(column = 0, row = 0, sticky = (N, S, E, W))
listFrame.columnconfigure(0, weight = 1)
listFrame.rowconfigure(1, weight = 1)
pWin.add(listFrame)
pWin.add(rightFrame)

#Frame for decklist
deckFrame = ttk.Frame(pRight, padding = 10)
deckFrame.grid(column = 0, row = 1, sticky = (N, S, E, W))
deckFrame.columnconfigure(0, weight = 1)
deckFrame.columnconfigure(1, minsize = 25)
deckFrame.rowconfigure(0, weight = 1)

pRight.add(deckFrame)

# Create a frame to store input widgets in
inFrame = ttk.Frame(listFrame, padding = 10)
inFrame.grid(column = 0, row = 0, sticky = N)

# Create a frame to store full card list in
dbTreeFrame = ttk.Frame(listFrame, padding = 10)
dbTreeFrame.columnconfigure(0, weight = 1)
dbTreeFrame.columnconfigure(1, minsize = 25)
dbTreeFrame.rowconfigure(0, weight = 1)

def dbListPlace():
    dbTreeFrame.grid(column = 0, row = 1, sticky = (N, S, E, W))

# Full card list display
dbTree = ttk.Treeview(dbTreeFrame, columns = ('id', 'name', 't', 'mc'), show='headings', selectmode = 'browse')
dbTree['displaycolumns']=('name', 't', 'mc')
dbTree.heading('name', text='Name')
dbTree.heading('t', text='Type')
dbTree.heading('mc', text='Mana Cost')
dbTree.grid(column = 0, row = 0, sticky = (N, S, E, W))
dbScroll = ttk.Scrollbar(dbTreeFrame,
                         orient = 'vertical',
                         command = dbTree.yview)
dbScroll.grid(column = 1, row = 0, sticky = (N, S))
dbTree.configure(yscrollcommand = dbScroll.set)

# Image database display
dbImgFrame = ttk.Frame(listFrame, padding = 5)
dbImgFrame.grid(column = 0, row = 1, sticky = (N, S, E, W))

ciWidth = 0
ciHeight = 0
ciColCount = 0
ciRowCount = 0
ciArr = []

# Calculate format for card image page
def formatCIPage():
    global ciWidth, ciColCount
    DBW = dbImgFrame.winfo_width()
    if DBW > 1000:
        # Size for 4 cards
        ciWidth = (DBW - CI_PADDING*5)*0.25
        ciColCount = 4
    elif DBW > 700:
        # Size for 3 cards
        ciWidth = (DBW - CI_PADDING*4)*0.33
        ciColCount = 3
    else:
        #Size for 2 cards
        ciWidth = (DBW - CI_PADDING*4)*0.5
        ciColCount = 2

# Define array to hold card image objects
def defCardObjArr():
    global ciHeight, ciRowCount, ciArr
    
    # Purge old card labels
    for cx in ciArr:
        for cy in cx:
            cy.grid_forget()
            del cy
    
    DBH = dbImgFrame.winfo_height()
    ciHeight = ciWidth*1.4
    ciRowCount = int((DBH - CI_PADDING) / (ciHeight + 10))
    
    totalImg = int(ciColCount * ciRowCount)
    
    dbCurLis = dbTree.get_children()
    
    if len(dbCurLis) <= 1:
        return
    
    idArray = []
    
    ciArr = []
    
    for n in range(totalImg):
        idArray.append(dbTree.item(dbCurLis[n])["values"][0])
    
    for ciX in range(ciColCount):
        ciArr.append([])
        for ciY in range (ciRowCount):
            ciArr[ciX].append(ttk.Label(dbImgFrame))
            ciArr[ciX][ciY].grid(column = ciX, row = ciY)
            card = searchDB(ID = idArray[ciX + ciY])
            
            if "card_faces" in card:
                pilImg = convertImg(card["card_faces"][0]["image_uris"][IMG_SIZE])
            else:
                pilImg = convertImg(card["image_uris"][IMG_SIZE])
            
            updateImg(pilImg, ciWidth, ciHeight, cardObj = ciArr[ciX][ciY])

def updateImgDB(*args):
    formatCIPage()
    defCardObjArr()

def placeImgDB():
    dbImgFrame.grid(column = 0, row = 1, sticky = (N, S, E, W))
    updateImgDB()


# Deck list display
deckTree = ttk.Treeview(deckFrame, columns = ('id', 'q', 'name'), show='headings', selectmode = 'browse')
deckTree["displaycolumns"] = ('q', 'name')
deckTree.heading('q', text='#')
deckTree.column('q', minwidth = 20, width = 20, stretch = False)
deckTree.heading('name', text='Name')
deckTree.grid(column = 0, row = 0, sticky = (N, S, E, W))

deckScroll = ttk.Scrollbar(deckFrame,
                         orient = "vertical",
                         command = deckTree.yview)
deckScroll.grid(column = 1, row = 0, sticky = (N, S))
deckTree.configure(yscrollcommand = deckScroll.set)


# Load Card DB
for card in oracleDB:
    if 'paper' not in card['games']:
        continue

    item = [card['id'], card['name'], card['type_line']]
    if 'mana_cost' in card:
        item.append(card['mana_cost'])
    else:
        item.append('None')

    dbTree.insert('', END, values=item)

treeChildren = dbTree.get_children()
if treeChildren:
    top_child = treeChildren[0]
    dbTree.focus(top_child)
    dbTree.selection_set(top_child)

# Add card object to DB treelist
def addDBItem(card):
    if 'paper' not in card['games']:
        return -1
    item = [card['id'], card['name'], card['type_line']]
    if "mana_cost" in card:
        item.append(card['mana_cost'])
    else:
        item.append('None')
    dbTree.insert('', END, values=item)

# Select / focus top treelist item
def selectDBTop():
    treeChildren = dbTree.get_children()
    if treeChildren:
        top_child = treeChildren[0]
        dbTree.focus(top_child)
        dbTree.selection_set(top_child)

def filterByName(*args):
    dbTree.delete(*dbTree.get_children())
    for card in oracleDB:
        if cardName.get().upper() in card['name'].upper():
            addDBItem(card)
    selectDBTop()

# returns scryfall search query as json
def scrySearch(query):
    str = urllib.parse.quote(query)
    print("Fetching from scryfall...")
    response = requests.get('https://api.scryfall.com/cards/search?q='+str)
    print("...Fetch complete")
    return response.json()['data']
# Load scryfall search into tree
def scryFilter(*args):
    dbTree.delete(*dbTree.get_children())
    db = scrySearch(cardName.get())
    for card in db:
        addDBItem(card)
    selectDBTop()


# Card Input
cin = ttk.Entry(inFrame, textvariable=cardName) # Card Name Input
cin.grid(column = 0, row = 0, sticky = W)
cin.focus_force()

# Button to swap between text DB and image DB
imgDB = True

def swapDBMode(*args):
    global imgDB
    if imgDB:
        dbImgFrame.grid_forget()
        dbListPlace()
        imgDB = False
    else:
        dbTreeFrame.grid_forget()
        placeImgDB()
        imgDB = True

swapDBMode()

def refresh(event = None):
    if root.focus_get() == cin and simpleSearch.get():
        filterByName()
        select(event)
        if imgDB:
            placeImgDB()
        root.after(1000, refresh)

dbSwapButton = ttk.Button(inFrame, command = swapDBMode, text = "Swab DB Mode")
dbSwapButton.grid(column = 1, row = 0)

seachMode = ttk.Checkbutton(inFrame, variable = simpleSearch, text = "Simple Search Mode")
seachMode.grid(column = 2, row = 0)

scryRefresh = ttk.Button(inFrame, command = scryFilter, text = "Refresh Scryfall Query")
scryRefresh.grid(column = 3, row = 0)

refresh()

# Key Binds
root.bind('<Expose>', select)
root.bind('<Button-1>', select)
root.bind('<Up>', select)
root.bind('<Down>', select)
root.bind('<Return>', addCard)
dbTree.bind('Double-Button-1', addCard())

# Run Event Loop
#cardViewer.mainloop()
root.mainloop()
