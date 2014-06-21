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

# The e-mail subject used when sending profile request approval messages.
APPROVAL_SUBJECT = u"[Farnsworth - {house}] Welcome to {house}"

# The e-mail template used when sending profile request approval messages.
# username_bit should be "the username and password you selected",
# "the username <username> and the password you selected",
# or "<OAuth_provider.title()>" depending on whether the original username provided by the user was used to
# create the new user.
APPROVAL_EMAIL = u'''Dear {full_name},

Your request for an account on the house site for {house} has been approved.
You may now login at {login_url} using {username_bit}.

A profile request using this e-mail address and the name above was submitted to us on {request_date}.
If you believe this was done in error, please e-mail us at {admin_email} immediately.

Thank you,
{admin_name}
{house} Site Admin




This message was auto-generated by Farnsworth (https://www.github.com/knagra/farnsworth).'''

# The e-mail subject used when sending profile request deletion messages.
DELETION_SUBJECT = u"[Farnsworth - {house}] Profile Request Deleted"

# The e-mail template used when sending profile request approval messages.
DELETION_EMAIL = u'''Dear {full_name},

Your request for an account on the house site for {house} has been rejected.
All the information you have provided has been permanently deleted from our database.

If you believe this was done in error, please contact us at {admin_email}.

Thank you,
{admin_name}
{house} Site Admin




This message was auto-generated by Farnsworth (https://www.github.com/knagra/farnsworth).'''

# The e-mail subject used when sending profile request submission messages.
SUBMISSION_SUBJECT = u"[Farnsworth - {house}] Profile Request Received"

# The e-mail template used when sending profile request submission messages.
SUBMISSION_EMAIL = u'''Dear {full_name},

Your request for a profile on the house website for {house} has been received.
If you did not make this request or you are not {full_name}, please contact us at {admin_email} immediately.

Thank you,
{admin_name}
{house} Site Admin




This message was auto-generated by Farnsworth (https://www.github.com/knagra/farnsworth).'''

# A tuple of random substrings to show underneath the 404 title in the 404 page.
SUBTEXTS_404 = (u"The number you have dialed has crashed into a planet.  Please make a note of it.",
	u"Good news, everyone!  Wait, that's not good news...",
	u"I could fix this, but...well, I am already in my pajamas.",
	u"Aaahhh...to be young again...and also a 404 page.",
	u"You take one nap in a ditch in the park, and people start declaring you this and that!",
	u"Oh my, yes.",
	u"Better yet, I'll build a page to replace it for you.  Some kind of gamma-powered mechanical monster, with freeway on-ramps for arms and a heart as black as coal...",
	u"We tore the universe a new space-hole, all right.  And now it's clenching shut.",
	u"You still have your old pal Zoidberg.  YOU ALL HAVE ZOIDBERG!!!",
	u"Woob woob woob woob woob!",
	u"Science cannot move forward without heaps!",
	u"It's nothing a lawsuit won't cure.",
	u"Well, we're boned.",
	u"Sweet Yeti of the Serengeti! She's gone crazy Eddie in the heady!",
	u"I'm back, baby!",
	u"Let's go, alreadaaaay!",
	u"Yeah, well, I'm gonna go make my own page.  With blackjack.  And hookers! In fact, forget the page!",
	u"Fine, I'll go build my own 404 page.  With blackjack.  And hookers!  In fact, forget the 404 page and the blackjack!  Eeeh, screw the whole thing!",
	u"Kill all humans...kill all humans...",
	u"Like most of life's problems, this one can be solved by bending.",
	u"Tempers are wearing thin.  Let's just hope some 404 page doesn't kill everybody.",
	u"It worked for me.  I used to be a little blonde girl named Virginia.",
	u"Maybe it's time to leave the science to the hundred and twenty year olds.",
	u"Let's face it, comedy is a dead artform.  Now, tragedy...that's funny.",
	u"The web page that browses back.",
	u"One word: Thundercougarfalconbird.",
	u"Nothing makes you feel more like a man than a Thundercougarfalconbird.",
	u"You've come to the Wong place.",
	u"I'm a cold-blooded punk.",
	u"A byproduct of the web development industry.",
	u"Made you look!",
	u"This time, it's personal.",
	u"Provides a full day's supply of vitamin F!",
	)

# Standard messages sent to clients on errors.
MESSAGES = {
	'ADMINS_ONLY': u"You do not have permission to view the page you were trying to access.",
	'ADMIN_PASSWORD': u"You are not allowed to change your own password from this page.",
	'SELF_DELETE': u"You are not allowed to delete yourself.",
	'NO_PROFILE': u"A profile for you could not be found.  Please contact a site admin.",
	'UNKNOWN_FORM': u"Your post request could not be processed.  Please contact a site admin.",
	'MESSAGE_ERROR': u"Your message post was not successful.  Please try again.",
	'THREAD_ERROR': u"Your thread post was not successful.  Both subject and body are required.  Please try again.",
	'USER_ADDED': u"User {username} was successfully added.",
	'USER_DELETED': u"User {username} was successfully deleted.",
	'PREQ_DEL': u"Profile request by {first_name} {last_name} for username {username} successfully deleted.",
	'USER_PROFILE_SAVED': u"User {username}'s profile has been successfully updated.",
	'USER_PW_CHANGED': u"User {username}'s password has been successfully changed.",
	'PASSWORD_UNHASHABLE': u"Could not hash password.  Please try again.",
	'PROFILE_SUBMITTED': u"Your request has been submitted.  An admin will contact you soon.",
	'PROFILE_TAKEN': u"An account request for {first_name} {last_name} has already been made.",
	'USERNAME_TAKEN': u"This username is taken.  Try one of {username}_1 through {username}_10.",
	'RESET_MESSAGE': u'Forgot your password? You can reset it at <a href="{reset_url}" class="alert-link">{reset_url}</a>.',
	'PROFILE_REQUEST_RESET': u'You already have an account on this site. Forgot your password? You can reset it at <a href="{reset_url}" class="alert-link">{reset_url}</a>.',
	'INVALID_LOGIN': u'Invalid username/password combination.',
	'EMAIL_TAKEN': u"This e-mail address is already taken.",
	'INVALID_USERNAME': u'Invalid username. Must be characters A-Z, a-z, 0-9, or _.',
	'EVENT_ERROR': u"Your event post was not successful.  Please check for errors and try again.",
	'RSVP_ADD': u"You've been successfully added to the list of RSVPs for {event}.",
	'RSVP_REMOVE': u"You've been successfully removed from the list of RSVPs for {event}.",
	'EVENT_UPDATED': u"Event {event} successfully updated.",
	'REQ_CLOSED': u"Request successfully marked closed.",
	'REQ_FILLED': u"Request successfully marked filled.",
	'SPINELESS': u"You cannot modify the anonymous user profile.",
	'ANONYMOUS_EDIT': u"THIS IS THE ANONYMOUS USER PROFILE.  IT IS HIGHLY RECOMMENDED THAT YOU NOT MODIFY IT. IT SHOULD BE INACTIVE TO PREVENT USERS FROM TRYING TO MANUALLY LOGIN AS THE ANONYMOUS USER.",
	'ANONYMOUS_DENIED': u"Only superadmins are allowed to login the anonymous user or end the anonymous session.",
	'ANONYMOUS_LOGIN': u"You have successfully logged out and started an anonymous session on this machine.",
	'ANONYMOUS_SESSION_ENDED': u"You have successfully ended the anonymous session on this machine.",
	'RECOUNTED': u"Thread messages and request responses successfully recounted.  {threads_changed} of {thread_count} threads and {requests_changed} of {request_count} requests were out-of-date and updated.",
	'ALREADY_PAST': u"This event has already passed.  You can no longer RSVP to this event.",
	'LAST_SUPERADMIN': u"You are the only superadmin in the database.  To prevent permanent system lock-out, you have been prevented from changing your own superadmin status.",
	'PRESIDENTS_ONLY': u"This page is restricted to Presidents and superadmins.",
	'WORKSHIFT_MANAGER_ONLY': u"This page is restricted to Workshift Managers and superadmins.",
	'NO_MANAGER': u"The manager page {managerTitle} could not be found.",
	'NO_REQUEST_TYPE': u"The request type {requestType} could not be found.",
	'MANAGER_ADDED': u"Manager {managerTitle} has been successfully added.",
	'MANAGER_SAVED': u"Manager {managerTitle} has been successfully saved.",
	'INVALID_FORM': u"Your input could not be properly processed.  Please try again.",
	'INACTIVE_MANAGER': u"{managerTitle} is currently deactivated.",
	'REQUEST_TYPE_ADDED': u"Request type {typeName} has been successfully added.",
	'REQUEST_TYPE_SAVED': u"Request type {typeName} has been successfully saved.",
	'PROFILE_REQUEST_APPROVAL_EMAIL': u' A profile request approval e-mail was successfully sent to {full_name} at <a title="Write E-mail" href="mailto:{email}" class="alert-link">{email}</a>.', # The initial space is necessary.
	'PROFILE_REQUEST_DELETION_EMAIL': u' A profile request deletion e-mail was successfully sent to {full_name} at <a title="Write E-mail" href="mailto:{email}" class="alert-link">{email}</a>.', # The initial space is necessary.
	'EMAIL_FAIL': u'Farnsworth failed at sending an e-mail to <a title="Write E-mail" href="mailto:{email}" class="alert-link">{email}</a>.',
}
