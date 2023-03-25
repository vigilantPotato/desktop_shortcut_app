import csv
import tkinter
import webbrowser


class CreateShortCutButtons():
    """
    read csv file and create ShortCut buttons.
    create new csv file if not existing.
    """

    def __init__(self):
        pass

    def create_buttons(self, title, url):
        pass


class ShortCutButton(tkinter.Button):
    """
    simple short cut button widget.
    open the url when clicked with webbrowser module    
    """

    def __init__(self, master, title, url):
        super().__init__(
            master,
            text=title,
            width=15,
            command=self.shortcut,
        )
        self.url = url
        self.pack()

    def shortcut(self):
        if self.url != "":
            webbrowser.open(self.url)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("ShortCut")
    sc_button = ShortCutButton(
        root,
        "ShortCut",
        r"C:\Users",
        )
    root.mainloop()
