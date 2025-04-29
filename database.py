# File: database.py
# Purpose: Handles Oracle Database connectivity and queries
import oracledb
import logging

# Configure logging for error tracking
logging.basicConfig(level=logging.INFO, filename='library.log')

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establishes connection to Oracle Database."""
        try:
            self.connection = oracledb.connect(
                user="your_username",
                password="your_password",
                dsn="your_dsn"  # e.g., localhost:1521/orcl
            )
            self.cursor = self.connection.cursor()
            logging.info("Database connection established.")
        except oracledb.Error as e:
            logging.error(f"Database connection error: {e}")
            raise

    def execute_query(self, query, params=None, fetch=False):
        """Executes a SQL query with optional parameters."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if fetch:
                return self.cursor.fetchall()
            self.connection.commit()
        except oracledb.Error as e:
            logging.error(f"Query execution error: {e}")
            raise

    def setup_database(self):
        """Sets up database tables, sequences, and triggers."""
        try:
            # Create Books Table
            self.execute_query("""
                CREATE TABLE books (
                    book_id NUMBER PRIMARY KEY,
                    title VARCHAR2(100),
                    author VARCHAR2(50),
                    genre VARCHAR2(50),
                    isbn VARCHAR2(13),
                    is_available NUMBER(1) DEFAULT 1
                )
            """)

            # Create Customers Table
            self.execute_query("""
                CREATE TABLE customers (
                    customer_id NUMBER PRIMARY KEY,
                    name VARCHAR2(100),
                    email VARCHAR2(100),
                    membership_status VARCHAR2(20)
                )
            """)

            # Create Transactions Table
            self.execute_query("""
                CREATE TABLE transactions (
                    transaction_id NUMBER PRIMARY KEY,
                    book_id NUMBER,
                    customer_id NUMBER,
                    checkout_date DATE,
                    return_date DATE,
                    due_date DATE,
                    fine NUMBER DEFAULT 0,
                    FOREIGN KEY (book_id) REFERENCES books(book_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )
            """)

            # Create Sequence for Auto-incrementing IDs
            self.execute_query("CREATE SEQUENCE book_seq START WITH 1 INCREMENT BY 1")
            self.execute_query("CREATE SEQUENCE customer_seq START WITH 1 INCREMENT BY 1")
            self.execute_query("CREATE SEQUENCE transaction_seq START WITH 1 INCREMENT BY 1")

            # Create Trigger for Auto-incrementing Book ID
            self.execute_query("""
                CREATE OR REPLACE TRIGGER book_trigger
                BEFORE INSERT ON books
                FOR EACH ROW
                BEGIN
                    SELECT book_seq.NEXTVAL INTO :NEW.book_id FROM dual;
                END;
            """)

            # Create Trigger for Auto-incrementing Customer ID
            self.execute_query("""
                CREATE OR REPLACE TRIGGER customer_trigger
                BEFORE INSERT ON customers
                FOR EACH ROW
                BEGIN
                    SELECT customer_seq.NEXTVAL INTO :NEW.customer_id FROM dual;
                END;
            """)

            # Create Trigger for Auto-incrementing Transaction ID
            self.execute_query("""
                CREATE OR REPLACE TRIGGER transaction_trigger
                BEFORE INSERT ON transactions
                FOR EACH ROW
                BEGIN
                    SELECT transaction_seq.NEXTVAL INTO :NEW.transaction_id FROM dual;
                END;
            """)

            # Database Trigger to Calculate Fines
            self.execute_query("""
                CREATE OR REPLACE TRIGGER fine_trigger
                AFTER UPDATE OF return_date ON transactions
                FOR EACH ROW
                BEGIN
                    IF :NEW.return_date > :NEW.due_date THEN
                        UPDATE transactions
                        SET fine = (TRUNC(:NEW.return_date) - TRUNC(:NEW.due_date)) * 1
                        WHERE transaction_id = :NEW.transaction_id;
                    END IF;
                END;
            """)
            logging.info("Database setup completed.")
        except oracledb.Error as e:
            logging.error(f"Database setup error: {e}")
            raise

    def close(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Database connection closed.")