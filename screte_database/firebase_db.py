from firebase import firebase


class Database:
    def __init__(self, user_email, user_key):
        self.db = firebase.FirebaseApplication('https://testqua-f8fb9.firebaseio.com/', authentication=None)
        authentication = firebase.FirebaseAuthentication(user_key, user_email)
        firebase.authentication = authentication
        print self.db
        self._project = '/screte_test'
        self._users = 'users'
        self._ip_address = 'ip-address'
        self._mac_address = 'mac-address'
        self._registration_date = 'registration-date'

    @staticmethod
    def valid_ip_address(ip_address):
        ip_address = ip_address.split('.')
        if len(ip_address) != 4:
            return False
        try:
            for el in ip_address:
                if not 0 <= int(el) <= 255:
                    return False
        except (TypeError, ValueError):
            return False
        return True

    @staticmethod
    def valid_mac_address(mac_address):
        mac_address = mac_address.split(':')
        if len(mac_address) != 6:
            return False
        try:
            for el in mac_address:
                if not 0 <= int(el, 16) <= 255:
                    return False
        except (TypeError, ValueError):
            return False
        return True

    @staticmethod
    def valid_date(date):
        date = date.split('/')
        try:
            if not 1 <= int(date[0]) <= 31:
                return False
            if not 1 <= int(date[1]) <= 12:
                return False
            if not 0 < int(date[2]):
                return False
        except (TypeError, ValueError):
            return False
        return True

    def _user_info(self, username):
        return self.db.get('{}/{}/{}'.format(self._project, self._users, username), None)

    def user_exists(self, username):
        return self._user_info(username) is not None

    def add_user(self, username='None', ip_address='None',
                 mac_address='None', registration_date='None'):
        if self.user_exists(username):
            raise UserExists
        if self.valid_ip_address(ip_address) and \
                self.valid_mac_address(mac_address) and self.valid_date(registration_date):
            self.db.put('{}/{}'.format(self._project, self._users), username, {self._ip_address: ip_address,
                                                                             self._mac_address: mac_address,
                                                                             self._registration_date: registration_date})
        else:
            raise NotValidArguments

    def get_ip_address(self, username='None'):
        if self.user_exists(username):
            return self._user_info(username)[self._ip_address]
        else:
            raise UserDoesNotExist

    def get_mac_address(self, username='None'):
        if self.user_exists(username):
            return self._user_info(username)[self._mac_address]
        else:
            raise UserDoesNotExist

    def get_registration_date(self, username='None'):
        if self.user_exists(username):
            return self._user_info(username)[self._registration_date]
        else:
            raise UserDoesNotExist

    def delete_user(self, username='None'):
        if self.user_exists(username):
            self.db.delete('{}/{}'.format(self._project, self._users), username)
        else:
            raise UserDoesNotExist


class UserDoesNotExist(Exception):
    pass


class UserExists(Exception):
    pass


class NotValidArguments(Exception):
    pass
