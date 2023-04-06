import tkinter as tk
from tkinter import ttk
from pytube import YouTube, Playlist
import os

def check_downloads_folder():
    """C:\Downloads\ klasörünü kontrol et ve yoksa oluştur."""
    downloads_path = "C:\\Downloads\\"
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)

def update_output_path():
    """Checkbox durumuna göre output path'i güncelle."""
    if remember_var.get() == 1:
        output_path = output_entry.get()
        with open("output_path.txt", "w") as f:
            f.write(output_path)
    else:
        output_path = "C:\\Downloads\\"
        with open("output_path.txt", "w") as f:
            f.write(output_path)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

def download():
    url = url_entry.get()

    if remember_var.get() == 1:
        update_output_path()

    output_path = output_entry.get()

    if "playlist" in url:
        playlist = Playlist(url)
        for video in playlist.videos:
            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=output_path)
    else:
        video = YouTube(url)
        video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=output_path)

    status_label.config(text="FIN")

root = tk.Tk()
root.geometry("700x600")
root.title("YouTube Downloader")

url_label = tk.Label(root, text="Enter YouTube URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

output_label = tk.Label(root, text="Enter download path:")
output_label.pack()

output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=10)

remember_var = tk.IntVar()
remember_checkbox = tk.Checkbutton(root, text="Remember path", variable=remember_var, command=update_output_path)
remember_checkbox.pack()

quality_label = tk.Label(root, text="Select video quality:")
quality_label.pack()

quality_var = tk.StringVar()
quality_var.set("high")

quality_radio1 = tk.Radiobutton(root, text="High", variable=quality_var, value="high")
quality_radio1.pack()

quality_radio2 = tk.Radiobutton(root, text="Medium", variable=quality_var, value="medium")
quality_radio2.pack()

quality_radio3 = tk.Radiobutton(root, text="Low", variable=quality_var, value="low")
quality_radio3.pack()

download_button = tk.Button(root, text="Download", command=download, bg="red", fg="white")
download_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=20)

# C:\Downloads\ klasörünü kontrol et ve yoksa oluştur
check_downloads_folder()

# output path'i hatırla seçeneğini kontrol et ve gerekirse güncelle
if os.path.exists("output_path.txt"):
    with open("output_path.txt", "r") as f:
        output_path = f.read()
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)
        remember_var.set(1)
else:
    remember_var.set(0)

root.mainloop()
