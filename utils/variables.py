'''
Project: Farnsworth

Author: Karandeep Singh Nagra

A set of variables used elsewhere in Farnsworth.
These should be things that are rarely or never changed in an implementation of Farnsworth.
'''

# The anonymous username.
ANONYMOUS_USERNAME = "spineless"

# List of time formats accepted by event forms.
time_formats = ['%m/%d/%Y %I:%M %p', '%m/%d/%Y %I:%M:%S %p', '%Y-%m-%d %H:%M:%S']

# Standard messages sent to clients on errors.
MESSAGES = {
	'ADMINS_ONLY': "You do not have permission to view the page you were trying to access.",
	'NO_PROFILE': "A profile for you could not be found.  Please contact a site admin.",
	'UNKNOWN_FORM': "Your post request could not be processed.  Please contact a site admin.",
	'MESSAGE_ERROR': "Your message post was not successful.  Please try again.",
	'THREAD_ERROR': "Your thread post was not successful.  Both subject and body are required.  Please try again.",
	'USER_ADDED': "User {username} was successfully added.",
	'PREQ_DEL': "Profile request by {first_name} {last_name} for username {username} successfully deleted.",
	'USER_PROFILE_SAVED': "User {username}'s profile has been successfully updated.",
	'USER_PW_CHANGED': "User {username}'s password has been successfully changed.",
	'EVENT_ERROR': "Your event post was not successful.  Please check for errors and try again.",
	'RSVP_ADD': "You've been successfully added to the list of RSVPs for {event}.",
	'RSVP_REMOVE': "You've been successfully removed from the list of RSVPs for {event}.",
	'EVENT_UPDATED': "Event {event} successfully updated.",
	'REQ_CLOSED': "Request successfully marked closed.",
	'REQ_FILLED': "Request successfully marked filled.",
	'SPINELESS': "You cannot modify the anonymous user profile.",
	'ANONYMOUS_EDIT': "THIS IS THE ANONYMOUS USER PROFILE.  IT IS HIGHLY RECOMMENDED THAT YOU NOT MODIFY IT.",
	'ANONYMOUS_DENIED': "Only superadmins are allowed to login the anonymous user or end the anonymous session.",
	'ANONYMOUS_LOGIN': "You have successfully logged out and started an anonymous session on this machine.",
	'ANONYMOUS_SESSION_ENDED': "You have successfully ended the anonymous session on this machine.",
	'RECOUNTED': "Thread messages and request responses successfully recounted.  {threads_changed} of {thread_count} threads and {requests_changed} of {request_count} requests were out-of-date and updated.",
	'ALREADY_PAST': "This event has already passed.  You can no longer RSVP to this event.",
	'LAST_SUPERADMIN': "You are the only superadmin in the database.  To prevent permanent system lock-out, you have been prevented from changing your own superadmin status.",
	'PRESIDENTS_ONLY': "This page is restricted to Presidents and superadmins.",
	'WORKSHIFT_MANAGER_ONLY': "This page is restricted to Workshift Managers and superadmins.",
	'NO_MANAGER': "The manager page {managerTitle} could not be found.",
	'NO_REQUEST_TYPE': "The request type {requestType} could not be found.",
	'MANAGER_ADDED': "Manager {managerTitle} has been successfully added.",
	'MANAGER_SAVED': "Manager {managerTitle} has been successfully saved.",
	'INVALID_FORM': "Your input could not be properly processed.  Please try again.",
	'INACTIVE_MANAGER': "{managerTitle} is currently deactivated.",
	'REQUEST_TYPE_ADDED': "Request type {typeName} has been successfully added.",
	'REQUEST_TYPE_SAVED': "Request type {typeName} has been successfully saved.",
}