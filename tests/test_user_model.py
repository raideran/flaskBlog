import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, Permission, AnonymousUser, Role


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all() 
        self.app_context.pop()

    def test_password_setter(self):
        user = User(password='cat')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password='cat')
        with self.assertRaises(AttributeError):
            user.password
    
    def test_password_verification(self):
        user = User(password='cat')
        self.assertTrue(user.verify_password('cat'))
        self.assertFalse(user.verify_password('dog'))

    def test_password_salts_are_random(self):
        user = User(password='cat')
        user2 = User(password='cat')
        self.assertTrue(user.password_hash != user2.password_hash)

    def test_valid_confirmation_token(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        self.assertTrue(user.confirm_token(token))

    def test_invalid_confirmation_token(self):
        user1 = User(password='cat')
        user2 = User(password='dog')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user1.generate_confirmation_token()
        self.assertFalse(user2.confirm_token(token))

    def test_expired_confirmation_token(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(user.confirm_token(token))

    def test_valid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    def test_invalid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + bytes('a'.encode('utf-8')), 'horse'))
        self.assertTrue(u.verify_password('cat'))

    def test_valid_email_change_token(self):
        u = User(email='john@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('susan@example.org')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'susan@example.org')

    def test_invalid_email_change_token(self):
        u1 = User(email='john@example.com', password='cat')
        u2 = User(email='susan@example.org', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_email_change_token('david@example.net')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'susan@example.org')

    def test_duplicate_email_change_token(self):
        u1 = User(email='john@example.com', password='cat')
        u2 = User(email='susan@example.org', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token('john@example.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'susan@example.org')

    def test_user_role(self):
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_timestamps(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.member_since).total_seconds() < 3)
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)