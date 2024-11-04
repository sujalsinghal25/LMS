import os
import csv

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

class Library:
    def __init__(self, book_file, issued_books_file):
        self.book_file = book_file
        self.issued_books_file = issued_books_file
        self.books = []
        self.issued_books = []
        self.load_books()
        self.load_issued_books()

    def load_books(self):
        if os.path.exists(self.book_file):
            with open(self.book_file, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                self.books = [Book(row[0], row[1]) for row in reader]

    def load_issued_books(self):
        if os.path.exists(self.issued_books_file):
            with open(self.issued_books_file, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                self.issued_books = [row for row in reader]

    def add_book(self, title, author):
        self.books.append(Book(title, author))
        self.save_books()

    def save_books(self):
        with open(self.book_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Author'])
            for book in self.books:
                writer.writerow([book.title, book.author])

    def display_books(self):
        print("Books available in the library:")
        for book in self.books:
            print(f"Title: {book.title}, Author: {book.author}")

    def search_book(self, title):
        for book in self.books:
            if book.title == title:
                print(f"Book found - Title: {book.title}, Author: {book.author}")
                return
        print("Book not found.")

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]
        self.save_books()
        print("Book removed successfully.")

    def issue_book(self, username, title):
        for book in self.books:
            if book.title == title:
                self.issued_books.append([username, title])
                self.save_issued_books()
                print("Book issued successfully.")
                return
        print("Book not found in the library.")

    def save_issued_books(self):
        with open(self.issued_books_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Title'])
            for issued_book in self.issued_books:
                writer.writerow(issued_book)

    def return_book(self, username, title):
        self.issued_books = [issued_book for issued_book in self.issued_books if issued_book != [username, title]]
        self.save_issued_books()
        print("Book returned successfully.")

    def issued_book_report(self, username):
        print(f"Issued books report for {username}:")
        for issued_book in self.issued_books:
            if issued_book[0] == username:
                print(f"Title: {issued_book[1]}")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def view_student_information(self, users):
        print("Registered Students:")
        for username, user in users.items():
            if isinstance(user, Student):
                print(f"Username: {username}, Password: {user.password}")

class Student(User):
    def __init__(self, username, password):
        super().__init__(username, password)

def load_user_credentials(file_name):
    users = {}
    if os.path.exists(file_name):
        with open(file_name, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                user_type, username, password = row
                if user_type == 'admin':
                    users[username] = Admin(username, password)
                elif user_type == 'student':
                    users[username] = Student(username, password)
    return users

def save_user_credentials(file_name, users):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['User Type', 'Username', 'Password'])
        for username, user in users.items():
            writer.writerow(['admin' if isinstance(user, Admin) else 'student', username, user.password])

def admin_menu(library, admin):
    while True:
        print("\nAdmin Menu:")
        print("1. Add a Book")
        print("2. Display all Books")
        print("3. Remove a Book")
        print("4. View Student Information")
        print("5. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            library.add_book(title, author)
        elif choice == '2':
            library.display_books()
        elif choice == '3':
            title = input("Enter the title of the book you want to remove: ")
            library.remove_book(title)
        elif choice == '4':
            admin.view_student_information(User)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def student_menu(library, username):
    while True:
        print("\nStudent Menu:")
        print("1. Display all Books")
        print("2. Search for a Book")
        print("3. Issue a Book")
        print("4. Return a Book")
        print("5. Issued Books Report")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            library.display_books()
        elif choice == '2':
            title = input("Enter the title of the book you want to search for: ")
            library.search_book(title)
        elif choice == '3':
            title = input("Enter the title of the book you want to issue: ")
            library.issue_book(username, title)
        elif choice == '4':
            title = input("Enter the title of the book you want to return: ")
            library.return_book(username, title)
        elif choice == '5':
            library.issued_book_report(username)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def login_menu(users):
    print("\nWelcome to the Library Management System")
    while True:
        login_option = input("Are you an admin, a student, or do you want to register? (admin/student/register): ").lower()
        if login_option in ['admin', 'student']: 
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username in users and users[username].password == password:
                print(f"Welcome, {username}!")
                return login_option, username
            else:
                print("Invalid username or password. Please try again.")
        elif login_option == 'register':
            user_type = input("Do you want to register as an admin or a student? (admin/student): ").lower()
            if user_type in ['admin', 'student']:  
                new_username = input(f"Enter your new {user_type} username: ")
                if new_username not in users:
                    new_password = input("Enter your new password: ")
                    users[new_username] = Admin(new_username, new_password) if user_type == 'admin' else Student(new_username, new_password)
                    print(f"{user_type.capitalize()} registration successful!")
                else:
                    print("Username already exists. Please choose another username.")
            else:
                print("Invalid option. Please enter 'admin' or 'student'.")
        else:
            print("Invalid option. Please enter 'admin', 'student', or 'register'.")

def main():
    library = Library("library.csv", "issued_books.csv")
    users = load_user_credentials("user_credentials.csv")

    user_type, username = login_menu(users)

    if user_type == 'admin':
        admin_menu(library, users[username])
    elif user_type == 'student':
        student_menu(library, username)

    save_user_credentials("user_credentials.csv", users)

if __name__ == "__main__":
    main()
