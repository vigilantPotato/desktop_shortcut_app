import tkinter
from tkinter import colorchooser
import ctypes


class InputDialog(tkinter.Toplevel):
    """
    show a dialog which asks user to input something
    return title and url as tuple
    if canceled, return None
    """
    
    def __init__(self, root, default_title=None, default_url=None):
        super().__init__(root)
        self.root = root

        frame1 = tkinter.Frame(self)
        frame1.pack(padx=5, pady=5)

        #demo button
        label = tkinter.Label(frame1, text="Demo : ")
        label.grid(row=0, column=0)
        self.var = tkinter.StringVar(root)
        demo_button = TestButton(frame1, self.var)
        demo_button.grid(row=0, column=1, sticky="w")

        #title
        self.attributes("-topmost", True)
        self.title("Input information")
        label = tkinter.Label(frame1, text="Title : ")
        label.grid(row=1, column=0)
        self.entry = tkinter.Entry(frame1, width=30, textvariable=self.var)
        if default_title:
            self.entry.insert(0, default_title)
        self.entry.grid(row=1, column=1, sticky="w")

        #url
        label = tkinter.Label(frame1, text="URL : ")
        label.grid(row=2, column=0)
        self.entry2 = tkinter.Entry(frame1, width=50)
        if default_url:
            self.entry2.insert(0, default_url)
        self.entry2.grid(row=2, column=1)

        #color setting
        label = tkinter.Label(frame1, text="Background Color: ")
        label.grid(row=3, column=0)
        self.color_select = ColorSelectButton(frame1, text="background", button=demo_button)
        self.color_select.grid(row=3, column=1, sticky="w")

        label = tkinter.Label(frame1, text="Text Color: ")
        label.grid(row=4, column=0)
        self.color_select = ColorSelectButton(frame1, text="text color", button=demo_button)
        self.color_select.grid(row=4, column=1, sticky="w")

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
        self.result = self.entry.get(), self.entry2.get()
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
        color = colorchooser.askcolor()[1]
        if self["text"] == "background":
            self.button["bg"] = color
        elif self["text"] == "text color":
            self.button["fg"] = color


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
    print(InputDialog(root).result)
    root.mainloop()