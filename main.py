import os
from app.main_window import App

if __name__ == '__main__':
    os.makedirs('keys/private_keys', exist_ok=True)
    os.makedirs('keys/public_keys', exist_ok=True)
    os.makedirs('PK', exist_ok=True)

    app = App()
    app.mainloop()
