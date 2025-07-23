import tkinter as tk
import math
import time

class round_clock:
    """
    Description:
        A class for running a windowed application with a round clock that measures time in the real world
    """

    HOUR_ARROW_LENGTH_OFFSET: int = 30
    MINUTE_ARROW_LENGTH_OFFSET: int = 50
    SECOND_ARROW_LENGTH_OFFSET: int = 80

    HOUR_MARKER_OFFSET: int = 20
    MINUTE_MARKER_OFFSET: int = 10

    THICKNESS: int = 1

    def __init__(self, delay: float = 20) -> None:
        if delay < 0:
            raise ValueError("'delay' less than zero")
        
        self._root = tk.Tk()
        self._background_color = "white"
        self._figure_color = "black"

        self._delay: float = delay
        self._center: tuple[int, int] = (500 / 2, 500 / 2)  # Clock center
        self._radius: float = 200 # Clock radius

        # Window settings
        self._root.title("Round clock")
        self._root.configure(background=self._background_color)
        self._root.resizable(False, False)

        self._canvas = tk.Canvas(self._root, width=500, height=500)
        self._canvas.pack()

    def run(self) -> None:
        """
        Description:
            Opens a windowed application with a round clock
        """

        self.draw()
        self.animate_arrows()
        self._root.mainloop()

    def draw(self) -> None:
        """
        Description:
            Draws the base of the clock: circle and time markers
        """

        # Drawing a circle of clocks
        self._canvas.create_oval(self._center[0] - self._radius, self._center[1] - self._radius,
                                self._center[0] + self._radius, self._center[1] + self._radius,
                                outline=self._figure_color, width=round_clock.THICKNESS * 4)

        # Drawing hour markers
        for i in range(12):
            angle: float = - math.pi / 6 * i + math.pi / 2 # The angle between the hour markers is 30 degrees (pi/6 radians)

            x0: float = self._center[0] + (self._radius - round_clock.HOUR_MARKER_OFFSET) * math.cos(angle)
            x1: float = self._center[0] + self._radius * math.cos(angle)

            y0: float = self._center[1] - (self._radius - round_clock.HOUR_MARKER_OFFSET) * math.sin(angle)
            y1: float = self._center[1] - self._radius * math.sin(angle)

            self._canvas.create_line(x0, y0, x1, y1, width=round_clock.THICKNESS, fill=self._figure_color)
            self._canvas.create_text(x0, y0, text=(i + 11) % 12 + 1, fill=self._figure_color)
        
        # Drawing minute markers
        for i in range(60):
            if i % 5 != 0:
                angle: float = math.pi / 30 * i  # The angle between the minute markers is 6 degrees (pi/30 radians)

                x0: float = self._center[0] + (self._radius - round_clock.MINUTE_MARKER_OFFSET) * math.sin(angle)
                x1: float = self._center[0] + self._radius * math.sin(angle)

                y0: float = self._center[1] - (self._radius - round_clock.MINUTE_MARKER_OFFSET) * math.cos(angle)
                y1: float = self._center[1] - self._radius * math.cos(angle)

                self._canvas.create_line(x0, y0, x1, y1, width=round_clock.THICKNESS, fill=self._figure_color)
    
    def animate_arrows(self) -> None:
        """
        Description:
            Updates the clock state. Redraws clock hands
        """

        self._canvas.delete("arrows") # The 'arrows' tag is used to avoid redrawing the base of the clock

        now: float = time.time()
        local_time = time.localtime(now)
        hour: int = local_time.tm_hour % 12
        minute: int = local_time.tm_min
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
                                 fill=self._figure_color, width=round_clock.THICKNESS, tag="arrows")

        mx: float = self._center[0] + mlength * math.sin(mangle)
        my: float = self._center[1] - mlength * math.cos(mangle)
        self._canvas.create_line(self._center[0], self._center[1], mx, my,
                                 fill=self._figure_color, width=round_clock.THICKNESS * 3, tag="arrows")

        hx: float = self._center[0] + hlength * math.sin(hangle)
        hy: float = self._center[1] - hlength * math.cos(hangle)
        self._canvas.create_line(self._center[0], self._center[1], hx, hy,
                                 fill=self._figure_color, width=round_clock.THICKNESS * 5, tag="arrows")

        self._root.after(self._delay, self.animate_arrows)

class pendulum_clock(round_clock):
    """
    Description:
        A class for running a windowed application with a pendulum clock that measures time in the real world
    """

    PENDULUM_LENGTH: int = 250
    PENDULUM_RADIUS: int = 30
    
    def __init__(self, delay: int = 20):
        self._root = tk.Tk()
        self._background_color = "white"
        self._figure_color = "black"

        self._center: tuple[int, int] = (500 / 2, 500 / 2)  # Clock center
        self._radius: float = 200 # Clock radius
        self._delay = delay

        # Window settings
        self._root.title("Pendulum clock")
        self._root.configure(background=self._background_color)
        self._root.resizable(False, False)

        self._canvas = tk.Canvas(self._root, width=500, height=750)
        self._canvas.pack()

        self._start_time = time.time()

    def run(self):
        """
        Description:
            Opens a windowed application with a pendulum clock
        """
            
        super().draw()
        super().animate_arrows()
        self.animate_pendulum()
        self._root.mainloop()

    
    def animate_pendulum(self):
        """
        Description:
            Updates the clock state. Redraws clock pendulum
        """
                
        self._canvas.delete("pendulum")

        temp = time.time() - self._start_time
        angle: float = math.sin(temp * math.pi) * math.pi / 6

        x0: float = self._center[0]
        x1: float = x0 + pendulum_clock.PENDULUM_LENGTH * math.sin(angle)

        y0: float = self._center[1] + self._radius
        y1: float = y0 + pendulum_clock.PENDULUM_LENGTH * math.cos(angle)
        
        self._canvas.create_line(x0, y0, x1, y1, width=round_clock.THICKNESS*4, tags="pendulum")
        self._canvas.create_oval(x1 - pendulum_clock.PENDULUM_RADIUS, y1 - pendulum_clock.PENDULUM_RADIUS,
                                 x1 + pendulum_clock.PENDULUM_RADIUS, y1 + pendulum_clock.PENDULUM_RADIUS,
                                 width=round_clock.THICKNESS, tags="pendulum")

        self._root.after(self._delay, self.animate_pendulum)

# Each segment is a polygon
# Segments are numbered like this:
#   ---0---
#  |       |
# 1|       |2
#  |---3---|
#  |       |
# 4|       |5
#  |---6---|

_SEGMENT_POINTS = { # Segment coordinates
    0: [(22, 10), (78, 10), (70, 20), (30, 20)],
    1: [(15, 15), (25, 25), (25, 65), (15, 75)],
    2: [(85, 15), (75, 25), (75, 65), (85, 75)],
    3: [(22, 75), (30, 80), (70, 80), (78, 75), (70, 70), (30, 70)],
    4: [(15, 80), (25, 90), (25, 130), (15, 140)],
    5: [(85, 80), (75, 90), (75, 130), (85, 140)],
    6: [(22, 140), (78, 140), (70, 130), (30, 130)]
}

_DIGIT_MAP = { # Mapping between number and lit segments
    '0': [0,1,2,4,5,6],
    '1': [2,5],
    '2': [0,2,3,4,6],
    '3': [0,2,3,5,6],
    '4': [1,2,3,5],
    '5': [0,1,3,5,6],
    '6': [0,1,3,4,5,6],
    '7': [0,2,5],
    '8': [0,1,2,3,4,5,6],
    '9': [0,1,2,3,5,6]
}

class _seven_segment_digit:
    """
    Description:
        Class representing a single seven-segment digit using polygons
    """
    def __init__(self, root):
        self._canvas = tk.Canvas(root, width=100, height=150, bg='black', highlightthickness=0)
        self._segments = []
        for i in range(7):
            temp = [coordinate_pair for point in _SEGMENT_POINTS[i] for coordinate_pair in point]
            self._segments.append(self._canvas.create_polygon(temp, fill="#3F0000", outline="#3F0000"))
    
    def set_digit(self, digit: str):
        """
        Description:
            Set the digit to display by turning on/off segments
        """

        active_segments = _DIGIT_MAP.get(digit, [])
        for index, segment in enumerate(self._segments):
            if index in active_segments:
                self._canvas.itemconfig(segment, fill="red")
            else:
                self._canvas.itemconfig(segment, fill="#3F0000")

    def grid(self, **kwargs):
        """
        Description:
            Grid the digit canvas in the parent widget
        """
        self._canvas.grid(**kwargs)

        
class _colon:
    """
    Description:
        Class representing the colon separator in digital clock display
    """

    def __init__(self, root):
        self._canvas = tk.Canvas(root, width=30, height=150, bg='black', highlightthickness=0)
        self._canvas.create_oval(5, 50, 25, 70, fill='red', outline='red')
        self._canvas.create_oval(5, 100, 25, 120, fill='red', outline='red')
        
    def grid(self, **kwargs):
        self._canvas.grid(**kwargs)

class digital_clock:
    """
    Description:
        A class for running a windowed application with a digital clock displaying HH:MM:SS with seven-segment digits that measures time in the real world
    """

    def __init__(self):        
        self._root = tk.Tk()
        self._background_color = "white"
        self._figure_color = "black"

        self._digits = []

        for i in range(6):
            d = _seven_segment_digit(self._root)
            d.grid(row=0, column=i + (i // 2))
            self._digits.append(d)
        
        c1: _colon = _colon(self._root)
        c2: _colon = _colon(self._root)
        
        c1.grid(row=0, column=2)
        c2.grid(row=0, column=5)
        
        self._root.title("Digital clock")
        self._root.configure(background=self._background_color)
        self._root.resizable(False, False)

    def animate_digits(self):
        """
        Description:
            Update the displayed time
        """

        now: str = time.strftime("%H%M%S")

        for i, d in enumerate(now):
            self._digits[i].set_digit(d)

        self._root.after(1000, self.animate_digits)

    def run(self):
        """
        Description:
            Opens a windowed application with a digital clock
        """

        self.animate_digits()
        self._root.mainloop()