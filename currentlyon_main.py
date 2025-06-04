import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image


THEME_MODE = ""

basedir = os.path.dirname(__file__)

class TaskFrame(ctk.CTkFrame):
    def __init__(self, master, custom_text, width = 300, height = 200):
        super().__init__(master, width, height)


        self.text_label = ctk.CTkLabel(self, text=custom_text,
                                       width=270, height=100, wraplength=250, fg_color="white", corner_radius=15)
        self.text_label.grid(column=0, row=0, columnspan=3)

        self.button1 = ctk.CTkCheckBox(self, text='', width=10, height=10)
        self.button1.grid(column=0, row=1)

        self.spacer = ctk.CTkLabel(self, text='', width=50)
        self.spacer.grid(column=1, row=1)

        self.button2 = ctk.CTkButton(self, text='', width=45, height=20)
        self.button2.grid(column=2, row=1)

        

class TasksContainer(ctk.CTkScrollableFrame):
    def __init__(self, master, values, width, height):
        super().__init__(master, width, height)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.frames = []

        for i, value in enumerate(self.values):
            frame = TaskFrame(self, custom_text=value)
            frame.grid(column=0, row=i, padx=10, pady=(10, 0), sticky="w")
            self.frames.append(frame)

class CON(ctk.CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>" ,self.clickwin)
        super().bind("<B1-Motion>", self.dragwin)

        self.title("Currently-ON!")
        self.attributes('-topmost', True)
        
        
        WINDOW_HEIGHT = self.winfo_screenheight()
        WINDOW_WIDTH = 350
        
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT*0.75}")

        image = ctk.CTkImage(Image.open(os.path.join(basedir, "assets/ON.png")), size=(30, 30))
        self.icon_label =  ctk.CTkLabel(self, image=image, text="")
        self.icon_label.grid(column=0, row=0, padx=10, pady=15, sticky='n')

        self.title_label = ctk.CTkLabel(self, text='CURRENTLY ON!    ', font=("Martel Sans Bold", 18))
        self.title_label.grid(column=1, row=0, padx=10, pady=15)

        self.changeTheme_button = ctk.CTkButton(self, text='', width=15, height=15, corner_radius=20, fg_color="#6a93ec", hover_color="#4e6bac", command=self.change_theme)
        self.changeTheme_button.grid(column=2, row=0, padx=10, pady=10, sticky='w')

        self.minimize_button = ctk.CTkButton(self, text='', width=15, height=15, corner_radius=20, fg_color="#00E658", hover_color="#03B346", command=self.hide_window)
        self.minimize_button.grid(column=3, row=0, padx=10, pady=10, sticky='w')

        self.quit_button = ctk.CTkButton(self, text='', width=15, height=15, corner_radius=20, fg_color='#FE0F0F', hover_color="#C90F0F", command=self.quit)
        self.quit_button.grid(column=4, row=0, padx=10, pady=10, sticky='w')

        self.topBar_separator = ctk.CTkFrame(self, width=WINDOW_WIDTH-10, height=2, fg_color="#9E9999")
        self.topBar_separator.grid(column=0, row=0, columnspan=5, padx=0, sticky='s')

        values = ["Buy Raspberry pico", "Install Arch Linux", "Repeair Laptop screen", "Complete git course", "Impedance analyzer app in C#", "Start git course"]
        self.Alltasks_frame = TasksContainer(self, values=values, width=WINDOW_WIDTH-50, height=(WINDOW_HEIGHT*0.75)-200)
        self.Alltasks_frame.grid(column=0, row=1, columnspan=5, padx=5, pady=5)

        self.Tasks_separator = ctk.CTkFrame(self, width=WINDOW_WIDTH-10, height=2, fg_color="#9E9999")
        self.Tasks_separator.grid(column=0, row=2, columnspan=5, padx=0, sticky='s')


    def dragwin(self,event):
        x = super().winfo_pointerx() - self._offsetx
        y = super().winfo_pointery() - self._offsety
        super().geometry(f"+{x}+{y}")

    def clickwin(self,event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

    def hide_window(self):
        print('Hide window not yet implemented...')
        
    def change_theme(self):
        THEME_MODE = ctk.get_appearance_mode()
        match THEME_MODE:
            case "Dark":
                ctk.set_appearance_mode("light")
            case "Light":
                ctk.set_appearance_mode("dark")
    


if __name__ == "__main__":
    app = CON()
    app.iconbitmap(os.path.join(basedir, "assets\\ON.bmp"))

    
    app.mainloop()
