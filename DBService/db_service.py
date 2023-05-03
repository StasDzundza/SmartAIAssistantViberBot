import sqlite3
from cryptography.fernet import Fernet

class UserDataDatabaseService:
    def __init__(self, encryption_key: str, db_name: str = "user_data.db"):
        self._db_name = db_name
        self._init_database()
        self._fernet = Fernet(encryption_key)

    def _init_database(self):
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id TEXT NOT NULL,
                api_key TEXT DEFAULT NULL,
                chat_state INTEGER DEFAULT 1,
                img_description TEXT DEFAULT 'Empty',
                img_count INTEGER DEFAULT 1,
                last_keyboard TEXT DEFAULT NULL
            )
            """
        )

        connection.commit()
        connection.close()

    def _add_user_if_not_exists(self, user_id: str):
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO user_data (user_id) VALUES (?)", (user_id,))
        connection.commit()
        connection.close()

    def get_api_key(self, user_id: str) -> str:
        self._add_user_if_not_exists(user_id)
        encrypted_api_key = self._get_table_field(user_id, 'api_key')
        if encrypted_api_key:
            decrypted_api_key = self._fernet.decrypt(encrypted_api_key.encode()).decode()
            return decrypted_api_key
        else:
            return None

    def store_api_key(self, user_id: str, api_key: str):
        encrypted_api_key = self._fernet.encrypt(api_key.encode()).decode()
        self._set_table_field(user_id, 'api_key', encrypted_api_key)

    def get_chat_state(self, user_id: str) -> int | None:
        return self._get_table_field(user_id, 'chat_state')
    
    def set_chat_state(self, user_id: str, chat_state: int):
        self._set_table_field(user_id, 'chat_state', chat_state)

    def get_img_description(self, user_id: str) -> str | None:
        return self._get_table_field(user_id, 'img_description')

    def set_img_description(self, user_id: str, img_description: str):
        self._set_table_field(user_id, 'img_description', img_description)

    def get_img_count(self, user_id: str) -> int | None:
        return self._get_table_field(user_id, 'img_count')
    
    def set_img_count(self, user_id: str, img_count: int):
        self._set_table_field(user_id, 'img_count', img_count)

    def get_last_keyboard(self, user_id: str) -> str | None:
        return self._get_table_field(user_id, 'last_keyboard')

    def set_last_keyboard(self, user_id: str, last_keyboard_json: str):
        self._set_table_field(user_id, 'last_keyboard', last_keyboard_json)

    def _get_table_field(self, user_id: str, field: str):
        self._add_user_if_not_exists(user_id)
    
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT {field} FROM user_data WHERE user_id = ?", (user_id,))
        field_data = cursor.fetchone()
        connection.close()

        return field_data[0]

    def _set_table_field(self, user_id: str, field: str, value):
        self._add_user_if_not_exists(user_id)

        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute(f"UPDATE user_data SET {field} = ? WHERE user_id = ?", (value, user_id))
        connection.commit()
        connection.close()
