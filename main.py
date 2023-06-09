import csv
import ctypes
import input_dialog
import os
import pandas as pd
import re
import sys
import tkinter
import tkinter.simpledialog, tkinter.messagebox
import webbrowser


class DisplayMainForm():
    """
    Display a main form with shortcut buttons, a create-new button and a delete button.
    The form appears at the top-right of the monitor.
    """

    def __init__(self):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.root = tkinter.Tk()
        l = tkinter.LabelFrame(
            master=self.root,
            text="short cut",
            relief="ridge",
            )
        l.pack(ipadx=5, ipady=5)
        create = CreateShortCutButtons()
        create.create_shortcut_buttons(l)
        c = CreateNewButton(self.root)
        d = DeleteButton(self.root)
        d.bind("<Map>", self.set_window_position_when_delete_button_is_displayed)
        self.root.mainloop()
    
    def set_window_position_when_delete_button_is_displayed(self, event):
        frame = self.root.winfo_rootx() - self.root.winfo_x()
        x = self.root.winfo_screenwidth() - self.root.winfo_width()
        self.root.geometry('+%d+%d' % (x - frame, 0))

class CreateShortCutButtons():
    """
    read csv file and create ShortCut buttons.
    csv file name is list.csv
    """

    def __init__(self):
        pass

    def create_shortcut_buttons(self, master):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if not os.path.exists(filename):
            self.create_list(filename)
        with open(filename, 'r', encoding="utf-8") as open_file:
            file_reader = csv.reader(open_file)
            for row in file_reader:
                ShortCutButton(master, row[0], row[1])
            if file_reader.line_num == 0:
                row = self.create_list(filename)
                ShortCutButton(master, row[0], row[1])

    def create_list(self, filename):
        initial_row = ["google", "https://google.com"]
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            output_writer = csv.writer(f)
            output_writer.writerow(initial_row)
        return initial_row


class ShortCutButton(tkinter.Button):
    """
    simple short cut button widget.
    open the url when clicked with webbrowser module    
    """

    def __init__(self, master, title, url):
        super().__init__(
            master,
            text=title,
            background="cyan",
            width=15,
            command=self.shortcut,
        )
        self.url = url
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)
        self.pack(pady=1)
    
    def mouse_on(self, event):
        self["background"] = "cyan4"
        self["foreground"] = "white"

    def mouse_leave(self, event):
        self["background"] = "cyan"
        self["foreground"] = "black"

    def shortcut(self):
        if self.url != "":
            webbrowser.open(self.url)


class CreateNewButton(tkinter.Button):
    """
    ask user to input shortcut button's title and url when clicked
    the information is saved to list.csv and restart this script
    """

    def __init__(self, master):
        self.root = master
        super().__init__(
            master,
            text="create new",
            background="SeaGreen1",
            width=15,
            command=self.ask_info,
        )
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)
        self.pack(pady=1)
    
    def mouse_on(self, event):
        self["background"] = "green"
        self["foreground"] = "white"

    def mouse_leave(self, event):
        self["background"] = "SeaGreen1"
        self["foreground"] = "black"

    def ask_info(self):
        try:
            title, url = input_dialog.InputDialog(self.root).result
            if(title == None or title == '' or self.check_title_isin_csv(title)):
                tkinter.messagebox.showerror("error", "Title is empty or already used.")
                return

            if(url == None or url == ''):
                return
            self.add_info_to_csv_and_show_new_button(title, url)
        except:
            pass
    
    def add_info_to_csv_and_show_new_button(self, title, url):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if os.path.exists(filename):
            with open(filename, 'a', newline='', encoding="utf-8") as f:
                output_writer = csv.writer(f)
                output_writer.writerow([title, url])
            w = self.root.winfo_children()
            ShortCutButton(w[0], title, url) #w[0] is a LabelFrame widget

    def check_title_isin_csv(self, title):
        filename = os.path.join(os.getcwd(), 'list.csv')
        try:
            df = pd.read_csv(filename, index_col=0, header=None)
            return title in df.index.values
        except pd.errors.EmptyDataError:
            return False

class DeleteButton(tkinter.Button):
    """
    ask user to input shortcut button's title when clicked
    the title and related url is removed from list.csv and restart this script
    """

    def __init__(self, master):
        self.root = master
        super().__init__(
            master,
            text="delete",
            background="light pink",
            width=15,
            command=self.ask_title_to_delete,
        )
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)
        self.pack(pady=1)
    
    def mouse_on(self, event):
        self["background"] = "red"
        self["foreground"] = "white"

    def mouse_leave(self, event):
        self["background"] = "light pink"
        self["foreground"] = "black"

    def ask_title_to_delete(self):
        title = tkinter.simpledialog.askstring('delete title', 'please input title to delete')
        if(title == None or title == ''):
            return
        self.delete_info_from_csv_and_remove_button(title)
    
    def delete_info_from_csv_and_remove_button(self, title):
        filename = os.path.join(os.getcwd(), 'list.csv')
        try:
            df = pd.read_csv(filename,index_col=0, header=None)
            df.drop(title, axis=0, inplace=True)
            df.to_csv(filename, header=False)
            w = self.root.winfo_children()
            for b in w[0].winfo_children(): #w[0] is a LabelFrame widget
                if b["text"] == title:
                    b.destroy()
        except:
            pass


if __name__ == "__main__":
    DisplayMainForm()
