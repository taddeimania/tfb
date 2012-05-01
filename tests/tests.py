"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
import unittest
from players.models import *
from django.db.models import Q
from django.contrib.auth.models import User
from myproject import views

USERNAME = 'what'
EMAIL = 'jtaddei@gmail.com'

class TFBTests(unittest.TestCase):
    def test_user_created(self):
        ''' Create a User, associates a UserProfile table entry with it.
            2 test cases to ensure querysets are returning the correct results.
        '''
        user = User.objects.create_user(USERNAME, EMAIL, 'salt')
        user1 = User.objects.create_user('butt', 'butt@head.com', 'salt')
        userQS = UserProfile.objects.get(user__username = USERNAME)
        user1QS = UserProfile.objects.get(user__email = 'butt@head.com')
        self.assertEqual(user.userprofile.user.id, userQS.user.id)       # This superfulous (circular?) join does serve a purpose.
        self.assertEqual(user1.userprofile.user.id, user1QS.user.id)      # It ensures the UserProfile table is populated correctly
    
    def test_setting_userprofile_attr(self):
        ''' Create a user (why wont it reuse above user?) and set it's userpic
            attribute.  Verify attribute is updated.
        '''
        _user = User.objects.create_user(USERNAME, EMAIL, 'salt')
        _userQS = UserProfile.objects.get(user__username = USERNAME)
        _userQS.userpic = '1e'
        self.assertEqual(_userQS.userpic, '1e')
