import csv
import os
import tkinter
import tkinter.simpledialog
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


class CreateNewButton(tkinter.Button):
    """
    issue #2

    """

    def __init__(self, master):
        super().__init__(
            master,
            text="create new",
            width=15,
            command=self.ask_info,
        )
        self.pack()

    def ask_info(self):
        title = tkinter.simpledialog.askstring('input title', 'please input title')
        if(title == None or title == ''):
            return
        url = tkinter.simpledialog.askstring('input URL', 'please input URL')
        if(url == None or url == ''):
            return
        self.add_info_to_csv(title, url)
    
    def add_info_to_csv(self, title, url):
        filename = os.path.join(os.getcwd(), 'list.csv')
        open_file = open(filename, 'a', newline='')
        output_writer = csv.writer(open_file)
        output_writer.writerow([title, url])


if __name__ == "__main__":
    root = tkinter.Tk()
    create = CreateShortCutButtons()
    create.create_shortcut_buttons(root)
    c = CreateNewButton(root)
    root.mainloop()
