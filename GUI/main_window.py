import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лабораторная работа 1")
        # self.geometry("900x500")

        # Создаем строку меню
        menu_bar = tk.Menu(self)
        self['menu'] = menu_bar

        self.config(menu=menu_bar)

        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Создать")
        file_menu.add_command(label="Сохранить")
        file_menu.add_command(label="Загрузить")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)

        # Меню "Управление ключами"
        keys_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Управление ключами", menu=keys_menu)
        keys_menu.add_command(label="Выбор закрытого ключа")
        keys_menu.add_command(label="Экспорт открытого ключа")
        keys_menu.add_command(label="Импорт открытого ключа")
        keys_menu.add_command(label="Удалить пару")

        # Меню "О программе"
        about_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="О программе", menu=about_menu)
        about_menu.add_command(label="Справка")

        username_label = tk.Label(self, text="Имя пользователя:")
        username_entry = tk.Entry(self, state='disabled')
        choice_user_btn = tk.Button(self, text='Выбрать пользователя')
        load_document_btn = tk.Button(self, text='Загрузить документ')
        save_document_btn = tk.Button(self, text='Сохранить документ')
        text_place = tk.Text(self, width=100)

        username_label.grid(row=0, column=0, padx=5, pady=5)
        username_entry.grid(row=1, column=0, padx=5, pady=5)
        choice_user_btn.grid(row=0, column=1, padx=5, pady=5, rowspan=2)
        load_document_btn.grid(row=0, column=2, padx=5, pady=5, rowspan=2)
        save_document_btn.grid(row=0, column=3, padx=5, pady=5, rowspan=2)
        text_place.grid(row=2, pady=5, columnspan=4)


if __name__ == '__main__':
    app = App()
    app.mainloop()