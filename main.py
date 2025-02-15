import customtkinter
import json
from PIL import Image

customtkinter.set_appearance_mode("System")

# Creating the Scrollable Frame with all the tasks
class TaskFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        with open("task.json", "r") as f:
            tasks = json.load(f)

        self.checkboxes = []

        # Creating the Checkboxes for each incomplete task
        for i in tasks:
            if tasks[i]["completion"] == False:
                index = len(self.checkboxes)
                self.check_box = customtkinter.CTkCheckBox(
                    self,
                    text=f'Task: {tasks[i]["name"]} || Date: {tasks[i]["date"]}',
                    variable=customtkinter.StringVar(value="off"),
                    onvalue=i,
                    offvalue="off",
                    command=lambda x=index: self.checked(x),
                )
                self.check_box.pack(padx=20, pady=20)
                self.checkboxes.append(
                    self.check_box
                )  # Adding Checkbox to a list of Checkboxes for easier access later

    def checked(self, index):
        task = self.checkboxes[index].cget("onvalue")

        with open("task.json", "r") as f:
            tasks = json.load(f)

        tasks[task]["completion"] = True

        with open("task.json", "w") as f:
            json.dump(tasks, f)

        self.checkboxes[index].configure(
            state="disabled"
        )  # Makes Checkbox unclickable after being checked


class advcsUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ADVCS")
        self.geometry("1100x580")
        self.resizable(False, False)

        # Use Image as background

        self.image = Image.open("forest.jpg")
        self.background_image = customtkinter.CTkImage(self.image, size=(1100, 580))

        self.background_label = customtkinter.CTkLabel(
            self, image=self.background_image
        )
        self.background_label.place(x=0, y=0)

        self.task_frame = TaskFrame(
            master=self, width=600, height=540, corner_radius=0, fg_color="transparent"
        )
        self.task_frame.pack(padx=20, pady=20)
        self.task_frame.place(x=300, y=20)

        self.task = customtkinter.CTkEntry(
            self, placeholder_text="Task", width=200, height=30
        )
        self.task.pack(padx=20, pady=20)
        self.task.place(x=50, y=50)

        self.date = customtkinter.CTkEntry(
            self, placeholder_text="mm/dd/yy", width=200, height=30
        )
        self.date.pack(padx=20, pady=20)
        self.date.place(x=50, y=100)

        self.add_button = customtkinter.CTkButton(
            self, text="Add", command=self.add_task
        )
        self.add_button.pack(padx=20, pady=20)
        self.add_button.place(x=75, y=150)

        self.reload_button = customtkinter.CTkButton(
            self, text="Reload", command=self.reload_tasks
        )
        self.reload_button.pack(padx=20, pady=20)
        self.reload_button.place(x=75, y=200)

    def add_task(self):
        task = self.task.get()
        date = self.date.get()
        with open("task.json", "r") as f:
            tasks = json.load(f)

        # Creating a new dict for new task

        existing_task = len(tasks) + 1
        task_name = f"task{existing_task}"

        tasks[task_name] = {}
        tasks[task_name]["name"] = task
        tasks[task_name]["date"] = date
        tasks[task_name]["completion"] = False

        with open("task.json", "w") as f:
            json.dump(tasks, f)

        # Clearing the entry boxes

        self.task.delete(0, "end")
        self.date.delete(0, "end")

        # Creating new checkbox for new task

        index = len(self.task_frame.checkboxes)
        self.task_frame.check_box = customtkinter.CTkCheckBox(
            self.task_frame,
            text=f'Task: {tasks[task_name]["name"]} || Date: {tasks[task_name]["date"]}',
            variable=customtkinter.StringVar(value="off"),
            onvalue=task_name,
            offvalue="off",
            command=lambda x=index: self.task_frame.checked(x),
        )
        self.task_frame.check_box.pack(padx=20, pady=20)
        self.task_frame.checkboxes.append(self.task_frame.check_box)

    def reload_tasks(self):
        # Reloading the Tasks by destroying all the checkboxes and recreating them with existing tasks

        for checkbox in self.task_frame.checkboxes:
            checkbox.destroy()

        self.task_frame.checkboxes = []

        with open("task.json", "r") as f:
            tasks = json.load(f)

        for i in tasks:
            if tasks[i]["completion"] == False:
                index = len(self.task_frame.checkboxes)
                self.task_frame.check_box = customtkinter.CTkCheckBox(
                    self.task_frame,
                    text=f'Task: {tasks[i]["name"]} || Date: {tasks[i]["date"]}',
                    variable=customtkinter.StringVar(value="off"),
                    onvalue=i,
                    offvalue="off",
                    command=lambda x=index: self.task_frame.checked(x),
                )
                self.task_frame.check_box.pack(padx=20, pady=20)
                self.task_frame.checkboxes.append(self.task_frame.check_box)


app = advcsUI()
app.mainloop()
