from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Create Tk root
root = Tk()
root.withdraw()

# Open file explorer
file_path = askopenfilename()

# Show selected file path
print(file_path)