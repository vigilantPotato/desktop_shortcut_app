import csv
import ctypes
import input_dialog
import os
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
        l = LabelFrame(self.root)
        c = CreateNewButton(self.root, l)
        c.bind("<Map>", self.set_window_position_when_createnew_button_is_displayed)
        self.root.mainloop()
    
    def set_window_position_when_createnew_button_is_displayed(self, event):
        frame = self.root.winfo_rootx() - self.root.winfo_x()
        x = self.root.winfo_screenwidth() - self.root.winfo_width()
        self.root.geometry('+%d+%d' % (x - frame, 0))


class LabelFrame(tkinter.LabelFrame):
    def __init__(self, master, text="main"):
        super().__init__(
            master,
            text=text,
            relief="ridge",
            )
        self.button_info = []
        self.create_shortcut_buttons()
        self.pack()

    def create_shortcut_buttons(self):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if not os.path.exists(filename):
            self.create_list(filename)
        with open(filename, 'r', encoding="utf-8") as open_file:
            file_reader = csv.reader(open_file)
            header = next(file_reader)
            for row in file_reader:
                button = ShortCutButton(self, row)
                self.button_info.append(button)
            if file_reader.line_num == 0:
                row = self.create_list(filename)
                ShortCutButton(self, row)

    def update_shortcut_buttons(self):
        """
        open list.csv and update button information
        """
        filename = os.path.join(os.getcwd(), 'list.csv')
        if not os.path.exists(filename):
            self.create_list(filename)
        with open(filename, 'r', encoding="utf-8") as open_file:
            file_reader = csv.reader(open_file)
            header = next(file_reader)
            for i, row in enumerate(file_reader):
                self.button_info[i]["text"] = row[0]
                self.button_info[i].url = row[1]
                self.button_info[i]["bg"] = row[2]
                self.button_info[i]["fg"] = row[3]

    def create_list(self, filename):
        header = ["title", "url", "bg", "fg"]
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            output_writer = csv.writer(f)
            output_writer.writerow(header)
    


class ShortCutButton(tkinter.Button):
    """
    simple short cut button widget.
    open the url when clicked with webbrowser module    
    """

    sc_buttons_info = []
    dummy_button = False

    def __init__(self, master, row):
        self.sc_buttons_info.append(row)
        self.text = row[0]
        self.url = row[1]
        self.bg = row[2]
        self.fg = row[3]
        self.root = master
        super().__init__(
            master,
            text=self.text,
            background=self.bg,
            foreground=self.fg,
            width=15,
            command=self.shortcut,
            relief="groove"
        )
        self.swap_count = 0
        self.y_position = 0
        self.frame_width = 0
        self.dummy_x = 0
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)
        self.bind("<B1-Motion>", self.when_dragged)
        self.bind("<ButtonRelease-1>", self.when_released)
        self.pack(pady=1)
    
    def when_released(self, event):
        if self.swap_count == 0:
            if self.dummy_x < - self.winfo_width():
                self.delete_info_from_csv_and_remove_button(self["text"])
                self.destroy()
            elif self.dummy_x > self.winfo_width()/2:
                self.modify_button_info()
        
        if self.dummy_button is not False:
            self.dummy_x = 0
            self.dummy_button.destroy()
            self.dummy_button = False
        
    def when_dragged(self, event):
        #ダミーボタンがない場合、全ウィジェット情報を取得後にダミー生成、上下ボタンの情報取得
        if not self.dummy_button:
            self.swap_count = 0        
            self.dummy_button = tkinter.Button(
                self.root,
                text = self["text"],
                bg = self["bg"],
                fg = self["fg"],
                width = self["width"],
                )

            self.button_info = [self["text"], self.url, self["bg"], self["fg"]]  
            self["state"] = "disable"   #自身をdisable
            
            self.frame_widthx = self.root.button_info[0].winfo_rootx() - self.root.winfo_rootx()
            self.frame_widthy = self.root.button_info[0].winfo_rooty() - self.root.winfo_rooty()

        #dragされたらdummy_buttonをポインタに合わせて表示
        x_dummy = self.winfo_x() - self.frame_widthx + event.x - self.winfo_width() / 2
        y_dummy = self.winfo_y() - self.frame_widthy + event.y - self.winfo_height() / 2

        self.dummy_button.place(
            x = x_dummy,
            y = y_dummy,
        )
        self.dummy_x = self.dummy_button.winfo_x()
        
        if event.y < self.swap_count * self.winfo_height() and self.sc_buttons_info.index(self.button_info) != 0:
            self.swap_count -= 1
            index = self.sc_buttons_info.index(self.button_info)
            self.swap_button(index, index - 1)

        if event.y > (self.swap_count + 1) * self.winfo_height() and self.sc_buttons_info.index(self.button_info) != len(self.sc_buttons_info) - 1:
            self.swap_count += 1
            index = self.sc_buttons_info.index(self.button_info)
            self.swap_button(index, index + 1)

    def swap_button(self, self_index, target_index):
        target_info = self.sc_buttons_info[target_index]    #入れ替え対象
        self.sc_buttons_info[target_index] = self.button_info    #対象の情報を上書き
        self.sc_buttons_info[self_index] = target_info
        self.update_csv_file()
        self.root.update_shortcut_buttons()

    def update_csv_file(self):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if os.path.exists(filename):
            with open(filename, 'w', newline='', encoding="utf-8") as f:
                header = ["title", "url", "bg", "fg"]
                output_writer = csv.writer(f)
                output_writer.writerow(header)
                for row in self.sc_buttons_info:
                    output_writer.writerow(row)

    def mouse_on(self, event):
        self["relief"] = "solid"
        if self["state"] == "disabled":
            self["state"] = "normal"

    def mouse_leave(self, event):
        self["relief"] = "groove"

    def shortcut(self):
        if self.url != "":
            print(self.root.button_info)
            #webbrowser.open(self.url)

    def delete_info_from_csv_and_remove_button(self, title):
        for row in self.sc_buttons_info:
            print(row)
            if row[0] == title:
                self.sc_buttons_info.remove(row)
                self.root.button_info.remove(self)
                break
        self.destroy()
        self.update_csv_file()

    def modify_button_info(self):
        try:
            dialog = ButtonInformationInputDialog(self.root)
            current_info = [self["text"], self.url, self["bg"], self["fg"]]
            index = self.sc_buttons_info.index(current_info)
            new_info = dialog.ask_info(self["text"], self.url, bg=self["bg"], fg=self["fg"])
            self.sc_buttons_info[index] = new_info
            self["text"] = new_info[0]
            self.url = new_info[1]
            self["bg"] = new_info[2]
            self["fg"] = new_info[3]
            self.update_csv_file()
        except:
            pass


class CreateNewButton(tkinter.Button):
    """
    ask user to input shortcut button's title and url when clicked
    the information is saved to list.csv and restart this script
    """

    def __init__(self, master, labelframe):
        self.root = master
        super().__init__(
            master,
            text="create new",
            background="SeaGreen1",
            width=15,
            command=self.ask_info,
        )
        self.labelframe = labelframe
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)
        self.pack(pady=1)
    
    def ask_info(self):
        dialog = ButtonInformationInputDialog(self.labelframe)
        info = dialog.ask_info()
        new_button = ShortCutButton(self.labelframe, info)
        self.labelframe.button_info.append(new_button)

    def mouse_on(self, event):
        self["background"] = "green"
        self["foreground"] = "white"

    def mouse_leave(self, event):
        self["background"] = "SeaGreen1"
        self["foreground"] = "black"


class ButtonInformationInputDialog():
    """
    ask user to input button information.
    Methods:
    1. ask_info:
        When create a new button, both the default_title and default_url must be None. Input data will be saved to the CSV file and then create a new button.
        When modify button info, the default_title and default_url must be the title and url you want to modify. The new title and url is returned.
    """

    def __init__(self, root):
        self.root = root

    def ask_info(self, default_title=None, default_url=None, bg=None, fg=None):
        try:
            title, url, bg, fg = input_dialog.InputDialog(self.root, default_title, default_url, bg=bg, fg=fg).result
            
            if (title == None or title == ''):
                tkinter.messagebox.showerror("error", "Title is empty.")
            else:
                if default_title:
                    return([title, url, bg, fg])
                else:
                    self.add_info_to_csv(title, url, bg, fg)
                    return([title, url, bg, fg])
        except:
            pass
    
    def add_info_to_csv(self, title, url, bg, fg):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if os.path.exists(filename):
            with open(filename, 'a', newline='', encoding="utf-8") as f:
                output_writer = csv.writer(f)
                output_writer.writerow([title, url, bg, fg])
            
    def check_title_isin_csv(self, title):
        filename = os.path.join(os.getcwd(), 'list.csv')
        with open(filename) as instream:
            # Setup the input
            file_reader = csv.reader(instream)
            for row in file_reader:
                if row[0] == title:
                    return title

if __name__ == "__main__":
    DisplayMainForm()
