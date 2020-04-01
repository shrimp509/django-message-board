from .models import User


def check_register_data(raw_data):
    return get_all_err_msg(
        check_name(raw_data.get('name')),
        check_password(raw_data.get('password')),
        check_email(raw_data.get('email'))
    )


def check_name(name: str):
    # check name format
    if len(name) > 20 or len(name) < 1:
        err_msg = "name length error, should be 1~20, your len of name: {}".format(len(name))
        return err_msg
    return None


def check_password(password: str):
    # check password format
    if len(password) > 30 or len(password) < 6:
        err_msg = "password length error, should be 6~30, your length of password: {}".format(len(password))
        return err_msg
    return None


def check_email(email: str):
    # check email format
    email_list = str(email).split('@')
    if len(email_list) == 2:
        email_account = email_list[0]
        email_domain = email_list[1]

        # check account
        if len(email_account) <= 0 or len(email_account) > 35:
            err_msg = "email account error, account length should be 1~35, your account: {}".format(email_account)
            return err_msg

        # check domain
        if email_domain != 'gmail.com' and email_domain != 'hotmail.com':
            err_msg = "email domain error, domain should be `gmail.com` or `hotmail.com`, but your domain: {}".format(
                email_domain)
            return err_msg
    else:
        err_msg = "email format error, cannot have two or more `@`, yours: {}".format(str(email_list))
        return err_msg

    if len(str(email)) > 50:
        err_msg = "email length error, should be <= 50, your len of email: {}".format(len(str(email)))
        return err_msg

    # check email exists or not
    for obj in User.objects.all():
        if str(obj.email) == str(email):
            err_msg = "email duplicated, email `{}` exists".format(str(email))
            return err_msg


def get_all_err_msg(err_name: str, err_password: str, err_email: str, others: str = None):
    err_msg = {}
    if err_name is not None:
        err_msg['err_name'] = err_name
    if err_password is not None:
        err_msg['err_password'] = err_password
    if err_email is not None:
        err_msg['err_email'] = err_email
    if others is not None:
        err_msg['others'] = others

    if bool(err_msg):
        return err_msg
    else:
        return None
