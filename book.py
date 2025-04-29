# File: book.py
# Purpose: Handles book-related logic

class Book:
    def __init__(self, db):
        self.db = db

    def add_book(self, title, author, genre, isbn):
        """Adds a new book to the database."""
        query = """
            INSERT INTO books (title, author # File: book.py (continued)
            author, genre, isbn) 
            VALUES (:1, :2, :3, :4)
        """
        try:
            self.db.execute_query(query, [title, author, genre, isbn])
            return True
        except oracledb.Error as e:
            logging.error(f"Error adding book: {e}")
            return False

    def update_book(self, book_id, title, author, genre, isbn, is_available):
        """Updates book details."""
        query = """
            UPDATE books 
            SET title = :1, author = :2, genre = :3, isbn = :4, is_available = :5
            WHERE book_id = :6
        """
        try:
            self.db.execute_query(query, [title, author, genre, isbn, is_available, book_id])
            return True
        except oracledb.Error as e:
            logging.error(f"Error updating book: {e}")
            return False

    def delete_book(self, book_id):
        """Deletes a book from the database."""
        query = "DELETE FROM books WHERE book_id = :1"
        try:
            self.db.execute_query(query, [book_id])
            return True
        except oracledb.Error as e:
            logging.error(f"Error deleting book: {e}")
            return False

    def search_books(self, search_term):
        """Searches books by title, author, genre, or ISBN."""
        query = """
            SELECT book_id, title, author, genre, isbn, is_available
            FROM books
            WHERE LOWER(title) LIKE LOWER(:1)
            OR LOWER(author) LIKE LOWER(:1)
            OR LOWER(genre) LIKE LOWER(:1)
            OR isbn LIKE :1
        """
        try:
            return self.db.execute_query(query, ['%' + search_term + '%'], fetch=True)
        except oracledb.Error as e:
            logging.error(f"Error searching books: {e}")
            return []
