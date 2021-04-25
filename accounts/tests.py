from django.contrib.auth import get_user_model
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.core.exceptions import ValidationError
from .forms import RegisterationForm, LogInForm
from .views import RegisterView, HomePageView, LogInView
from .models import Account

class UserModelTest(TestCase):

    def test_create_user(self):

        User = get_user_model()
        user = User.objects.create_user(
            email="test111@email.com",
            password='testpass123'
        )

        self.assertEqual(user.email, "test111@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_user(email=None)

    def test_create_superuser(self):

        User = get_user_model()
        adminUser = User.objects.create_superuser(
            email='superuser111@email.com',
            password='testpass123'
        )

        self.assertEqual(adminUser.email, 'superuser111@email.com')
        self.assertTrue(adminUser.is_active)
        self.assertTrue(adminUser.is_staff)
        self.assertTrue(adminUser.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=None)


class RegisterViewTests(TestCase):

    def setUp(self):

        url = reverse('register')
        self.response = self.client.get(url)

    def test_register_template(self):

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/register.html')
        self.assertContains(self.response, '註冊')

    def test_register_view(self):
        view = resolve('/register/')
        self.assertEqual(
            view.func.__name__,
            RegisterView.__name__
        )

    def test_register_process(self):

        self.testNewUser = {
            'email': 'testNewUser@email.com',
            'password1': 'testing123',
            'password2': 'testing123',
        }

        # register and redirect to homepage
        self.response = self.client.post('/register/', self.testNewUser, follow=True)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'index.html')


class RegisterFormTest(TestCase):

    def test_fogot_email_error_messages(self):

        forgotEmail = {
            "email":"",
            "password1":"testing123",
            "password2":"testing123",
        }

        form = RegisterationForm(data=forgotEmail)
        self.assertEqual(
            form.errors['email'][0], "尚未輸入電子信箱"
        )

    def test_invaild_email_error_messages(self):

        invaildEmail = {
            "email":"failEmail@xxxxx",
            "password1":"testing123",
            "password2":"testing123",
        }

        form = RegisterationForm(data=invaildEmail)
        self.assertEqual(
            form.errors['email'][0], "請輸入有效電子信箱"
        )

    def test_forgot_password1_error_messages(self):

        forgotPassword1 = {
            "email":"failEmail@email.com",
            "password1":"",
            "password2":"testing123",
        }

        form = RegisterationForm(data=forgotPassword1)
        self.assertEqual(
            form.errors['password1'][0], "尚未輸入密碼"
        )

    def test_forgot_password2_error_messages(self):

        forgotPassword2 = {
            "email":"failEmail@email.com",
            "password1":"testing123",
            "password2":"",
        }

        form = RegisterationForm(data=forgotPassword2)
        self.assertEqual(
            form.errors['password2'][0], "尚未輸入確認密碼"
        )

    def test_two_password_different_error_messages(self):

        twoPasswordDifferent = {
            "email":"failEmail@email.com",
            "password1":"testing123",
            "password2":"testing123456",
        }

        form = RegisterationForm(data=twoPasswordDifferent)
        self.assertEqual(
            form.errors['password2'][0], "兩次密碼輸入不同"
        )


class LoginViewTests(TestCase):

    def setUp(self):

        url = reverse('login')
        self.response = self.client.get(url)

    def test_login_template(self):

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/login.html')
        self.assertContains(self.response, '登入')

    def test_login_view(self):

        view = resolve('/login/')
        self.assertEqual(
            view.func.__name__,
            LogInView.__name__
        )

    def test_success_login(self):

        User = get_user_model()
        user = User.objects.create_user(
            email="ExistedUser@email.com",
            password='testpass123'
        )
        self.ExistedUser = {
            "email":"ExistedUser@email.com",
            "password":"testpass123"
        }

        self.response = self.client.post('/login/', self.ExistedUser, follow=True)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'index.html')

    def test_fail_login(self):

        self.UserDoesNotExist = {
            "email":"UserDoesNotExist@email.com",
            "password":"testpass123"
        }

        self.response = self.client.post('/login/', self.UserDoesNotExist, follow=True)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/login.html')


# class LogInFormTest(TestCase):

#     def setUp(self):

#         User = get_user_model()
#         user = User.objects.create_user(
#             email="ExistedUser@email.com",
#             password='testpass123'
#         )

#         form = LogInForm(data={
#                 "email":"ExistedUser@email.com",
#                 "password":"testpass123"
#         })

#     def test_wrong_email_login_error_message(self):

#         # wrongEmail = {
#         #     "email":"WrongEmail@email.com",
#         #     "password":"testpass123"
#         # }

#         # form = LogInForm(data=wrongEmail)
#         # self.assertEqual(
#         #     form.errors['email'][0], "登入失敗，請確認電子信箱和密碼"
#         # )

#         with self.assertRaises(ValidationError) as errorMessage:

#             form = LogInForm(data={
#                 "email":"WrongEmail@email.com",
#                 "password":"testpass123"
#             })

#             self.assertEqual(
#                 "登入失敗，請確認電子信箱和密碼",
#                 str(errorMessage.expected_regexp)
#             )

#         # with self.assertRaises(ValueError) as errorMessage:
#         #     form = LogInForm(data={
#         #         "email":"ExistedUser@email.com",
#         #         "password":"wrongPassword"
#         #     })
#         #     self.assertEqual(
#         #         "登入失敗，請確認電子信箱和密碼",
#         #         str(errorMessage)
#         #     )



class HomepageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_homepage_url_resolves_homepageview(self): # new
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.__name__
        )
