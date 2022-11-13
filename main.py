import re
from core import *
from sort import *


CONTACTS = AddressBook()


def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except (ValueError, IndexError, UnboundLocalError, TypeError):
            print("Error. Give me correct name, phone, birthday or email, please")
        except KeyError:
            print("Error. Enter user name, please")
    return wrapper


def hello_handler():
    print("Hello user i have this commands")
    for com in COMMANDS:
        print('{:<15} - {:>27}'.format(com, COMMANDS[com][-1]))



def quit_handler():
    print("Good bye!")
    CONTACTS.save_contacts()
    quit()


@input_error
def add_contact_handler(var):
    name = var.split()[0]
    phone = var.split()[1]
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
        if name == var.split()[0]:
            print(
                f"{name.capitalize()}: {[phone.value for phone in record.phones]}")
        else:
            print('no')


@input_error
def delete_contact_handler(var):
    name = var.split()[0]
    phone_for_delete = var.split()[1]
    record = CONTACTS.data[name]
    record.delete_phone(phone_for_delete)
    print("Contact's phone was deleted")


@input_error
def change_contact_handler(var):
    name = var.split()[0]
    phone_for_change = var.split()[1]
    new_phone = var.split()[2]
    if phone_for_change and new_phone:
        record = CONTACTS.data[name]
        record.change_phone(phone_for_change, new_phone)
        print("Contact was changed")


@input_error
def add_birthday_handler(var):
    name = var.split()[0]
    birthday = var.split()[1]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.birthday == "":
            record.add_birthday(birthday)
            print("Contact's birthday was added")
        else:
            print("Contact's birthday was added before")
    else:
        print('This contact dont exist')


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
    for command in COMMANDS.keys():
        command_dict = {}
        count = 0
        for i in var:
            if re.search(i, command):
                count += 1
        command_dict["command"] = command
        command_dict["count"] = count
        command_list.append(command_dict)
    if command_list == []:
        raise Exception
    command_list = sorted(command_list, key=lambda x: x['count'], reverse=True)
    print(
        f"You are looking for '{var}', the most suitable command is: {list(command_list[0].values())[0]}")


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
    print(
        f"You are looking for '{var}', the most suitable contact is: {show_list}")


# Сортування папки з файлами
def clean_folder():
    get_main_path()
    print('Done!')


@input_error
def add_note_handler(var):
    name = var.split()[0]
    note = " ".join(var.split()[1:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.note == "":
            record.add_note(note)
            print("Contact's note was added")
    else:
        print('name dont exist')


def show_notes_handler():
    show_list = []
    for name, record in CONTACTS.items():
        if record.note != "":
            show_list.append(f"{name.capitalize()}, note: {record.note}")
    if show_list != []:
        print(show_list)
    else:
        print("The are no notes!")


@input_error
def add_tag_handler(var):
    name = var.split()[0]
    tag = " ".join(var.split()[1:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.note != "":
            record.add_tag(tag)
            print("Contact's tag was added")
        else:
            print("You should write contact's note before")


def show_tags_handler():
    show_list = []
    for name, record in CONTACTS.items():
        print(name, record)
        print(record.tag)
        if record.tag != {}:
            show_list.append(record.tag)
    if show_list != []:
        show_list = sorted(show_list, key=lambda x: x['tag'])
        print(show_list)
    else:
        print("The are no tags!")


@input_error
def delete_note_handler(var):
    name = var.split()[0]
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
    print(
        f"You are looking for '{var}', the most suitable notes is: {show_list}")


@input_error
def add_address_handler(var):
    name = var.split()[0]
    address = " ".join(var.split()[3:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.address == "":
            record.add_address(address)
            print("Contact's address was added")
        else:
            print("Contact's address was added before")



def find_address_handler():
    show_list = []
    for name, record in CONTACTS.items():
        if record.address != "":
            show_list.append(
                f"{name.capitalize()}, address: {record.address.value}")
    if show_list != []:
        print(show_list)
    else:
        print("The are no address!")



@input_error
def show_list_birthday_handler(var):
    interval = int(var.split()[0])
    for record in CONTACTS.values():
        record.interval_birthday(interval)


@input_error
def add_email_handler(var):  # ____________________________email
    name = var.split()[0]
    email = var.split()[1]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.email == "":
            record.add_email(email)
            print("Contact's email was added")
        else:
            print("Contact's email was added before")


def show_email_handler():  # ____________________________email
    show_list = []
    for name, record in CONTACTS.items():
        if record.email != "":
            show_list.append(
                f"{name.capitalize()}, email: {record.email.value}")
    if show_list != []:
        print(show_list)
    else:
        print("The are no notes!")


COMMANDS = {
     "hello": [hello_handler, 'show commands'],
     "add": [add_contact_handler, '[name] [phone]'],
     "add birthday" : [add_birthday_handler, '[name] [dd.mm.yyyy]'],
     "add address" : [add_address_handler, '[name] [adress]'],
     "add note" : [add_note_handler, '[name] [note]'],
     "add tag" : [add_tag_handler, '[name] [tag]'],
     "change note" : [change_note_handler, '[name] [new_note]'],
     "delete note" : [delete_note_handler, '[name]'],
     "change phone" : [change_contact_handler,'[name] [phone] [new_phone]'],
     "delete phone" : [delete_contact_handler, '[name] [number]'],
     "find phone" : [find_contact_handler, ' -- [name]'],
     "find tag" : [find_tag_handler, '[tag_name]'],
     "all tags": [show_tags_handler, 'show all tags'],
     "all notes": [show_notes_handler, 'show all notes'],
     "all email": [show_email_handler, 'show all emails'],
     "show all": [show_contacts_handler, 'show all contacts'],  
     "days before birthday" : [days_to_birthday_handler, '[name]'],
     "iter": [iteration, 'iteration with all notes'],
     "adress": [find_address_handler,'All adress'],
     "sort": [clean_folder,'???'],
}


def main():

    while True:
        var = (input("Enter command: ")).lower().strip()
        if var in COMMANDS and COMMANDS[var][-1].endswith(']'):
            print('тут нужны арги')
            args = input('args: ')
            COMMANDS[var][0](args)
        elif var in COMMANDS:
            COMMANDS[var][0]()
        elif var in ('quit', 'exit', 'q', 'break', 'bye', 'good bye'):
            quit_handler()
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
