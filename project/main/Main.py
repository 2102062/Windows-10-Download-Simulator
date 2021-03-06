import tkinter as tk
import math
from functools import partial
import os
import Enemy
import time
import random
import sys
from subprocess import Popen
import subprocess

root = tk.Tk()


class Main(tk.Frame):
    global x, y
    canvas_width = 1920
    canvas_height = 1080
    score_increase = 1
    x, y = 0, 90

    def __init__(self, master, **kwargs):
        # launches the canvas in fullscreen
        tk.Frame.__init__(self, master, **kwargs)
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Escape>", self.end_fullscreen)
        self.state = True
        root.attributes("-fullscreen", self.state)
        master.wm_state("zoomed")
        # assigns all the variables
        self.curve_radius = 105
        self.angle_start = 90
        self.score = 0
        self.level = 10
        self.angle_length = self.score / 100.0 * 360.0
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, border=0, relief="raised")
        self.canvas.config(bg="#000000")
        self.canvas.pack_propagate(False)
        self.canvas.pack(side="top", fill="both", expand=True)
        # make canvas components
        self.percent_id = self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2,
                                                  text=str(int(self.angle_length / 360 * 100)) + "%", fill="#FFFFFF",
                                                  justify="center", font=("Microsoft JhengHei Light", 40),
                                                  anchor="center")
        self.installing_id = self.canvas.create_text(self.canvas_width / 2, (self.canvas_height / 2 - 270),
                                                     text="Installing Windows " + str(self.level),
                                                     fill="#FFFFFF", justify="center",
                                                     font=("Microsoft JhengHei Light", 36))
        self.restart_id = self.canvas.create_text(self.canvas_width / 2, (self.canvas_height / 2 - 200),
                                                  text="Your PC will restart several times. Sit back and relax.",
                                                  fill="#999999", justify="center", font=("Microsoft YaHei UI", 11),
                                                  anchor="center")
        self.copying_files = self.canvas.create_text((self.canvas_width / 2) - 210, (self.canvas_height - 40),
                                                     text="Copying Files",
                                                     fill="#12498F", justify="center", font=("Microsoft YaHei UI", 11),
                                                     anchor="center")
        self.installing_features_id = self.canvas.create_text((self.canvas_width / 2 - 8), (self.canvas_height - 40),
                                                              text="Installing features and drivers",
                                                              fill="#999999", justify="center",
                                                              font=("Microsoft YaHei UI", 11), anchor="center")
        self.configuring_settings_id = self.canvas.create_text((self.canvas_width / 2) + 220, (self.canvas_height - 40),
                                                               text="Configuring Settings",
                                                               fill="#999999", justify="center",
                                                               font=("Microsoft YaHei UI", 11), anchor="center")
        self.oval_id3 = self.canvas.create_oval(self.canvas_width / 2 + self.curve_radius,
                                                self.canvas_height / 2 + self.curve_radius,
                                                self.canvas_width / 2 - self.curve_radius,
                                                self.canvas_height / 2 - self.curve_radius, outline="#888888",
                                                width=3.3)
        self.oval_id2 = self.canvas.create_oval(self.canvas_width / 2 + self.curve_radius,
                                                self.canvas_height / 2 + self.curve_radius,
                                                self.canvas_width / 2 - self.curve_radius,
                                                self.canvas_height / 2 - self.curve_radius, outline="#555555",
                                                width=3.9)
        self.oval_id = self.canvas.create_oval(self.canvas_width / 2 + self.curve_radius,
                                               self.canvas_height / 2 + self.curve_radius,
                                               self.canvas_width / 2 - self.curve_radius,
                                               self.canvas_height / 2 - self.curve_radius, outline="#666666", width=3.5)
        self.arc_id = self.canvas.create_arc((self.canvas_width / 2 + self.curve_radius,
                                              self.canvas_height / 2 + self.curve_radius,
                                              self.canvas_width / 2 - self.curve_radius,
                                              self.canvas_height / 2 - self.curve_radius),
                                             outline="#12498F", style="arc", width=4.6, extent=-self.angle_length,
                                             start=self.angle_start)
        root.bind('<Motion>', partial(self.motion))

        # Ian's Place
        self.x_intvar = tk.IntVar()
        self.x_intvar.set(150)
        self.y_intvar = tk.IntVar()
        self.y_intvar.set(150)

        self.speed_intvar = tk.IntVar()
        self.speed_intvar.set(15)
        self.img1_direction_intvar = tk.IntVar()
        self.img1_direction_intvar.set(1)

        self.img1_direction = 1

        # Initializes Windows 10 center coordinates
        self.img1_x_var = tk.IntVar()
        self.img1_x_var.set(300)
        self.img1_y_var = tk.IntVar()
        self.img1_y_var.set(500)

        self.object1 = Enemy.Enemy()
        self.object1.create("\modified_img\Win10.png", self.canvas)
        self.object1.spawn()
        root.after(200, self.enemy_animation)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        root.attributes("-fullscreen", False)
        return "break"

    # update bar's position
    def update_bar(self):
        global x, y
        self.angle_length = self.score / 100.0 * 360.0
        self.update_rotation(x, y)

    # increases percent by 1
    def increase_score(self):
        if self.score < 100:
            self.score += self.score_increase
            self.update_bar()
            self.canvas.itemconfig(self.arc_id, extent=-self.angle_length)
            self.canvas.itemconfig(self.percent_id, text=str(self.score) + "%")
            self.object1.update_speed(1.015)
        else:
            self.reset_score()
            self.object1.reset_speed()
            self.level_up()
            self.object1.update_speed(1 + self.level / 3)

    # increases level by 1
    def level_up(self):
        self.level += 1
        self.canvas.itemconfig(self.installing_id, text="Installing Windows " + str(self.level))

    # calculate the bar's rotation from the mouse movement
    def update_rotation(self, x, y):
        self.angle_start = 270 + (math.degrees(
            math.atan2((x - self.canvas_width / 2), (y - self.canvas_height / 2))) + .5 * self.angle_length)
        self.canvas.itemconfig(self.arc_id, start=self.angle_start)

    # check for mouse movement
    def motion(self, event):
        global x, y
        x, y = event.x, event.y
        self.update_rotation(x, y)

    # moves the windows logos towards the center until it hits the circle
    def enemy_animation(self):
        self.object1.move_towards_center()
        if (math.sqrt(math.pow(.5 * float(self.canvas_width) - float(self.object1.x_var), 2))) < float(
                self.curve_radius) + 8.0:
            self.increase_score()
            if self.object1.edge in [1, 2]:
                if (self.angle_start - self.angle_length) > self.object1.angle > self.angle_start or (
                        self.angle_start - self.angle_length) < self.object1.angle < self.angle_start:
                    if self.score != 0:
                        self.object1.reset_speed()
                        self.reset_score()
                        self.game_over()
                self.object1.spawn()
            else:
                if (self.angle_start - self.angle_length - 360) > self.object1.angle > self.angle_start - 360 or (
                        self.angle_start - self.angle_length - 360) < self.object1.angle < self.angle_start - 360:
                    if self.score != 0:
                        self.object1.reset_speed()
                        self.reset_score()
                        self.game_over()
                self.object1.spawn()


        root.after(16, self.enemy_animation)

    def reset_score(self):
        self.score = 0
        self.update_bar()
        self.canvas.itemconfig(self.arc_id, extent=-self.angle_length)
        self.canvas.itemconfig(self.percent_id, text=str(int(self.angle_length / 360 * 100)) + "%")

    # fun commands!
    def game_over(self):
        os.system(os.getcwd() + "\popups\msg" + str(random.randint(1, 20)) + ".vbs")


if __name__ == "__main__":
    view = Main(root)
    view.pack(side="top", fill="both", expand=True)
    root.mainloop()
