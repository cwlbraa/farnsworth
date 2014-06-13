'''
Project: Farnsworth

Author: Karandeep Singh Nagra
'''

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages

from farnsworth.settings import max_threads, max_messages
from utils.variables import MESSAGES
from base.models import UserProfile
from base.decorators import profile_required
from threads.models import Thread, Message
from threads.forms import ThreadForm, MessageForm

def _threads_dict(threads):
	# A pseudo-dictionary, actually a list with items of form
	# (thread.subject, [thread_messages_list], thread.pk, number_of_more_messages)
	threads_dict = list()
	x = 0
	for thread in threads:
		y = 0 # number of messages loaded
		thread_messages = list()
		for message in Message.objects.filter(thread=thread).reverse():
			thread_messages.append(message)
			y += 1
			if y >= max_messages:
				break
		more_messages = thread.number_of_messages - max_messages
		if more_messages < 0:
			more_messages = 0
		thread_messages.reverse()
		threads_dict.append((thread.subject, thread_messages, thread.pk, more_messages))
		x += 1
		if x >= max_threads:
			break
	return threads_dict

@profile_required
def member_forums_view(request):
	''' Forums for current members. '''
	page_name = "Member Forums"
	userProfile = UserProfile.objects.get(user=request.user)
	thread_form = ThreadForm(
		request.POST if 'submit_thread_form' in request.POST else None,
		profile=userProfile,
		)
	message_form = MessageForm(
		request.POST if 'submit_message_form' in request.POST else None,
		profile=userProfile,
		)

	if thread_form.is_valid():
		thread_form.save()
		return HttpResponseRedirect(reverse('member_forums'))
	elif 'submit_thread_form' in request.POST:
		messages.add_message(request, messages.ERROR, MESSAGES['THREAD_ERROR'])
	if message_form.is_valid():
		message_form.save()
		return HttpResponseRedirect(reverse('member_forums'))
	elif 'submit_message_form' in request.POST:
		messages.add_message(request, messages.ERROR, MESSAGES['MESSAGE_ERROR'])
	threads_dict = _threads_dict(Thread.objects.all())
	return render_to_response('threads.html', {
			'page_name': page_name,
			'thread_title': 'Active Threads',
			'threads_dict': threads_dict,
			'thread_form': thread_form,
			}, context_instance=RequestContext(request))

@profile_required
def all_threads_view(request):
	''' View of all threads. '''
	page_name = "Archives - All Threads"
	userProfile = UserProfile.objects.get(user=request.user)
	thread_form = ThreadForm(
		request.POST if 'submit_thread_form' in request.POST else None,
		profile=userProfile,
		)
	message_form = MessageForm(
		request.POST if 'submit_message_form' in request.POST else None,
		profile=userProfile,
		)

	if thread_form.is_valid():
		thread_form.save()
		return HttpResponseRedirect(reverse('all_threads'))
	elif 'submit_thread_form' in request.POST:
		messages.add_message(request, messages.ERROR, MESSAGES['THREAD_ERROR'])
	if message_form.is_valid():
		message_form.save()
		return HttpResponseRedirect(reverse('all_threads'))
	elif 'submit_message_form' in request.POST:
		messages.add_message(request, messages.ERROR, MESSAGES['MESSAGE_ERROR'])

	threads_dict = _threads_dict(Thread.objects.all())
	return render_to_response('threads.html', {
			'page_name': page_name,
			'thread_title': 'Archives - All Threads',
			'threads_dict': threads_dict,
			'thread_form': thread_form,
			}, context_instance=RequestContext(request))

@profile_required
def my_threads_view(request):
	''' View of my threads. '''
	page_name = "My Threads"
	userProfile = UserProfile.objects.get(user=request.user)
	thread_form = ThreadForm(
		request.POST if 'submit_thread_form' in request.POST else None,
		profile=userProfile,
		)
	message_form = MessageForm(
		request.POST if 'submit_message_form' in request.POST else None,
		profile=userProfile,
		)

	if thread_form.is_valid():
		thread_form.save()
		return HttpResponseRedirect(reverse('my_threads'))
	elif 'submit_thread_form' in request.POST:
		messages.add_message(request, messages.ERROR, MESSAGES['THREAD_ERROR'])
	if message_form.is_valid():
		message_form.save()
		return HttpResponseRedirect(reverse('my_threads'))
	elif 'submit_message_form' in request.POST:
		messages.add_message(request, messages.ERROR, MESSAGES['MESSAGE_ERROR'])

	threads_dict = _threads_dict(Thread.objects.filter(owner=userProfile))
	return render_to_response('threads.html', {
			'page_name': page_name,
			'thread_title': 'My Threads',
			'threads_dict': threads_dict,
			'thread_form': thread_form,
			}, context_instance=RequestContext(request))

@profile_required
def list_my_threads_view(request):
	''' View of my threads. '''
	userProfile = UserProfile.objects.get(user=request.user)
	threads = Thread.objects.filter(owner=userProfile)
	return render_to_response('list_threads.html', {
			'page_name': "My Threads",
			'threads': threads,
			}, context_instance=RequestContext(request))

@profile_required
def list_user_threads_view(request, targetUsername):
	''' View of my threads. '''
	if targetUsername == request.user.username:
		return list_my_threads_view(request)
	targetUser = get_object_or_404(User, username=targetUsername)
	targetProfile = get_object_or_404(UserProfile, user=targetUser)
	threads = Thread.objects.filter(owner=targetProfile)
	page_name = "%s's Threads" % targetUsername
	return render_to_response('list_threads.html', {
			'page_name': page_name,
			'threads': threads,
			'targetUsername': targetUsername,
			}, context_instance=RequestContext(request))

@profile_required
def list_all_threads_view(request):
	''' View of my threads. '''
	threads = Thread.objects.all()
	return render_to_response('list_threads.html', {
			'page_name': "Archives - All Threads",
			'threads': threads,
			}, context_instance=RequestContext(request))

@profile_required
def thread_view(request, thread_pk):
	''' View an individual thread. '''
	userProfile = UserProfile.objects.get(user=request.user)
	thread = get_object_or_404(Thread, pk=thread_pk)
	messages_list = Message.objects.filter(thread=thread)
	message_form = MessageForm(
		request.POST or None,
		profile=userProfile,
		initial={'thread_pk': thread_pk},
		)
	if message_form.is_valid():
		message_form.save()
		return HttpResponseRedirect(reverse('view_thread', kwargs={
					'thread_pk': thread_pk,
					}))
	elif 'submit_message_form' in request.POST:
		messages.add_message(request, messages.ERROR, MESSAGES['MESSAGE_ERROR'])
	return render_to_response('view_thread.html', {
			'thread': thread,
			'page_name': "View Thread",
			'messages_list': messages_list,
			}, context_instance=RequestContext(request))
