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

    def __init__(self, root, button=None):
        self.root = root
        self.button = button
        if button:  #sub-window
            text = button["text"]
        else:       #main-window
            text = "main"
        
        l = LabelFrame(root, text)
        c = CreateNewButton(root, l)
        c.bind("<Map>", self.set_window_position_when_createnew_button_is_displayed)
        
    def set_window_position_when_createnew_button_is_displayed(self, event):
        if self.button: #sub-window
            frame = self.root.winfo_rootx() - self.root.winfo_x()
            x = self.root.winfo_screenwidth() - 2 * self.root.winfo_width()
            y = self.button.winfo_y()
        else:   #main-window
            frame = self.root.winfo_rootx() - self.root.winfo_x()
            x = self.root.winfo_screenwidth() - self.root.winfo_width()
            y=0
        self.root.geometry('+%d+%d' % (x - frame, y))


class LabelFrame(tkinter.LabelFrame):
    """
    button_info
    """

    def __init__(self, master, text):
        super().__init__(
            master,
            text=text,
            relief="ridge",
            )
        self.button_info = [] #widget list of this label frame
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
                if self["text"] == row[4]:
                    button = ShortCutButton(self, row)
                    button.pack(pady=1)
                    self.button_info.append(button)
        
            if file_reader.line_num == 0:
                row = self.create_list(filename)
                ShortCutButton(self, row)

    def create_list(self, filename):
        header = ["title", "url", "bg", "fg", "label"]
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            output_writer = csv.writer(f)
            output_writer.writerow(header)
    
    def swap_button(self, order_1, order_2):
        #swap button_info_dict
        temp = (
            self.button_info[order_1]["text"],
            self.button_info[order_1].url,
            self.button_info[order_1]["bg"],
            self.button_info[order_1]["fg"],
        )
        
        self.button_info[order_1]["text"] = self.button_info[order_2]["text"]
        self.button_info[order_1].url = self.button_info[order_2].url
        self.button_info[order_1]["bg"] = self.button_info[order_2]["bg"]
        self.button_info[order_1]["fg"] = self.button_info[order_2]["fg"]
        
        self.button_info[order_2]["text"] = temp[0]
        self.button_info[order_2].url = temp[1]
        self.button_info[order_2]["bg"] = temp[2]
        self.button_info[order_2]["fg"] = temp[3]   

        self.update_csv()

    def update_csv(self, label=None):
        #clear button_info and set again
        to_csv_info = []

        filename = os.path.join(os.getcwd(), 'list.csv')

        #read csv data without this label's button information
        if not os.path.exists(filename):
            self.create_list(filename)
        
        with open(filename, 'r', encoding="utf-8") as open_file:
            file_reader = csv.reader(open_file)
            header = next(file_reader)
            for row in file_reader:
                if self["text"] != row[4] and label != row[4]:
                    to_csv_info.append(row)
        
        #add information of buttons on this label frame
        for i in range(len(self.button_info)):
            info = [
                self.button_info[i]["text"],
                self.button_info[i].url,
                self.button_info[i]["bg"],
                self.button_info[i]["fg"],
                self.button_info[i].label,
            ]
            to_csv_info.append(info)
        
        #update csv
        with open(filename, 'w', newline='', encoding="utf-8") as f:
            header = ["title", "url", "bg", "fg", "label"]
            output_writer = csv.writer(f)
            output_writer.writerow(header)
            for row in to_csv_info:
                output_writer.writerow(row)


class ShortCutButton(tkinter.Button):
    """
    simple short cut button widget.
    open the url when clicked with webbrowser module    
    """

    dummy_button = False

    def __init__(self, master, row):
        self.url = row[1]
        self.label = row[4]
        self.root = master
        super().__init__(
            master,
            text=row[0],
            background=row[2],
            foreground=row[3],
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

            self.button_info = [self["text"], self.url, self["bg"], self["fg"], self.label]
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

        if event.y < self.swap_count * self.winfo_height() and self.root.button_info.index(self) + self.swap_count != 0:
            index = self.root.button_info.index(self) + self.swap_count
            self.swap_count -= 1
            self.root.swap_button(index, index - 1)

        if event.y > (self.swap_count + 1) * self.winfo_height() and self.root.button_info.index(self) + self.swap_count != len(self.root.button_info) - 1:
            index = self.root.button_info.index(self) + self.swap_count
            self.swap_count += 1
            self.root.swap_button(index, index + 1)

    def mouse_on(self, event):
        self["relief"] = "solid"
        if self["state"] == "disabled":
            self["state"] = "normal"

    def mouse_leave(self, event):
        self["relief"] = "groove"

    def shortcut(self):
        if self.url != "":
            print(self["text"], self.url, self["bg"], self["fg"], self.label)
            #webbrowser.open(self.url)
        else:
            new_window = tkinter.Toplevel()
            DisplayMainForm(new_window, self)

    def delete_info_from_csv_and_remove_button(self, title):
        self.root.button_info.remove(self)
        if self.url == "":
            label = self["text"]
        else:
            label = None
        self.root.update_csv(label)
        self.destroy()

    def modify_button_info(self):
        try:
            dialog = ButtonInformationInputDialog(self.root)
            new_info = dialog.ask_info(
                self["text"],
                self.url,
                bg=self["bg"],
                fg=self["fg"]
            )
            self["text"] = new_info[0]
            self.url = new_info[1]
            self["bg"] = new_info[2]
            self["fg"] = new_info[3]
            self.root.update_csv()
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
        if info:
            new_button = ShortCutButton(self.labelframe, info)
            new_button.pack(pady=1)
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
        #title, url, bg, fg = input_dialog.InputDialog(self.root, default_title, default_url, bg=bg, fg=fg).result
        result = input_dialog.InputDialog(self.root, default_title, default_url, bg=bg, fg=fg).result
        if result:
            if (result[0] == None or result[0] == ''):
                tkinter.messagebox.showerror("error", "Title is empty.")
            elif (self.root["text"] != "main" and result[1] == ''):
                tkinter.messagebox.showerror("error", "URL is empty.")
            else:
                result.append(self.root["text"])
                if default_title:   #modify button information
                    return(result)
                else:               #create new button
                    self.add_info_to_csv(result)
                    return(result)
    
    def add_info_to_csv(self, title, url, bg, fg, label):
        filename = os.path.join(os.getcwd(), 'list.csv')
        if os.path.exists(filename):
            with open(filename, 'a', newline='', encoding="utf-8") as f:
                output_writer = csv.writer(f)
                output_writer.writerow([title, url, bg, fg, label])
            
    def check_title_isin_csv(self, title):
        filename = os.path.join(os.getcwd(), 'list.csv')
        with open(filename) as instream:
            # Setup the input
            file_reader = csv.reader(instream)
            for row in file_reader:
                if row[0] == title:
                    return title

if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tkinter.Tk()
    DisplayMainForm(root)
    root.mainloop()