from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from urllib.request import urlopen
import io
import json

"""
Sample Card Object
Card =
{
    "CO": <Card Object From DB>,
    "n": <Quantity>,
    "cat1": <T/F> ,
    "cat2": <T/F> ,
    "cat3": <T/F> 
}
"""

IMG_SIZE = 'normal'
TYPELINE_WIDTH = 35
NAME_WIDTH = 50
MANA_WIDTH = 15
DB_HEIGHT = 60

# Load full card list from scryfall dump
oracleFile = open('JSON\oracle-cards.json', 'r', encoding="utf8")
oracleDB = json.load(oracleFile)

# Initialize Tkinter Window
root = Tk()
root.title("QuickSilver")

# Store Current Card Name
cardName = StringVar()
# Store Current Card Categories
cat1 = BooleanVar()
cat2 = BooleanVar()
cat3 = BooleanVar()

"""
# Remove unwanted items from DB
for card in oracleDB:
    if card["type_line"] == 'Card':
        print(card["name"])
        oracleDB.remove(card)
"""
"""
# Find longest cardname length and use to set width of cardname lists
cNameWidth = 0
for card in oracleDB:
    if len(card["name"]) > cNameWidth:
        cNameWidth = len(card["name"])
        print(card["name"])

cNameWidth = cNameWidth + 2
"""



def searchDB(cardName):
    for card in oracleDB:
        if card["name"].upper() == cardName.upper():
            return card
    print('Card not found')
    return -1

# Check all listboxes for selected card
def select(*args):
    for widget in dbFrame.winfo_children():
        if type(widget) is ttk.Treeview:
            iid = widget.focus()
            displayCard(searchDB(widget.item(iid)['values'][0]))

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

# Add card to all aplicable categories
def addToDeck(card):
    if card["cat1"]:
        if card["cat2"]:
            if card["cat3"]:
                catAllList.insert(END, f'{card["n"]} {card["CO"]["name"]}')
            else:
                cat12List.insert(END, f'{card["n"]} {card["CO"]["name"]}')
        elif card["cat3"]:
            cat13List.insert(END, f'{card["n"]} {card["CO"]["name"]}')
        else:
            cat1List.insert(END, f'{card["n"]} {card["CO"]["name"]}')
    elif card["cat2"]:
        if card["cat3"]:
            cat23List.insert(END, f'{card["n"]} {card["CO"]["name"]}')
        else:
            cat2List.insert(END, f'{card["n"]} {card["CO"]["name"]}')
    elif card["cat3"]:
        cat3List.insert(END, f'{card["n"]} {card["CO"]["name"]}')

# Reload List Into Display
def reload(*args):
    cat1List.delete(0, END)
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
        displayCard(current)
    reload()

"""
# Initialize Card Viewer Windows
cardViewer = Tk()
cardViewer.title("Card Viewer")
cardFrame = ttk.Frame(cardViewer, padding=10)
cardFrame.grid()
"""

# Store Card Image URL
URL = "https://c1.scryfall.com/file/scryfall-cards/normal/front/8/4/84f2c8f5-8e11-4639-b7de-00e4a2cbabee.jpg?1618996002"

cardView = ttk.Label(root)
cardView.pack()
cardView.grid(column = 2, row = 1)

def convertImg(imgURL):
    page = urlopen(imgURL)
    img = io.BytesIO(page.read())
    pilImg = Image.open(img)
    tkImg = ImageTk.PhotoImage(pilImg)
    cardView.configure(image = tkImg)
    cardView.image = tkImg

def displayCard(card):
    if "card_faces" in card:
        convertImg(card["card_faces"][0]["image_uris"][IMG_SIZE])
    else:
        convertImg(card["image_uris"][IMG_SIZE])

convertImg(URL)

# Create a frame to store input widgets in
inFrame = ttk.Frame(root, padding = 10)
inFrame.grid(column = 0, row = 0)

# Create a frame to store cards in
listFrame = ttk.Frame(root, padding = 10)
listFrame.grid(column = 1, row = 1)

# Create a frame to store full card list in
dbFrame = ttk.Frame(root, padding = 10)
dbFrame.grid(column = 0, row = 1)

# Full card list display
dbTree = ttk.Treeview(dbFrame, columns = ('name', 't', 'mc'), height = DB_HEIGHT, show='headings')
dbTree.heading('name', text='Name')
dbTree.heading('t', text='Type')
dbTree.heading('mc', text='Mana Cost')
dbTree.grid(column = 0, row = 0)


# Load Card DB
for card in oracleDB:
    item = [card["name"], card["type_line"]]
    if "mana_cost" in card:
        item.append(card["mana_cost"])
    else:
        item.append('None')
    dbTree.insert('', END, values=item)


# Deck List Display
# Category 1
cat1List = Listbox(listFrame, listvariable = deck, bg = '#ffccab')
cat1List.grid(column = 0, row = 0)
# Category 1/2 Overlap
cat12List = Listbox(listFrame, listvariable = deck, bg = '#abc0c3')
cat12List.grid(column = 1, row = 0)
# Category 1/3 Overlap
cat13List = Listbox(listFrame, listvariable = deck, bg = '#e89daf')
cat13List.grid(column = 0, row = 1)
# Category 2
cat2List = Listbox(listFrame, listvariable = deck, bg = '#abe2fb')
cat2List.grid(column = 2, row = 0)
# Category 2/3 Overlap
cat23List = Listbox(listFrame, listvariable = deck, bg = '#afabe5')
cat23List.grid(column = 2, row = 1)
# Category 3
cat3List = Listbox(listFrame, listvariable = deck, bg = '#e7bfe7')
cat3List.grid(column = 1, row = 2)
# All Categories Overlap
catAllList = Listbox(listFrame, listvariable = deck, bg = '#af95bf')
catAllList.grid(column = 1, row = 1)


# Card Input
cin = ttk.Entry(inFrame, textvariable=cardName).grid(column = 0, row = 0) # Card Name Input
c1 = ttk.Checkbutton(inFrame, text = "Category 1", variable = cat1, onvalue = True, offvalue = False).grid(column = 1, row = 0)
c2 = ttk.Checkbutton(inFrame, text = "Category 2", variable = cat2, onvalue = True, offvalue = False).grid(column = 2, row = 0)
c3 = ttk.Checkbutton(inFrame, text = "Category 3", variable = cat3, onvalue = True, offvalue = False).grid(column = 3, row = 0)
ttk.Button(inFrame, text="Add", command=addCard).grid(column = 4, row = 0) # Add To List

# Key Binds
root.bind('<Return>', addCard)
root.bind('<Button-1>', select)

# Run Event Loop
#cardViewer.mainloop()
root.mainloop()
