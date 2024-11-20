import requests
import os
import tkinter as tk
from tkinter import filedialog


def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[('JPEG', '*.jpg'), ('PNG', '*.png'), ('GIF', '*.gif')])
    if file:
        global image_path
        image_path = os.path.abspath(file.name)
        filename = os.path.basename(file.name)
        selected_file['text'] = filename


def upload_to_imgur():
    url = "https://api.imgur.com/3/image"
    client_id = imgur_id.get().rstrip('\n')
    headers = {"Authorization": f"Client-ID {client_id}"}
    with open(image_path, "rb") as image_file:
        payload = {"image": image_file.read()}

    response = requests.post(url, headers=headers, files=payload)
    if response.status_code == 200:
        data = response.json()
        image_url = data["data"]["link"]
        ready.configure(state=tk.NORMAL)
        ready.insert(tk.END, f"[img]{image_url}[/img]")
        ready.configure(state=tk.DISABLED)
    else:
        ready.configure(state=tk.NORMAL)
        ready.insert(tk.END, "Failed to upload image:\n", response.text)
        ready.configure(state=tk.DISABLED)


root = tk.Tk()


def write(text_widget, text):
    text_widget.configure(state=tk.NORMAL)
    text_widget.insert(tk.END, text)
    text_widget.configure(state=tk.DISABLED)


root.title('Загрузка изображения на Imgur')
root.geometry('400x300')

import_button = tk.Button(root, text='Импорт', command=open_file)
import_button.pack(padx=6, pady=6)

selected = tk.Label(text='Выбранный файл:')
selected.pack(padx=3, pady=3)
selected_file = tk.Label(root)
selected_file.pack(padx=6, pady=6)

enter_id = tk.Label(root, text='Ваш Client ID на Imgur:')
enter_id.pack(padx=6, pady=6)
imgur_id = tk.Entry(root)
imgur_id.pack(padx=6, pady=3)

submit_button = tk.Button(root, text='Загрузить', command=upload_to_imgur)
submit_button.pack(padx=6, pady=10)

uploaded_status = tk.Label(root, text='В этом поле появится ссылка с тегами (или код ошибки):')
uploaded_status.pack(padx=6, pady=6)
ready = tk.Text(root, state=tk.DISABLED)
ready.pack(padx=6, pady=6)

root.mainloop()
