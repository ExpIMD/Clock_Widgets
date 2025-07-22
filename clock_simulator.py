import tkinter as tk
import math
import time

class round_clock:
    def __init__(self, radius: float):
        self._root = tk.Tk()
        self._radius = radius
        self._canvas_size = 800
        self._center = self._canvas_size / 2

        self._root.title("Round clock")
        self._canvas = tk.Canvas(self._root, width=self._canvas_size, height=self._canvas_size, bg='white')
        self._canvas.pack()
    def run(self):
        self.draw()
        self.update_state()
        self._root.mainloop()

    def draw(self):
        # Round label
        self._canvas.create_oval(self._center - self._radius, self._center - self._radius,
                                self._center + self._radius, self._center + self._radius,
                                outline='black', width=4)

        # Hour labels
        for i in range(12):
            angle: float = math.pi / 6 * i

            x0: float = self._center + (self._radius - 20) * math.sin(angle)
            x1: float = self._center + self._radius * math.sin(angle)

            y0: float = self._center - (self._radius - 20) * math.cos(angle)
            y1: float = self._center - self._radius * math.cos(angle)

            self._canvas.create_line(x0, y0, x1, y1, width=1)
            self._canvas.create_text(x0, y0, text=(i+11) % 12 + 1)
        # Minute labels
        for i in range(60):
            if i % 5 != 0:
                angle: float = math.pi / 30 * i

                x0: float = self._center + (self._radius - 10) * math.sin(angle)
                x1: float = self._center + self._radius * math.sin(angle)

                y0: float = self._center - (self._radius - 10) * math.cos(angle)
                y1: float = self._center - self._radius * math.cos(angle)

                self._canvas.create_line(x0, y0, x1, y1, width=1)
    
    def update_state(self):
        self._canvas.delete("arrows")

        now = time.localtime()
        hours = now.tm_hour % 12
        minutes = now.tm_min
        seconds = now.tm_sec

        second_angle: float = math.pi / 30 * seconds
        minute_angle: float = math.pi / 30 * minutes + second_angle / 60
        hour_angle: float = math.pi / 6  * hours + minute_angle / 12

        second_length: float = self._radius - 80
        minute_length: float = self._radius - 50
        hour_length: float = self._radius - 30

        xs = self._center + second_length * math.sin(second_angle)
        ys = self._center - second_length * math.cos(second_angle)
        self._canvas.create_line(self._center, self._center, xs, ys, fill='black', width=1, tag="arrows")

        xm = self._center + minute_length * math.sin(minute_angle)
        ym = self._center - minute_length * math.cos(minute_angle)
        self._canvas.create_line(self._center, self._center, xm, ym, fill='black', width=3, tag="arrows")

        xh = self._center + hour_length * math.sin(hour_angle)
        yh = self._center - hour_length * math.cos(hour_angle)
        self._canvas.create_line(self._center, self._center, xh, yh, fill='black', width=5, tag="arrows")

        self._root.after(1000, self.update_state)

class digital_clock:
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Digital clock")
        self.__label = tk.Label(self.__root, font=("DS-Digital", 100), bg="black", fg="red")
        self.__label.pack(padx=40, pady=40)

    def update_state(self):
        now = time.strftime("%H:%M:%S")
        self.__label.config(text=now)
        self.__root.after(1000, self.update_state)
    
    def run(self):
        self.update_state()
        self.__root.mainloop()
            
class pendulum_clock(round_clock):
    def __init__(self, radius: float):
        round_clock.__init__(self, radius)
        self.__start_time = time.time()

    def run(self):
        round_clock.draw(self)
        round_clock.update_state(self)
        self.animate_pendulum()
        self._root.mainloop()

    
    def animate_pendulum(self):
        self._canvas.delete("pendulum")

        temp = time.time() - self.__start_time
        angle: float = math.sin(temp * math.pi) * math.pi / 6

        x0: float = self._center
        x1: float = x0 + 200 * math.sin(angle) # 100 - длина маятника

        y0: float = self._center + self._radius
        y1: float = y0 + 200 * math.cos(angle)
        
        self._canvas.create_line(x0, y0, x1, y1, width=4, tags="pendulum")
        self._canvas.create_oval(x1 - 30, y1 - 30, x1 + 30, y1 + 30, width=2, tags="pendulum")

        self._root.after(20, self.animate_pendulum)


