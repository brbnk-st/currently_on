import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import json
from PIL import Image
import datetime
import uuid

THEME_MODE = ""
COLORS = {"1":"#DD2222", "2":"#F0C119", "3":"#10BA00"}

basedir = os.path.dirname(__file__)
ctk.set_appearance_mode("dark")

def load_tasks():
    try:
        with open("currentlyon.json", 'r') as file:
            tasks_dict = json.load(file)
            tasks = tasks_dict["tasks"]
        
        tasks.sort(key=lambda x: int(x["urgency"]))
    except json.JSONDecodeError:
        return False
    return tasks

class TaskFrame(ctk.CTkFrame):
    def __init__(self, master, custom_text, taskid, date, urgency, width = 300, height = 200):
        super().__init__(master, width, height)


        self.text_label = ctk.CTkLabel(self, text=custom_text,
                                       width=270, height=100, wraplength=250, fg_color=COLORS[urgency], corner_radius=15)
        self.text_label.grid(column=0, row=0, columnspan=3)

        # self.button1 = ctk.CTkCheckBox(self, text='', width=10, height=10)
        # self.button1.grid(column=0, row=1)

        self.spacer = ctk.CTkLabel(self, text=f"{date}\n {taskid}", width=50, font=("Swis721 Lt BT", 8), text_color="#BCBCBE")
        self.spacer.grid(column=1, row=1)

        self.button2 = ctk.CTkButton(self, text='Cmplt', width=45, height=20, command=self.destroy)
        self.button2.grid(column=2, row=1)
 
class TasksContainer(ctk.CTkScrollableFrame):
    def __init__(self, master, values, width, height):
        super().__init__(master, width, height)
        self.grid_columnconfigure(0, weight=1)
        
        self.values = values
        self.frames = []

        if self.values == False:
            self.initial_state()
            return

        self.create_task_frames()
    
    def initial_state(self):
        frame = ctk.CTkFrame(self, width=300, height=300)
        label = ctk.CTkLabel(frame, text="You are currently not tracking any tasks...\n Add one usnig the button below.", width=270, height=100, wraplength=250)
        frame.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="w")
        label.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="w")

        self.frames.append(frame)

    def create_task_frames(self):
        for i, value in enumerate(self.values):
            frame = TaskFrame(self, custom_text=value["text"], taskid=value["taskID"], date=value["date_created"], urgency=value["urgency"])

            frame.grid(column=0, row=i, padx=10, pady=(10, 0), sticky="w")
            self.frames.append(frame)
    
    def refresh_tasks(self, new_values):
        for frame in self.frames:
            frame.destroy()
        self.frames.clear()

        self.values = new_values
        self.create_task_frames()
        
class NewTask(ctk.CTkToplevel):
        def __init__(self):
            super().__init__()

            self.title("Add New Task")
            self.geometry("350x350")
            self.attributes('-topmost', True)

            self.urgency_label = ctk.CTkLabel(self, text="Urgency: ")
            self.urgency_label.grid(column=0, row=1, padx=10, pady=20)
            self.text_label = ctk.CTkLabel(self, text="Task description: ")
            self.text_label.grid(column=0, row=2, padx=10, pady=20, sticky='n')

            
            self.urgency = ctk.CTkComboBox(self, width=100, height=20, values=["1", "2", "3"])
            self.urgency.grid(column=1, row=1, padx=10, pady=20)
            self.task_text = ctk.CTkTextbox(self, width=200, height=200)
            self.task_text.grid(column=1, row=2, padx=10, pady=20)

            self.add_btn = ctk.CTkButton(self, text="Add", width=300, command=self.add_task)
            self.add_btn.grid(column=0, row=3, columnspan=3)
            
        def add_task(self):
            tasks = load_tasks()
            if tasks == False:
                tasks = []

            urgency = self.urgency.get()
            text = self.task_text.get("1.0", ctk.END)
            now = datetime.datetime.now()
            date = now.strftime("%d-%m-%Y")
            taskid = uuid.uuid4()
            temp_task = {"taskID": f"{taskid}",
                        "date_created": f"{date}",
                        "urgency": f"{urgency}",
                        "text": f"{text}",
                        "state": "InProgress"}

            if len(text) < 2:
                messagebox.showwarning("Invalid Task", "Task entered too short or empty, please check your input.")
                self.destroy()
                return
            
            tasks.append(temp_task)
            to_json = {"tasks": tasks}
            with open("currentlyon.json", "w") as file:
                json.dump(to_json, file, indent=4)
            messagebox.showinfo("Task Created", "Succesfully added new task.")
            self.destroy()
         



class CON(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>" ,self.clickwin)
        super().bind("<B1-Motion>", self.dragwin)

        self.title("Currently-ON!")
        self.attributes('-topmost', True)
        
        
        WINDOW_HEIGHT = self.winfo_screenheight()
        WINDOW_WIDTH = 350
        
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT*0.75+1+1}")

        image = ctk.CTkImage(Image.open(os.path.join(basedir, "assets/ON.png")), size=(30, 30))
        self.icon_label =  ctk.CTkLabel(self, image=image, text="")
        self.icon_label.grid(column=0, row=0, padx=10, pady=15, sticky='n')

        self.title_label = ctk.CTkLabel(self, text='CURRENTLY ON!    ', font=("Martel Sans Bold", 18))
        self.title_label.grid(column=1, row=0, padx=10, pady=15)

        self.changeTheme_button = ctk.CTkButton(self, text='☼/☾', width=30, height=15, corner_radius=20, fg_color="#6a93ec", hover_color="#4e6bac", command=self.change_theme)
        self.changeTheme_button.grid(column=3, row=0, padx=10, pady=10, sticky='e')

        self.topBar_separator = ctk.CTkFrame(self, width=WINDOW_WIDTH-10, height=2, fg_color="#9E9999")
        self.topBar_separator.grid(column=0, row=0, columnspan=5, padx=5, sticky='s')

        self.Alltasks_frame = TasksContainer(self, values=tasks, width=WINDOW_WIDTH-50, height=(WINDOW_HEIGHT*0.75)-200)
        self.Alltasks_frame.grid(column=0, row=1, columnspan=5, padx=5, pady=5)

        self.Tasks_separator = ctk.CTkFrame(self, width=WINDOW_WIDTH-10, height=2, fg_color="#9E9999")
        self.Tasks_separator.grid(column=0, row=2, columnspan=5, padx=5, sticky='s')

        self.addtask_button = ctk.CTkButton(self, text="+ Add New Task", width=270, height=50, command=self.add_task_window)
        self.addtask_button.grid(column=0, row=3, columnspan=5, padx=10, pady=20)

    def add_task_window(self):
        new_task_window = NewTask()
        new_task_window.iconbitmap(os.path.join(basedir, "assets\\ON.ico"))
        self.attributes('-topmost', False)
        new_task_window.attributes('-topmost', True)

        self.wait_window(new_task_window)

        new_tasks = load_tasks()
        self.Alltasks_frame.refresh_tasks(new_tasks)


    def dragwin(self, event):
        x = super().winfo_pointerx() - self._offsetx
        y = super().winfo_pointery() - self._offsety
        super().geometry(f"+{x}+{y}")

    def clickwin(self, event):
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
    tasks = load_tasks()
    app = CON()


    app.iconbitmap(os.path.join(basedir, "assets\\ON.ico"))
    app.mainloop()


#TODO 
# Add a archive of completed tasks and use a method to erase the frame from the tasks, and move it from the "tasks" in the json file to "completed".