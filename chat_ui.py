import tkinter as tk
from tkinter import filedialog
from chat_backend import (
    send_message,
    send_image_file,
    send_audio_file,
    start_receiver_thread,
    send_status_online
)

def send():
    msg = entry.get()
    selected_M = int(qam_option.get())
    if msg:
        send_message(msg, selected_M)
        chat_window.insert(tk.END, "You: " + msg + "\n")
        entry.delete(0, tk.END)

def send_image():
    filepath = filedialog.askopenfilename(filetypes=[
        ("Image files", ".png;.jpg;.jpeg;.bmp;.gif;.webp"),
        ("All files", ".")
    ])
    if filepath:
        selected_M = int(qam_option.get())
        send_image_file(filepath, selected_M)
        chat_window.insert(tk.END, f"You sent an image: {filepath}\n")

def send_audio():
    filepath = filedialog.askopenfilename(filetypes=[
        ("WAV files", "*.wav"),
        ("All files", ".")
    ])
    if filepath:
        selected_M = int(qam_option.get())
        send_audio_file(filepath, selected_M)
        chat_window.insert(tk.END, f"You sent audio: {filepath}\n")

def mark_receiver_online():
    status_label.config(text="Receiver status: Online", fg="green")

# UI setup
root = tk.Tk()
root.title("QAM UDP Chat")

status_label = tk.Label(root, text="Receiver: Offline", fg="red")
status_label.pack()

root.bind('<Return>', lambda event: send())

chat_window = tk.Text(root, height=20, width=50)
chat_window.pack()

entry_frame = tk.Frame(root)
entry_frame.pack(pady=5)

entry = tk.Entry(entry_frame, width=40)
entry.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(entry_frame, text="Send", command=send)
send_button.pack(side=tk.RIGHT, padx=5)

image_button = tk.Button(root, text="Send Image", command=send_image)
image_button.pack(pady=2)

audio_button = tk.Button(root, text="Send Audio", command=send_audio)
audio_button.pack(pady=2)

qam_option = tk.StringVar(root)
qam_option.set("16")
qam_menu = tk.OptionMenu(root, qam_option, "4", "16", "64", "256")
qam_menu.pack()

# Start listening and send STATUS
start_receiver_thread(chat_window, qam_option, mark_receiver_online)
send_status_online(int(qam_option.get()))

root.mainloop()
