import tkinter as tk
import math
from PIL import Image, ImageTk
import random

class AnimeSunsetVisuals:
    def __init__(self, root):
        self.root = root
        self.root.title("Anime Sunset Visuals")
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.running = True
        
        self.width = 800  # Default size
        self.height = 800  # Default size
        
        self.root.bind("<Configure>", self.on_resize)
        self.start_animation()
    
    def start_animation(self):
        self.animate()
    
    def animate(self):
        frame = 0
        self.draw_frame(frame)
        if self.running:
            self.root.after(30, self.animate)
    
    def draw_frame(self, frame):
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        pixels = img.load()
        
        # Draw the sun
        sun_x, sun_y = self.width // 2, int(self.height * 0.65)
        sun_radius = self.height // 5
        self.draw_sun(pixels, sun_x, sun_y, sun_radius)
        
        # Draw the sky
        self.draw_sky(pixels, frame)
        
        # Draw clouds
        self.draw_clouds(pixels, frame)
        
        # Draw stars
        self.draw_stars(pixels, frame)
        
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
    
    def draw_sun(self, pixels, sun_x, sun_y, sun_radius):
        for i in range(self.width):
            for j in range(self.height):
                dist_to_sun = math.sqrt((i - sun_x) ** 2 + (j - sun_y) ** 2)
                if dist_to_sun < sun_radius:
                    r = int(255 - (dist_to_sun / sun_radius) * 50)
                    g = int(180 - (dist_to_sun / sun_radius) * 100)
                    b = int(80 - (dist_to_sun / sun_radius) * 80)
                    pixels[i, j] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    def draw_sky(self, pixels, frame):
        for i in range(self.width):
            for j in range(self.height):
                wave = math.sin(i * 0.015 + frame * 0.02) * 80
                gradient = (j / self.height) * 255
                
                r = int(255 - gradient * 0.9 + wave * 0.3)
                g = int(100 + wave * 0.5)
                b = int(200 - gradient * 0.7)
                
                pixels[i, j] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    def draw_clouds(self, pixels, frame):
        num_clouds = 5
        for _ in range(num_clouds):
            cloud_x = int((math.sin(frame * 0.01 + _ * 0.5) * 0.5 + 0.5)) * self.width
            cloud_y = random.randint(0, self.height // 3)
            cloud_radius = random.randint(50, 100)
            self.draw_cloud(pixels, cloud_x, cloud_y, cloud_radius)
    
    def draw_cloud(self, pixels, x, y, radius):
        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if 0 <= i < self.width and 0 <= j < self.height:
                    dist = math.sqrt((i - x) ** 2 + (j - y) ** 2)
                    if dist < radius:
                        r, g, b = pixels[i, j]
                        r = min(255, r + 50)
                        g = min(255, g + 50)
                        b = min(255, b + 50)
                        pixels[i, j] = (r, g, b)
    
    def draw_stars(self, pixels, frame):
        num_stars = 100
        for _ in range(num_stars):
            star_x = random.randint(0, self.width)
            star_y = random.randint(0, self.height // 2)
            brightness = random.randint(200, 255)
            pixels[star_x, star_y] = (brightness, brightness, brightness)
    
    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.canvas.config(width=self.width, height=self.height)
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimeSunsetVisuals(root)
    root.protocol("WM_DELETE_WINDOW", app.stop)
    root.mainloop()