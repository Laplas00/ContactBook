import re
from core import *
from sort import *


CONTACTS = AddressBook()


def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except (ValueError, IndexError, UnboundLocalError):
            print("Error. Give me correct name, phone or birthday, please")
        except KeyError:
            print("Error. Enter user name, please")
    return wrapper


def hello_handler():
    print("How can I help you?")


def quit_handler():
    print("Good bye!")
    CONTACTS.save_contacts()
    quit()


@input_error
def add_contact_handler(var):
    name = var.split()[1]
    phone = var.split()[2]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        record.add_phone(phone)
    else:
        record = Record(name, phone)
        CONTACTS.add_record(record)
    print("New contact was added")


@input_error
def find_contact_handler(var):
    for name, record in CONTACTS.items():
        if name == var.split()[1]:
            print(
                f"{name.capitalize()}: {[phone.value for phone in record.phones]}")


@input_error
def delete_contact_handler(var):
    name = var.split()[1]
    phone_for_delete = var.split()[2]
    record = CONTACTS.data[name]
    record.delete_phone(phone_for_delete)
    print("Contact's phone was deleted")


@input_error
def change_contact_handler(var):
    name = var.split()[1]
    phone_for_change = var.split()[2]
    new_phone = var.split()[3]
    if phone_for_change and new_phone:
        record = CONTACTS.data[name]
        record.change_phone(phone_for_change, new_phone)
        print("Contact was changed")


@input_error
def add_birthday_handler(var):
    name = var.split()[2]
    birthday = var.split()[3]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.birthday == "":
            record.add_birthday(birthday)
            print("Contact's birthday was added")
        else:
            print("Contact's birthday was added before")


@input_error
def days_to_birthday_handler(var):
    name = var.split()[0]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        record.days_to_birthday()


def show_contacts_handler():
    for name, record in CONTACTS.items():
        if record.birthday != "":
            print("{:<10}{:^35}{:>10}".format(name.capitalize(), " ".join(
                [phone.value for phone in record.phones]), record.birthday))
        else:
            print("{:<10}{:^35}{:>10}".format(name.capitalize(), " ".join(
                [phone.value for phone in record.phones]), "-"))


def iteration():
    for i in CONTACTS.iterator():
        print(i)


# Пошук за не повними значеннями команд
@input_error
def find_com(var):
    command_list = []
    for command in COMMANDS:
        if re.search(var, command):
            command_list.append(command)
    if command_list == []:
        raise Exception
    print(
        f"You are looking for '{var}', the most suitable command is: {command_list}")


# Пошук за не повними значеннями контактів
@input_error
def find(var):
    show_list = []
    for name, record in CONTACTS.items():
        if re.search(var, name):
            show_list.append(
                f"{name.capitalize()}: {[phone.value for phone in record.phones]}")
        for phone in record.phones:
            if re.search(var, phone.value):
                show_list.append(
                    f"{name.capitalize()}: {[phone.value for phone in record.phones]}")
    if show_list == []:
        raise Exception
    print(f"You are looking for '{var}', the most suitable contact is: {show_list}")


# Сортування папки з файлами
def clean_folder():
    get_main_path()
    print('Done!')


@input_error
def add_note_handler(var):
    name = var.split()[1]
    note = " ".join(var.split()[2:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.note == "":
            record.add_note(note)
            print("Contact's note was added")


def show_notes_handler():
    show_list = []
    for name, record in CONTACTS.items():
        if record.note != "":
            show_list.append(f"{name.capitalize()}; note: {record.note}")
    if show_list != []:
        print(show_list)
    else:
        print("The are no notes!")


@input_error
def add_tag_handler(var):
    name = var.split()[1]
    tag = " ".join(var.split()[2:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.note != "":
            record.add_tag(tag)
            print("Contact's tag was added")
        else:
            print("You should write contact's note before")


def show_tags_handler():
    show_list = []
    for record in CONTACTS.values():
        if record.tag != {}:
            show_list.append(record.tag)
    if show_list != []:
        show_list = sorted(show_list, key=lambda x: x['tag'])
        print(show_list)
    else:
        print("The are no tags!")


@input_error
def delete_note_handler(var):
    name = var.split()[2]
    record = CONTACTS.data[name]
    record.note = ""
    record.tag = {}
    print("Contact's note was deleted")


@input_error
def change_note_handler(var):
    name = var.split()[2]
    note = " ".join(var.split()[3:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.note != "":
            record.update_dict(note)
            print("Contact's note was changed")


@input_error
def find_tag_handler(var):
    tag_for_find = " ".join(var.split()[2:])
    show_list = []
    for name, record in CONTACTS.items():
        if record.tag != {}:
            if re.search(tag_for_find, record.tag["tag"]):
                show_list.append(f"{name.capitalize()}; {record.tag}")
    if show_list != []:
        print(show_list)
    else:
        print("Dont find any tags!")


@input_error
def find_notes(var):
    show_list = []
    for name, record in CONTACTS.items():
        if re.search(var, record.note):
            show_list.append(f"{name.capitalize()}; {record.note}")
    if show_list == []:
        raise Exception
    print(f"You are looking for '{var}', the most suitable notes is: {show_list}")


COMMANDS = {
    "hello": hello_handler,
    "show all": show_contacts_handler,
    "exit": quit_handler,
    "close": quit_handler,
    "good bye": quit_handler,
    "iter": iteration,
    "sort": clean_folder,
    "all notes": show_notes_handler,
    "all tags": show_tags_handler
}


def main():
    while True:
        var = (input("Enter command: ")).lower()
        if var.startswith('add birthday'):
            add_birthday_handler(var)
        elif var.endswith("birthday"):
            days_to_birthday_handler(var)
        elif var.startswith('add'):
            add_contact_handler(var)
        elif var.startswith('change note'):
            change_note_handler(var)
        elif var.startswith('change'):
            change_contact_handler(var)
        elif var.startswith('phone'):
            find_contact_handler(var)
        elif var.startswith('delete phone'):
            delete_contact_handler(var)
        elif var.startswith('note'):
            add_note_handler(var)
        elif var.startswith('tag'):
            add_tag_handler(var),
        elif var.startswith('delete note'):
            delete_note_handler(var),
        elif var.startswith('find tag'):
            find_tag_handler(var)
        elif var in COMMANDS:
            COMMANDS[var]()
        else:
            try:
                find(var)
            except:
                print("Nothing found in contacts!")
            try:
                find_com(var)
            except:
                print("Nothing found in command!")
            try:
                find_notes(var)
            except:
                print("Nothing found in notes!")
            continue



if __name__ == "__main__":
    main()