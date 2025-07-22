import tkinter as tk
import math
import time

class round_clock:
    """
    Description:
        A class for running a windowed application with a round clock that measures time in the real world
    """

    HOUR_ARROW_LENGTH_OFFSET = 30
    MINUTE_ARROW_LENGTH_OFFSET = 50
    SECOND_ARROW_LENGTH_OFFSET = 80

    HOUR_MARKER_OFFSET = 20
    MINUTE_MARKER_OFFSET = 10

    MARGIN = 20

    def __init__(self, width: int = 400, height: int = 400, radius: int = 100, delay: float = 50,
                 thickness: int = 1, background_color: str = "white", figure_color: str = "black") -> None:
        if width < 0:
            raise ValueError("'width' less than zero")
        if height < 0:
            raise ValueError("'height' less than zero")
        if radius < 0:
            raise ValueError("'radius' less than zero")
        if radius > min(width, height) / 2 - round_clock.MARGIN:
            raise ValueError("The clock doesn't fit in the window")
        if delay < 0:
            raise ValueError("'delay' less than zero")
        
        self._root = tk.Tk() 
        self._canvas_width = width
        self._canvas_height = height

        self._background_color = background_color
        self._figure_color = figure_color

        self._center: tuple[float, float] = (self._canvas_width / 2, self._canvas_height / 2)  # Clock center
        self._radius: float = radius # Clock radius
        self._thickness: float = thickness
        self._delay = delay

        # Window settings
        self._root.title("Round clock")
        self._root.resizable(False, False)

        self._canvas = tk.Canvas(self._root, width=self._canvas_width, height=self._canvas_height, bg=self._background_color)
        self._canvas.pack()

    def run(self) -> None:
        """
        Description:
            Opens a windowed application with a round clock
        """

        self.draw()
        self.update_state()
        self._root.mainloop()

    def draw(self) -> None:
        """
        Description:
            Draws the base of the clock: circle and time markers
        """

        # Drawing a circle of clocks
        self._canvas.create_oval(self._center[0] - self._radius, self._center[1] - self._radius,
                                self._center[0] + self._radius, self._center[1] + self._radius,
                                outline=self._figure_color, width=self._thickness * 4)

        # Drawing hour markers
        for i in range(12):
            angle: float = math.pi / 6 * i # The angle between the hour markers is 30 degrees (pi/6 radians)

            x0: float = self._center[0] + (self._radius - round_clock.HOUR_MARKER_OFFSET) * math.sin(angle)
            x1: float = self._center[0] + self._radius * math.sin(angle)

            y0: float = self._center[1] - (self._radius - round_clock.HOUR_MARKER_OFFSET) * math.cos(angle)
            y1: float = self._center[1] - self._radius * math.cos(angle)

            self._canvas.create_line(x0, y0, x1, y1, width=self._thickness, fill=self._figure_color)
            self._canvas.create_text(x0, y0, text=(i+11) % 12 + 1, fill=self._figure_color)
        
        # Drawing minute markers
        for i in range(60):
            if i % 5 != 0:
                angle: float = math.pi / 30 * i  # The angle between the minute markers is 6 degrees (pi/30 radians)

                x0: float = self._center[0] + (self._radius - round_clock.MINUTE_MARKER_OFFSET) * math.sin(angle)
                x1: float = self._center[0] + self._radius * math.sin(angle)

                y0: float = self._center[1] - (self._radius - round_clock.MINUTE_MARKER_OFFSET) * math.cos(angle)
                y1: float = self._center[1] - self._radius * math.cos(angle)

                self._canvas.create_line(x0, y0, x1, y1, width=self._thickness, fill=self._figure_color)
    
    def update_state(self) -> None:
        """
        Description:
            Updates the clock state. Redraws clock hands
        """

        self._canvas.delete("arrows") # The 'arrows' tag is used to avoid redrawing the base of the clock

        now = time.time()
        local_time = time.localtime(now)
        hour = local_time.tm_hour % 12
        minute = local_time.tm_min
        second = now % 60  

        sangle: float = math.pi / 30 * second
        mangle: float = math.pi / 30 * minute + sangle / 60
        hangle: float = math.pi / 6  * hour + mangle / 12

        slength: float = self._radius - round_clock.SECOND_ARROW_LENGTH_OFFSET
        mlength: float = self._radius - round_clock.MINUTE_ARROW_LENGTH_OFFSET
        hlength: float = self._radius - round_clock.HOUR_ARROW_LENGTH_OFFSET

        sx: float = self._center[0] + slength * math.sin(sangle)
        sy: float = self._center[1] - slength * math.cos(sangle)
        self._canvas.create_line(self._center[0], self._center[1], sx, sy,
                                 fill=self._figure_color, width=self._thickness, tag="arrows")

        mx: float = self._center[0] + mlength * math.sin(mangle)
        my: float = self._center[1] - mlength * math.cos(mangle)
        self._canvas.create_line(self._center[0], self._center[1], mx, my,
                                 fill=self._figure_color, width=self._thickness * 3, tag="arrows")

        hx: float = self._center[0] + hlength * math.sin(hangle)
        hy: float = self._center[1] - hlength * math.cos(hangle)
        self._canvas.create_line(self._center[0], self._center[1], hx, hy,
                                 fill=self._figure_color, width=self._thickness * 5, tag="arrows")

        self._root.after(self._delay, self.update_state)

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


