from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import os

# Set Kivy window size
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

class Algorithm_SelectorApp(App):
    def build(self):
        # Create main layout with padding and spacing
        main_layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20), size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Create dropdown menu
        dropdown = DropDown()

        # Add options to the dropdown menu
        options = ["FCFS", "RR", "PS", "SJF"]
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=dp(44), size_hint_x=1)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        # Create main button to display dropdown, centered
        main_button = Button(text='Select Algorithm', size_hint=(None, None), width=dp(200), height=dp(50), pos_hint={'center_x': 0.5})
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=self.on_select)

        # Add main button to layout
        main_layout.add_widget(main_button)

        # Add label to display output
        self.output_label = Label(size_hint=(1, None), height=dp(500), text_size=(None, None))
        main_layout.add_widget(self.output_label)

        # Wrap the main layout in a ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(main_layout)
        return scroll

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
