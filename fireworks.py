

import colorsys
import math
import random
import time
import tkinter as tk
from dataclasses import dataclass, field


def fade_color(color, opacity):
    opacity = max(0.0, min(1.0, opacity))
    return "#{:02x}{:02x}{:02x}".format(
        *(round(channel * opacity) for channel in color))


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    lifetime: float
    color: tuple
    size: float
    opacity: float
    item: int
    trail_item: int
    age: float = 0.0
    trail: list = field(default_factory=list)

    def advance(self, dt, gravity):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt + gravity * dt * dt / 2
        self.vy += gravity * dt
        self.trail.append((self.x, self.y))
        self.trail = self.trail[-8:]
        return self.age < self.lifetime


@dataclass
class Rocket:
    x: float
    y: float
    target_y: float
    speed: float
    color: tuple
    item: int
    age: float = 0.0
class Fireworks:
    COLORS = 12
    MAX_PARTICLES = 1800
    MAX_ROCKETS = 12

    def __init__(self, root):
        self.root = root
        root.title("Лабораторная работа 3.2 — Фейерверки")
        root.geometry("1000x720")
        root.minsize(640, 480)
        self.gravity = tk.DoubleVar(value=100.0)
        self.paused = False
        self.rockets = []
        self.particles = []
        self.width, self.height = 1000, 600
        self.spawn_in = 0.2

        controls = tk.Frame(root, padx=10, pady=5)
        controls.pack(fill="x")
        tk.Label(controls, text="Гравитация (пикс./с²):").pack(side="left")
        tk.Scale(controls, from_=-150, to=350, resolution=10,
                 orient="horizontal", variable=self.gravity,
                 length=260).pack(side="left")
        self.pause_button = tk.Button(controls, text="Пауза", command=self.toggle_pause)
        self.pause_button.pack(side="left", padx=10)
        tk.Button(controls, text="Сброс", command=self.reset).pack(side="left")
        tk.Label(root, text="Щелчок по небу — взрыв • Пробел — пауза • "
                 "R — сброс • Esc — выход").pack(fill="x")
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.status = tk.Label(root, anchor="w")
        self.status.pack(fill="x", padx=10)

        self.canvas.bind("<Configure>", self.resize)
        self.canvas.bind("<Button-1>", self.click)
        root.bind("<space>", self.toggle_pause)
        root.bind("<KeyPress-r>", self.reset)
        root.bind("<KeyPress-R>", self.reset)
        root.bind("<Escape>", lambda event: root.destroy())
        self.last_time = time.perf_counter()
        self.after_id = None
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.animate()



    

if __name__ == "__main__":
    window = tk.Tk()
    Fireworks(window)
    window.mainloop()
