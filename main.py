from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass
    # реалізація класу


class Phone(Field):

    def __init__(self, phone):
        if len(phone) == 10 and phone.isdigit():
            self.value = self.phone = phone
        else:
            raise ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_number, new_number):
        phone_obj = self.find_phone(old_number)
        if phone_obj:
            phone_obj.value = new_number
        else:
            raise ValueError

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        print(f'We added {record.name}')
        self.data[record.name.value] = record

    def find(self, name):
        for record_name, record in self.data.items():
            if str(record_name) == name:
                # print(f'We found {record_name}')
                return record
        print('There is not {name} in address book')

    def delete(self, name):
        print(f'DELETE {name}')
        # del self.data[name]
        self.data = {r_name: record for r_name,
                     record in self.data.items() if str(r_name) != name}
    # реалізація класу


if __name__ == '__main__':
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    for name, record in book.data.items():
        print(record)
