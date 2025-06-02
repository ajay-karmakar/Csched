from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

class PrioritySchedulingApp(App):
    def build(self):
        self.process_input_widgets = []

        # Create the main layout (vertical BoxLayout)
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=dp(20), size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Add text input for number of processes
        self.num_processes_input = TextInput(hint_text="Enter number of processes", size_hint=(1, None), height=dp(40), multiline=False)
        main_layout.add_widget(self.num_processes_input)

        # Add button to dynamically generate input fields based on the number of processes
        generate_button = Button(text="Generate Input Fields", size_hint=(1, None), height=dp(40))
        generate_button.bind(on_press=self.generate_input_fields)
        main_layout.add_widget(generate_button)

        # Add button to trigger Priority Scheduling calculation
        calculate_button = Button(text="Calculate Priority Scheduling", size_hint=(1, None), height=dp(40))
        calculate_button.bind(on_press=self.calculate_priority_scheduling)
        main_layout.add_widget(calculate_button)

        # Add a container for process input fields
        self.process_inputs_container = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        self.process_inputs_container.bind(minimum_height=self.process_inputs_container.setter('height'))
        main_layout.add_widget(self.process_inputs_container)

        # Add label to display output
        self.output_label = Label(size_hint=(1, None), height=dp(500), text_size=(None, None))
        main_layout.add_widget(self.output_label)

        # Wrap the main layout in a ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(main_layout)
        return scroll

    def generate_input_fields(self, instance):
        try:
            num_processes = int(self.num_processes_input.text)
            if num_processes <= 0:
                raise ValueError
        except ValueError:
            self.output_label.text = "Error: Invalid input for number of processes"
            return

        # Clear previous input fields
        self.process_input_widgets.clear()
        self.process_inputs_container.clear_widgets()

        # Generate input fields based on the number of processes
        for i in range(num_processes):
            process_label = Label(text=f"Process {i + 1}:", size_hint_y=None, height=dp(40))
            process_input = TextInput(hint_text=f"Enter burst time and priority for process {i + 1}", size_hint_y=None, height=dp(40), multiline=False)
            self.process_inputs_container.add_widget(process_label)
            self.process_inputs_container.add_widget(process_input)
            self.process_input_widgets.extend([process_label, process_input])

    def calculate_priority_scheduling(self, instance):
        try:
            num_processes = int(self.num_processes_input.text)
            if num_processes <= 0:
                raise ValueError
        except ValueError:
            self.output_label.text = "Error: Invalid input for number of processes"
            return

        processes = []
        try:
            for i in range(num_processes):
                process_values = self.process_input_widgets[i * 2 + 1].text.split()
                if len(process_values) != 2:
                    raise ValueError
                burst_time = int(process_values[0])
                priority = int(process_values[1])
                processes.append({'pid': i + 1, 'burst_time': burst_time, 'priority': priority})
        except (ValueError, IndexError):
            self.output_label.text = "Error: Invalid input for process values"
            return

        # Sort processes based on priority (lower value = higher priority)
        processes_sorted = sorted(processes, key=lambda x: x['priority'])

        # Calculate waiting and turnaround times
        waiting_times = [0] * num_processes
        turnaround_times = [0] * num_processes
        current_time = 0
        execution_order = []
        for idx, proc in enumerate(processes_sorted):
            execution_order.append(proc['pid'])
            waiting_times[idx] = current_time
            current_time += proc['burst_time']
            turnaround_times[idx] = current_time

        # Map results back to original process order for output
        pid_to_result = {proc['pid']: (proc['burst_time'], proc['priority'], turnaround_times[i], waiting_times[i]) for i, proc in enumerate(processes_sorted)}

        # Calculate averages
        avg_turnaround_time = sum(turnaround_times) / num_processes
        avg_waiting_time = sum(waiting_times) / num_processes

        # Prepare output
        output_text = "Process No.\tBurst Time\tPriority\tTurnaround Time\tWaiting Time\n"
        for i in range(1, num_processes + 1):
            bt, pr, tat, wt = pid_to_result[i]
            output_text += f"{i}\t\t{bt}\t\t{pr}\t\t{tat}\t\t{wt}\n"
        output_text += f"\nExecution Order: {' -> '.join(map(str, execution_order))}\n\nAverage Turnaround Time: {avg_turnaround_time}\nAverage Waiting Time: {avg_waiting_time}"

        self.output_label.text = output_text

if __name__ == '__main__':
    PrioritySchedulingApp().run()
