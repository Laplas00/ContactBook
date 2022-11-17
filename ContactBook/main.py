import re
from ContactBook.core import *
from ContactBook.sort import *


CONTACTS = AddressBook()


def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except (ValueError, IndexError, UnboundLocalError):
            print("Error. Give me correct name, phone, birthday or email, please")
        except TypeError:
            print('Nothing found')
        except KeyError:
            print("Error. Enter user name, please")
    return wrapper


def hello_handler():
    print("Hello user i have this commands\n")
    for com in COMMANDS:
        print('{:<23} - {:>27}'.format(com, COMMANDS[com][-1]))
    print('\n')


def quit_handler():
    print("Good bye!")
    CONTACTS.save_contacts()
    quit()


@input_error
def add_contact_handler(var):    
    name, phone = var.split()[0], var.split()[1]
    

    if name in CONTACTS:
        record = CONTACTS.data[name]
        record.add_phone(phone)
    else:
        record = Record(name, phone)
        CONTACTS.add_record(record)


@input_error
def find_contact_handler(var):
    for name, record in CONTACTS.items():
        if name == var.split()[0]:
            print(
                f"{name.capitalize()}: {[phone.value for phone in record.phones]}")



@input_error
def delete_contact_handler(var):
    name = var.split()[0]
    phone_for_delete = var.split()[1]
    record = CONTACTS.data[name]
    record.delete_phone(phone_for_delete)


@input_error
def change_contact_handler(var):
    name = var.split()[0]
    phone_for_change = var.split()[1]
    new_phone = var.split()[2]
    if phone_for_change and new_phone:
        record = CONTACTS.data[name]
        record.change_phone(phone_for_change, new_phone)



@input_error
def add_birthday_handler(var):
    name = var.split()[0]
    birthday = var.split()[1]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if not record.birthday:
            record.add_birthday(birthday)



@input_error
def days_to_birthday_handler(var):
    name = var.split()[0]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        record.days_to_birthday()


def show_contacts_handler():
    for name, record in CONTACTS.items():
        if record.birthday:
            print("{:<10}{:^35}{:>10}".format(name.capitalize(), " ".join(
                [phone.value for phone in record.phones]), record.birthday))
        else:
            print("{:<10}{:^35}{:>10}".format(name.capitalize(), " ".join(
                [phone.value for phone in record.phones]), "-"))



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
    if not command_list:
        raise Exception
    command_list = sorted(command_list, key=lambda x: x['count'], reverse=True)
    print(
        f"You are looking for '{var}', the most suitable command is: {list(command_list[0].values())[0]}")


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


def clean_folder():
    get_main_path()



@input_error
def add_note_handler(var):
    name = var.split()[0]
    note = " ".join(var.split()[1:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if not record.note:
            record.add_note(note)
    else:
        raise KeyError



@input_error
def show_notes_handler():
    show_list = []
    for name, record in CONTACTS.items():
        if record.note:
            show_list.append(f"{name.capitalize()}: {record.note}")
    if show_list:
        for item in show_list:
            print(item)
    else:
        raise TypeError



@input_error
def add_tag_handler(var):
    name = var.split()[0]
    tag = " ".join(var.split()[1:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.note:
            record.add_tag(tag)
            return True
        else:
            print('rur else')
            raise TypeError 
    raise KeyError
        


@input_error
def show_tags_handler():
    show_list = []
    for name, record in CONTACTS.items():
        if record.tag != {}:
            show_list.append(record.tag)
    if show_list != []:
        show_list = sorted(show_list, key=lambda x: x['tag'])
        for i in show_list:
            print(i)
    else:
        raise TypeError
        
        

    


@input_error
def delete_note_handler(var):
    name = var.split()[0]
    record = CONTACTS.data[name]
    record.note = ""
    record.tag = {}



@input_error
def change_note_handler(var):
    name = var.split()[0]
    note = " ".join(var.split()[1:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.note:
            record.update_dict(note)
    else:
        raise KeyError



@input_error
def find_tag_handler(var):
    tag_for_find = " ".join(var.split()[0:])
    show_list = []
    for name, record in CONTACTS.items():
        if record.tag:
            if re.search(tag_for_find, record.tag["tag"]):
                show_list.append(f"{name.capitalize()}; {record.tag}")
    if show_list:
        print(show_list)


@input_error
def find_notes(var):
    show_list = []
    for name, record in CONTACTS.items():
        if re.search(var, record.note):
            show_list.append(f"{name.capitalize()}; {record.note}")
    if not show_list:
        raise Exception
    print(
        f"You are looking for '{var}', the most suitable notes is: {show_list}")


@input_error
def add_address_handler(var):
    name = var.split()[0]
    address = " ".join(var.split()[1:])
    if name in CONTACTS:
        record = CONTACTS.data[name]
        record.add_address(address)






def find_address_handler():
    show_list = []
    for name, record in CONTACTS.items():
        if record.address:
            show_list.append(
                f"{name.capitalize()}'s address: {record.address.value}")
    if show_list:
        for item in show_list:
            print(item)



@input_error
def show_list_birthday_handler(var):
    interval = int(var.split()[0])
    for record in CONTACTS.values():
        record.interval_birthday(interval)
        return True


@input_error
def add_email_handler(var):
    name = var.split()[0]
    email = var.split()[1]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if not record.email:
            record.add_email(email)
    else:
        raise TypeError



def show_email_handler():
    show_list = []
    for name, record in CONTACTS.items():
        if record.email:
            show_list.append(
                f"{name.capitalize()}'s email: {record.email.value}")
        else:
            continue
    if show_list:
        for item in show_list:
            print(item)


# ---------- TEST ----------

# add_contact_handler('Bog +380963031892')
# add_contact_handler('Ksy +380963031333')
# add_contact_handler('Sop +380963031222')
# add_contact_handler('Lan +380963031222')

# add_birthday_handler('Bog 03.09.2002')
# add_birthday_handler('Ksy 02.02.2004')
# add_birthday_handler('Sop 01.01.2001')
# add_birthday_handler('Lan 09.11.2005')

# add_note_handler('Bog This is test1')
# add_note_handler('Ksy This is test2')
# add_note_handler('Sop This is test3')
# add_note_handler('Lan This is test4')

# add_tag_handler('Bog 1st')
# add_tag_handler('Ksy 2st')
# add_tag_handler('Sop 3st')
# add_tag_handler('Lan 4st')

# add_address_handler('Bog doma')
# add_address_handler('Ksy S Rostikom')
# add_address_handler('Sop DaVotTut')

# add_email_handler('Bog test1@gmail.com')
# add_email_handler('Ksy test2@gmail.com')
# add_email_handler('Lan test3@gmail.com')

# ---------- TEST ----------


COMMANDS = {
    "hello": [hello_handler, 'show commands'],
    "add": [add_contact_handler, '[name] [phone]'],
    "add birthday": [add_birthday_handler, '[name] [dd.mm.yyyy]'],
    "add address": [add_address_handler, '[name] [address]'],
    "add note": [add_note_handler, '[name] [note]'],
    "add tag": [add_tag_handler, '[name] [tag]'],
    "add email": [add_email_handler, '[name] [email]'],
    "change note": [change_note_handler, '[name] [new_note]'],
    "delete note": [delete_note_handler, '[name]'],
    "change phone": [change_contact_handler, '[name] [phone] [new_phone]'],
    "delete phone": [delete_contact_handler, '[name] [number]'],
    "find phone": [find_contact_handler, '[name]'],
    "find tag": [find_tag_handler, '[tag_name]'],
    "all tags": [show_tags_handler, 'show all tags'],
    "all notes": [show_notes_handler, 'show all notes'],
    "all email": [show_email_handler, 'show all emails'],
    "all address": [find_address_handler, 'show all address'],
    "show all": [show_contacts_handler, 'show all contacts'],
    "days before birthday": [days_to_birthday_handler, '[name]'],
    "to birthday": [show_list_birthday_handler, '[number of days]'],
    "sort": [run, 'Sort folder [path]'],
    "exit" : [quit_handler, 'Quit']
}


def main():

    while True:
        var = (input("Enter command: ")).lower().strip()

        if var in COMMANDS and COMMANDS[var][-1].endswith(']'):
            args = input('Enter arguments: ')
            COMMANDS[var][0](args)
            continue

        if var in COMMANDS:
            result = COMMANDS[var][0]()
            if result:
                print('Done')
                continue

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
