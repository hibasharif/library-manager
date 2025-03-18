import json
import os
import webbrowser  # Import the webbrowser module

class Book:
    def __init__(self, title, author, publication_year, genre, read_status):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.read_status = read_status

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "genre": self.genre,
            "read_status": self.read_status
        }

    @staticmethod
    def from_dict(data):
        return Book(data['title'], data['author'], data['publication_year'], data['genre'], data['read_status'])

class LibraryManager:
    def __init__(self):
        self.library = []
        self.load_library()

    def load_library(self):
        if os.path.exists('library.txt'):
            with open('library.txt', 'r') as file:
                data = file.readlines()
                for line in data:
                    title, author, year, genre, read_status = line.strip().split('|')
                    self.library.append(Book(title, author, int(year), genre, read_status == 'True'))

    def save_library(self):
        with open('library.txt', 'w') as file:
            for book in self.library:
                file.write(f"{book.title}|{book.author}|{book.publication_year}|{book.genre}|{book.read_status}\n")

    def add_book(self, title, author, publication_year, genre, read_status):
        self.library.append(Book(title, author, publication_year, genre, read_status))
        self.save_library()

    def remove_book(self, title):
        self.library = [book for book in self.library if book.title.lower() != title.lower()]
        self.save_library()

    def edit_book(self, old_title, new_title, new_author, new_publication_year, new_genre, new_read_status):
        for book in self.library:
            if book.title.lower() == old_title.lower():
                book.title = new_title
                book.author = new_author
                book.publication_year = new_publication_year
                book.genre = new_genre
                book.read_status = new_read_status
                break
        self.save_library()

    def search_books(self, search_term):
        return [book for book in self.library if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower()]

    def display_all_books(self):
        if not self.library:
            print("No books in the library.")
        else:
            for book in self.library:
                print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}, Genre: {book.genre}, Read: {'Yes' if book.read_status else 'No'}")

    def display_statistics(self):
        total_books = len(self.library)
        read_count = sum(book.read_status for book in self.library)
        percentage_read = (read_count / total_books * 100) if total_books > 0 else 0
        print(f"Total books: {total_books}")
        print(f"Percentage read: {percentage_read:.2f}%")

    def download_book(self, title):
        # Open a Google search for the book title
        search_url = f"https://www.google.com/search?q={title.replace(' ', '+')}"
        webbrowser.open(search_url)
        print(f"Searching for '{title}' on Google...")

def main():
    manager = LibraryManager()
    while True:
        print("\nWelcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Edit a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Display statistics")
        print("7. Download a book")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter the book title: ")
            author = input("Enter the author: ")
            publication_year = int(input("Enter the publication year: "))
            genre = input("Enter the genre: ")
            read_status = input("Have you read this book? (yes/no): ").lower() == 'yes'
            manager.add_book(title, author, publication_year, genre, read_status)
            print("Book added successfully!")

        elif choice == '2':
            title = input("Enter the title of the book to remove: ")
            manager.remove_book(title)
            print("Book removed successfully!")

        elif choice == '3':
            old_title = input("Enter the title of the book to edit: ")
            new_title = input("Enter the new title: ")
            new_author = input("Enter the new author: ")
            new_publication_year = int(input("Enter the new publication year: "))
            new_genre = input("Enter the new genre: ")
            new_read_status = input("Have you read this book? (yes/no): ").lower() == 'yes'
            manager.edit_book(old_title, new_title, new_author, new_publication_year, new_genre, new_read_status)
            print("Book edited successfully!")

        elif choice == '4':
            search_term = input("Enter the title or author to search for: ")
            results = manager.search_books(search_term)
            if results:
                print("Search results:")
                for book in results:
                    print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}, Genre: {book.genre}, Read: {'Yes' if book.read_status else 'No'}")
            else:
                print("No books found.")

        elif choice == '5':
            manager.display_all_books()

        elif choice == '6':
            manager.display_statistics()

        elif choice == '7':
            title = input("Enter the title of the book to download: ")
            manager.download_book(title)

        elif choice == '8':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()