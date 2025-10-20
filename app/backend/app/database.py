import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict
import threading

class Database:
    def __init__(self, db_path: str = "synerchat.db"):
        self.db_path = db_path
        self.local = threading.local()
        self.init_db()
    
    def get_connection(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                username TEXT,
                profile_picture TEXT,
                public_key TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER NOT NULL,
                to_user_id INTEGER NOT NULL,
                verification_code TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_user_id) REFERENCES users(id),
                FOREIGN KEY (to_user_id) REFERENCES users(id)
            )
        ''')
        
        # Active chats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                user1_code TEXT NOT NULL,
                user2_code TEXT NOT NULL,
                last_verification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                next_verification TIMESTAMP,
                verification_pending BOOLEAN DEFAULT 0,
                user1_wants_delete BOOLEAN DEFAULT 0,
                user2_wants_delete BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user1_id) REFERENCES users(id),
                FOREIGN KEY (user2_id) REFERENCES users(id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                sender_id INTEGER NOT NULL,
                encrypted_content TEXT NOT NULL,
                message_type TEXT DEFAULT 'text',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES active_chats(id),
                FOREIGN KEY (sender_id) REFERENCES users(id)
            )
        ''')
        
        # Add message_type column if it doesn't exist (for existing databases)
        try:
            cursor.execute('ALTER TABLE messages ADD COLUMN message_type TEXT DEFAULT "text"')
            conn.commit()
        except:
            pass  # Column already exists
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
    
    def create_user(self, email: str, password_hash: str, username: str = None, 
                   profile_picture: str = None, public_key: str = None) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, password_hash, username, profile_picture, public_key) VALUES (?, ?, ?, ?, ?)',
            (email, password_hash, username, profile_picture, public_key)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_user_profile(self, user_id: int, username: str = None, 
                           profile_picture: str = None, public_key: str = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        updates = []
        params = []
        
        if username is not None:
            updates.append('username = ?')
            params.append(username)
        if profile_picture is not None:
            updates.append('profile_picture = ?')
            params.append(profile_picture)
        if public_key is not None:
            updates.append('public_key = ?')
            params.append(public_key)
        
        if updates:
            params.append(user_id)
            cursor.execute(
                f'UPDATE users SET {", ".join(updates)} WHERE id = ?',
                params
            )
            conn.commit()
    
    def create_session(self, user_id: int, token: str, expires_at: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)',
            (user_id, token, expires_at)
        )
        conn.commit()
    
    def get_session(self, token: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions WHERE token = ?', (token,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def delete_session(self, token: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
        conn.commit()
    
    def create_chat_request(self, from_user_id: int, to_user_id: int, 
                           verification_code: str) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chat_requests (from_user_id, to_user_id, verification_code) VALUES (?, ?, ?)',
            (from_user_id, to_user_id, verification_code)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_pending_requests(self, user_id: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT cr.*, u.email, u.username, u.profile_picture 
            FROM chat_requests cr
            JOIN users u ON cr.from_user_id = u.id
            WHERE cr.to_user_id = ? AND cr.status = 'pending'
            ORDER BY cr.created_at DESC
        ''', (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def accept_chat_request(self, request_id: int, user2_code: str) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get request details
        cursor.execute('SELECT * FROM chat_requests WHERE id = ?', (request_id,))
        request = dict(cursor.fetchone())
        
        # Create active chat
        from datetime import datetime, timedelta
        next_verification = datetime.now() + timedelta(minutes=30)
        
        cursor.execute('''
            INSERT INTO active_chats 
            (user1_id, user2_id, user1_code, user2_code, next_verification) 
            VALUES (?, ?, ?, ?, ?)
        ''', (request['from_user_id'], request['to_user_id'], 
              request['verification_code'], user2_code, next_verification))
        
        chat_id = cursor.lastrowid
        
        # Update request status
        cursor.execute('UPDATE chat_requests SET status = ? WHERE id = ?', 
                      ('accepted', request_id))
        
        conn.commit()
        return chat_id
    
    def get_active_chats(self, user_id: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ac.*, 
                   u1.email as user1_email, u1.username as user1_username, 
                   u1.profile_picture as user1_picture, u1.public_key as user1_public_key,
                   u2.email as user2_email, u2.username as user2_username,
                   u2.profile_picture as user2_picture, u2.public_key as user2_public_key
            FROM active_chats ac
            JOIN users u1 ON ac.user1_id = u1.id
            JOIN users u2 ON ac.user2_id = u2.id
            WHERE ac.user1_id = ? OR ac.user2_id = ?
            ORDER BY ac.last_verification DESC
        ''', (user_id, user_id))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_chat(self, chat_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM active_chats WHERE id = ?', (chat_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_chat_verification(self, chat_id: int):
        from datetime import datetime, timedelta
        conn = self.get_connection()
        cursor = conn.cursor()
        next_verification = datetime.now() + timedelta(minutes=30)
        cursor.execute('''
            UPDATE active_chats 
            SET last_verification = CURRENT_TIMESTAMP, 
                next_verification = ?,
                verification_pending = 0
            WHERE id = ?
        ''', (next_verification, chat_id))
        conn.commit()
    
    def set_verification_pending(self, chat_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE active_chats SET verification_pending = 1 WHERE id = ?',
            (chat_id,)
        )
        conn.commit()
    
    def clear_messages(self, chat_id: int):
        """Clear all messages from a chat"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        conn.commit()
    
    def request_chat_deletion(self, chat_id: int, user_id: int):
        """Mark that a user wants to delete the chat"""
        conn = self.get_connection()
        cursor = conn.cursor()
        chat = self.get_chat(chat_id)
        if not chat:
            return False
        
        # Check which user is requesting
        if chat['user1_id'] == user_id:
            cursor.execute('UPDATE active_chats SET user1_wants_delete = 1 WHERE id = ?', (chat_id,))
        elif chat['user2_id'] == user_id:
            cursor.execute('UPDATE active_chats SET user2_wants_delete = 1 WHERE id = ?', (chat_id,))
        else:
            return False
        
        conn.commit()
        
        # Check if both users want to delete
        cursor.execute('SELECT user1_wants_delete, user2_wants_delete FROM active_chats WHERE id = ?', (chat_id,))
        row = cursor.fetchone()
        if row and row['user1_wants_delete'] and row['user2_wants_delete']:
            self.delete_chat(chat_id)
            return True
        return False
    
    def delete_chat(self, chat_id: int):
        """Permanently delete a chat and all its messages"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        cursor.execute('DELETE FROM active_chats WHERE id = ?', (chat_id,))
        conn.commit()
    
    def save_message(self, chat_id: int, sender_id: int, encrypted_content: str, message_type: str = 'text') -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO messages (chat_id, sender_id, encrypted_content, message_type) VALUES (?, ?, ?, ?)',
            (chat_id, sender_id, encrypted_content, message_type)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_messages(self, chat_id: int, limit: int = 100) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, u.email, u.username, u.profile_picture, u.public_key
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE m.chat_id = ?
            ORDER BY m.created_at DESC
            LIMIT ?
        ''', (chat_id, limit))
        messages = [dict(row) for row in cursor.fetchall()]
        return list(reversed(messages))
    
    def search_users(self, query: str, exclude_user_id: int = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if exclude_user_id:
            cursor.execute('''
                SELECT id, email, username, profile_picture 
                FROM users 
                WHERE (email LIKE ? OR username LIKE ?) AND id != ?
                LIMIT 20
            ''', (f'%{query}%', f'%{query}%', exclude_user_id))
        else:
            cursor.execute('''
                SELECT id, email, username, profile_picture 
                FROM users 
                WHERE email LIKE ? OR username LIKE ?
                LIMIT 20
            ''', (f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cursor.fetchall()]

db = Database()
