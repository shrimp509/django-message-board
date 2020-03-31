from .models import User


def check_register_data(raw_data):
    print("check register data: ", raw_data)

    # check email format
    email = raw_data.get('email')
    email_list = str(email).split('@')
    if len(email_list) == 2:
        email_account = email_list[0]
        email_domain = email_list[1]

        # check domain
        domain_split = email_domain.split('.')
        if len(domain_split) == 2 or len(domain_split) == 3:
            if domain_split[0] != 'gmail' and domain_split[0] != 'hotmail':
                err_msg = "email domain error, domain should be gmail or hotmail, but you are {}".format(domain_split[0])
                return False, err_msg
    else:
        err_msg = "email format error, email_list: {}".format(str(email_list))
        return False, err_msg

    if len(str(email)) > 50:
        err_msg = "email format error, len of email: {}".format(len(str(email)))
        return False, err_msg

    # check email repeat or not
    for obj in User.objects.all():
        if str(obj.email) == str(email):
            err_msg = "email duplicated, email: {} and obj.email: {}".format(str(email), str(obj.email))
            return False, err_msg

    # check name format
    name = raw_data.get('name')
    if len(name) > 20:
        err_msg = "name format error, len of name: {}".format(len(name))
        return False, err_msg

    # check password format
    password = raw_data.get('password')
    if len(password) > 30:
        err_msg = "password length error, length of password: {}".format(len(password))
        return False, err_msg

    return True, None


def custom_print(self, message):
    if True:
        print(message)
