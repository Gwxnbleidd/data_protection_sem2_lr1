import os
import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Hash import SHA256

from utils import get_users_key, create_user_keys, load_private_key, SignedDocument


# Вариант 28
# Алгоритм хеширования документа: SHA256
# Алгоритм подписи документа: ECDSA
# Алгоритм хеширования открытого ключа:SHA256
# Алгоритм подписи открытого ключа: ECDSA


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лабораторная работа 1")
        # self.geometry("900x500")

        # Создаем основные элементы управления
        self.username_label = tk.Label(self, text="Имя пользователя:")
        self.username_entry = tk.Entry(self, state='disabled')
        self.choice_user_btn = tk.Button(self, text='Выбрать пользователя', command=self._choice_user)
        self.load_document_btn = tk.Button(self, text='Загрузить документ', state='disabled')
        self.save_document_btn = tk.Button(self, text='Сохранить документ', state='disabled',
                                           command=self._save_document)
        self.text_place = tk.Text(self, width=100)

        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry.grid(row=1, column=0, padx=5, pady=5)
        self.username_entry.bind("<FocusOut>", self._focus_out_user_entry)

        self.choice_user_btn.grid(row=0, column=1, padx=5, pady=5, rowspan=2)
        self.load_document_btn.grid(row=0, column=2, padx=5, pady=5, rowspan=2)
        self.save_document_btn.grid(row=0, column=3, padx=5, pady=5, rowspan=2)
        self.text_place.grid(row=2, pady=5, columnspan=4)

        # Создаем строку меню
        menu_bar = tk.Menu(self)
        self['menu'] = menu_bar

        self.config(menu=menu_bar)

        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Создать", command=self._create_document)
        file_menu.add_command(label="Сохранить", command=self._save_document)
        file_menu.add_command(label="Загрузить")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)

        # Меню "Управление ключами"
        keys_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Управление ключами", menu=keys_menu)
        keys_menu.add_command(label="Выбор закрытого ключа", command=self._choice_user)
        keys_menu.add_command(label="Экспорт открытого ключа")
        keys_menu.add_command(label="Импорт открытого ключа")
        keys_menu.add_command(label="Удалить пару")

        # Меню "О программе"
        about_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="О программе", menu=about_menu)
        about_menu.add_command(label="Справка")

    def _choice_user(self):
        """
        Обработчик нажатия на кнопку "Выбор пользователя" и "Выбор закрытого ключа"
        """
        self.username_entry.config(state='normal')
        self.username_entry.focus_set()

    def _focus_out_user_entry(self, event):
        """
        Функция срабатывает как только пользователь потерял фокус с username_entry
        """
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Ошибка", "Введите имя пользователя")
            self.load_document_btn.config(state='disabled')
            self.save_document_btn.config(state='disabled')
            self.current_user = None
            self.private_key = None
            return

        path_to_private_key = get_users_key(username)
        if not path_to_private_key:
            if not messagebox.askyesno("Ключи не найдены",
                                       "Ключи для этого пользователя не найдены\nСоздать новую пару?"):
                self.username_entry.delete(0, tk.END)
                return
            create_user_keys(username)
            path_to_private_key = get_users_key(username)

        self.load_document_btn.config(state='normal')
        self.save_document_btn.config(state='normal')
        # Загрузить закрытый ключ
        self.private_key = load_private_key(path_to_private_key)
        if self.private_key:
            self.current_user = username
            messagebox.showinfo("Приватный ключ", f"Приватный ключ для пользователя '{username}' загружен")
        else:
            messagebox.showwarning('Ошибка', f'Приватный ключ для пользователя {username} не загружен!')
            return

    def _create_document(self):
        """
        Обработчик кнопки "Создать" меню "Файл"
        """
        self.text_place.delete("1.0", tk.END)
        self.title('Подписанный документ')

    def _save_document(self):
        """
        Обработчик кнопки "Сохранить" меню "Файл" и "Сохранить документ"
        """
        text_content = self.text_place.get("1.0", tk.END).strip()
        if not text_content:
            messagebox.showwarning("Ошибка", "Текстовое поле пустое")
            return
        hash_text = SHA256.new(text_content.encode('utf-8'))

        if not self.private_key:
            messagebox.showwarning("Ошибка", "Приватный ключ не загружен")
            return
        signature = self.private_key.sign(hash_text.digest())

        document = SignedDocument(username=self.current_user, sign=signature, text=text_content)
        signed_document_path = filedialog.asksaveasfilename(title="Сохранить документ")
        if not signed_document_path:
            return
        try:
            document._save_as_file(signed_document_path)
            messagebox.showinfo("Сохранение", "Документ успешно сохранён.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить документ:\n{e}")


if __name__ == '__main__':
    if not os.path.exists('private_keys'):
        os.mkdir('private_keys')
    if not os.path.exists('public_keys'):
        os.mkdir('public_keys')

    app = App()
    app.mainloop()
