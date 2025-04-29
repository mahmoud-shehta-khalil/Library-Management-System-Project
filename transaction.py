# File: transaction.py
# Purpose: Manages checkout and return operations
from datetime import datetime, timedelta

class Transaction:
    def __init__(self, db):
        self.db = db

    def checkout_book(self, book_id, customer_id):
        """Checks out a book to a customer."""
        due_date = datetime.now() + timedelta(days=14)  # 2-week loan period
        query = """
            INSERT INTO transactions (book_id, customer_id, checkout_date, due_date)
            VALUES (:1, :2, SYSDATE, :3)
        """
        update_book_query = """
            UPDATE books SET is_available = 0 WHERE book_id = :1
        """
        try:
            self.db.execute_query(query, [book_id, customer_id, due_date])
            self.db.execute_query(update_book_query, [book_id])
            return True
        except oracledb.Error as e:
            logging.error(f"Error checking out book: {e}")
            return False

    def return_book(self, book_id, transaction_id):
        """Returns a book to the library."""
        query = """
            UPDATE transactions
            SET return_date = SYSDATE
            WHERE transaction_id = :1
        """
        update_book_query = """
            UPDATE books SET is_available = 1 WHERE book_id = :1
        """
        try:
            self.db.execute_query(query, [transaction_id])
            self.db.execute_query(update_book_query, [book_id])
            return True
        except oracledb.Error as e:
            logging.error(f"Error returning book: {e}")
            return False

    def get_transactions_by_customer(self, customer_id):
        """Fetches all transactions for a customer."""
        query = """
            SELECT t.transaction_id, t.book_id, b.title, t.checkout_date, t.due_date, t.return_date, t.fine
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            WHERE t.customer_id = :1
        """
        try:
            return self.db.execute_query(query, [customer_id], fetch=True)
        except oracledb.Error as e:
            logging.error(f"Error fetching transactions: {e}")
            return []
