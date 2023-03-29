import csv
import os
import pandas as pd
import sys
import tkinter
import tkinter.simpledialog
import webbrowser


class DisplayMainForm():
    """
    Display a main form with shortcut buttons, a create-new button and a delete button.
    The form appears at the top-right of the monitor.
    """

    def __init__(self):
        root = tkinter.Tk()
        create = CreateShortCutButtons()
        create.create_shortcut_buttons(root)
        c = CreateNewButton(root)
        d = DeleteButton(root)

        screen_width = root.winfo_screenwidth()
        x = 130
        root.geometry('+%d+%d' % (screen_width-x, 0))
        root.mainloop()


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
    ask user to input shortcut button's title and url when clicked
    the information is saved to list.csv and restart this script
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
        self.add_info_to_csv_and_restart(title, url)

    def add_info_to_csv_and_restart(self, title, url):
        filename = os.path.join(os.getcwd(), 'list.csv')
        with open(filename, 'a', newline='') as f:
            output_writer = csv.writer(f)
            output_writer.writerow([title, url])
        os.execv(sys.executable, ['python'] + sys.argv)


class DeleteButton(tkinter.Button):
    """
    ask user to input shortcut button's title when clicked
    the title and related url is removed from list.csv and restart this script
    """

    def __init__(self, master):
        super().__init__(
            master,
            text="delete",
            width=15,
            command=self.ask_title_to_delete,
        )
        self.pack()
    
    def ask_title_to_delete(self):
        title = tkinter.simpledialog.askstring('delete title', 'please input title to delete')
        if(title == None or title == ''):
            return
        self.delete_info_from_csv_and_restart(title)
    
    def delete_info_from_csv_and_restart(self, title):
        filename = os.path.join(os.getcwd(), 'list.csv')
        try:
            df = pd.read_csv(filename,index_col=0, header=None)
            df.drop(title, axis=0, inplace=True)
            df.to_csv(filename, header=False)
            os.execv(sys.executable, ['python'] + sys.argv)
        except:
            pass


if __name__ == "__main__":
    DisplayMainForm()
