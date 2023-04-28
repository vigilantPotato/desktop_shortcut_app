import tkinter
import ctypes


class InputDialog(tkinter.Toplevel):
    """
    show a dialog which asks user to input something
    """
    
    def __init__(self, root):
        super().__init__(root)
        self.attributes("-topmost", True)
        self.title("Input information")
        label = tkinter.Label(self, text="Title")
        label.pack()
        self.entry = tkinter.Entry(self, width=30)
        self.entry.pack()

        label2 = tkinter.Label(self, text="URL")
        label2.pack()
        self.entry2 = tkinter.Entry(self, width=50)
        self.entry2.pack()

        ok_button = tkinter.Button(
            self,
            text="OK",
            command=self.finished,
            )
        ok_button.pack()

        cancel_button = tkinter.Button(
            self,
            text="cancel",
            command=self.canceled,
        )
        cancel_button.pack()

        self.wait_visibility()
        self.grab_set()
        self.wait_window()
    
    def finished(self):
        self.result = self.entry.get(), self.entry2.get()
        self.destroy()
    
    def canceled(self):
        self.result = None
        self.destroy()


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  #resolution setting
    root = tkinter.Tk()
    print(InputDialog(root).result)
    root.mainloop()