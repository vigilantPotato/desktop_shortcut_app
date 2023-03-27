from main import CreateShortCutButtons

import tkinter


class TestCreateShortCutButtons():
    def __init__(self, master):
        b = CreateShortCutButtons()
        b.create_shortcut_buttons(master)


if __name__ == "__main__":
    root = tkinter.Tk()
    t = TestCreateShortCutButtons(root)
    root.mainloop()
