import tkinter as tk
from tkinter import filedialog
from HWsplitter import HWsplitter

root = tk.Tk()


def selectFiles():
    path = filedialog.askopenfilename(title="Select the HW File")

    if not path.endswith(".pdf"):
        raise TypeError("Please select a .pdf file")

    file = HWsplitter.pathToFilename(path)
    hf = HWsplitter(file, path)
    hf.Split()
    root.destroy()


def showMenu():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"500x120+{screen_width//2 - 500 //2}+{screen_height//2 - 120}")
    root.title("CSC236 HW Splitter for Crowdmark")

    label = tk.Label(
        root,
        text="Make sure to check the created files after running the program"
        + "\n Extra precaution for the Windows users: all the testings were done on a MacOS",
    )
    label.pack()
    label2 = tk.Label(root, text="Andrew Chun (ay.chun@mail.utoronto.ca) July 2022")
    label2.place(relx=0.5, rely=0.85, anchor="center")

    button = tk.Button(text="Select your finished HW file", command=selectFiles)
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()
