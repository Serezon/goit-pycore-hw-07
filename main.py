from functools import wraps
import task1 as contact_book

def input_error_factory(default_message="Invalid input", value_error_message=None, index_error_message=None):
    if value_error_message is None:
        value_error_message = default_message
    if index_error_message is None:
        index_error_message = default_message

    def input_error(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return value_error_message
            except IndexError:
                return index_error_message
            except Exception:
                return default_message

        return inner
    
    return input_error

def parse_input(user_input):
    if not user_input:
        return None, None
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error_factory(value_error_message="Please provide a name and a phone number.")
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name].add_phone(phone)
        return "Phone added to existing contact."

    record = contact_book.Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."

@input_error_factory(value_error_message="Please provide a name and a phone number.")
def change_contact(args, contacts):
    name, old_phone, phone = args
    if name in contacts:
        contacts[name].edit_phone(old_phone, phone)
        return "Phone number changed."
    else:
        return "Contact not found."

@input_error_factory(index_error_message="Please provide a name.")
def get_phone(args, contacts):
    name = args[0]
    if name in contacts:
        phones = contacts[name].phones
        if len(phones) > 0:
            print(f"Phone numbers for {name}:")
            for phone in phones:
                print(phone)
        else:
            return "No phone numbers found."
                
    else:
        return "Contact not found."

@input_error_factory(value_error_message="Please provide a name.")
def get_birthday(args, contacts):
    name = args[0]
    if name in contacts:
        birthday = contacts[name].birthday
        if birthday:
            return f"{name} birthday: {birthday}"
        else:
            return "No birthday found."
    else:
        return "Contact not found."

@input_error_factory(value_error_message="Please provide a name.")
def add_birthday(args, contacts):
    name, birthday = args
    if name in contacts:
        contacts[name].add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

def get_upcoming_birthdays(contacts):
    def print_birthday(contact):
        return f"{contact.name.value} has a birthday on {contact.birthday.value.date()}"

    return "\n".join([print_birthday(contact) for contact in contact_book.get_upcoming_birthdays(contacts)])

def get_contacts(contacts):
    return contacts

def help():
    return """
    Available commands:
    help - Show available commands.
    hello - Greet the bot.
    add <name> <phone> - Add a new contact.
    change <name> <old_phone> <new_phone> - Change the phone number of a contact.
    phone <name> - Get the phone number of a contact.
    add-birthday <name> <birthday> - Add a birthday to a contact.
    show-birthday <name> - Show the birthday of a contact.
    birthdays - Show upcoming birthdays.
    all - Get all contacts.
    close - Close the bot.
    exit - Close the bot.
    """

def main():
    contacts = contact_book.AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(get_phone(args, contacts))
        elif command == "all":
            print(get_contacts(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(get_birthday(args, contacts))
        elif command == "birthdays":
            print(get_upcoming_birthdays(contacts))
        elif command == "help":
            print(help())
        else:
            print("Invalid command. Type 'help' to see available commands.")

if __name__ == "__main__":
    main()
