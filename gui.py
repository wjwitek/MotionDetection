import math
import time
from threading import Thread

from src.motion_detector import MotionDetector
import tkinter as tk
from tkinter import ttk


class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.source = 0
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        self.root.title("GUI")
        self.root.geometry("500x500+20000+0")

        self.root.bind("q", lambda e: self.exit())
        self.mode = "normal"
        self.detector = MotionDetector(mask=[0, 0, 1, 1])

        self.t_slider = ttk.Scale(self.root, from_=0, to=200, value=50, orient=tk.HORIZONTAL,
                                  command=self.slider_changed)
        self.t_slider.bind("<ButtonRelease-1>", lambda event: self.update_threshold())
        self.t_slider_label = ttk.Label(self.root, text="Sensitivity: 50")
        self.threshold = 0

        self.t_slider.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.t_slider_label.grid(row=0, column=1, sticky=tk.W)

        self.area_slider = ttk.Scale(self.root, from_=1, to=20000, value=100, orient=tk.HORIZONTAL,
                                     command=self.area_slider_changed)
        self.area_slider_label = ttk.Label(self.root, text="Area: 100")
        self.area_slider_label.grid(row=1, column=1, sticky=tk.W)
        self.area_slider.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.area_value = 0

        self.mode_button = ttk.Button(self.root, text="Debug", command=self.change_mode)
        self.mode_button.grid(row=2, column=0, sticky=tk.W)
        self.set_reference_button = ttk.Button(self.root, text="Set reference frame", command=self.set_reference)
        self.set_reference_button.grid(row=2, column=0, sticky=tk.E)


        self.source_label = ttk.Label(self.root, text="Set source. 0 for webcam, orangutan.mp4 for orangutan \n <video_path> for any other video file")
        self.source_label.grid(row=8, column=0, sticky=tk.W, columnspan=2, rowspan=2)
        self.source_text_box = tk.Text(self.root, height=1)
        self.source_text_box.insert("end-1c", "orangutan.mp4")
        self.source_text_box.grid(row=10, column=0, sticky=tk.W)

        self.change_source_button = ttk.Button(self.root, text="Change source", command=self.change_source)
        self.change_source_button.grid(row=11, column=0, sticky=tk.W)
        self.box_sliders = []
        self.box_sliders_labels = []
        for i in range(4):
            value = 0 if i < 2 else 1
            self.box_sliders.append(
                ttk.Scale(self.root, from_=0.1, to=0.99, value=value, orient=tk.HORIZONTAL,
                          command=lambda value, i=i: self.box_slider_changed(value, i))
            )
            labels = ["X", "Y", "X2", "Y2"]
            if i < 2:
                label = ttk.Label(self.root, text=f"{labels[i]}: 0")
            else:
                label = ttk.Label(self.root, text=f"{labels[i]}: 1")

            self.box_sliders_labels.append(label)
            self.box_sliders[i].grid(row=i + 4, column=0, sticky=tk.W + tk.E)
            self.box_sliders_labels[i].grid(row=i + 4, column=1, sticky=tk.W)
    def exit(self):
        self.detector.stop()
        self.root.destroy()
    def change_source(self):
        try:
            self.source = int(self.source_text_box.get("1.0", tk.END))
        except ValueError:
            self.source = 0
            if self.source_text_box.get("1.0", tk.END) == "":
                self.source = 0
            else:
                self.source = self.source_text_box.get("1.0", tk.END).strip()
        print(self.source)
        print(self.source)
        self.detector.change_source(self.source)

    def set_reference(self):
        self.detector.set_reference_frame()

    def area_slider_changed(self, value):
        self.area_value = int(float(value))
        self.detector.change_minimal_detected_area(self.area_value)
        self.area_slider_label.configure(text="Area: " + str(self.area_value))
        time.sleep(0.05)

    def box_slider_changed(self, value, idx):
        labels = ["X", "Y", "W", "H"]
        value = round(float(value), 2)
        self.box_sliders_labels[idx].configure(text=f"{labels[idx]}: {value}")
        mask = list(self.detector.mask)
        mask[idx] = value
        mask[2] = max(mask[2], mask[0] + 0.01)
        mask[3] = max(mask[3], mask[1] + 0.01)
        self.box_sliders[2].configure(value=mask[2])
        self.box_sliders[3].configure(value=mask[3])
        self.detector.change_mask(mask)
        time.sleep(0.05)

    def slider_changed(self, value):
        value = int(float(value))
        self.detector.change_sensitivity(self.t_slider.cget("to") - value)
        self.threshold = value
        self.t_slider_label.configure(text="Sensitivity: " + str(value))
        time.sleep(0.05)

    def run(self):
        self.detector_thread = Thread(target=self.detector.start)
        self.detector_thread.start()
        self.root.mainloop()

    def update_threshold(self):
        self.detector.change_sensitivity(self.threshold)

    def main_loop(self):
        self.detector.main_loop()
        self.root.update()

    # self.change_mode() should change the mode of the program to "normal" or "debug",
    # depending on the current mode it should also change the text of the button to "Debug" or "Normal"

    def change_mode(self):
        print(self.detector)
        if self.mode == "normal":
            self.mode = "debug"
            self.detector.change_mode(True)
            self.mode_button.configure(text="Normal")
        elif self.mode == "debug":
            self.mode = "normal"
            self.detector.change_mode(False)

            self.mode_button.configure(text="Debug")
        else:
            print("Error: Unknown mode")


if __name__ == "__main__":
    gui = Gui()
    gui.run()
