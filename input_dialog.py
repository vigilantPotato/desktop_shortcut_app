import tkinter
from tkinter import colorchooser
import ctypes


class InputDialog(tkinter.Toplevel):
    """
    show a dialog which asks user to input something
    return title and url as tuple
    if canceled, return None
    """
    
    def __init__(self, root, default_title=None, default_url=None, bg=None, fg=None):
        super().__init__(root)
        self.root = root
        self.var = tkinter.StringVar(root)

        #demo button
        demo_frame = tkinter.LabelFrame(self, text="Demo button")
        demo_frame.pack()
        self.demo_button = TestButton(demo_frame, self.var, default_bg=bg, default_fg=fg)
        self.demo_button.pack(padx=5, pady=5)

        #input information frame
        input_frame = tkinter.LabelFrame(self, text="Input button information")
        input_frame.pack()

        #title
        self.title("Input information")
        label = tkinter.Label(input_frame, text="Title : ")
        label.grid(row=0, column=0)
        self.entry = tkinter.Entry(input_frame, width=30, textvariable=self.var)
        if default_title:
            self.entry.insert(0, default_title)
        self.entry.grid(row=0, column=1, sticky="w")

        #url
        label = tkinter.Label(input_frame, text="URL : ")
        label.grid(row=1, column=0)
        self.entry2 = tkinter.Entry(input_frame, width=50)
        if default_url:
            self.entry2.insert(0, default_url)
        self.entry2.grid(row=1, column=1)

        #color setting
        color_setting_frame = tkinter.LabelFrame(self, text="Button color setting")
        color_setting_frame.pack()
        self.color_select = ColorSelectButton(color_setting_frame, text="Background", button=self.demo_button)
        self.color_select.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.color_select = ColorSelectButton(color_setting_frame, text="Text", button=self.demo_button)
        self.color_select.pack(side=tkinter.LEFT, padx=5, pady=5)

        frame2 = tkinter.Frame(self)
        frame2.pack(padx=5, pady=5)

        #ok and cancel butons
        self.ok_button = tkinter.Button(
            frame2,
            text="OK",
            width=15,
            background="SeaGreen1",
            command=self.finished,
            )
        self.ok_button.bind("<Motion>", self.mouse_on_ok)
        self.ok_button.bind("<Leave>", self.mouse_leave_ok)
        self.ok_button.pack(side=tkinter.LEFT)

        self.cancel_button = tkinter.Button(
            frame2,
            text="Cancel",
            width=15,
            background="light pink",
            command=self.canceled,
        )
        self.cancel_button.bind("<Motion>", self.mouse_on_cancel)
        self.cancel_button.bind("<Leave>", self.mouse_leave_cancel)
        self.cancel_button.bind("<Map>", self.locate_form)
        self.cancel_button.pack(side=tkinter.LEFT)
        self.protocol("WM_DELETE_WINDOW", self.canceled)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()
    
    def finished(self):
        self.result = self.entry.get(), self.entry2.get(), self.demo_button["bg"], self.demo_button["fg"]
        self.destroy()
    
    def canceled(self):
        self.result = None
        self.destroy()

    def mouse_on_ok(self, event):
        self.ok_button["background"] = "green"
        self.ok_button["foreground"] = "white"

    def mouse_leave_ok(self, event):
        self.ok_button["background"] = "SeaGreen1"
        self.ok_button["foreground"] = "black"

    def mouse_on_cancel(self, event):
        self.cancel_button["background"] = "red"
        self.cancel_button["foreground"] = "white"

    def mouse_leave_cancel(self, event):
        self.cancel_button["background"] = "light pink"
        self.cancel_button["foreground"] = "black"

    def locate_form(self, event):
        x = (self.root.winfo_screenwidth() - self.winfo_width()) / 2
        y = (self.root.winfo_screenheight() - self.winfo_height()) / 2
        self.geometry("+%d+%d" % (x, y))


class ColorSelectButton(tkinter.Button):
    def __init__(self, root, text, button):
        super().__init__(
            root,
            text=text,
            width=15,
            command=self.color_select
            )
        self.button = button

    def color_select(self):
        try:
            self["state"] = "disable"
            color = colorchooser.askcolor(title=self["text"])[1]
            self["state"] = "normal"
            if self["text"] == "Background":
                self.button["bg"] = color
            elif self["text"] == "Text":
                self.button["fg"] = color
        except:
            pass


class TestButton(tkinter.Button):
    def __init__(self, root, var, default_bg="cyan", default_fg="black"):
        super().__init__(
            root,
            textvariable=var,
            width=15,
            bg=default_bg,
            fg=default_fg,
            relief="groove"
        )
    
        self.bind("<Motion>", self.mouse_on)
        self.bind("<Leave>", self.mouse_leave)

    def mouse_on(self, event):
        self["relief"] = "solid"
    def mouse_leave(self, event):
        self["relief"] = "groove"

if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  #resolution setting
    root = tkinter.Tk()
    root.mainloop()