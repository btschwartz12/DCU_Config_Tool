import os
import tkinter
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showerror
from config.config import Config
from src.gui.main_screen import DcuWorksheetPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()


        
        # Runtime data


        try:
            self.config = Config()
        except Exception as e:
            raise e

        fn = os.path.join(self.config.SRC_DIR, 'data/misc/aclara.png')
        photo = tk.PhotoImage(file = fn)
        self.iconphoto(True, photo)

        self.__buildGUI()


    def __buildGUI(self):

        self.title("DCU Config Tool")
        self.geometry(self.config.REG_DIMENSIONS)
        min_dim = self.config.MIN_DIMENSIONS.split('x')
        max_dim = self.config.MAX_DIMENSIONS.split('x')
        self.minsize(min_dim[0], min_dim[1])
        self.maxsize(max_dim[0], max_dim[1])

        container = tk.Frame(self, bg="#444343")
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.DCU_PAGE = DcuWorksheetPage(container, self.config)
        self.DCU_PAGE.pack(fill=tkinter.BOTH, expand=True)

        menubar = self.DCU_PAGE.create_menubar(self)

        self.configure(menu=menubar)

        self.DCU_PAGE.grab_set()
        self.DCU_PAGE.tkraise()

def main():
    window = App()
    window.mainloop()


if __name__ == "__main__":
    
    try: 
        main()
    except Exception as e:
        showerror("Fatal error!", "Config Editor crashed.\n\n"+str(e))
        raise  