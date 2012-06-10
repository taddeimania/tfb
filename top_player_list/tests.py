import unittest
from django.contrib.auth.models import User
from django.http import HttpRequest
import mock
from top_player_list import views

class TopPlayerListTests(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = User()

    @mock.patch('top_player_list.views.get_top_ten_for_pos')
    def test_does_this_work(self, top_ten):
        views.playerpage(self.request, arg="TOP")
        self.assertEqual(5, top_ten.call_count)