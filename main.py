import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'books.json'

# Загрузка данных
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = []

# Основное окно
root = tk.Tk()
root.title("Book Tracker")

# Поля ввода
tk.Label(root, text="Название книги").grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(root)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Автор").grid(row=1, column=0, padx=5, pady=5)
entry_author = tk.Entry(root)
entry_author.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр").grid(row=2, column=0, padx=5, pady=5)
entry_genre = tk.Entry(root)
entry_genre.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Количество страниц").grid(row=3, column=0, padx=5, pady=5)
entry_pages = tk.Entry(root)
entry_pages.grid(row=3, column=1, padx=5, pady=5)

# Таблица (Treeview)
columns = ('title', 'author', 'genre', 'pages')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())

tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# Функции для работы с данными
def save_to_json():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def refresh_treeview(data=None):
    for item in tree.get_children():
        tree.delete(item)
    data = data if data is not None else books
    for book in data:
        tree.insert('', tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    # Проверка
    if not title or not author or not genre or not pages:
        messagebox.showwarning("Пустое поле", "Заполните все поля!")
        return
    if not pages.isdigit():
        messagebox.showwarning("Некорректный ввод", "Количество страниц должно быть числом.")
        return

    book = {
        'title': title,
        'author': author,
        'genre': genre,
        'pages': int(pages)
    }
    books.append(book)
    save_to_json()
    refresh_treeview()
    # Очистка полей
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

def delete_selected():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Выбор отсутствует", "Выберите книгу для удаления.")
        return
    index = tree.index(selected_item)
    # Удаление из списка
    del books[index]
    save_to_json()
    refresh_treeview()

def filter_books():
    genre_filter = simple_filter_genre.get().strip().lower()
    pages_filter = simple_filter_pages.get().strip()

    filtered = books
    if genre_filter:
        filtered = [b for b in filtered if genre_filter in b['genre'].lower()]
    if pages_filter.isdigit():
        threshold = int(pages_filter)
        filtered = [b for b in filtered if b['pages'] > threshold]

    refresh_treeview(filtered)

def reset_filter():
    simple_filter_genre.set('')
    simple_filter_pages.set('')
    refresh_treeview()

# Кнопки
btn_frame = tk.Frame(root)
btn_frame.grid(row=4, column=0, columnspan=4, pady=5)

tk.Button(btn_frame, text="Добавить книгу", command=add_book).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Удалить выбранное", command=delete_selected).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Сбросить фильтр", command=reset_filter).pack(side=tk.LEFT, padx=5)

# Фильтры
tk.Label(root, text="Фильтр по жанру").grid(row=6, column=0, padx=5, pady=2)
simple_filter_genre = tk.StringVar()
tk.Entry(root, textvariable=simple_filter_genre).grid(row=6, column=1, padx=5, pady=2)

tk.Label(root, text="По страницам (более)").grid(row=7, column=0, padx=5, pady=2)
simple_filter_pages = tk.StringVar()
tk.Entry(root, textvariable=simple_filter_pages).grid(row=7, column=1, padx=5, pady=2)

tk.Button(root, text="Применить фильтр", command=filter_books).grid(row=8, column=0, columnspan=2, pady=5)

# Первое отображение
refresh_treeview()

root.mainloop()
