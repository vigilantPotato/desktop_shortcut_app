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
        short_cut_buttons_in_label = CreateShortCutButtons(self.root)
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
    read csv file and create ShortCut buttons in a LabelFrame.
    csv file name is list.csv
    """

    def __init__(self, master):
        self.label = tkinter.LabelFrame(
            master=master,
            text="short cut",
            relief="ridge",
            )
        self.label.pack(ipadx=5, ipady=5)
        self.create_shortcut_buttons(self.label)

    def create_shortcut_buttons(self, master):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if not os.path.exists(filename):
            self.create_list(filename)
        with open(filename, 'r', encoding="utf-8") as open_file:
            file_reader = csv.reader(open_file)
            header = next(file_reader)
            for row in file_reader:
                ShortCutButton(master, row)
            if file_reader.line_num == 0:
                row = self.create_list(filename)
                ShortCutButton(master, row)

    def create_list(self, filename):
        initial_row = ["google", "https://google.com", 1]
        header = ["title", "url", "order"]
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            output_writer = csv.writer(f)
            output_writer.writerow(header)
            output_writer.writerow(initial_row)
        return initial_row


class ShortCutButton(tkinter.Button):
    """
    simple short cut button widget.
    open the url when clicked with webbrowser module    
    """

    def __init__(self, master, row):
        super().__init__(
            master,
            text=row[0],
            background="cyan",
            width=15,
            command=self.shortcut,
        )
        self.url = row[1]
        self.order = int(row[2])
        self.root = master
        self.dummy_button = None
        self.y_position = 0
        self.frame_width = 0
        self.dummy_x = 0
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)
        self.bind("<B1-Motion>", self.when_dragged)
        self.bind("<ButtonRelease-1>", self.when_released)
        self.pack(pady=1)
    
    def when_released(self, event):
        self.delete_dummy_button()
        if self.dummy_x < 0:
            self.delete_info_from_csv_and_remove_button(self["text"])
            self.destroy()

    def when_dragged(self, event):
        #ダミーボタンがない場合、全ウィジェット情報を取得後にダミー生成、上下ボタンの情報取得
        if not self.dummy_button:
            self.get_widget_info()      #全widgetの情報を辞書型で取得 key: order, value: button widget
            self["state"] = "disable"   #自身をdisable
            self.dummy_button = tkinter.Button(
                self.root,
                text = self["text"],
                bg = "red",
                width = self["width"],
            )
            self.frame_widthx = self.button_info[1].winfo_rootx() - self.root.winfo_rootx()
            self.frame_widthy = self.button_info[1].winfo_rooty() - self.root.winfo_rooty()

        #dragされたらdummy_buttonをポインタに合わせて表示
        x_dummy = self.winfo_x() - self.frame_widthx + event.x
        y_dummy = self.winfo_y() - self.frame_widthy + event.y
        self.dummy_button.place(
            x = x_dummy,
            y = y_dummy,
        )

        if self.order == 1:
            above_y = None
            below_y = self.button_info[self.order + 1].winfo_y()
        elif self.order == len(self.widgets):
            above_y = self.button_info[self.order - 1].winfo_y()
            below_y = None
        else:
            above_y = self.button_info[self.order - 1].winfo_y()
            below_y = self.button_info[self.order + 1].winfo_y()

        self.dummy_x = self.dummy_button.winfo_x()

        if above_y is not None and 0 < self.dummy_button.winfo_y() < self.winfo_y():
            self.swap_button(self.order - 1)
        elif  below_y is not None and 0 < self.dummy_button.winfo_y() > below_y:
            self.swap_button(self.order + 1)
    
    def swap_button(self, y_target):
        """
        ダミーを削除し、y_targetとselfを入れ替え
        """
        self.delete_dummy_button()
        self.button_info[y_target].order = self.order
        self.order = y_target
        self.get_widget_info()
        for w in self.widgets:
            w.pack_forget()
        for i in range(1, len(self.button_info) + 1):
            self.button_info[i].pack(pady=1)
        self.update_csv_file()

    def update_csv_file(self):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if os.path.exists(filename):
            with open(filename, 'w', newline='', encoding="utf-8") as f:
                header = ["title", "url", "order"]
                output_writer = csv.writer(f)
                output_writer.writerow(header)
                for i in range(1, len(self.button_info) + 1):
                    b = self.button_info[i]
                    output_writer.writerow([b["text"], b.url, b.order])

    def delete_dummy_button(self):
        if self.dummy_button:
            self.dummy_button.destroy()
            self.dummy_button = None
    
    def get_widget_info(self):
        self.widgets = []
        self.widgets = self.root.winfo_children()
        self.button_info = {}
        for w in self.widgets:
            if w.winfo_ismapped():
                self.button_info[w.order] = w

    def mouse_on(self, event):
        self["background"] = "cyan4"
        self["foreground"] = "white"
        if self["state"] == "disabled":
            self["state"] = "normal"

    def mouse_leave(self, event):
        self["background"] = "cyan"
        self["foreground"] = "black"

    def shortcut(self):
        if self.url != "":
            print(self.order)
            #webbrowser.open(self.url)

    def delete_info_from_csv_and_remove_button(self, title):
        filename = os.path.join(os.getcwd(), 'list.csv')
        try:
            df = pd.read_csv(filename,index_col=0, header=None)
            df.drop(title, axis=0, inplace=True)
            df.to_csv(filename, header=False)
        except:
            pass

        """
        update the order of widgets
        """
        del self.button_info[self.order]
        for i in range(1, len(self.button_info) + 1):
            
            if i >= self.order:
                self.button_info[i] = self.button_info[i+1]
                self.button_info[i].order = i
                del self.button_info[i+1]

        self.update_csv_file()

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
        w = self.root.winfo_children()
        button_order = len(w[0].winfo_children()) + 1
        filename = os.path.join(os.getcwd(), 'list.csv')
        if os.path.exists(filename):
            with open(filename, 'a', newline='', encoding="utf-8") as f:
                output_writer = csv.writer(f)
                output_writer.writerow([title, url, button_order])
            ShortCutButton(w[0], [title, url, button_order]) #w[0] is a LabelFrame widget

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
