import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name):
        # Initialize and connect to the database
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # Create the table if it doesn't already exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expensetype TEXT NOT NULL,
                amount REAL,
                paymenttype TEXT,
                descr TEXT,
                IsActive INT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense_transaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expensetypeId INT NOT NULL,
                expensetype TEXT NOT NULL,
                amount REAL,
                paymenttype TEXT,
                descr TEXT,
                IsActive INT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_user (
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def alter_table(self):
        self.cursor.execute('update expenses set entryby="Ash"')
        self.connection.commit()
    
    def insert_expense(self, expensetype, amount, paymenttype, descr, entryby):
        # Insert a new user
        self.cursor.execute('''
            INSERT INTO expenses (expensetype, amount, paymenttype, descr, isactive, entryby)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (expensetype, amount, paymenttype, descr, "1", entryby))
        self.connection.commit()

    def insert_transaction(self, expensetypeid, expensetype, amount, paymenttype, descr, entryby):
        # Insert a new user
        
        self.cursor.execute('''
            INSERT INTO expense_transaction (expensetypeid, expensetype, amount, paymenttype, descr, isactive, entrydate, entryby)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (expensetypeid, expensetype, amount, paymenttype, descr, 1, datetime.now(), entryby))
        self.connection.commit()
    
    def insert_login(self, username, password):
        # Insert a new user
        
        self.cursor.execute('''
            INSERT INTO login_user (username, password)
            VALUES (?, ?)
        ''', (username, password))
        self.connection.commit()
    
    def update_changepassword(self, username, oldpassword, newpassword):
        # Insert a new user
        try:
            self.cursor.execute('''
                UPDATE login_user SET password = ?
                WHERE username = ? and password = ?
            ''', (newpassword, username, oldpassword))
            self.connection.commit()
            return self.cursor.rowcount 
        except Exception as e:
        # Log the error for debugging
            print(f"Error updating password: {e}")
            return None

    def update_user(self, user_id, name=None, age=None, email=None):
        # Update a user's information based on provided values
        updates = []
        parameters = []
        if name:
            updates.append("name = ?")
            parameters.append(name)
        if age:
            updates.append("age = ?")
            parameters.append(age)
        if email:
            updates.append("email = ?")
            parameters.append(email)
        
        if updates:
            parameters.append(user_id)
            sql = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(sql, tuple(parameters))
            self.connection.commit()

    def fetch_expensetypebyId(self, exptypeid):
        # Retrieve all users
        self.cursor.execute('''SELECT expensetype from expenses
                        WHERE isactive = 1 AND id = ? 
                       ''', (exptypeid,))
        return self.cursor.fetchone()
    
    def delete_expenses(self, expense_id):
        # Delete a user by their ID
        self.cursor.execute('UPDATE expenses SET IsActive = 0 WHERE id = ?', (expense_id,))
        self.connection.commit()
    def delete_expenses_trans(self, trnas_id):
        # Delete a user by their ID
        self.cursor.execute('UPDATE expense_transaction SET IsActive = 0 WHERE id = ?', (trnas_id,))
        self.connection.commit()

    def fetch_expenses(self):
        # Retrieve all users
        self.cursor.execute('SELECT * FROM expenses where isactive = 1')
        return self.cursor.fetchall()
    
    def fetch_transaction(self):
        # Retrieve all users
        self.cursor.execute('SELECT * FROM expense_transaction where isactive = 1')
        return self.cursor.fetchall()
    
    def fetch_homedisplay(self, exptypeid):
        # Retrieve all users
        self.cursor.execute('''SELECT paymenttype, sum(amount) as amount 
                        FROM expense_transaction
                        WHERE isactive = 1 AND expensetypeid = ? 
                        GROUP BY paymenttype 
                        ORDER BY paymenttype''', (exptypeid,))
        return self.cursor.fetchall()
    
    def fetch_report(self, exptypeid):
        # Retrieve all users
        self.cursor.execute('''SELECT e.expensetype, t.amount, t.paymenttype, t.descr, t.entrydate, t.entryby
                        FROM expenses e
                        join expense_transaction t
                        on e.id=t.expensetypeid
                        WHERE t.isactive = 1 AND expensetypeid = ? 
                        ORDER BY entrydate''', (exptypeid,))
        return self.cursor.fetchall()
    
    def fetch_login(self, username, password):
        # Retrieve all users
        self.cursor.execute('''SELECT username
                        FROM login_user
                        WHERE username = ? AND password = ? 
                        ''', (username,password,))
        return self.cursor.fetchone()
    
    def close(self):
        # Close the database connection
        self.connection.close()


# # Example usage
# if __name__ == "__main__":
#     db = DatabaseManager("example.db")
    
#     # Insert users
#     db.insert_user("Alice", 30, "alice@example.com")
#     db.insert_user("Bob", 25, "bob@example.com")
    
#     # Update user
#     db.update_user(1, name="Alice Cooper", age=31)
    
#     # Fetch and print all users
#     users = db.fetch_users()
#     print("Users:", users)

#     # Delete a user
#     db.delete_user(2)
    
#     # Fetch and print all users after deletion
#     users = db.fetch_users()
#     print("Users after deletion:", users)
    
#     # Close the database
#     db.close()
