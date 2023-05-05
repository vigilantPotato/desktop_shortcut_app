import tkinter
import ctypes


class InputDialog(tkinter.Toplevel):
    """
    show a dialog which asks user to input something
    """
    
    def __init__(self, root):
        super().__init__(root)
        frame1 = tkinter.Frame(self)
        frame1.pack(padx=5, pady=5)

        self.attributes("-topmost", True)
        self.title("Input information")
        label = tkinter.Label(frame1, text="Title : ")
        label.grid(row=0, column=0)
        self.entry = tkinter.Entry(frame1, width=30)
        self.entry.grid(row=0, column=1, sticky="w")

        label2 = tkinter.Label(frame1, text="URL : ")
        label2.grid(row=1, column=0)
        self.entry2 = tkinter.Entry(frame1, width=50)
        self.entry2.grid(row=1, column=1)

        frame2 = tkinter.Frame(self)
        frame2.pack(padx=5, pady=5)
        
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
        self.cancel_button.pack(side=tkinter.LEFT)

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

if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  #resolution setting
    root = tkinter.Tk()
    print(InputDialog(root).result)
    root.mainloop()