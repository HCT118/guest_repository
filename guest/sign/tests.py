#coding=utf-8
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from django.test import Client
from datetime import datetime
from unittest import mock

from .views import index
from django.contrib.auth.models import User
from .models import Event, Guest
import time


# Create your tests here.
class IndexPageTest(TestCase):
    ''' 测试index登录首页'''

    def test_root_url_resolves_to_index_page(self):
        ''' 测试根url是否解析到登录页 '''
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_page_returns_correct_html(self):
        ''' 测试调用index函数返回的页与模板加载的index2.html是否相等 '''
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('index2.html')
        self.assertEqual(response.content.decode(), expected_html)



class LoginActionTest(TestCase):
    ''' 测试登录动作'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_author_email(self):
        ''' 测试添加用户 '''
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_error(self):
        ''' 用户名密码为空 '''
        c = Client()
        response = c.post('/login_action/', {'username':'','password':''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password null!", response.content)

    def test_login_action_username_password_error(self):
        ''' 用户名密码错误 '''
        c = Client()
        response = c.post('/login_action/', {'username':'abc','password':'123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        ''' 登录成功 '''
        c = Client()
        response = c.post('/login_action/', data = {'username':'admin','password':'admin123456'})
        self.assertEqual(response.status_code, 302)


class EventMangeTest(TestCase):
    ''' 发布会管理 '''

    def setUp(self):
        Event.objects.create(name="xiaomi5",limit=2000,address='beijing',status=1,start_time=datetime.now())


    def test_data(self):
        ''' 测试添加发布会 '''
        event = Event.objects.get(name="xiaomi5")
        self.assertEqual(event.address, "beijing")

    def test_event_mange_success(self):
        ''' 测试发布会:xiaomi5 '''
        c = Client()
        response = c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_mange_sreach_success(self):
        ''' 测试发布会搜索 '''
        c = Client()
        response = c.post('/sreach_name/',{"name":"xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    ''' 嘉宾管理 '''

    def setUp(self):
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address='beijing',status=1,start_time=datetime.now())
        Guest.objects.create(realname="alen",phone=18611001100,email='alen@mail.com',sign=0,event_id=1)


    def test_data(self):
        ''' 测试添加嘉宾 '''
        guest = Guest.objects.get(realname="alen")
        self.assertEqual(guest.phone, "18611001100")
        self.assertEqual(guest.email, "alen@mail.com")
        self.assertFalse(guest.sign)


    def test_event_mange_success(self):
        ''' 测试嘉宾信息: alen '''
        c = Client()
        response = c.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)


'''
运行所有用例：
python3 manage.py test

运行sign应用下的所有用例：
python3 manage.py test sign

运行sign应用下的tests.py文件用例：
python3 manage.py test sign.tests

运行sign应用下的tests.py文件中的 GuestManageTest 测试类：
python3 manage.py test sign.tests.GuestManageTest

......


'''