from application.services.library_service import LibraryService
from application.services.user_service import UserService
from application.services.loan_service import LoanService
from domain.exceptions.book_exceptions import (
    BookNotFoundException,
    DuplicateIsbnException,
)
from domain.exceptions.user_exceptions import (
    UserNotFoundException,
    UserHasLoansException,
)
from domain.exceptions.copy_exceptions import (
    NoAvailableCopiesException,
    CopyNotFoundException,
)
from domain.exceptions.loan_exceptions import (
    LoanLimitExceededException,
    NoActiveLoanException,
    LoanNotFoundException,
)


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
            print("1. Register a book")
            print("2. Register a user")
            print("3. Review available books")
            print("4. Loan request")
            print("5. Return a book")
            print("6. Review user by ID")
            print("7. Review loan by ID")
            print("8. Delete a book")
            print("9. Register copies")
            print("10. Review users")
            print("11. Review users by role")
            print("12. Review books")
            print("13. Find book by ISBN")
            print("14. Update a book")
            print("15. Review all loans")
            print("16. Review loans by user")
            print("17. Review active loans by user")
            print("18. Delete user")
            print("19. Update user")
            print("20. Exit")

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
                    loan = self.loan_service.loan_book(book_id, user_id)
                    print(f"Loan completed succesfully with loan ID {loan.loan_id}")
                except UserNotFoundException as e:
                    print(e)
                except LoanLimitExceededException as e:
                    print(e)
                except NoAvailableCopiesException as e:
                    print(e)
                except BookNotFoundException as e:
                    print(e)

            elif opcion == "5":
                try:
                    copy_id = int(input("Enter copy ID: "))
                    self.loan_service.return_book(copy_id)
                    print("Book returned successfully")
                except ValueError as e:
                    print(e)
                except CopyNotFoundException as e:
                    print(e)
                except NoActiveLoanException as e:
                    print(e)
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
                try:
                    loan_id = int(input("Enter loan ID: "))
                    print(self.loan_service.find_by_id(loan_id))
                except ValueError as e:
                    print(e)
                except LoanNotFoundException as e:
                    print(e)
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
                try:
                    isbn = input("Enter the ISBN: ")
                    print(self.library_service.find_by_isbn(isbn))
                except ValueError as e:
                    print(e)
                except BookNotFoundException as e:
                    print(e)
            elif opcion == "14":
                try:
                    book_id = int(input("Enter the book ID: "))
                except ValueError:
                    print("Please enter a valid number")
                    continue
                try:
                    book = self.library_service.find_by_id(book_id)

                    isbn = input(f"ISBN [{book.isbn}]: ").strip() or None
                    title = input(f"Title [{book.title}]: ").strip() or None
                    author = input(f"Author [{book.author}]: ").strip() or None

                    self.library_service.patch(
                        book_id=book_id,
                        isbn=isbn,
                        title=title,
                        author=author,
                    )

                    print("Book updated successfully")

                except BookNotFoundException as e:
                    print(e)
            elif opcion == "15":
                loans = self.loan_service.find_all()

                if not loans:
                    print("No loans found")
                else:
                    for loan in loans:
                        print(loan)
            elif opcion == "16":
                try:
                    user_id = int(input("Enter user ID: "))

                    loans = self.loan_service.find_by_user(user_id)

                    if not loans:
                        print("This user has no loans")
                    else:
                        for loan in loans:
                            print(loan)

                except ValueError as e:
                    print(e)
                except UserNotFoundException as e:
                    print(e)
            elif opcion == "17":
                try:
                    user_id = int(input("Enter user ID: "))

                    loans = self.loan_service.find_active_by_user(user_id)

                    if not loans:
                        print("This user has no active loans")
                    else:
                        for loan in loans:
                            print(loan)

                except ValueError as e:
                    print(e)
                except UserNotFoundException as e:
                    print(e)
            elif opcion == "18":
                try:
                    user_id = int(input("Enter user ID: "))
                    self.user_service.delete(user_id)
                    print("User deleted successfully")
                except ValueError as e:
                    print(e)
                except UserNotFoundException as e:
                    print(e)
                except UserHasLoansException as e:
                    print(e)
            elif opcion == "19":
                try:
                    user_id = int(input("Enter user ID: "))

                    user = self.user_service.find_by_id(user_id)

                    name = input(f"Name [{user.name}]: ").strip() or None
                    role = input(f"Role [{user.role.value}]: ").strip() or None

                    self.user_service.patch(
                        user_id=user_id,
                        name=name,
                        role=role,
                    )

                    print("User updated successfully")

                except ValueError as e:
                    print(e)
                except UserNotFoundException as e:
                    print(e)
            elif opcion == "20":
                print("Saliendo del menú.")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
