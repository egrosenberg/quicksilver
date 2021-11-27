from tkinter import *
from tkinter import ttk


# Initialize decklist
deck = []

# Define function to add card to decklist
def addCard(*args):
    deck.append(cardName.get())
    listDisplay.insert(END, cardName.get())

# Initialize Tkinter
root = Tk()
root.title("QuickSilver")

# Store Current Card Name
cardName = StringVar()

# Create a frame to store widgets in
inFrame = ttk.Frame(root, padding=10)
inFrame.grid()

# Deck List Display
listDisplay = Listbox(inFrame, listvariable = deck)
listDisplay.grid(column = 0, row = 1)

# Card Input
cin = ttk.Entry(inFrame, textvariable=cardName).grid(column = 0, row = 0)
ttk.Button(inFrame, text="Add", command=addCard).grid(column = 1, row = 0)

# Run Event Loop
root.mainloop()