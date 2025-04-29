# File: main.py
# Purpose: Entry point of the application and GUI launcher
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import logging

# Assuming other modules (database.py, book.py, customer.py, transaction.py, report.py) are available
from database import Database
from book import Book
from customer import Customer
from transaction import Transaction
from report import Report

# Configure logging for error tracking
logging.basicConfig(level=logging.INFO, filename='library.log')


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.db = Database()
        self.book_manager = Book(self.db)
        self.customer_manager = Customer(self.db)
        self.transaction_manager = Transaction(self.db)
        self.report_manager = Report(self.db)
        self.current_customer_index = 0
        self.customers = []
        self.current_book_index = 0
        self.books = []

        # Setup database tables and triggers
        try:
            self.db.setup_database()
        except oracledb.Error as e:
            messagebox.showerror("Error", f"Failed to setup database: {e}")
            self.root.quit()

        # Create main GUI components
        self.create_widgets()

    def create_widgets(self):
        """Creates the main GUI layout with tabs."""
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True)

        # Book Management Tab
        book_frame = ttk.Frame(notebook)
        notebook.add(book_frame, text="Book Management")
        self.create_book_widgets(book_frame)

        # Customer Management Tab
        customer_frame = ttk.Frame(notebook)
        notebook.add(customer_frame, text="Customer Management")
        self.create_customer_widgets(customer_frame)

        # Transaction Management Tab
        transaction_frame = ttk.Frame(notebook)
        notebook.add(transaction_frame, text="Transaction Management")
        self.create_transaction_widgets(transaction_frame)

        # Reports Tab
        report_frame = ttk.Frame(notebook)
        notebook.add(report_frame, text="Reports")
        self.create_report_widgets(report_frame)

    def create_book_widgets(self, frame):
        """Creates widgets for book management."""
        # Input fields for book details
        tk.Label(frame, text="Title").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.book_title = tk.Entry(frame)
        self.book_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Author").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.book_author = tk.Entry(frame)
        self.book_author.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Genre").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.book_genre = ttk.Combobox(frame, values=["Fiction", "Non-Fiction", "Science", "History"])
        self.book_genre.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="ISBN").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.book_isbn = tk.Entry(frame)
        self.book_isbn.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Availability").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.book_available = tk.BooleanVar()
        tk.Checkbutton(frame, variable=self.book_available).grid(row=4, column=1, padx=5, pady=5)

        # Search field
        tk.Label(frame, text="Search").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.book_search = tk.Entry(frame)
        self.book_search.grid(row=5, column=1, padx=5, pady=5)
        tk.Button(frame, text="Search", command=self.search_books).grid(row=5, column=2, padx=5, pady=5)

        # CRUD buttons
        tk.Button(frame, text="Add Book", command=self.add_book).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(frame, text="Update Book", command=self.update_book).grid(row=6, column=1, padx=5, pady=5)
        tk.Button(frame, text="Delete Book", command=self.delete_book).grid(row=6, column=2, padx=5, pady=5)

        # Navigation buttons
        tk.Button(frame, text="First", command=self.first_book).grid(row=7, column=0, padx=5, pady=5)
        tk.Button(frame, text="Previous", command=self.prev_book).grid(row=7, column=1, padx=5, pady=5)
        tk.Button(frame, text="Next", command=self.next_book).grid(row=7, column=2, padx=5, pady=5)
        tk.Button(frame, text="Last", command=self.last_book).grid(row=7, column=3, padx=5, pady=5)

        # Treeview for displaying books
        self.book_tree = ttk.Treeview(frame, columns=("ID", "Title", "Author", "Genre", "ISBN", "Available"),
                                      show="headings")
        self.book_tree.heading("ID", text="Book ID")
        self.book_tree.heading("Title", text="Title")
        self.book_tree.heading("Author", text="Author")
        self.book_tree.heading("Genre", text="Genre")
        self.book_tree.heading("ISBN", text="ISBN")
        self.book_tree.heading("Available", text="Available")
        self.book_tree.grid(row=8, column=0, columnspan=4, padx=5, pady=5)
        self.book_tree.bind("<<TreeviewSelect>>", self.load_selected_book)

        # Load initial book data
        self.load_books()

    def create_customer_widgets(self, frame):
        """Creates widgets for customer management with master-detail form."""
        # Input fields for customer details
        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.customer_name = tk.Entry(frame)
        self.customer_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.customer_email = tk.Entry(frame)
        self.customer_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Membership").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.customer_membership = ttk.Combobox(frame, values=["Active", "Inactive", "Suspended"])
        self.customer_membership.grid(row=2, column=1, padx=5, pady=5)

        # CRUD buttons
        tk.Button(frame, text="Add Customer", command=self.add_customer).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(frame, text="Update Customer", command=self.update_customer).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(frame, text="Delete Customer", command=self.delete_customer).grid(row=3, column=2, padx=5, pady=5)

        # Navigation buttons
        tk.Button(frame, text="First", command=self.first_customer).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(frame, text="Previous", command=self.prev_customer).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(frame, text="Next", command=self.next_customer).grid(row=4, column=2, padx=5, pady=5)
        tk.Button(frame, text="Last", command=self.last_customer).grid(row=4, column=3, padx=5, pady=5)

        # Treeview for displaying customers
        self.customer_tree = ttk.Treeview(frame, columns=("ID", "Name", "Email", "Membership"), show="headings")
        self.customer_tree.heading("ID", text="Customer ID")
        self.customer_tree.heading("Name", text="Name")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.heading("Membership", text="Membership")
        self.customer_tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
        self.customer_tree.bind("<<TreeviewSelect>>", self.load_selected_customer)

        # Treeview for displaying customer transactions (master-detail)
        self.customer_transactions_tree = ttk.Treeview(frame, columns=("ID", "Book Title", "Checkout", "Due", "Return",
                                                                       "Fine"), show="headings")
        self.customer_transactions_tree.heading("ID", text="Transaction ID")
        self.customer_transactions_tree.heading("Book Title", text="Book Title")
        self.customer_transactions_tree.heading("Checkout", text="Checkout Date")
        self.customer_transactions_tree.heading("Due", text="Due Date")
        self.customer_transactions_tree.heading("Return", text="Return Date")
        self.customer_transactions_tree.heading("Fine", text="Fine")
        self.customer_transactions_tree.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

        # Load initial customer data
        self.load_customers()

    def create_transaction_widgets(self, frame):
        """Creates widgets for transaction management."""
        # Input fields for transactions
        tk.Label(frame, text="Book ID").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.transaction_book_id = tk.Entry(frame)
        self.transaction_book_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Customer ID").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.transaction_customer_id = tk.Entry(frame)
        self.transaction_customer_id.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Transaction ID (for return)").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.transaction_id = tk.Entry(frame)
        self.transaction_id.grid(row=2, column=1, padx=5, pady=5)

        # Transaction buttons
        tk.Button(frame, text="Checkout Book", command=self.checkout_book).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(frame, text="Return Book", command=self.return_book).grid(row=3, column=1, padx=5, pady=5)

        # Treeview for displaying transactions
        self.transaction_tree = ttk.Treeview(frame,
                                             columns=("ID", "Book Title", "Customer", "Checkout", "Due", "Return",
                                                      "Fine"), show="headings")
        self.transaction_tree.heading("ID", text="Transaction ID")
        self.transaction_tree.heading("Book Title", text="Book Title")
        self.transaction_tree.heading("Customer", text="Customer Name")
        self.transaction_tree.heading("Checkout", text="Checkout Date")
        self.transaction_tree.heading("Due", text="Due Date")
        self.transaction_tree.heading("Return", text="Return Date")
        self.transaction_tree.heading("Fine", text="Fine")
        self.transaction_tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

        # Load initial transaction data
        self.load_transactions()

    def create_report_widgets(self, frame):
        """Creates widgets for report generation."""
        # Static report button
        tk.Button(frame, text="Generate Overdue Report", command=self.show_overdue_report).grid(row=0, column=0, padx=5,
                                                                                                pady=5)

        # Dynamic report input
        tk.Label(frame, text="Start Date (YYYY-MM-DD)").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.report_start_date = tk.Entry(frame)
        self.report_start_date.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="End Date (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.report_end_date = tk.Entry(frame)
        self.report_end_date.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Generate Transaction History", command=self.show_transaction_history).grid(row=3,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          padx=5,
                                                                                                          pady=5)

        # Treeview for displaying reports
        self.report_tree = ttk.Treeview(frame, columns=("ID", "Book Title", "Customer", "Details"), show="headings")
        self.report_tree.heading("ID", text="ID")
        self.report_tree.heading("Book Title", text="Book Title")
        self.report_tree.heading("Customer", text="Customer")
        self.report_tree.heading("Details", text="Details")
        self.report_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Book Management Methods
    def load_books(self):
        """Loads all books into the treeview."""
        self.books = self.book_manager.search_books("")
        self.book_tree.delete(*self.book_tree.get_children())
        for book in self.books:
            self.book_tree.insert("", "end", values=book)
        if self.books:
            self.current_book_index = 0
            self.display_book()

    def search_books(self):
        """Searches books based on user input."""
        search_term = self.book_search.get()
        self.books = self.book_manager.search_books(search_term)
        self.book_tree.delete(*self.book_tree.get_children())
        for book in self.books:
            self.book_tree.insert("", "end", values=book)
        self.current_book_index = 0
        self.display_book()

    def add_book(self):
        """Adds a new book."""
        title = self.book_title.get()
        author = self.book_author.get()
        genre = self.book_genre.get()
        isbn = self.book_isbn.get()
        if not all([title, author, genre, isbn]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if self.book_manager.add_book(title, author, genre, isbn):
            messagebox.showinfo("Success", "Book added successfully!")
            self.load_books()
            self.clear_book_fields()
        else:
            messagebox.showerror("Error", "Failed to add book.")

    def update_book(self):
        """Updates the selected book."""
        if not self.books or self.current_book_index >= len(self.books):
            messagebox.showerror("Error", "No book selected!")
            return
        book_id = self.books[self.current_book_index][0]
        title = self.book_title.get()
        author = self.book_author.get()
        genre = self.book_genre.get()
        isbn = self.book_isbn.get()
        is_available = 1 if self.book_available.get() else 0
        if not all([title, author, genre, isbn]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if self.book_manager.update_book(book_id, title, author, genre, isbn, is_available):
            messagebox.showinfo("Success", "Book updated successfully!")
            self.load_books()
        else:
            messagebox.showerror("Error", "Failed to update book.")

    def delete_book(self):
        """Deletes the selected book."""
        if not self.books or self.current_book_index >= len(self.books):
            messagebox.showerror("Error", "No book selected!")
            return
        book_id = self.books[self.current_book_index][0]
        if self.book_manager.delete_book(book_id):
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.load_books()
        else:
            messagebox.showerror("Error", "Failed to delete book.")

    def load_selected_book(self, event):
        """Loads the selected book into input fields."""
        selected = self.book_tree.selection()
        if not selected:
            return
        item = self.book_tree.item(selected[0])
        book_id = item["values"][0]
        for i, book in enumerate(self.books):
            if book[0] == book_id:
                self.current_book_index = i
                self.display_book()
                break

    def display_book(self):
        """Displays the current book in input fields."""
        if not self.books or self.current_book_index >= len(self.books):
            return
        book = self.books[self.current_book_index]
        self.book_title.delete(0, tk.END)
        self.book_title.insert(0, book[1])
        self.book_author.delete(0, tk.END)
        self.book_author.insert(0, book[2])
        self.book_genre.set(book[3])
        self.book_isbn.delete(0, tk.END)
        self.book_isbn.insert(0, book[4])
        self.book_available.set(bool(book[5]))

    def clear_book_fields(self):
        """Clears book input fields."""
        self.book_title.delete(0, tk.END)
        self.book_author.delete(0, tk.END)
        self.book_genre.set("")
        self.book_isbn.delete(0, tk.END)
        self.book_available.set(False)

    def first_book(self):
        """Navigates to the first book."""
        self.current_book_index = 0
        self.display_book()

    def prev_book(self):
        """Navigates to the previous book."""
        if self.current_book_index > 0:
            self.current_book_index -= 1
            self.display_book()

    def next_book(self):
        """Navigates to the next book."""
        if self.current_book_index < len(self.books) - 1:
            self.current_book_index += 1
            self.display_book()

    def last_book(self):
        """Navigates to the last book."""
        self.current_book_index = len(self.books) - 1
        self.display_book()

    # Customer Management Methods
    def load_customers(self):
        """Loads all customers into the treeview."""
        self.customers = self.db.execute_query("SELECT customer_id, name, email, membership_status FROM customers",
                                               fetch=True)
        self.customer_tree.delete(*self.customer_tree.get_children())
        for customer in self.customers:
            self.customer_tree.insert("", "end", values=customer)
        if self.customers:
            self.current_customer_index = 0
            self.display_customer()

    def add_customer(self):
        """Adds a new customer."""
        name = self.customer_name.get()
        email = self.customer_email.get()
        membership = self.customer_membership.get()
        if not all([name, email, membership]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if self.customer_manager.add_customer(name, email, membership):
            messagebox.showinfo("Success", "Customer added successfully!")
            self.load_customers()
            self.clear_customer_fields()
        else:
            messagebox.showerror("Error", "Failed to add customer.")

    def update_customer(self):
        """Updates the selected customer."""
        if not self.customers or self.current_customer_index >= len(self.customers):
            messagebox.showerror("Error", "No customer selected!")
            return
        customer_id = self.customers[self.current_customer_index][0]
        name = self.customer_name.get()
        email = self.customer_email.get()
        membership = self.customer_membership.get()
        if not all([name, email, membership]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if self.customer_manager.update_customer(customer_id, name, email, membership):
            messagebox.showinfo("Success", "Customer updated successfully!")
            self.load_customers()
        else:
            messagebox.showerror("Error", "Failed to update customer.")

    def delete_customer(self):
        """Deletes the selected customer."""
        if not self.customers or self.current_customer_index >= len(self.customers):
            messagebox.showerror("Error", "No customer selected!")
            return
        customer_id = self.customers[self.current_customer_index][0]
        if self.customer_manager.delete_customer(customer_id):
            messagebox.showinfo("Success", "Customer deleted successfully!")
            self.load_customers()
        else:
            messagebox.showerror("Error", "Failed to delete customer.")

    def load_selected_customer(self, event):
        """Loads the selected customer into input fields and their transactions."""
        selected = self.customer_tree.selection()
        if not selected:
            return
        item = self.customer_tree.item(selected[0])
        customer_id = item["values"][0]
        for i, customer in enumerate(self.customers):
            if customer[0] == customer_id:
                self.current_customer_index = i
                self.display_customer()
                self.load_customer_transactions(customer_id)
                break

    def display_customer(self):
        """Displays the current customer in input fields."""
        if not self.customers or self.current_customer_index >= len(self.customers):
            return
        customer = self.customers[self.current_customer_index]
        self.customer_name.delete(0, tk.END)
        self.customer_name.insert(0, customer[1])
        self.customer_email.delete(0, tk.END)
        self.customer_email.insert(0, customer[2])
        self.customer_membership.set(customer[3])

    def clear_customer_fields(self):
        """Clears customer input fields."""
        self.customer_name.delete(0, tk.END)
        self.customer_email.delete(0, tk.END)
        self.customer_membership.set("")

    def first_customer(self):
        """Navigates to the first customer."""
        self.current_customer_index = 0
        self.display_customer()
        self.load_customer_transactions(self.customers[self.current_customer_index][0])

    def prev_customer(self):
        """Navigates to the previous customer."""
        if self.current_customer_index > 0:
            self.current_customer_index -= 1
            self.display_customer()
            self.load_customer_transactions(self.customers[self.current_customer_index][0])

    def next_customer(self):
        """Navigates to the next customer."""
        if self.current_customer_index < len(self.customers) - 1:
            self.current_customer_index += 1
            self.display_customer()
            self.load_customer_transactions(self.customers[self.current_customer_index][0])

    def last_customer(self):
        """Navigates to the last customer."""
        self.current_customer_index = len(self.customers) - 1
        self.display_customer()
        self.load_customer_transactions(self.customers[self.current_customer_index][0])

    def load_customer_transactions(self, customer_id):
        """Loads transactions for the selected customer."""
        transactions = self.transaction_manager.get_transactions_by_customer(customer_id)
        self.customer_transactions_tree.delete(*self.customer_transactions_tree.get_children())
        for transaction in transactions:
            self.customer_transactions_tree.insert("", "end", values=transaction)

    # Transaction Management Methods
    def load_transactions(self):
        """Loads all transactions into the treeview."""
        transactions = self.db.execute_query("""
            SELECT t.transaction_id, b.title, c.name, t.checkout_date, t.due_date, t.return_date, t.fine
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN customers c ON t.customer_id = c.customer_id
        """, fetch=True)
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        for transaction in transactions:
            self.transaction_tree.insert("", "end", values=transaction)

    def checkout_book(self):
        """Checks out a book to a customer."""
        book_id = self.transaction_book_id.get()
        customer_id = self.transaction_customer_id.get()
        if not all([book_id, customer_id]):
            messagebox.showerror("Error", "Book ID and Customer ID are required!")
            return
        try:
            book_id = int(book_id)
            customer_id = int(customer_id)
            if self.transaction_manager.checkout_book(book_id, customer_id):
                messagebox.showinfo("Success", "Book checked out successfully!")
                self.load_transactions()
                self.transaction_book_id.delete(0, tk.END)
                self.transaction_customer_id.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to check out book.")
        except ValueError:
            messagebox.showerror("Error", "Invalid Book ID or Customer ID!")

    def return_book(self):
        """Returns a book to the library."""
        book_id = self.transaction_book_id.get()
        transaction_id = self.transaction_id.get()
        if not all([book_id, transaction_id]):
            messagebox.showerror("Error", "Book ID and Transaction ID are required!")
            return
        try:
            book_id = int(book_id)
            transaction_id = int(transaction_id)
            if self.transaction_manager.return_book(book_id, transaction_id):
                messagebox.showinfo("Success", "Book returned successfully!")
                self.load_transactions()
                self.transaction_book_id.delete(0, tk.END)
                self.transaction_id.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to return book.")
        except ValueError:
            messagebox.showerror("Error", "Invalid Book ID or Transaction ID!")

    # Report Generation Methods
    def show_overdue_report(self):
        """Displays the overdue books report."""
        report = self.report_manager.generate_overdue_report()
        self.report_tree.delete(*self.report_tree.get_children())
        for row in report:
            self.report_tree.insert("", "end", values=(row[0], row[1], row[2], f"Due: {row[3]}, Fine: {row[4]}"))

    def show_transaction_history(self):
        """Displays the transaction history report for a date range."""
        start_date = self.report_start_date.get()
        end_date = self.report_end_date.get()
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
            return
        report = self.report_manager.generate_transaction_history(start_date, end_date)
        self.report_tree.delete(*self.report_tree.get_children())
        for row in report:
            self.report_tree.insert("", "end", values=(row[0], row[1], row[2], f"Checkout: {row[3]}, Return: {row[4]}"))


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()