import tkinter as tk
import math

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