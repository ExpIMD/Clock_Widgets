import tkinter as tk
import math
import time

class round_clock:
    def __init__(self, radius: float):
        self.__root = tk.Tk()
        self.__radius = radius
        self.__canvas_size = 400
        self.__center = self.__canvas_size / 2

        self.__root.title("Round clock")
        self.__canvas = tk.Canvas(self.__root, width=self.__canvas_size, height=self.__canvas_size, bg='white')
        self.__canvas.pack()
    def run(self):
        self.draw()
        self.update_state()
        self.__root.mainloop()

    def draw(self):
        # Round label
        self.__canvas.create_oval(self.__center - self.__radius, self.__center - self.__radius,
                                self.__center + self.__radius, self.__center + self.__radius,
                                outline='black', width=4)

        # Hour labels
        for i in range(12):
            angle: float = math.pi / 6 * i

            x0: float = self.__center + (self.__radius - 20) * math.sin(angle)
            x1: float = self.__center + self.__radius * math.sin(angle)

            y0: float = self.__center - (self.__radius - 20) * math.cos(angle)
            y1: float = self.__center - self.__radius * math.cos(angle)

            self.__canvas.create_line(x0, y0, x1, y1, width=1)
            self.__canvas.create_text(x0, y0, text=(i+11) % 12 + 1)
        # Minute labels
        for i in range(60):
            if i % 5 != 0:
                angle: float = math.pi / 30 * i

                x0: float = self.__center + (self.__radius - 10) * math.sin(angle)
                x1: float = self.__center + self.__radius * math.sin(angle)

                y0: float = self.__center - (self.__radius - 10) * math.cos(angle)
                y1: float = self.__center - self.__radius * math.cos(angle)

                self.__canvas.create_line(x0, y0, x1, y1, width=1)
    
    def update_state(self):
        self.__canvas.delete("arrows")

        now = time.localtime()
        hours = now.tm_hour % 12
        minutes = now.tm_min
        seconds = now.tm_sec

        second_angle: float = math.pi / 30 * seconds
        minute_angle: float = math.pi / 30 * minutes + second_angle / 60
        hour_angle: float = math.pi / 6  * hours + minute_angle / 12

        second_length: float = self.__radius - 80
        minute_length: float = self.__radius - 50
        hour_length: float = self.__radius - 30

        xs = self.__center + second_length * math.sin(second_angle)
        ys = self.__center - second_length * math.cos(second_angle)
        self.__canvas.create_line(self.__center, self.__center, xs, ys, fill='black', width=1, tag="arrows")

        xm = self.__center + minute_length * math.sin(minute_angle)
        ym = self.__center - minute_length * math.cos(minute_angle)
        self.__canvas.create_line(self.__center, self.__center, xm, ym, fill='black', width=3, tag="arrows")

        xh = self.__center + hour_length * math.sin(hour_angle)
        yh = self.__center - hour_length * math.cos(hour_angle)
        self.__canvas.create_line(self.__center, self.__center, xh, yh, fill='black', width=5, tag="arrows")

        self.__root.after(1000, self.update_state)
