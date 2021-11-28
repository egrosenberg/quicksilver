from tkinter import *
from tkinter import ttk

"""
Sample Card Object
Card =
{
    "name": <name>,
    "n": <Quantity>,
    "imageURL": <URL>,
    "o": <Oracle Text>,
    "cost": <Mana Cost>,
    "cat1": <T/F> ,
    "cat2": <T/F> ,
    "cat3": <T/F> 
}
"""

# Initialize decklist
deck = []

def inDeck(name):
    cursor = 0
    for card in deck:
        if ("name", name) in card.items():
            print(1)
            return cursor
        cursor = cursor + 1
    return -1

# Add card to all aplicable categories
def addToDeck(card):
    if card["cat1"]:
        if card["cat2"]:
            if card["cat3"]:
                catAllList.insert(END, f'{card["n"]} {card["name"]}')
            else:
                cat12List.insert(END, f'{card["n"]} {card["name"]}')
        elif card["cat3"]:
            cat13List.insert(END, f'{card["n"]} {card["name"]}')
        else:
            cat1List.insert(END, f'{card["n"]} {card["name"]}')
    elif card["cat2"]:
        if card["cat3"]:
            cat23List.insert(END, f'{card["n"]} {card["name"]}')
        else:
            cat2List.insert(END, f'{card["n"]} {card["name"]}')
    elif card["cat3"]:
        cat3List.insert(END, f'{card["n"]} {card["name"]}')

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
        print(card)
        addToDeck(card)

# Define function to add card to decklist
def addCard(*args):
    name = cardName.get()
    # Fetch card location
    locus = inDeck(name)
    # If card not in deck, add
    if locus == -1:
        deck.append({"name": name, "n": 1, "cat1": cat1.get(), "cat2": cat2.get(), "cat3": cat3.get()})
    # If card is in deck, increase quantity
    else:
        current = deck.pop(locus)
        current["n"] = current["n"] + 1
        current["cat1"] = cat1.get()
        current["cat2"] = cat2.get()
        current["cat3"] = cat3.get()
        deck.append(current)
    reload()


# Initialize Tkinter
root = Tk()
root.title("QuickSilver")

# Store Current Card Name
cardName = StringVar()
# Store Current Card Categories
cat1 = BooleanVar()
cat2 = BooleanVar()
cat3 = BooleanVar()

# Create a frame to store input widgets in
inFrame = ttk.Frame(root, padding = 10)
inFrame.grid()

# Create a frame to store cards in
cardFrame = ttk.Frame(root, padding = 10)
cardFrame.grid()

# Deck List Display
# Category 1
cat1List = Listbox(cardFrame, listvariable = deck, bg = '#ffccab')
cat1List.grid(column = 0, row = 0)
# Category 1/2 Overlap
cat12List = Listbox(cardFrame, listvariable = deck, bg = '#abc0c3')
cat12List.grid(column = 1, row = 0)
# Category 1/3 Overlap
cat13List = Listbox(cardFrame, listvariable = deck, bg = '#e89daf')
cat13List.grid(column = 0, row = 1)
# Category 2
cat2List = Listbox(cardFrame, listvariable = deck, bg = '#abe2fb')
cat2List.grid(column = 2, row = 0)
# Category 2/3 Overlap
cat23List = Listbox(cardFrame, listvariable = deck, bg = '#afabe5')
cat23List.grid(column = 2, row = 1)
# Category 3
cat3List = Listbox(cardFrame, listvariable = deck, bg = '#e7bfe7')
cat3List.grid(column = 1, row = 2)
# All Categories Overlap
catAllList = Listbox(cardFrame, listvariable = deck, bg = '#af95bf')
catAllList.grid(column = 1, row = 1)


# Card Input
cin = ttk.Entry(inFrame, textvariable=cardName).grid(column = 0, row = 0) # Card Name Input
c1 = ttk.Checkbutton(inFrame, text = "Category 1", variable = cat1, onvalue = True, offvalue = False).grid(column = 1, row = 0)
c2 = ttk.Checkbutton(inFrame, text = "Category 2", variable = cat2, onvalue = True, offvalue = False).grid(column = 2, row = 0)
c3 = ttk.Checkbutton(inFrame, text = "Category 3", variable = cat3, onvalue = True, offvalue = False).grid(column = 3, row = 0)
ttk.Button(inFrame, text="Add", command=addCard).grid(column = 4, row = 0) # Add To List

# Run Event Loop
root.mainloop()
