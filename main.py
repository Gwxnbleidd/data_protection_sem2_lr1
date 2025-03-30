import os
from app.main_window import App

if __name__ == '__main__':
    if not os.path.exists('keys/private_keys'):
        os.mkdir('keys/private_keys')
    if not os.path.exists('keys/public_keys'):
        os.mkdir('keys/public_keys')

    app = App()
    app.mainloop()
