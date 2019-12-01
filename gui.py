import tkinter as tk

class BusTimeApp:
    def __init__(self, master):
        self.master = master
        self.master.winfo_toplevel().title("Bus Time Display")

        self.is_fullscreen = False
        self.master.bind('<Command-f>', self.toggle_fullscreen)

        self.WIDTH = root.winfo_screenwidth()
        self.HEIGHT = root.winfo_screenheight()

        self.background_color = '#181d22'

        self.canvas = tk.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg=self.background_color)
        self.canvas.pack()

        self.top_frame = tk.Frame(self.master, bd=5, bg=self.background_color)
        self.top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        self.top_bus_widget = self.BusTimeWidget(self.top_frame, 'Q39', 'LI CITY QUEENS PLZ', 15)

        self.lower_frame = tk.Frame(self.master, bd=5, bg=self.background_color)
        self.lower_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        self.lower_bus_widget = self.BusTimeWidget(self.lower_frame, 'Q67', 'LI CITY QUEENS PLZ', 1)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen
        self.is_fullscreen = not self.is_fullscreen
        root.attributes('-fullscreen', self.is_fullscreen)
        return "break"

    class BusTimeWidget:
        def __init__(self, frame, line_name, destination_name, wait_time):

            self.line_name = line_name
            self.destination_name = destination_name
            self.wait_time = wait_time

            self.frame = frame
            self.frame_button = tk.Button(self.frame, command=lambda: print("Button Pressed"))
            self.frame_button.place(relwidth=1, relheight=1)

            bus_line_label = tk.Button(self.frame_button, text=line_name, font=('Roboto', 150, 'bold'), bg='#4d94ff')
            bus_line_label.place(relx=0.025, rely=0.25, relwidth=0.25, relheight=0.5)

            destination_label = tk.Button(self.frame_button, text=destination_name, font=('Roboto', 60, 'bold'), relief='flat')
            destination_label.place(relx=0.3, rely=0.25, relwidth=0.45, relheight=0.5)

            wait_time_label = tk.Button(self.frame_button, text=f"{wait_time} min", font=('Roboto', 80, 'bold'), command=self.clear)
            wait_time_label.place(relx=0.775, rely=0.25, relwidth=0.20, relheight=0.5)

        def clear(self):
            for widget in self.frame.winfo_children():
                widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    BusTimeApp(root)
    root.mainloop()
