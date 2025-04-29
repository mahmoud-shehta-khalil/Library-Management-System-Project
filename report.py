# File: report.py
# Purpose: Generates static and dynamic reports

class Report:
    def __init__(self, db):
        self.db = db

    def generate_overdue_report(self):
        """Generates a static report of overdue books."""
        query = """
            SELECT t.transaction_id, b.title, c.name, t.due_date, t.fine
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.return_date IS NULL AND t.due_date < SYSDATE
        """
        try:
            return self.db.execute_query(query, fetch=True)
        except oracledb.Error as e:
            logging.error(f"Error generating overdue report: {e}")
            return []

    def generate_transaction_history(self, start_date, end_date):
        """Generates a dynamic report of transactions within a date range."""
        query = """
            SELECT t.transaction_id, b.title, c.name, t.checkout_date, t.return_date
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.checkout_date BETWEEN TO_DATE(:1, 'YYYY-MM-DD') AND TO_DATE(:2, 'YYYY-MM-DD')
        """
        try:
            return self.db.execute_query(query, [start_date, end_date], fetch=True)
        except oracledb.Error as e:
            logging.error(f"Error generating transaction history: {e}")
            return []