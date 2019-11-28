import tkinter as tk

root = tk.Tk()
is_fullscreen = False
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
background_color = '#181d22'

def toggle_fullscreen(self, event=None):
        global is_fullscreen
        is_fullscreen = not is_fullscreen
        root.attributes('-fullscreen', is_fullscreen)
        return "break"

root.bind('<Command-f>', toggle_fullscreen)

class BusWidget:
    def __init__(self, frame):
        self.frame = frame
        self.frame_button = tk.Button(self.frame, command=lambda: print("Button Pressed"))
        self.frame_button.place(relwidth=1, relheight=1)

        bus_line_label = tk.Button(self.frame_button, text="Q39", font=('Roboto', 150, 'bold'), bg='#4d94ff')
        bus_line_label.place(relx=0.025, rely=0.25, relwidth=0.25, relheight=0.5)

        destination_label = tk.Button(self.frame_button, text="LI CITY QUEENS PLZ", font=('Roboto', 60, 'bold'), relief='flat')
        destination_label.place(relx=0.3, rely=0.25, relwidth=0.45, relheight=0.5)

        wait_time_label = tk.Button(self.frame_button, text="15 min", font=('Roboto', 80, 'bold'))
        wait_time_label.place(relx=0.775, rely=0.25, relwidth=0.20, relheight=0.5)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=background_color)
canvas.pack()

top_frame = tk.Frame(root, bd=5, bg=background_color)
top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)

top_bus_widget = BusWidget(top_frame)

lower_frame = tk.Frame(root, bd=5, bg=background_color)
lower_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

lower_bus_widget = BusWidget(lower_frame)

root.mainloop()