from main import CreateShortCutButtons, CreateNewButton

import tkinter


class TestCreateShortCutButtons():
    def __init__(self, master):
        b = CreateShortCutButtons()
        b.create_shortcut_buttons(master)


class TestCreateNewButton():
    def __init__(self, master):
        self.cn_button = CreateNewButton(master)



if __name__ == "__main__":
    root = tkinter.Tk()
    t = TestCreateShortCutButtons(root)
    root.mainloop()
