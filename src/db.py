import json
import sqlite3


class UserDatabase:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            onboarded BOOLEAN DEFAULT 0,
            curriculum TEXT,
            user_context TEXT,
            memory TEXT
        )
        ''')
        self.conn.commit()

    def create_user(self, user_id, username):
        """Create a new user with basic information."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, user_id):
        """Get user information by user_id."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        user = cursor.fetchone()
        if user:
            return {
                'id': user[0],
                'user_id': user[1],
                'username': user[2],
                'created_at': user[3],
                'onboarded': bool(user[4]),
                'curriculum': json.loads(user[5]) if user[5] else None,
                'user_context': json.loads(user[6]) if user[6] else None
            }
        return None

    def update_onboarding_status(self, user_id, onboarded=True):
        """Update user's onboarding status."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE users SET onboarded = ? WHERE user_id = ?",
            (onboarded, user_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def update_curriculum(self, user_id, curriculum_data):
        """Update user's curriculum data."""
        cursor = self.conn.cursor()
        curriculum_json = json.dumps(curriculum_data) if curriculum_data else None
        cursor.execute(
            "UPDATE users SET curriculum = ? WHERE user_id = ?",
            (curriculum_json, user_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def update_user_context(self, user_id, context_data):
        """Update user's context data."""
        cursor = self.conn.cursor()
        context_json = json.dumps(context_data) if context_data else None
        cursor.execute(
            "UPDATE users SET user_context = ? WHERE user_id = ?",
            (context_json, user_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def update_user(self, user_id, **kwargs):
        """
        Update any user fields provided in kwargs.
        Example: update_user("user123", username="New Name", onboarded=True)
        """
        allowed_fields = {'username', 'onboarded', 'curriculum', 'user_context'}
        update_fields = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                if field in ['curriculum', 'user_context'] and value is not None:
                    value = json.dumps(value)
                update_fields.append(f"{field} = ?")
                values.append(value)
        
        if not update_fields:
            return False
            
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
        values.append(user_id)
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        return cursor.rowcount > 0

    def get_all_users(self):
        """Get all users from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return [{
            'id': user[0],
            'user_id': user[1],
            'username': user[2],
            'created_at': user[3],
            'onboarded': bool(user[4]),
            'curriculum': json.loads(user[5]) if user[5] else None,
            'user_context': json.loads(user[6]) if user[6] else None
        } for user in users]

    def delete_user(self, user_id):
        """Delete a user from the database."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def user_exists(self, user_id):
        """Check if a user exists in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None

    def user_onboarded(self, user_id):
        """Check if a user is onboarded in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT onboarded FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]
    
    def user_is_onboarded(self, user_id):
        """Update user's onboarded status to True."""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET onboarded = 1 WHERE user_id = ?", (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_memory(self, user_id):
        """Get user's memory from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT memory FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]
    
    def update_memory(self, user_id, memory):
        """Update user's memory in the database."""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET memory = ? WHERE user_id = ?", (memory, user_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def close(self):
        """Close the database connection."""
        self.conn.close()