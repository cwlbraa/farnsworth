"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import utc
from base.models import UserProfile
from threads.models import Thread, Message
from managers.models import Manager, Announcement, RequestType, Request
from events.models import Event

class VerifyThread(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(username="u", password="pwd")

		self.profile = UserProfile.objects.get(user=self.u)

		self.thread = Thread(owner=self.profile, subject="Default Thread Test")
		self.thread.save()

		self.message = Message(owner=self.profile, body="Default Reply Test",
							   thread=self.thread)
		self.message.save()

		self.client.login(username="u", password="pwd")

	def test_thread_created(self):
		self.assertEqual(1, Thread.objects.all().count())
		self.assertEqual(self.thread, Thread.objects.get(pk=self.thread.pk))
		self.assertEqual(1, Thread.objects.filter(subject=self.thread.subject).count())
		self.assertEqual(0, Thread.objects.filter(subject="Tabboo").count())

	def test_thread_created(self):
		urls = [
			"/",
			"/threads/",
			"/threads/{0}/".format(self.thread.pk),
			"/threads/all/",
            "/threads/list/",
			"/my_threads/",
			"/profile/{0}/threads/".format(self.u.username),
			]

		for url in urls:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 200)
			self.assertIn(self.thread.subject, response.content)

	def test_create_thread(self):
		urls = [
			"/my_threads/",
			"/threads/",
			"/threads/all/",
			]
		subject = "Thread Subject Test"
		body = "Thread Body Test"
		for url in urls:
			response = self.client.post(url, {
					"submit_thread_form": "",
					"subject": subject,
					"body": body,
					}, follow=True)
			self.assertRedirects(response, url)
			self.assertIn(subject, response.content)
			self.assertIn(body, response.content)

			thread = Thread.objects.get(subject=subject)

			self.assertNotEqual(thread, None)
			self.assertEqual(Message.objects.filter(thread=thread).count(), 1)
			self.assertEqual(Message.objects.get(thread=thread).body, body)

			thread.delete()

	def test_post_reply(self):
		urls = [
			"/threads/",
			"/threads/{0}/".format(self.thread.pk),
			"/threads/all/",
			]
		body = "Reply Body Test"
		for url in urls:
			response = self.client.post(url, {
					"submit_message_form": "",
					"thread_pk": "{0}".format(self.thread.pk),
					"body": body,
					}, follow=True)
			self.assertRedirects(response, url)
			self.assertIn(body, response.content)

			thread = Thread.objects.get(pk=self.thread.pk)

			self.assertNotEqual(thread, None)
			self.assertEqual(Message.objects.filter(thread=thread).count(), 2)

			message = Message.objects.get(thread=thread, body=body)

			self.assertNotEqual(message, None)

			message.delete()
