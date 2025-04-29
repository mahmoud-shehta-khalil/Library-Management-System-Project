# File: customer.py
# Purpose: Manages customer-related operations
class Customer:
    def __init__(self, db):
        self.db = db

    def add_customer(self, name, email, membership_status):
        """Adds a new customer to the database."""
        query = """
            INSERT INTO customers (name, email, membership_status)
            VALUES (:1, :2, :3)
        """
        try:
            self.db.execute_query(query, [name, email, membership_status])
            return True
        except oracledb.Error as e:
            logging.error(f"Error adding customer: {e}")
            return False

    def update_customer(self, customer_id, name, email, membership_status):
        """Updates customer details."""
        query = """
            UPDATE customers
            SET name = :1, email = :2, membership_status = :3
            WHERE customer_id = :4
        """
        try:
            self.db.execute_query(query, [name, email, membership_status, customer_id])
            return True
        except oracledb.Error as e:
            logging.error(f"Error updating customer: {e}")
            return False

    def delete_customer(self, customer_id):
        """Deletes a customer from the database."""
        query = "DELETE FROM customers WHERE customer_id = :1"
        try:
            self.db.execute_query(query, [customer_id])
            return True
        except oracledb.Error as e:
            logging.error(f"Error deleting customer: {e}")
            return False

    def get_customer(self, customer_id):
        """Fetches customer details by ID."""
        query = """
            SELECT customer_id, name, email, membership_status
            FROM customers
            WHERE customer_id = :1
        """
        try:
            result = self.db.execute_query(query, [customer_id], fetch=True)
            return result[0] if result else None
        except oracledb.Error as e:
            logging.error(f"Error fetching customer: {e}")
            return None
