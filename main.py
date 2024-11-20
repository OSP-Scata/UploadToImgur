import os
import tkinter as tk
from tkinter import filedialog

import requests


def open_file():
    files = filedialog.askopenfilenames(filetypes=[('JPEG', '*.jpg'), ('PNG', '*.png'), ('GIF', '*.gif')])
    if files:
        global lst
        lst = list(files)
        for file in lst:
            filename = os.path.basename(file)
            selected_file.configure(state=tk.NORMAL)
            selected_file.insert(tk.END, filename + '\n')
            selected_file.configure(state=tk.DISABLED)


def upload(lst, url, headers):
    for file in lst:
        image_path = os.path.abspath(file)
        with open(image_path, "rb") as image_file:
            payload = {"image": image_file.read()}

        response = requests.post(url, headers=headers, files=payload)
        if response.status_code == 200:
            data = response.json()
            image_url = data["data"]["link"]
            ready.configure(state=tk.NORMAL)
            ready.insert(tk.END, f"[img]{image_url}[/img]\n")
            ready.configure(state=tk.DISABLED)
        else:
            ready.configure(state=tk.NORMAL)
            ready.insert(tk.END, "Failed to upload image:\n", response.text)
            ready.configure(state=tk.DISABLED)


def upload_to_imgur():
    url = "https://api.imgur.com/3/image"
    try:
        with open('client_id.txt', "r") as id_file:
            client_id = id_file.readline()
            headers = {"Authorization": f"Client-ID {client_id}"}
            upload(lst, url, headers)
    except FileNotFoundError:
        client_id = imgur_id.get().rstrip('\n')
        if client_id:
            with open('client_id.txt', 'w') as f:
                f.write(client_id)
            headers = {"Authorization": f"Client-ID {client_id}"}
            upload(lst, url, headers)
        else:
            ready.configure(state=tk.NORMAL)
            ready.insert(tk.END, 'Введите Client ID!')
            ready.configure(state=tk.DISABLED)


# print('Client ID:', client_id)


root = tk.Tk()

root.title('Загрузка изображения на Imgur')
root.geometry('400x400')

import_button = tk.Button(root, text='Импорт', command=open_file)
import_button.pack(padx=6, pady=6)

selected = tk.Label(text='Выбранные файлы:')
selected.pack(padx=3, pady=3)
selected_file = tk.Text(width=40, height=5, state=tk.DISABLED)
selected_file.pack()

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
