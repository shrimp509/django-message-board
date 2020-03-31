

def check_register_data(raw_data):

    # check account format
    account = raw_data.get('account')
    if len(account) > 30:
        custom_print("account length error, length of account: ", len(account))
        return False

    # check password format
    password = raw_data.get('password')
    if len(password) > 30:
        custom_print("password length error, length of password: ", len(password))
        return False

    # check birthday format (1994-05-09)
    birthday = raw_data.get('birthday')
    birthday_list = str(birthday).split('-')
    if len(birthday_list) == 3:
        year = birthday_list[0]
        month = birthday_list[1]
        day = birthday_list[2]
    else:
        custom_print("birthday format error, length of birthday_list: ", len(birthday_list))
        return False

    if len(birthday) > 30 or int(year) < 0 or int(month) > 12 or \
            int(month) < 1 or int(day) > 30 or int(day) < 1:
        custom_print("birthday format error, birthday_list: ", birthday_list)
        return False

    # check phone format
    phone = raw_data.get('phone')
    if not str(phone).startswith('09') and not str(phone).startswith('+886'):
        custom_print("phone format error, phone: ", str(phone))
        return False

    # check email format
    email = raw_data.get('email')
    email_list = str(email).split('@')
    if len(email_list) == 2:
        email_account = email_list[0]
        email_domain = email_list[1]
    else:
        custom_print("email format error, email_list: ", str(email_list))
        return False

    if len(str(email)) > 50:
        custom_print("email format error, len of email: ", len(str(email)))
        return False

    # check first name format
    first_name = raw_data.get('first_name')
    if len(first_name) > 20:
        custom_print("first_name format error, len of first_name: ", len(first_name))
        return False

    # check last name format
    last_name = raw_data.get('last_name')
    if len(last_name) > 20:
        custom_print("last_name format error, len of last_name: ", len(last_name))
        return False

    # check gender format
    gender = raw_data.get('gender')
    if gender != 'male' and gender != 'female':
        print("gender format error, is not boolean: ", gender, ", type: ", type(gender))
        return False

    return True


def custom_print(self, str):
    if True:
        print(str)
