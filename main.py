from collections import UserDict
import csv
import os


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

    def search(self, value):
        search_list = list()
        if value.isdigit():
            for address in self.data.values():
                for phone in address.phones:
                    if phone.startswith(value):
                        search_list.append(address)
            return search_list
        else:
            for address in self.data.values():
                if str(address.name).startswith(value):
                    search_list.append(address)
            return search_list

    def dump(self):
        if os.path.exists('addressbook.csv'):
            with open('addressbook.csv', 'a', newline='\n') as fh:
                address_book_disk = self.load()
                field_names = ['first_name', 'phones']
                writer = csv.DictWriter(fh, fieldnames=field_names)
                for address in self.data.values():
                    if str(address.name) in address_book_disk:
                        continue
                    else:
                        writer.writerow({'first_name': address.name, 'phones': [
                            str(phone) for phone in address.phones]})
        else:
            with open('addressbook.csv', 'a', newline='\n') as fh:
                field_names = ['first_name', 'phones']
                writer = csv.DictWriter(fh, fieldnames=field_names)
                writer.writeheader()
                for address in self.data.values():
                    writer.writerow({'first_name': address.name, 'phones': [
                                    str(phone) for phone in address.phones]})

    def load(self):
        with open('addressbook.csv', newline='\n') as fh:
            reader = csv.DictReader(fh)
            address_book_disk = list()
            for row in reader:
                # print(row['first_name'], row['phones'])
                address_book_disk.append(row['first_name'])
                if row['first_name'] in self.data:
                    continue
                else:
                    the_record = Record(row['first_name'])
                    the_record.phones = row['phones']
                    self.add_record(self, the_record)
            print(address_book_disk)
            return address_book_disk
    # реалізація класу


if __name__ == '__main__':
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    for name, record in book.data.items():
        print(record)

    book.dump()
    book.load()

    print('_________________________________________________')

    for name, record in book.data.items():
        print(record)

    print(book.search('J'))
