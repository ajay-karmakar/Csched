from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class PrioritySchedulingApp(App):
    def build(self):
        self.process_input_widgets = []

        # Create GUI layout
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Add text input for number of processes
        self.num_processes_input = TextInput(hint_text="Enter number of processes")
        layout.add_widget(self.num_processes_input)

        # Add button to dynamically generate input fields based on the number of processes
        generate_button = Button(text="Generate Input Fields", on_press=self.generate_input_fields)
        layout.add_widget(generate_button)

        # Add button to trigger Priority Scheduling calculation
        calculate_button = Button(text="Calculate Priority Scheduling")
        calculate_button.bind(on_press=self.calculate_priority_scheduling)
        layout.add_widget(calculate_button)

        # Add label to display output
        self.output_label = Label(size_hint=(1, None), height=500)
        layout.add_widget(self.output_label)

        return layout

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

        # Generate input fields based on the number of processes
        for i in range(num_processes):
            process_label = Label(text=f"Process {i + 1}:")
            process_input = TextInput(hint_text=f"Enter burst time and priority for process {i + 1}")
            self.process_input_widgets.extend([process_label, process_input])

        # Update layout
        layout = self.root
        layout.clear_widgets()
        layout.add_widget(self.num_processes_input)
        layout.add_widget(Button(text="Generate Input Fields", on_press=self.generate_input_fields))
        for widget in self.process_input_widgets:
            layout.add_widget(widget)
        layout.add_widget(Button(text="Calculate Priority Scheduling", on_press=self.calculate_priority_scheduling))
        layout.add_widget(self.output_label)

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
                processes.append((i + 1, burst_time, priority))
        except (ValueError, IndexError):
            self.output_label.text = "Error: Invalid input for process values"
            return

        # Sort processes based on priority
        processes.sort(key=lambda x: x[2])

        # Calculate Priority Scheduling
        turnaround_times = []
        waiting_times = []
        total_turnaround_time = 0
        total_waiting_time = 0
        current_time = 0
        execution_order = []

        for process in processes:
            execution_order.append(process[0])
            current_time += process[1]
            turnaround_time = current_time
            waiting_time = turnaround_time - process[1]
            turnaround_times.append(turnaround_time)
            waiting_times.append(waiting_time)
            total_turnaround_time += turnaround_time
            total_waiting_time += waiting_time

        # Calculate average turnaround time and average waiting time
        avg_turnaround_time = total_turnaround_time / num_processes
        avg_waiting_time = total_waiting_time / num_processes

        # Prepare output
        output_text = "Process No.\tBurst Time\tPriority\tTurnaround Time\tWaiting Time\n"
        for i in range(num_processes):
            output_text += f"{processes[i][0]}\t\t{processes[i][1]}\t\t{processes[i][2]}\t\t{turnaround_times[i]}\t\t{waiting_times[i]}\n"
        output_text += f"\nExecution Order: {' -> '.join(map(str, execution_order))}\n\nAverage Turnaround Time: {avg_turnaround_time}\nAverage Waiting Time: {avg_waiting_time}"

        # Update output label
        self.output_label.text = output_text

if __name__ == '__main__':
    PrioritySchedulingApp().run()
