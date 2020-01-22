from tkinter.font import Font

courier: Font = None

def initializeFonts():
    
    global courier
    courier = Font(family = "Courier", size = 12)
