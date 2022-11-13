from collections import UserDict
from datetime import datetime
import pickle
import re


class AddressBook(UserDict):
    current_index = 0
    N = 2

    def __init__(self):
        try:
            with open("save_file.txt", "rb") as file:
                self.data = pickle.load(file)
        except:
            self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self):
        show_list = []
        names = [name for name in self.data]
        while len(self.data) >= AddressBook.current_index:
            for name in names[AddressBook.current_index: min(len(self.data), AddressBook.current_index + AddressBook.N)]:
                if self.data[name].birthday != "":
                    show_list.append("{:<10}{:^35}{:>10}".format((self.data[name].name.value).capitalize(
                    ), " ".join([phone.value for phone in self.data[name].phones]), self.data[name].birthday))
                else:
                    show_list.append("{:<10}{:^35}{:>10}".format((self.data[name].name.value).capitalize(
                    ), " ".join([phone.value for phone in self.data[name].phones]), "-"))
            yield show_list
            AddressBook.current_index += AddressBook.N
            show_list = []

    def save_contacts(self):
        if self.data != {}:
            with open("save_file.txt", "wb") as file:
                contacts = pickle.dump(self.data, file)


class Record:
    # --------------------------------email
    def __init__(self, name, phone=None, birthday=None, note=None, address=None, email=None):
        self.name = Name(name)
        self.tag = {}
        self.address = ""
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = ""
        if note:
            self.note = Note(note)
        else:
            self.note = ""
        if email:  # --------------------------------email
            self.email = Email(email)
        else:
            self.email = ""

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday).value.strftime('%d.%m.%Y')

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_note(self, note):
        self.note = Note(note).value

    def add_tag(self, tag):
        self.tag["tag"] = tag
        self.tag["note"] = self.note

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):  # --------------------------------email
        self.email = Email(email)

    def update_dict(self, note):
        for tag in self.tag.keys():
            self.note = note
            self.tag["note"] = note

    def delete_phone(self, phone_for_delete):
        for phone in self.phones:
            if phone.value == phone_for_delete:
                self.phones.remove(phone)

    def change_phone(self, phone_for_change, new_phone):
        for index, phone in enumerate(self.phones):
            if phone.value == phone_for_change:
                self.phones[index] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
            if ((birthday).replace(year=(datetime.now()).year)) > datetime.now():
                print(
                    f"to birthday {(((birthday).replace(year=(datetime.now()).year)) - datetime.now()).days} days")
            else:
                print(
                    f"to birthday {(((birthday).replace(year=(datetime.now()).year + 1)) - datetime.now()).days} days")
        else:
            print("Contact's birthday wasn't added")

    def interval_birthday(self, interval):
        if self.birthday != "":
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
            if ((birthday).replace(year=(datetime.now()).year)) > datetime.now():
                diference = (
                    ((birthday).replace(year=(datetime.now()).year)) - datetime.now()).days
            else:
                diference = (
                    ((birthday).replace(year=(datetime.now()).year + 1)) - datetime.now()).days
            if diference < interval:
                print(f"{(self.name.value).capitalize()}, birthday: {self.birthday}")
        else:
            print("No birthday in this interval")


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if not all((value.startswith('+380'), value[1:].isdigit(), len(value) == 13)):
            raise ValueError(
                print("Your phone should be like this: +380888888888"))
        self.__value = value


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return datetime.strftime(self.__value, '%d.%m.%Y')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            birthday = datetime.strptime(value, '%d.%m.%Y')
            self.__value = birthday
        except:
            raise ValueError(
                print("Your birthday should be like this: 20.12.2000"))


class Email(Field):         # --------------------------------email
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if not re.search("[a-zA-Z][a-zA-Z0-9_.]+@\w+\.\w\w+", value):
            raise ValueError(
                print("Your email should be like this: example@gmail.com"))
        self.__value = value


class Note(Field):
    pass


class Address(Field):
    pass
