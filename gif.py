import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import imageio
import io
import webbrowser
import random
import os

API_KEY = "LIVDSRZULELA"
LIMIT = 20

current_gif_url = ""
frames = []
frame_index = 0
animation_running = False

# Fetch GIF
def fetch_gif(keyword=None):
    global current_gif_url, frames, frame_index, animation_running

    if keyword is None:
        keyword = entry.get()

    if keyword == "":
        messagebox.showwarning("Warning", "Enter keyword!")
        return

    status_label.config(text="Loading...", fg="yellow")
    root.update()

    url = f"https://g.tenor.com/v1/search?q={keyword}&key={API_KEY}&limit={LIMIT}"

    try:
        res = requests.get(url)
        data = res.json()

        if not data["results"]:
            messagebox.showinfo("No Result", "No GIF found")
            return

        gif = random.choice(data["results"])
        current_gif_url = gif["media"][0]["gif"]["url"]

        gif_data = requests.get(current_gif_url).content
        gif_bytes = io.BytesIO(gif_data)

        reader = imageio.get_reader(gif_bytes)
        frames.clear()

        for frame in reader:
            img = Image.fromarray(frame)
            img = img.resize((320, 320))
            frames.append(ImageTk.PhotoImage(img))

        frame_index = 0
        animation_running = True
        animate()

        save_btn.config(state="normal")
        download_btn.config(state="normal")
        status_label.config(text="GIF Loaded", fg="lightgreen")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Animate
def animate():
    global frame_index
    if animation_running and frames:
        gif_label.config(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        root.after(80, animate)


# Save favorite
def save_favorite():
    if current_gif_url:
        with open("favorites.txt", "a") as f:
            f.write(current_gif_url + "\n")
        messagebox.showinfo("Saved", "Added to favorites")


# View favorites
def view_favorites():
    try:
        with open("favorites.txt", "r") as f:
            links = f.readlines()

        if not links:
            messagebox.showinfo("Empty", "No favorites yet")
            return

        win = tk.Toplevel(root)
        win.title("Favorites")

        for link in links:
            link = link.strip()
            btn = tk.Button(win, text=link[:50], fg="blue",
                            command=lambda url=link: webbrowser.open(url))
            btn.pack(pady=3)

    except:
        messagebox.showinfo("Error", "No favorites file found")


# Download GIF
def download_gif():
    if current_gif_url:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        file_path = f"downloads/gif_{random.randint(1,10000)}.gif"
        data = requests.get(current_gif_url).content

        with open(file_path, "wb") as f:
            f.write(data)

        messagebox.showinfo("Downloaded", f"Saved to {file_path}")


# UI
root = tk.Tk()
root.title("GIF Grabber ULTRA")
root.geometry("420x600")
root.config(bg="#121212")

title = tk.Label(root, text="GIF Grabber", font=("Arial", 20, "bold"),
                 fg="#00ffcc", bg="#121212")
title.pack(pady=10)

entry = tk.Entry(root, width=25, font=("Arial", 12))
entry.pack(pady=10)

search_btn = tk.Button(root, text="Search",
                       command=lambda: fetch_gif(),
                       bg="#00ffcc", fg="black")
search_btn.pack(pady=5)

# Quick category buttons
frame = tk.Frame(root, bg="#121212")
frame.pack(pady=5)

tk.Button(frame, text=" Meme", command=lambda: fetch_gif("meme")).grid(row=0, column=0, padx=5)
tk.Button(frame, text=" Cat", command=lambda: fetch_gif("cat")).grid(row=0, column=1, padx=5)
tk.Button(frame, text=" Cool", command=lambda: fetch_gif("cool")).grid(row=0, column=2, padx=5)

gif_label = tk.Label(root, bg="#121212")
gif_label.pack(pady=20)

status_label = tk.Label(root, text="", bg="#121212", fg="white")
status_label.pack()

save_btn = tk.Button(root, text="Save", state="disabled",
                     command=save_favorite, bg="#2196F3", fg="white")
save_btn.pack(pady=5)

download_btn = tk.Button(root, text="Download ", state="disabled",
                         command=download_gif, bg="#4CAF50", fg="white")
download_btn.pack(pady=5)

view_btn = tk.Button(root, text="Favorites ",
                     command=view_favorites, bg="#FF9800", fg="white")
view_btn.pack(pady=10)

root.mainloop()
