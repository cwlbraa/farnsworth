"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from threads.models import UserProfile, Thread
from managers.models import Manager, Announcement

class SimpleTest(TestCase):
	def test_basic_addition(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		self.assertEqual(1 + 1, 2)

class VerifyUser(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(username="u", email="u@email.com", password="pwd")
		self.u.save()

	def test_user_profile_created(self):
		''' Test that the user profile for a user is automatically created when a user is created. '''
		self.assertEqual(1, UserProfile.objects.filter(user=self.u).count())
		self.assertEqual(self.u, UserProfile.objects.get(user=self.u).user)

	def test_login(self):
		self.assertEqual(True, self.client.login(username="u", password="pwd"))
		self.assertEqual(None, self.client.logout())

	def test_homepage(self):
		response = self.client.get("/")
		self.assertRedirects(response, "/landing/", status_code=302,
				     target_status_code=200)
		self.client.login(username="u", password="pwd")
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)
		self.client.logout()
		response = self.client.get("/")
		self.assertRedirects(response, "/landing/", status_code=302,
				     target_status_code=200)

class VerifyThread(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(username="u", email="u@email.com", password="pwd")
		self.u.save()
		profile = UserProfile.objects.get(user=self.u)
		self.thread = Thread(owner=profile, subject="subject")
		self.thread.save()

	def test_thread_created(self):
		self.assertEqual(1, Thread.objects.all().count())
		self.assertEqual(self.thread, Thread.objects.get(pk=self.thread.pk))
		self.assertEqual(1, Thread.objects.filter(subject="subject").count())

class FromHome(TestCase):
	def setUp(self):
		self.su = User.objects.create_user(username="su", email="su@email.com", password="pwd")
		self.su.save()

		self.manager = Manager(title="Super Manager", url_title="super")
		self.manager.incumbent = UserProfile.objects.get(user=self.su)
		self.manager.save()

	def test_thread_post(self):
		self.client.login(username="su", password="pwd")

		response = self.client.post("/", {
				"submit_thread_form": "",
				"subject": "Thread Subject Test",
				"body": "Thread Body Text Test",
				 }, follow=True)
		self.assertRedirects(response, "/")
		self.assertIn("Thread Subject Test", response.content)

		thread = Thread.objects.get(subject="Thread Subject Test")
		user = User.objects.get(username="su")
		profile = UserProfile.objects.get(user=user)
		self.assertEqual(thread.owner, profile)
		thread.delete()

		self.client.logout()

	def test_announcment_post(self):
		self.client.login(username="su", password="pwd")

		response = self.client.post("/", {
				"post_announcement": "",
				"as_manager": "1",
				"body": "Announcement Body Text Test",
				}, follow=True)
		self.assertRedirects(response, "/")
		self.assertIn("Announcement Body Text Test", response.content)

		announcement = Announcement.objects.get(body="Announcement Body Text Test")
		user = User.objects.get(username="su")
		profile = UserProfile.objects.get(user=user)
		self.assertEqual(announcement.incumbent, profile)
		announcement.delete()

		self.client.logout()
