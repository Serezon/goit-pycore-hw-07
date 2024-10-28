from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not all(c.isdigit() for c in value):
            raise ValueError("Phone number must be 10 digits long")
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        day, month, year = map(int, value.split("."))
        if day < 1 or day > 31 or month < 1 or month > 12 or year > datetime.now().year:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = datetime(day=day, month=month, year=year)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

class AddressBook(UserDict):
    def __str__(self):
        for record in self.data.values():
            print(record)
        return ""

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def delete(self, name):
        del self.data[name]

def get_upcoming_birthdays(address_book):
    today = datetime.now().date()
    upcoming_birthdays = []
    
    for user in address_book.values():
        if not user.birthday:
            continue
        birthday = user.birthday.value.date().replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)

        if birthday.weekday() >= 5:
            birthday = birthday + datetime.timedelta(days=7 - birthday.weekday())

        if (birthday - today).days <= 7:
            upcoming_birthdays.append(user)
            
    return upcoming_birthdays

def main():
    book = AddressBook()

    record1 = Record("John")
    record1.add_phone("1234567890")
    book.add_record(record1)
    
    record2 = Record("Alice")
    record2.add_phone("0987654321")
    record2.add_birthday("01.01.2000")
    book.add_record(record2)

    record3 = Record("Bob")
    record3.add_phone("1112223334")
    record3.add_birthday("01.11.2024")
    book.add_record(record3)

    print(get_upcoming_birthdays(book))

if __name__ == "__main__":
    main()

