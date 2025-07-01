from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
import json
import os

FILENAME = "tasks.json"

class ToDoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.dialog = None
        self.tasks = self.load_tasks()

        self.screen = MDScreen()

        # Theme toggle button
        self.theme_btn = MDIconButton(
            icon="theme-light-dark",
            pos_hint={"center_x": 0.95, "center_y": 0.95},
            on_release=self.toggle_theme
        )
        self.screen.add_widget(self.theme_btn)

        # Title
        self.screen.add_widget(MDLabel(
            text=" To-Do List ",
            halign="center",
            pos_hint={"center_y": 0.93},
            font_style="H4",
            theme_text_color="Custom",
            text_color=(0, 1, 1, 1)
        ))

        # Input field
        self.task_input = MDTextField(
            hint_text="Enter your task",
            pos_hint={"center_x": 0.5, "center_y": 0.85},
            size_hint_x=0.85,
            mode="rectangle"
        )
        self.screen.add_widget(self.task_input)

        # Add button
        add_button = MDRaisedButton(
            text="Add Task",
            pos_hint={"center_x": 0.5, "center_y": 0.77},
            md_bg_color=(0, 0.7, 0.7, 1),
            on_release=self.add_task
        )
        self.screen.add_widget(add_button)

        # Task list box
        self.task_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        self.task_box.bind(minimum_height=self.task_box.setter("height"))

        self.scroll = ScrollView(
            size_hint=(1, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            do_scroll_x=False
        )
        self.scroll.add_widget(self.task_box)
        self.screen.add_widget(self.scroll)

        for task_data in self.tasks:
            self.add_task_to_ui(task_data)

        return self.screen

    def toggle_theme(self, instance):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"

    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:
            task_data = {"text": task_text, "done": False}
            self.tasks.append(task_data)
            self.add_task_to_ui(task_data)
            self.task_input.text = ""
            self.save_tasks()
        else:
            self.show_dialog("Please enter a task!")

    def add_task_to_ui(self, task_data):
        item_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="50dp", padding=10)

        label = MDLabel(
            text="✔️ " + task_data["text"] if task_data["done"] else task_data["text"],
            halign="left",
            valign="middle",
            theme_text_color="Custom",
            text_color=(0, 1, 0, 1) if task_data["done"] else (1, 1, 1, 1)
        )

        tick_btn = MDIconButton(
            icon="check-circle" if task_data["done"] else "checkbox-blank-circle-outline",
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self.toggle_done(task_data, label, tick_btn)
        )

        delete_btn = MDIconButton(
            icon="delete",
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self.remove_task(task_data, item_layout)
        )

        item_layout.add_widget(tick_btn)
        item_layout.add_widget(label)
        item_layout.add_widget(delete_btn)
        self.task_box.add_widget(item_layout)

    def toggle_done(self, task_data, label, tick_btn):
        task_data["done"] = not task_data["done"]
        label.text = "✔️ " + task_data["text"] if task_data["done"] else task_data["text"]
        label.text_color = (0, 1, 0, 1) if task_data["done"] else (1, 1, 1, 1)
        tick_btn.icon = "check-circle" if task_data["done"] else "checkbox-blank-circle-outline"
        self.save_tasks()

    def remove_task(self, task_data, item_layout):
        self.task_box.remove_widget(item_layout)
        self.tasks = [t for t in self.tasks if t != task_data]
        self.save_tasks()

    def save_tasks(self):
        with open(FILENAME, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                return json.load(f)
        return []

    def show_dialog(self, msg):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Warning!",
            text=msg,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

ToDoApp().run()
