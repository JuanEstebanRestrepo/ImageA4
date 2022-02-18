from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserImage
from .views import verify_file_name
import os
from dotenv import load_dotenv

load_dotenv()


class AccessTestCase(TestCase):

	def test_home_without_login_redirect(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_login_loads_properly(self):
		response = self.client.get('/login')
		self.assertEqual(response.status_code, 200)

	def test_register_loads_properly(self):
		response = self.client.get('/register')
		self.assertEqual(response.status_code, 200)

	def test_logout_without_login_redirect(self):
		response = self.client.get('/logout')
		self.assertRedirects(response, '/', status_code=302, 
							target_status_code=200, fetch_redirect_response=True)


class UserTest(TestCase):

	def setUp(self):
		self.user_data_test = {
			
			'username': os.getenv('TEST_USER'),
			'password': os.getenv('TEST_PASS'),
			'email': os.getenv('TEST_EMAIL'),
      	}	

		User.objects.create_user(**self.user_data_test)
		
		self.user_data_register = {
			'csrfmiddlewaretoken': ['s1JWwnHP01hYhO3MF3tY7I63j72M8sy00naoXYTG7hmjS20JOoTsE8VzO0GDdJPI'], 
			'username': ['user_test'], 
			'email': ['user_test@gmail.com'], 
			'password1': ['1234pass'], 
			'password2': ['1234pass']
		}
		
	def test_user_register(self):
		response = self.client.post('/register', data=self.user_data_register, follow=True)
		self.assertEqual(response.status_code, 200)
		user = User.objects.last()
		self.assertEqual(user.username, 'user_test')
		
	def test_user_login(self):
		response = self.client.post('/login', data=self.user_data_test, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['user'].is_authenticated)

class Image(TestCase):

	def setUp(self):
		self.user_data_test = {
			'username': os.getenv('TEST_USER'),
			'password': os.getenv('TEST_PASS'),
			'email': os.getenv('TEST_EMAIL'),
      	}	

		User.objects.create_user(**self.user_data_test)

		self.image_data_test = {
			'name': 'imagen_de_prueba',
			'description': 'descripcion',
			'image': 'images/paisaje.jpg', 
			'user_id': 1, 
			'original_height': '632', 
			'original_width': '1123', 
			'resize_height': '632', 
			'resize_width': '1123', 
      	}

		UserImage.objects.create(**self.image_data_test)

	def test_verify_file_name(self):
		file_name = 'paisaje.jpg'
		response = verify_file_name(file_name)
		self.assertEqual(response, '(copia1)'+file_name)

