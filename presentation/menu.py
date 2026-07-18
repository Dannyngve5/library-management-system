from services.library_service import LibraryService
from services.user_service import UserService
from services.loan_service import LoanService
from exceptions.book_exceptions import BookNotFoundException, DuplicateIsbnException
from exceptions.user_exceptions import UserNotFoundException
from exceptions.copy_exceptions import NoAvailableCopiesException
from exceptions.loan_exceptions import LoanLimitExceededException


class Menu:

    def __init__(
        self,
        library_service: LibraryService,
        user_service: UserService,
        loan_service: LoanService,
    ):
        self.library_service = library_service
        self.user_service = user_service
        self.loan_service = loan_service

    def show(self):
        while True:
            print("Options Menu:")
            print("1. Register a book")
            print("2. Register an user")
            print("3. Review available books")
            print("4. Loan request")  #
            print("5. Return a book")  #
            print("6. Review user by ID")
            print("7. Review loan history")  #
            print("8. Delete a book")
            print("9. Register a copy")
            print("10. Review users")
            print("11. Review users by role")
            print("12. Review books")
            print("13. Find book by ISBN")
            print("14. Update a book")

            print("15. Exit")

            opcion = input("Enter an option: ")

            if opcion == "1":
                isbn = input("ISBN: ")
                title = input("Title: ")
                author = input("Author: ")
                try:
                    self.library_service.add_book(isbn, title, author, 1)
                    print("Book added succesfully")
                except ValueError as e:
                    print(e)
                except DuplicateIsbnException as e:
                    print(e)
            elif opcion == "2":
                name = input("Name: ")
                role = input("Role: ")
                try:
                    self.user_service.add_user(name, role)
                    print("User added succesfully")
                except ValueError as e:
                    print(e)
            elif opcion == "3":
                books = self.library_service.find_books_with_available_copies()
                for book in books:
                    print(book)
            elif opcion == "4":
                book_id = int(input("Enter the book ID: "))
                user_id = int(input("Enter the user ID: "))

                try:
                    self.loan_service.loan_book(book_id, user_id)
                    print("Loan completed succesfully")
                except UserNotFoundException as e:
                    print(e)
                except LoanLimitExceededException as e:
                    print(e)
                except NoAvailableCopiesException as e:
                    print(e)
                except BookNotFoundException as e:
                    print(e)

            elif opcion == "5":
                pass
            elif opcion == "6":
                try:
                    user_id = int(input("Enter the user id: "))
                    user = self.user_service.find_by_id(user_id)
                    print(user)
                except ValueError:
                    print("Please enter a valid number")
                except UserNotFoundException as e:
                    print(e)
            elif opcion == "7":
                pass
            elif opcion == "8":
                try:
                    book_id = int(input("Enter the book id: "))
                    self.library_service.delete_book(book_id)
                    print("Book deleted succesfully")
                except ValueError:
                    print("Please enter a valid number")
                except BookNotFoundException as e:
                    print(e)

            elif opcion == "9":
                try:
                    book_id = int(input("Enter book ID: "))
                    copies = int(input("Enter the number of copies to add: "))
                    self.library_service.add_copies(book_id, copies)
                    print("Copy added succesfully")
                except ValueError:
                    print("Please enter a valid number")
                except BookNotFoundException as e:
                    print(e)
            elif opcion == "10":
                users = self.user_service.find_all()
                for user in users:
                    print(user)
            elif opcion == "11":
                try:
                    role = input("Select the role: ")
                    users = self.user_service.find_by_role(role)
                    for user in users:
                        print(user)
                except ValueError as e:
                    print(e)
            elif opcion == "12":
                books = self.library_service.find_all()
                for book in books:
                    print(book)
            elif opcion == "13":
                isbn = input("Enter the ISBN: ")
                book = self.library_service.find_by_isbn(isbn)
                if book is None:
                    print("Book not found")
                else:
                    print(book)
            elif opcion == "14":
                try:
                    book_id = int(input("Enter the book ID: "))
                except ValueError:
                    print("Please enter a valid number")
                    continue

                book = self.library_service.find_by_id(book_id)

                if book is None:
                    print(f"Book with ID {book_id} not found")
                else:
                    isbn = input(f"ISBN [{book.isbn}]: ").strip()
                    if not isbn:
                        isbn = book.isbn

                    title = input(f"Title [{book.title}]: ").strip()
                    if not title:
                        title = book.title

                    author = input(f"Author [{book.author}]: ").strip()
                    if not author:
                        author = book.author

                    try:
                        self.library_service.update(book.book_id, isbn, title, author)
                        print("Book updated succesfully")
                    except BookNotFoundException as e:
                        print(e)
            elif opcion == "15":
                print("Saliendo del menú.")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
