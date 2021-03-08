from barbados.objects.base import BaseObject


class User(BaseObject):
    def __init__(self, id, email, username, last_login_at,
                 current_login_at, last_login_ip, current_login_ip,
                 login_count, active, fs_uniquifier, confirmed_at,
                 roles):
        self.id = id
        self.email = email
        self.username = username
        self.last_login_at = last_login_at
        self.current_login_at = current_login_at
        self.last_login_ip = last_login_ip
        self.current_login_ip = current_login_ip
        self.login_count = login_count
        self.active = active
        self.fs_uniquifier = fs_uniquifier
        self.confirmed_at = confirmed_at
        self.roles = roles

    def __repr__(self):
        return "Barbados::Objects::User[]>"

    def serialize(self, serializer):
        serializer.add_property('id', self.id)
        serializer.add_property('email', self.email)
        serializer.add_property('username', self.username)
        serializer.add_property('last_login_at', self.last_login_at)
        serializer.add_property('current_login_at', self.current_login_at)
        serializer.add_property('last_login_ip', self.last_login_ip)
        serializer.add_property('current_login_ip', self.current_login_ip)
        serializer.add_property('login_count', self.login_count)
        serializer.add_property('active', self.active)
        serializer.add_property('fs_uniquifier', self.fs_uniquifier)
        serializer.add_property('confirmed_at', self.confirmed_at)
        serializer.add_property('roles', self.roles)
