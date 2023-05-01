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
                user_id TEXT,
                api_key TEXT,
                chat_state INTEGER DEFAULT 1,
                img_description TEXT DEFAULT 'Empty',
                img_count INTEGER DEFAULT 1
            )
            """
        )

        connection.commit()
        connection.close()

    def add_user(self, user_id: str):
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO user_data (user_id) VALUES (?)", (user_id))
        connection.commit()
        connection.close()

    def get_api_key(self, user_id: str) -> str:
        encrypted_api_key = self._get_table_field(user_id, 'api_key')

        if encrypted_api_key:
            decrypted_api_key = self._fernet.decrypt(encrypted_api_key[0].encode()).decode()
            return decrypted_api_key
        else:
            return None

    def store_api_key(self, user_id: str, api_key: str):
        encrypted_api_key = self._fernet.encrypt(api_key.encode()).decode()

        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO user_data (user_id, api_key) VALUES (?, ?)",
            (user_id, encrypted_api_key)
        )

        connection.commit()
        connection.close()

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

    def _get_table_field(self, user_id: str, field: str):
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT {field} FROM user_data WHERE user_id={user_id}")
        field_data = cursor.fetchone()
        connection.close()
        return field_data
    
    def _set_table_field(self, user_id: str, field: str, value):
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute(f"UPDATE user_data SET {field} = ? WHERE user_id = ?", (value, user_id))
        connection.commit()
        connection.close()
