import tkinter as tk
import bustime
from operator import attrgetter
from collections import namedtuple
from os import environ
from twilio.rest import Client

class BusTimeApp:

    Notification = namedtuple('Notification', 'vehicle_ref, wait_time')

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

        self.upper_frame = tk.Frame(self.master, bd=5, bg=self.background_color)
        self.upper_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        self.lower_frame = tk.Frame(self.master, bd=5, bg=self.background_color)
        self.lower_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        self.fixtures = []
        self.lower_bus_time = 1 # Index of bus time displayed in lower_frame

        self.account_sid = environ['TWILIO_ACCOUNT_SID']
        self.auth_token = environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)
        self.twilio_phone = '+12055513213'

        self.phone_number = environ['MY_PHONE_NUMBER']

        self.notification = None

        self.display_bus_times()

    def display_bus_times(self):
        q39_fixtures = bustime.bus_times(503991, dump_json=True)
        q67_fixtures = bustime.bus_times(505168, 'MTABC_Q67')

        self.clear_bus_times()

        self.fixtures = sorted(q39_fixtures + q67_fixtures,
                               key=attrgetter('estimated_wait_time'))

        if self.fixtures:
            self.upper_bus_widget = self.BusTimeWidget(self, self.upper_frame,
                                                       self.fixtures[0], 1)

            if len(self.fixtures) > 1:
                print(self.lower_bus_time)

                # Handle case where length of fixtures decreases
                # below lower_bus_time
                if self.lower_bus_time >= len(self.fixtures):
                    self.lower_bus_time = len(self.fixtures) - 1

                self.lower_bus_widget = self.BusTimeWidget(self,
                                             self.lower_frame,
                                             self.fixtures[self.lower_bus_time],
                                             self.lower_bus_time + 1)

                # Cycle through bus times after the first
                self.lower_bus_time = ((self.lower_bus_time) % (len(self.fixtures) - 1)) + 1

        self.master.after(5000, self.display_bus_times)

    def set_notification(self, vehicle_ref, wait_time=5):
        self.notification = self.Notification(vehicle_ref, wait_time)
        print("Notification Set")
        self.notify()

    def notify(self):
        for bus_time in self.fixtures:
            if (self.notification.vehicle_ref == bus_time.vehicle_ref and
                    self.notification.wait_time >= bus_time.estimated_wait_time):

                message_text = f"{bus_time.line_name} to {bus_time.destination_name} " \
                               f"arriving in {bus_time.estimated_wait_time} min."

                message = self.client.messages \
                              .create(
                                   body=message_text,
                                   from_=self.twilio_phone,
                                   to=self.phone_number
                               )
                print("SMS sent.")

                self.notification = None
                return

        self.master.after(5000, self.notify)

    def clear_bus_times(self):
        for widget in self.upper_frame.winfo_children():
            widget.destroy()
        for widget in self.lower_frame.winfo_children():
            widget.destroy()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen
        self.is_fullscreen = not self.is_fullscreen
        root.attributes('-fullscreen', self.is_fullscreen)
        return "break"

    class BusTimeWidget:
        def __init__(self, bustime_app, frame, bus_time, position):

            self.bustime_app = bustime_app
            self.frame = frame
            self.bus_time = bus_time # BusTime namedtuple
            self.position = position

            self.frame_button = tk.Button(self.frame, command=lambda: self.bustime_app.set_notification(self.bus_time.vehicle_ref))
            self.frame_button.place(relwidth=1, relheight=1)

            position_label = tk.Button(self.frame_button, text=f"{self.position}.", font=('Roboto', 60, 'bold'), command=lambda: self.bustime_app.set_notification(self.bus_time.vehicle_ref))
            position_label.place(relx=0.025, rely=0.025, relwidth=0.05, relheight=0.2)

            bus_line_label = tk.Button(self.frame_button, text=self.bus_time.line_name, font=('Roboto', 150, 'bold'), command=lambda: self.bustime_app.set_notification(self.bus_time.vehicle_ref))
            bus_line_label.place(relx=0.025, rely=0.25, relwidth=0.25, relheight=0.5)

            destination_label = tk.Button(self.frame_button, text=self.bus_time.destination_name, font=('Roboto', 60, 'bold'), command=lambda: self.bustime_app.set_notification(self.bus_time.vehicle_ref))
            destination_label.place(relx=0.3, rely=0.25, relwidth=0.45, relheight=0.5)

            wait_time_label = tk.Button(self.frame_button, text=f"{self.bus_time.estimated_wait_time} min", font=('Roboto', 80, 'bold'), command=lambda: self.bustime_app.set_notification(self.bus_time.vehicle_ref))
            wait_time_label.place(relx=0.775, rely=0.25, relwidth=0.20, relheight=0.5)

        def clear(self):
            for widget in self.frame.winfo_children():
                widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    BusTimeApp(root)
    root.mainloop()
