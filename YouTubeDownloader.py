from customtkinter import *
from pytube import YouTube
from threading import Thread
from tkinter import filedialog
import time

# UI Setup
window = CTk(fg_color="gray17")
window.config(padx=10, pady=10)
window.geometry("700x550")
window.title("Youtube Downloader v0.1.5")

# Url Setup
the_url = CTkLabel(window, text="Enter URL", text_color="Green", font=("Arial", 20))
the_url.pack(side="top", pady=10)
user_url = CTkEntry(window, width=400, height=30, placeholder_text="Enter URL")
user_url.pack(side="top", pady=10)

# Video info
def video_info():
    try:
        yt = YouTube(user_url.get())
        # show video name
        name = CTkLabel(window, text="Title: " + yt.title)
        name.pack(side="top", pady=10)
        # show views
        views = CTkLabel(window, text="Views: " + str(yt.views))
        views.pack(side="top", pady=10)
    except Exception as e:
        error_message = CTkLabel(window, text=f"Error: {str(e)}", text_color="Red")
        error_message.pack(side="top", pady=10)

get_info = CTkButton(window, text="Get info", command=video_info, width=200)
get_info.pack(side="top", pady=10)

# Choose folder to save the file in
folder_frame = CTkFrame(master=window, width=400, height=30, fg_color="gray17")
folder_frame.pack(pady=10)

my_directory = ''

def select_directory():
    global my_directory
    my_directory = filedialog.askdirectory()
    if my_directory:
        status_label.configure(text=f"Selected Directory: {my_directory}", text_color="Green")

select_folder = CTkButton(folder_frame, text="Select folder", command=select_directory)
select_folder.pack(side="left")

status_label = CTkLabel(folder_frame, text="", text_color="Black")
status_label.pack(side="left", after=select_folder, padx=5)


# Download options
download_frame = CTkFrame(master=window, height=30, fg_color="gray17")
download_frame.pack(pady=10)

combo = CTkComboBox(download_frame, values=["1440p", "1080p", "720p", "480p", "360p", "240p", "144p"])
combo.pack(side="left")

# Download progress
progress_bar = CTkProgressBar(window, width=400, progress_color="Green")
progress_bar.pack(side="top", pady=10)
progress_bar.set(0)  # Initialize progress bar to 0

# Real-time download speed
speed_label = CTkLabel(window, text="Speed: 0 KB/s", text_color="Blue", font=("Arial", 14))
speed_label.pack(side="top", pady=10)

# Variables to calculate download speed
start_time = None
bytes_downloaded_previous = 0

def on_progress(stream, chunk, bytes_remaining):
    global start_time, bytes_downloaded_previous
    if start_time is None:
        start_time = time.time()
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        speed = (bytes_downloaded - bytes_downloaded_previous) / elapsed_time / 1024  # speed in KB/s
        speed_label.configure(text=f"Speed: {speed:.2f} KB/s")
        bytes_downloaded_previous = bytes_downloaded
        start_time = time.time()
    percentage_of_completion = bytes_downloaded / total_size
    progress_bar.set(percentage_of_completion)

def update_progress_bar():
    while True:
        window.update_idletasks()
        time.sleep(0.01)

# Show downloading status
def show_status(message, color="Black"):
    status_label = CTkLabel(window, text=message, text_color=color)
    status_label.pack(side="top", pady=5)

# Download Video

def download():
    global start_time, bytes_downloaded_previous
    try:
        yt = YouTube(user_url.get())
        yt.register_on_progress_callback(on_progress)
        ys = yt.streams.get_by_resolution(resolution=combo.get())
        start_time = None  # Reset start time for each download
        bytes_downloaded_previous = 0
        Thread(target=update_progress_bar).start()
        ys.download(output_path=my_directory)
        show_status("Download Complete", "Green")
    except Exception as e:
        show_status(f"Error: {str(e)}", "Red")

download_button = CTkButton(download_frame, text="Download Custom Resolution", command=lambda: Thread(target=download).start())
download_button.pack(side="left", padx=10)

# Max Resolution download
def max_resolution():
    global start_time, bytes_downloaded_previous
    try:
        yt = YouTube(user_url.get(), use_oauth=False, allow_oauth_cache=True)
        yt.register_on_progress_callback(on_progress)
        ys = yt.streams.get_highest_resolution()
        start_time = None  # Reset start time for each download
        bytes_downloaded_previous = 0
        Thread(target=update_progress_bar).start()
        ys.download(output_path=my_directory)
        show_status("Download Complete", "Green")
    except Exception as e:
        show_status(f"Error: {str(e)}", "Red")

max_resolution_button = CTkButton(window, text="Max Resolution", command=lambda: Thread(target=max_resolution).start())
max_resolution_button.pack(side="top", pady=10)

# Lowest Resolution download
def lowest_resolution():
    global start_time, bytes_downloaded_previous
    try:
        yt = YouTube(user_url.get(), use_oauth=False, allow_oauth_cache=True)
        yt.register_on_progress_callback(on_progress)
        ys = yt.streams.get_lowest_resolution()
        start_time = None  # Reset start time for each download
        bytes_downloaded_previous = 0
        Thread(target=update_progress_bar).start()
        ys.download(output_path=my_directory)
        show_status("Download Complete", "Green")
    except Exception as e:
        show_status(f"Error: {str(e)}", "Red")

lowest_resolution_button = CTkButton(window, text="Lowest Resolution", command=lambda: Thread(target=lowest_resolution).start())
lowest_resolution_button.pack(side="top", pady=10)


# Signature and custom font

signature = CTkLabel(window, text="Made by: Moustafa Essam", font=("Arial", 14))
signature.pack(side="bottom")

window.mainloop()
