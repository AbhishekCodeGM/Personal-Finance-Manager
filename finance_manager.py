import sqlite3
from datetime import datetime

class FinanceManager:
    def __init__(self, db_name="FinanceDB.sqlite"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                Amount DECIMAL(10, 2),
                Date DATE,
                Category TEXT,
                Description TEXT
            )
        ''')

    def add_transaction(self, amount, category, description):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
            INSERT INTO Transactions (Amount, Date, Category, Description)
            VALUES (?, ?, ?, ?)
        ''', (amount, date, category, description))
        self.conn.commit()

    def view_transactions(self):
        self.cursor.execute('SELECT * FROM Transactions')
        return self.cursor.fetchall()

    def category_summary(self):
        self.cursor.execute('''
            SELECT Category, SUM(Amount) FROM Transactions
            GROUP BY Category
        ''')
        return self.cursor.fetchall()

    def monthly_report(self):
        current_month = datetime.now().strftime("%Y-%m")
        self.cursor.execute('''
            SELECT SUM(Amount) FROM Transactions
            WHERE Date LIKE ?
        ''', (f'{current_month}%',))
        return self.cursor.fetchone()[0]

    def close_connection(self):
        self.conn.close()

# Main function
def main():
    manager = FinanceManager()

    while True:
        print("\n1. Add Transaction")
        print("2. View Transactions")
        print("3. View Category Summary")
        print("4. View Monthly Report")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category (e.g., Food, Bills, Entertainment): ")
            description = input("Enter description: ")
            manager.add_transaction(amount, category, description)

        elif choice == '2':
            transactions = manager.view_transactions()
            for transaction in transactions:
                print(f"ID: {transaction[0]}, Amount: {transaction[1]}, Date: {transaction[2]}, Category: {transaction[3]}, Description: {transaction[4]}")

        elif choice == '3':
            summary = manager.category_summary()
            for category, total in summary:
                print(f"Category: {category}, Total: {total}")

        elif choice == '4':
            monthly_total = manager.monthly_report()
            print(f"Total for this month: {monthly_total}")

        elif choice == '5':
            manager.close_connection()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
