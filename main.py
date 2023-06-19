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
            for row in file_reader:
                ShortCutButton(master, row)
            if file_reader.line_num == 0:
                row = self.create_list(filename)
                ShortCutButton(master, row)

    def create_list(self, filename):
        initial_row = ["google", "https://google.com", 0, 0]
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            output_writer = csv.writer(f)
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
        self.root = master
        self.dummy_button = None
        self.y_position = 0
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)
        self.bind("<B1-Motion>", self.when_dragged)
        self.bind("<ButtonRelease-1>", self.when_released)
        self.pack(pady=1)
    
    def when_released(self, event):
        self.delete_dummy_button()

    def when_dragged(self, event):
        #ダミーボタンがない場合、全ウィジェット情報を取得後にダミー生成、上下ボタンの情報取得
        if not self.dummy_button:
            self.get_widget_info()      #全widgetの情報を辞書型で取得 key: y, value: text
            self["state"] = "disable"   #自身をdisable
            self.dummy_button = tkinter.Button(
                self.root,
                text = self["text"],
                bg = "red",
                width = self["width"],
            )
        
        if self.dragged_button_index == 0:
            #一番上のボタンをドラッグしている時
            y_up = False
            y_down = self.sorted_y_position[self.dragged_button_index + 1]
        elif self.dragged_button_index == len(self.sorted_y_position) - 1:
            #一番下のボタンをドラッグしている時
            y_up = self.sorted_y_position[self.dragged_button_index - 1]
            y_down = False
        else:
            #中間のボタンをドラッグしている時
            y_up = self.sorted_y_position[self.dragged_button_index - 1]
            y_down = self.sorted_y_position[self.dragged_button_index + 1]

        #dragされたらdummy_buttonをポインタに合わせて表示
        x_dummy = self.winfo_x() + event.x - self.winfo_width() / 2
        y_dummy = self.winfo_y() + event.y - self.winfo_height() / 2
        self.dummy_button.place(
            x = x_dummy,
            y = y_dummy,
        )

        #ダミーボタンの位置が上下ボタン位置を超えたとき、入れ替え
        if y_up is not False and y_dummy < y_up:
            self.swap_button(y_up)
        elif  y_down is not False and y_dummy > y_down:
            self.swap_button(y_down)
    
    def swap_button(self, y_target):
        """
        ダミーを削除し、y_targetとselfを入れ替え
        """
        target_button = self.button_info[y_target]  #widget        
        self.button_info[self.winfo_y()] = target_button
        self.button_info[target_button.winfo_y()] = self
       
        for w in self.widgets:
            w.pack_forget()
        
        for y in self.sorted_y_position:
            self.button_info[y].pack(pady=1)

        self.delete_dummy_button()

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
                self.button_info[w.winfo_y()] = w
        self.sorted_y_position = sorted(self.button_info.keys())
        self.dragged_button_index = self.sorted_y_position.index(self.winfo_y())

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
            print("clicked")
            #webbrowser.open(self.url)


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
            ShortCutButton(w[0], [title, url]) #w[0] is a LabelFrame widget

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
