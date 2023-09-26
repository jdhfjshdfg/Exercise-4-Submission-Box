import sqlite3

# Connect to database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create the Books table
c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID INTEGER PRIMARY KEY,
             Title TEXT NOT NULL,
             Author TEXT NOT NULL,
             ISBN TEXT NOT NULL,
             Status TEXT NOT NULL)''')

# Create the Users table
c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID INTEGER PRIMARY KEY,
             Name TEXT NOT NULL,
             Email TEXT NOT NULL)''')

# Create Reservations
c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID INTEGER PRIMARY KEY,
             BookID INTEGER NOT NULL,
             UserID INTEGER NOT NULL,
             ReservationDate DATE NOT NULL,
             FOREIGN KEY (BookID) REFERENCES Books(BookID),
             FOREIGN KEY (UserID) REFERENCES Users(UserID))''')

# Add new books to the database
def add_book():
    title = input("Book title：")
    author = input("Book author：")
    isbn = input("Book ISBN：")
    status = input("Book state：")
    c.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)",
              (title, author, isbn, status))
    conn.commit()
    print("Books have been added to the database。")

# Add user and reservation information to the database
def add_user_reservation():
    name = input("username：")
    email = input("User email：")
    c.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", (name, email))
    user_id = c.lastrowid
    book_id = int(input("The BookID of books："))
    reservation_date = input("Booking date：")
    c.execute("INSERT INTO Reservations (BookID, UserID, ReservationDate) VALUES (?, ?, ?)",
              (book_id, user_id, reservation_date))
    conn.commit()
    print("User and reservation information has been added to the database.")

# Find book details based on BookID
def find_book_details():
    book_id = int(input("The BookID of books："))
    c.execute('''SELECT Books.*, Users.UserID, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID = ?''', (book_id,))
    book_data = c.fetchone()
    if book_data:
        print("Book details：")
        print("BookID:", book_data[0])
        print("Title:", book_data[1])
        print("Author:", book_data[2])
        print("ISBN:", book_data[3])
        print("Status:", book_data[4])
        if book_data[5]:
            print("Booking Status: Booked")
            print("subscriber：")
            print("UserID:", book_data[5])
            print("Name:", book_data[6])
            print("Email:", book_data[7])
        else:
            print("Booking Status: No booking")
    else:
        print("The book does not exist in the database.")

# Find the reservation status of the book based on different input types
def find_reservation_status():
    input_text = input("Please enter BookID, Title, UserID, or ReservationID:")
    if input_text[:2] == 'LB':
        book_id = int(input_text[2:])
        c.execute('''SELECT Books.Title, Books.Status, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.BookID = ?''', (book_id,))
        reservation_data = c.fetchall()
        if reservation_data:
            print("Book reservation status:")
            for data in reservation_data:
                print("Title:", data[0])
                print("Status:", data[1])
                print("subscriber：")
                print("Name:", data[2])
                print("Email:", data[3])
                print("ReservationID:", data[4])
                print("ReservationDate:", data[5])
        else:
            print("The book does not exist in the database.")
    elif input_text[:2] == 'LU':
        user_id = int(input_text[2:])
        c.execute('''SELECT Books.Title, Books.Status, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                     FROM Users
                     JOIN Reservations ON Users.UserID = Reservations.UserID
                     JOIN Books ON Reservations.BookID = Books.BookID
                     WHERE Users.UserID = ?''', (user_id,))
        reservation_data = c.fetchall()
        if reservation_data:
            print("User's booking status:")
            for data in reservation_data:
                print("Title:", data[0])
                print("Status:", data[1])
                print("Name:", data[2])
                print("Email:", data[3])
                print("ReservationID:", data[4])
                print("ReservationDate:", data[5])
        else:
            print("The user did not order any books.")
    elif input_text[:2] == 'LR':
        reservation_id = int(input_text[2:])
        c.execute('''SELECT Books.Title, Books.Status, Users.Name, Users.Email, Reservations.ReservationDate
                     FROM Reservations
                     JOIN Users ON Reservations.UserID = Users.UserID
                     JOIN Books ON Reservations.BookID = Books.BookID
                     WHERE Reservations.ReservationID = ?''', (reservation_id,))
        reservation_data = c.fetchone()
        if reservation_data:
            print("Booking details:")
            print("Title:", reservation_data[0])
            print("Status:", reservation_data[1])
            print("Name:", reservation_data[2])
            print("Email:", reservation_data[3])
            print("ReservationDate:", reservation_data[4])
        else:
            print("The reservation does not exist in the database.")
    else:
        title = input_text
        c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.Title = ?''', (title,))
        reservation_data = c.fetchall()
        if reservation_data:
            print("Book reservation status:")
            for data in reservation_data:
                print("BookID:", data[0])
                print("Title:", data[1])
                print("Status:", data[2])
                print("Booking user:")
                print("Name:", data[3])
                print("Email:", data[4])
                print("ReservationID:", data[5])
                print("ReservationDate:", data[6])
        else:
            print("The book does not exist in the database.")
    #Find all the books in the database

def find_all_books():
        c.execute('''SELECT Books.Title, Books.Status,
                        Reservations.ReservationID, Reservations.ReservationDate,
                        Users.Name, Users.Email
                        FROM Books
                        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                        LEFT JOIN Users ON Reservations.UserID = Users.UserID''')

        result = c.fetchall()
        if result:
            print("All books:")
            for row in result:
                print("Title:", row[0])
                print("Status:", row[1])
                print("ReservationID:", row[2])
                print("ReservationDate:", row[3])
                print("UserName:", row[4])
                print("Email:", row[5])
        else:
            print("No books found.")


# Modify the book details according to BookID
def update_book_details():
    book_id = int(input("BookID of books to be modified:"))
    new_status = input("New book status：")
    c.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
    conn.commit()
    print("Book details have been updated.")

# Delete a book according to BookID
def delete_book():
    book_id = int(input("To delete the book BookID："))
    c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Books have been removed from the database.")

# Interactive interface
def interactive_menu():
    while True:
        print("\nLibrary management system")
        print("Please select operation：")
        print("1. Add new book ")
        print("2. Add user and reservation information")
        print("3. Find book details based on BookID")
        print("4. Find the reservation status of the book based on BookID, Title, UserID, or ReservationID")
        print("5. Find all books in the database")
        print("6. Modify the book details according to BookID")
        print("7. Delete a book according to BookID")
        print("8. quit")

        choice = input("Please enter options:")
        if choice == "1":
            add_book()
        elif choice == "2":
            add_user_reservation()
        elif choice == "3":
            find_book_details()
        elif choice == "4":
            find_reservation_status()
        elif choice == "5":
            find_all_books()
        elif choice == "6":
            update_book_details()
        elif choice == "7":
            delete_book()
        elif choice == "8":
            break
        else:
            print("Invalid option, please select again.")

# Run interactive interface
interactive_menu()

# Close database connection
conn.close()