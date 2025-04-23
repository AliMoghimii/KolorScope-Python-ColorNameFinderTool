import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageStat
from collections import Counter
from threading import Thread
import numpy as np
import csv
import cv2

class KolorScopeApp:
    def __init__(self, root):

        self.updating_frame = False

        self.root = root
        
        self.root.title("KolorScope | By: Ali Moghimi")
        root.iconbitmap("icon.ico")
        self.colors_data = self.load_csv("cleaned_colors.csv")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.MAX_PORT_WIDTH = int(screen_width * 0.8)
        self.MAX_PORT_HEIGHT = int(screen_height * 0.6)
        self.MAX_LAND_WIDTH = int(screen_width * 0.6)
        self.MAX_LAND_HEIGHT = int(screen_height * 0.5)

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.label = tk.Label(root, text="Click on the image to get color", font=("Helvetica", 12))
        self.label.pack()

        menubar = tk.Menu(root)

        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Open Image", command=self.open_image)
        menubar.add_cascade(label="File", menu=self.filemenu)

        self.source_menu = tk.Menu(menubar, tearoff=0)
        self.source_menu.add_command(label="Image Mode", command=self.switch_to_image_source)
        self.source_menu.add_separator()
        self.source_menu.add_command(label="Camera Mode", command=self.switch_to_camera_source)
        menubar.add_cascade(label="Source", menu=self.source_menu)

        self.selection_menu = tk.Menu(menubar, tearoff=0)
        self.selection_menu.add_command(label="Pixel", command=self.switch_to_pixel_mode)
        self.selection_menu.add_command(label="Area", command=self.switch_to_area_mode)
        menubar.add_cascade(label="Selection Mode", menu=self.selection_menu)

        root.config(menu=menubar)

        self.source = "image"
        self.mode = "pixel"
        self.image = None
        self.tk_image = None
        self.scale_x = 1
        self.scale_y = 1
        self.camera_on = False
        self.freeze_frame = False
        self.frame = None

        self.canvas.bind("<Button-1>", self.on_mouse_B1_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_B1_hold)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_B1_release)

        self.rect = None
        self.start_x = None
        self.start_y = None

    def load_csv(self, filename):
        data = {}
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    if len(row) >= 3:
                        exotic_name, hex_code, basic_name = row[0], row[1], row[2]
                        data[hex_code.lower()] = f"{exotic_name} ({basic_name})"
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        return data

    def switch_to_image_source(self):
        if self.camera_on:
            self.camera_on = False
        self.source = "image"
        self.filemenu.entryconfig("Open Image", state="normal")
        self.canvas.config(cursor="cross")
        self.label.config(text="Image Mode selected", bg=self.root.cget("bg"), fg="black")

    def switch_to_camera_source(self):
        self.source = "camera"
        self.filemenu.entryconfig("Open Image", state="disabled")
        self.label.config(text="Camera Mode selected", bg=self.root.cget("bg"), fg="black")
        self.canvas.config(cursor="cross")
        if not self.camera_on:
            self.camera_on = True
            Thread(target=self.camera_loop, daemon=True).start()

    def camera_loop(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while cap.isOpened():
            if not self.camera_on:
                break
            if not self.freeze_frame:
                ret, frame = cap.read()
                if not ret:
                    break
                self.frame = frame
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                self.image = img
                self.root.after(0, self.display_camera_frame, img)
        cap.release()

    def display_camera_frame(self, img):
        if self.updating_frame:
            return
        self.updating_frame = True

        width, height = img.size
        scale = min(self.MAX_LAND_WIDTH / width, self.MAX_LAND_HEIGHT / height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        self.scale_x = new_width / width
        self.scale_y = new_height / height

        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img_resized)

        self.canvas.delete("all")
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        self.root.geometry(f"{new_width}x{new_height + 50}")
        self.updating_frame = False

    def switch_to_pixel_mode(self):
        self.mode = "pixel"
        self.canvas.config(cursor="cross")
        self.label.config(text="Pixel Mode: Click to get color", bg=self.root.cget("bg"), fg="black")

    def switch_to_area_mode(self):
        self.mode = "area"
        self.canvas.config(cursor="arrow")
        self.label.config(text="Area Mode: Click and drag to select area", bg=self.root.cget("bg"), fg="black")

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.image = Image.open(file_path).convert("RGB")
            self.resize_image_to_fit()
            self.label.config(bg=self.root.cget("bg"), fg="black")

    def resize_image_to_fit(self):
        if self.image:
            img_width, img_height = self.image.size
            aspect_ratio = img_width / img_height

            if aspect_ratio > 1:
                new_width = min(img_width, self.MAX_LAND_WIDTH)
                new_height = int(new_width / aspect_ratio)
                if new_height > self.MAX_LAND_HEIGHT:
                    new_height = self.MAX_LAND_HEIGHT
                    new_width = int(new_height * aspect_ratio)
            elif aspect_ratio < 1:
                new_height = min(img_height, self.MAX_PORT_HEIGHT)
                new_width = int(new_height * aspect_ratio)
                if new_width > self.MAX_PORT_WIDTH:
                    new_width = self.MAX_PORT_WIDTH
                    new_height = int(new_width / aspect_ratio)
            else:
                new_width = new_height = min(img_width, self.MAX_PORT_WIDTH, self.MAX_PORT_HEIGHT)

            self.scale_x = new_width / img_width
            self.scale_y = new_height / img_height

            resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized_image)

            self.root.geometry(f"{new_width}x{new_height + 50}")
            self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def on_mouse_B1_press(self, event):

        if self.mode == "area":
            if self.source == "camera" and self.camera_on:
                self.camera_on = False
                self.freeze_frame = True
                if self.image:
                    self.display_camera_frame(self.image)

        if self.mode == "pixel":
            if self.image:
                x, y = event.x, event.y
                orig_x = int(x / self.scale_x)
                orig_y = int(y / self.scale_y)
                if orig_x < self.image.width and orig_y < self.image.height:
                    r, g, b = self.image.getpixel((orig_x, orig_y))
                    hex_color = f"#{r:02x}{g:02x}{b:02x}".lower()
                    color_name = self.get_closest_color_name(hex_color)
                    text_color = self.get_text_color((r, g, b))
                    self.label.config(text=f"HEX: {hex_color} | Name: {color_name}")
                    self.label.config(bg=hex_color, fg=text_color)

    def on_mouse_B1_hold(self, event):

        if self.mode == "area":
            if not self.rect:
                self.start_x = event.x
                self.start_y = event.y
                self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="magenta")
            else:
                x1 = min(self.start_x, event.x)
                y1 = min(self.start_y, event.y)
                x2 = max(self.start_x, event.x)
                y2 = max(self.start_y, event.y)
                self.canvas.coords(self.rect, x1, y1, x2, y2)

    def on_mouse_B1_release(self, event):
        if self.mode == "area":
            if self.rect:
                coords = self.canvas.coords(self.rect)
                if len(coords) != 4 or self.image is None:
                    self.canvas.delete(self.rect)
                    self.rect = None
                    return

            x1, y1, x2, y2 = coords
            x1, y1 = int(x1 / self.scale_x), int(y1 / self.scale_y)
            x2, y2 = int(x2 / self.scale_x), int(y2 / self.scale_y)

            if x1 == x2 or y1 == y2:
                self.canvas.delete(self.rect)
                self.rect = None
                return

            area_image = self.image.crop((x1, y1, x2, y2))
            area_image = area_image.resize((200, 200))
            stat = ImageStat.Stat(area_image)
            avg_color = stat.mean
            avg_color_hex = f"#{int(avg_color[0]):02x}{int(avg_color[1]):02x}{int(avg_color[2]):02x}"
            color_name = self.get_closest_color_name(avg_color_hex)
            text_color = self.get_text_color(avg_color)
            self.label.config(text=f"Average Color: {avg_color_hex} | Name: {color_name}", bg=avg_color_hex, fg=text_color)

            pixels = np.array(area_image).reshape((-1, 3))
            most_common = Counter(map(tuple, pixels)).most_common(1)[0][0]
            most_common_hex = f"#{most_common[0]:02x}{most_common[1]:02x}{most_common[2]:02x}"
            color_name = self.get_closest_color_name(most_common_hex)
            text_color = self.get_text_color(most_common)
            self.label.config(text=f"Most Prominent Color: {most_common_hex} | Name: {color_name}", bg=most_common_hex, fg=text_color)

            self.canvas.delete(self.rect)
            self.rect = None

            if self.source == "camera":
                self.freeze_frame = False
                if not self.camera_on:
                    self.camera_on = True
                    Thread(target=self.camera_loop, daemon=True).start()

    def get_closest_color_name(self, hex_color):
        if not (hex_color.startswith('#') and len(hex_color) == 7 and all(c in '0123456789abcdefABCDEF' for c in hex_color[1:])):
            return "Unknown"

        if hex_color in self.colors_data:
            return self.colors_data[hex_color]

        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        closest_color_name = None
        min_distance = float('inf')

        for color_hex, color_name in self.colors_data.items():
            if not (color_hex.startswith('#') and len(color_hex) == 7):
                continue
            r2, g2, b2 = int(color_hex[1:3], 16), int(color_hex[3:5], 16), int(color_hex[5:7], 16)
            distance = self.color_distance((r, g, b), (r2, g2, b2))
            if distance < min_distance:
                min_distance = distance
                closest_color_name = color_name

        return closest_color_name or "Unknown"

    def color_distance(self, color1, color2):
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))
    
    def get_text_color(self, color):
        r, g, b = color
        luminance = self.get_luminance(r, g, b)
        return "black" if luminance > 128 else "white"
    
    def get_luminance(self, r, g, b):
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

if __name__ == "__main__":
    root = tk.Tk()
    app = KolorScopeApp(root)
    root.mainloop()