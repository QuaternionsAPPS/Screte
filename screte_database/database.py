import datetime

import mysql.connector

import screte_database.screte_db_login as login
from screte_cryptography.diffie_hellman_keys import diffie_hellman_public_key


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(host=login.server, user=login.username,
                                            password=login.password, database=login.db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        self.cursor.close()

    def set_ip_address(self, username, ip_address):
        """
        :param username: varchar(32)
        :param ip_address: varchar(15)
        :return: True -- if everything is okay, False -- otherwise
        """
        if not self.get_general_user_info(username):
            return False

        self.cursor.execute("UPDATE users SET ip_address = (%s) WHERE username = (%s)", (ip_address, username))
        return True

    def reset_ip_address(self, username):
        """
        :param username: varchar(32)
        :return: True -- if everything is okay, False -- otherwise
        """
        if not self.get_general_user_info(username):
            return False

        self.cursor.execute("UPDATE users SET ip_address = (%s) WHERE username = (%s)", (None, username))
        return True

    def get_ip_address(self, username):
        """
        :param username: varchar(32)
        :return: ip_address: varchar(15)
        """
        if not self.get_general_user_info(username):
            return False

        self.cursor.execute("SELECT ip_address FROM users WHERE username = (%s)", (username, ))
        ip_address = self.cursor.fetchone()
        return ip_address[0]

    def add_user(self, user):
        """
        :param user: {'username': varchar(32),
                      'first_name': varchar(32),
                      'last_name': varchar(32),
                      'password': varchar(32)}
        :return: True if everything is okay, False otherwise.
        """
        key_check_set = {"username", "first_name", "last_name", "password"}
        check_list = [k for k in key_check_set if k not in user.keys()]
        if len(check_list) > 0:
            return False

        if (len(user["username"]) > 32) or (len(user["first_name"]) > 32) or (len(user["last_name"]) > 32) or (len(user["password"]) > 32):
            return False

        if self.get_general_user_info(user["username"]) is not None:
            return False

        today = self._current_time()

        pub_key = diffie_hellman_public_key()

        self.cursor.execute("INSERT INTO users (username, first_name, last_name, password, registration_time, sh_key) VALUES (%s, %s, %s, %s, %s, %s)",
                       (user["username"], user["first_name"], user["last_name"], user["password"], today, str(pub_key)))

        self.conn.commit()

        return True

    def check_password(self, username, password):
        """
        :param username: varchar(32)
        :param password: varchar(32)
        :return: True/False -- password does match. 422/404 otherwise.
        """
        if len(username) > 32:
            return False

        self.cursor.execute("SELECT password FROM users WHERE username = (%s)", (username,))
        real_password = self.cursor.fetchone()

        if real_password is not None:
            return real_password[0] == password.strip()

    def get_general_user_info(self, username):
        """
        :param username: varchar(32)
        :return: {"first_name": varchar(32),
                  "last_name": varchar(32)}
                  False - otherwise.

        """
        self.cursor.execute("SELECT first_name, last_name FROM users WHERE username = (%s)", (username,))
        user_info = self.cursor.fetchone()

        if user_info is not None:
            return {"first_name": user_info[0], "last_name": user_info[1]}

    def get_user_info_for_encryption(self, username):
        """
        :param username: varchar(32)
        :return: {"first_name": varchar(32),
                  "last_name": varchar(32),
                  "sh_key": int}
                  False - otherwise.
        """
        self.cursor.execute("SELECT first_name, last_name, sh_key FROM users WHERE username = (%s)", (username,))
        user_info = self.cursor.fetchone()

        if user_info is not None:
            return {"first_name": user_info[0], "last_name": user_info[1], "sh_key": int(user_info[2])}

    def add_contact(self, username1, username2):
        """
        :param username1: varchar(32)
        :param username2: varchar(32)
        :return: True if everything is okay.
                 False - otherwise
        """
        if (self.get_general_user_info(username1) is None) or (self.get_general_user_info(username2) is None):
            return False

        user_id_1 = self._get_user_id(username1)
        user_id_2 = self._get_user_id(username2)

        self.cursor.execute("SELECT * from contacts WHERE 1_user_id = (%s) and 2_user_id = (%s)", (user_id_1, user_id_2))
        contacts = self.cursor.fetchall()
        self.cursor.execute("SELECT * from contacts WHERE 1_user_id = (%s) and 2_user_id = (%s)", (user_id_2, user_id_1))
        contacts += self.cursor.fetchall()

        if contacts:
            return False

        self.cursor.execute("INSERT INTO contacts (1_user_id, 2_user_id) VALUES (%s, %s)", (user_id_1, user_id_2))

        self.conn.commit()

        return True

    def get_contacts(self, username):
        """
        :param username: varchar(32)
        :return: [username1, username2, ...]
                 False - otherwise
        """
        if len(username) > 32:
            return False

        if self.get_general_user_info(username) is None:
            return False

        user_id = self._get_user_id(username)
        self.cursor.execute("SELECT 2_user_id FROM contacts WHERE 1_user_id = (%s)", (user_id,))
        raw_contacts = self.cursor.fetchall()
        self.cursor.execute("SELECT 1_user_id FROM contacts WHERE 2_user_id = (%s)", (user_id,))
        raw_contacts += self.cursor.fetchall()

        contacts = [self._get_username(contact[0]) for contact in raw_contacts]
        contacts.append(username)

        return contacts

    def add_picture(self, picture):
        """
        :param picture: {"from_user": username,
                         "to_user": username,
                         "info_from_user": varchar(255)}
        :return: id of picture if everything is okay, False -- otherwise.
        """
        key_check_set = {"from_user", "to_user", "info_from_user"}
        check_list = [k for k in key_check_set if k not in picture.keys()]
        if len(check_list) > 0:
            return False

        if (self.get_general_user_info(picture["from_user"]) is None) and \
                (self.get_general_user_info(picture["to_user"] is None)):
            return False

        if len(picture["info_from_user"]) > 255:
            return False

        self.cursor.execute("INSERT INTO pictures (from_user_id, to_user_id, had_been_read, info_from_user) VALUES (%s, %s, %s, %s)",
                            (self._get_user_id(picture["from_user"]), self._get_user_id(picture["to_user"]), 0, picture["info_from_user"]))

        picture_id = self.cursor.lastrowid

        self.conn.commit()

        return picture_id

    def mark_picture_as_read(self, id):
        """
        :param id: id (int) of picture
        :return: True -- if everything is okay, False -- otherwise
        """
        self.cursor.execute("SELECT * FROM pictures WHERE id = (%s)", (id,))
        picture = self.cursor.fetchone()
        if picture is None:
            return False
        self.cursor.execute("UPDATE pictures SET had_been_read = 1 WHERE id = (%s)", (id,))
        return True

    def get_not_read_pictures(self, from_username, to_username):
        """
        :param from_username: varchar(32)
        :param to_username: varchar(32)
        :return: [id1, id2 ... ]
                 False -- otherwise
        """
        if self.get_general_user_info(from_username) is None:
            return False

        if self.get_general_user_info(to_username) is None:
            return False

        from_id = self._get_user_id(from_username)
        to_id = self._get_user_id(to_username)

        self.cursor.execute("SELECT id from pictures WHERE from_user_id = (%s) and to_user_id = (%s) and had_been_read = 0",
                            (from_id, to_id))
        raw_pictures = self.cursor.fetchall()

        return [pic[0] for pic in raw_pictures]

    def get_all_pictures(self, from_username, to_username):
        """
        :param username: varchar(32)
        :return: [ id1, id2, ...]
                   False -- otherwise
        """
        if self.get_general_user_info(from_username) is None:
            return False

        if self.get_general_user_info(to_username) is None:
            return False

        from_id = self._get_user_id(from_username)
        to_id = self._get_user_id(to_username)

        self.cursor.execute(
            "SELECT id from pictures WHERE from_user_id = (%s) and to_user_id = (%s)",
            (from_id, to_id))
        raw_pictures = self.cursor.fetchall()

        return [pic[0] for pic in raw_pictures]

    def start_session(self, username):
        user_id = self._get_user_id(username)
        start_time = self._current_time()
        number_of_encoded_pictures = self._num_all_send_pictures(username)
        number_of_decoded_pictures = self._num_all_received_pictures(username)
        self.cursor.execute("INSERT INTO sessions (user_id, start_time, finish_time, number_of_encoded_pictures, number_of_decoded_pictures) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, start_time, start_time, number_of_encoded_pictures, number_of_decoded_pictures))

        self.conn.commit()

    def end_session(self, username):
        user_id = self._get_user_id(username)
        self.cursor.execute("SELECT id, number_of_encoded_pictures, number_of_decoded_pictures FROM sessions WHERE user_id = (%s)",
                            (user_id,))
        raw_session = self.cursor.fetchall()[-1]
        finish_time = self._current_time()
        number_of_encoded_pictures = self._num_all_send_pictures(username)
        number_of_decoded_pictures = self._num_all_received_pictures(username)

        self.cursor.execute("UPDATE sessions SET finish_time = (%s), number_of_encoded_pictures = (%s), number_of_decoded_pictures = (%s) WHERE id = (%s)",
                            (finish_time, number_of_encoded_pictures - raw_session[1], number_of_decoded_pictures - raw_session[2], user_id))

        self.conn.commit()

    #
    #   Private functions
    #

    @staticmethod
    def _current_time():
        now = datetime.datetime.now()
        today = '{}:{}:{}_{}-{}-{}'.format(str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2),
                                           str(now.day).zfill(2), str(now.month).zfill(2), str(now.year)[-2:])
        return today

    def _get_user_id(self, username):
        """
        :param username: varchar(32)
        :return: integer
                 None - otherwise
        """
        self.cursor.execute("SELECT (id) FROM users WHERE username = (%s)", (username,))
        user_id = self.cursor.fetchone()

        if user_id is not None:
            return user_id[0]

    def _get_username(self, id):
        """
        :param id: integer
        :return: username: varchar(32)
                None - otherwise
        """
        self.cursor.execute("SELECT (username) FROM users WHERE id = (%s)", (id,))
        username = self.cursor.fetchone()

        if username is not None:
            return username[0]

    def _num_all_send_pictures(self, username):
        total = 0
        contacts = self.get_contacts(username)
        for to_user in contacts:
            total += len(self.get_all_pictures(username, to_user))
        return total

    def _num_all_received_pictures(self, username):
        total = 0
        contacts = self.get_contacts(username)
        for from_user in contacts:
            total += len(self.get_all_pictures(from_user, username))
        return total



