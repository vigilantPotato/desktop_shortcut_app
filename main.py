import csv
import os
import tkinter
import webbrowser


class CreateShortCutButtons():
    """
    read csv file and create ShortCut buttons.
    csv file name is list.csv
    """

    def __init__(self):
        pass

    def create_shortcut_buttons(self, master):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if os.path.exists(filename):
            open_file = open(filename)
            file_reader = csv.reader(open_file)
            for row in file_reader:
                ShortCutButton(master, row[0], row[1])


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
    CreateShortCutButtons(root)
    root.mainloop()
