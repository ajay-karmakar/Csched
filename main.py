from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
import os

# Set Kivy window size
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

class Algorithm_SelectorApp(App):
    def build(self):
        # Create GUI layout
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Create dropdown menu
        dropdown = DropDown()

        # Add options to the dropdown menu
        options = ["FCFS", "RR", "PS", "SJF"]
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        # Create main button to display dropdown
        main_button = Button(text='Select Algorithm', size_hint=(None, None), width=200, height=50)
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=self.on_select)

        # Add main button to layout
        layout.add_widget(main_button)

        # Add label to display output
        self.output_label = Label(size_hint=(1, None), height=500)
        layout.add_widget(self.output_label)

        return layout

    def on_select(self, instance, value):
        # Execute the selected algorithm code
        file_path = f"{value}.py"
        if os.path.exists(file_path):
            output = os.popen(f"python {file_path}").read()
            self.output_label.text = output
        else:
            self.output_label.text = f"Error: {value}.py file not found."

if __name__ == '__main__':
    Algorithm_SelectorApp().run()
