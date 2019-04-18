import random

from screte_database.firebase_db import Database
from Screte_PRIVATE import config


def generate_date():
    return '{}/{}/{}'.format(random.randint(1, 31), random.randint(1, 12), random.randint(2000, 2019))


def generate_mac_address():
    return ':'.join([str(hex(random.randint(0, 255))[2:]) for i in range(6)])


def generate_ip_address():
    return '.'.join([str(random.randint(0, 255)) for i in range(4)])


def generate_user_db(db):
    username = 'user-{}'.format(random.randint(1, 255))
    registration_date = generate_date()
    ip_address = generate_ip_address()
    mac_address = generate_mac_address()
    db.add_user(username=username, ip_address=ip_address,
                registration_date=registration_date, mac_address=mac_address)


def main():
    db = Database(config.my_email, config.my_key)
    for i in range(9):
        generate_user_db(db)


if __name__ == "__main__":
    main()
