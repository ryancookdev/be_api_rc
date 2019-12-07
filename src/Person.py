import re

class Person:
    def __init__(self, id, fname, mname, lname, phone):
        self.set_internal_id(id)
        self.set_first_name(fname)
        self.set_middle_name(mname)
        self.set_last_name(lname)
        self.set_phone(phone)

    def set_internal_id(self, id):
        if not id:
            raise Exception('Internal ID is required')
        if not id.isnumeric():
            raise Exception('Internal ID must be numeric')
        if int(id) < 0:
            raise Exception('Internal ID must be a positive integer')
        if not len(id) == 8:
            raise Exception('Internal ID must be 8 digits')
        self.internal_id = id

    def set_first_name(self, fname):
        if not fname:
            raise Exception('First name is required')
        if len(fname) > 15:
            raise Exception('First name cannot exceed 15 characters')
        self.first_name = fname

    def set_middle_name(self, mname):
        if len(mname) > 15:
            raise Exception('Middle name cannot exceed 15 characters')
        self.middle_name = mname

    def set_last_name(self, lname):
        if not lname:
            raise Exception('Last name is required')
        if len(lname) > 15:
            raise Exception('Last name cannot exceed 15 characters')
        self.last_name = lname

    def set_phone(self, phone):
        if not phone:
            raise Exception('Phone is required')
        if not re.match("^\d{3}-\d{3}-\d{4}$", phone):
            raise Exception('Phone must be in ###-###-#### format')
        self.phone = phone
