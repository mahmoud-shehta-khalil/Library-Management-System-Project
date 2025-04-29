Library Management System
Project Overview
The Library Management System is a Python-based desktop application designed to streamline the core operations of a library. It provides a user-friendly graphical user interface (GUI) built with Tkinter and integrates with an Oracle Database for robust data management. The system supports full CRUD (Create, Read, Update, Delete) operations and is structured modularly to ensure maintainability and scalability.
Key Features
📚 Book Management

Add: Register new books with details like title, author, genre, and ISBN.
Edit: Update book information, including availability status.
Delete: Remove books from the inventory.
Search: Find books by title, author, genre, or ISBN.

👤 Customer Management

Add: Enroll new customers with name, email, and membership status.
Edit: Update customer details as needed.
Delete: Remove customers from the system.

🔁 Transaction Management

Checkout: Loan books to customers with automatic due date assignment.
Return: Process book returns and update availability.
Fines: Calculate overdue fines automatically via database triggers.
Reports: Generate transaction history and overdue reports.

💡 Additional Features

Master-Detail Forms: View customer transactions and book transactions in a relational format.
Navigation: Browse records using First, Next, Previous, and Last buttons.
Static/Dynamic Lists: Use predefined lists (e.g., genres, membership types) and dynamic queries.
Auto-Incrementing IDs: Utilize Oracle sequences for unique identifiers.
Triggers: Implement database and application-level triggers for automation.
Reports: Generate static (overdue books) and dynamic (transaction history) reports.

Architecture
🧱 Database Layer

Backend: Oracle Database stores all data.
Tables:
books: Stores book details (book_id, title, author, genre, isbn, is_available).
customers: Stores customer details (customer_id, name, email, membership_status).
transactions: Tracks loans (transaction_id, book_id, customer_id, checkout_date, due_date, return_date, fine).


Sequences: Auto-incrementing IDs for books, customers, and transactions.
Triggers: Automate tasks like ID generation and fine calculation.

📦 Modular Python Design
The project is organized into separate Python modules for maintainability:

database.py: Manages Oracle Database connectivity and queries.
book.py: Handles book-related operations.
customer.py: Manages customer-related operations.
transaction.py: Processes checkout and return transactions.
report.py: Generates static and dynamic reports.
main.py: Entry point and GUI launcher.

🖼️ Graphical User Interface

Framework: Tkinter for a responsive, user-friendly interface.
Components:
Tabbed layout for Book Management, Customer Management, Transaction Management, and Reports.
Forms for adding, editing, and searching records.
Treeview widgets for displaying tabular data.
Navigation buttons for record browsing.
Report generation and display.



Prerequisites
To run the project, ensure the following are installed:

Python 3.8+: Download from python.org.
oracledb Library: Install via pip install oracledb.
Tkinter: Usually included with Python; on Linux, install with sudo apt-get install python3-tk.
Oracle Instant Client: Download from Oracle's website and configure for your OS.
Oracle Database: Local or remote server (e.g., Oracle 19c, 21c, or Autonomous Database).

Setup Instructions

Install Dependencies:
pip install oracledb

For Linux, install Tkinter if needed:
sudo apt-get install python3-tk


Install Oracle Instant Client:

Download the Basic or Basic Light package from Oracle's website.
Extract to a directory (e.g., /opt/oracle/instantclient_21_6 on Linux or C:\oracle\instantclient_21_6 on Windows).
Add the directory to your environment variables:
Linux:export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_6:$LD_LIBRARY_PATH


Windows: Add to PATH in System Settings.


On Linux, install libaio:sudo apt-get install libaio1




Configure Oracle Database:

Ensure an Oracle Database server is running (local or remote).
Create a user for the project:CREATE USER library_user IDENTIFIED BY your_password;
GRANT CONNECT, RESOURCE, CREATE SESSION, CREATE TABLE, CREATE SEQUENCE, CREATE TRIGGER TO library_user;


Note the Service Name, Host, and Port (e.g., localhost:1521/ORCL).


Update Database Connection:

Open database.py and modify the connection details in the connect method:self.connection = oracledb.connect(
    user="library_user",
    password="your_password",
    dsn="localhost:1521/ORCL"
)


For Oracle Autonomous Database, include Wallet details:self.connection = oracledb.connect(
    user="library_user",
    password="your_password",
    dsn="your_service_name",
    config_dir="/path/to/wallet",
    wallet_location="/path/to/wallet",
    wallet_password="wallet_password"
)




Organize Project Files:

Ensure all project files (main.py, database.py, book.py, customer.py, transaction.py, report.py) are in the same directory.
Verify that main.py imports all modules:from database import Database
from book import Book
from customer import Customer
from transaction import Transaction
from report import Report




Run the Application:

Navigate to the project directory in a terminal.
Execute:python main.py


The Tkinter GUI should launch, allowing you to interact with the system.



Usage

Book Management:

Navigate to the "Book Management" tab.
Add, edit, or delete books using the input fields and buttons.
Search for books by entering a term in the search field.
Use navigation buttons to browse books.


Customer Management:

Go to the "Customer Management" tab.
Add, edit, or delete customers.
View customer transactions in the master-detail Treeview.
Navigate customer records using buttons.


Transaction Management:

In the "Transaction Management" tab, enter Book ID and Customer ID to check out a book.
To return a book, provide the Book ID and Transaction ID.
View all transactions in the Treeview.


Reports:

Access the "Reports" tab to generate:
Overdue Report: Lists books not returned by the due date.
Transaction History: Shows transactions within a specified date range (YYYY-MM-DD format).





Troubleshooting

Connection Error (ORA-12154): Verify the DSN, Service Name, Host, and Port. Check tnsnames.ora if using TNS aliases.
Library Error (Cannot load native library): Ensure Oracle Instant Client is installed and its path is in LD_LIBRARY_PATH (Linux) or PATH (Windows).
Permission Error: Confirm the database user has sufficient privileges (CREATE TABLE, CREATE SEQUENCE, CREATE TRIGGER).
GUI Issues: Check that Tkinter is installed and Python is running correctly.
Logs: Review library.log in the project directory for detailed error messages.

Contributing
To contribute to this project:

Fork the repository (if hosted on a platform like GitHub).
Create a feature branch (git checkout -b feature/new-feature).
Commit changes (git commit -m "Add new feature").
Push to the branch (git push origin feature/new-feature).
Submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or support, contact the project maintainer at [ mahmoud.shehta.khalil@gmail.com ] .

Generated on April 29, 2025
