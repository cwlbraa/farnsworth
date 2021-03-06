'''
Project: Farnsworth

Author: Karandeep Singh Nagra
'''

from django import forms

from notifications import notify

from threads.models import Thread, Message

class ThreadForm(forms.ModelForm):
    ''' Form to post a new thread. '''
    body = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Thread
        fields = ("subject",)
        help_texts = {
            "subject": "",
            }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        super(ThreadForm, self).__init__(*args, **kwargs)

    def save(self):
        thread = super(ThreadForm, self).save(commit=False)
        thread.owner = self.profile
        thread.save()
        Message.objects.create(
            body=self.cleaned_data['body'],
            owner=self.profile,
            thread=thread,
            )
        return thread

class MessageForm(forms.ModelForm):
    ''' Form to post a new message. '''
    class Meta:
        model = Message
        fields = ("body",)
        help_texts = {
            "body": "",
            }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        self.thread = kwargs.pop('thread')
        super(MessageForm, self).__init__(*args, **kwargs)

    def save(self):
        message = super(MessageForm, self).save(commit=False)
        message.owner = self.profile
        message.thread = self.thread
        message.save()

        for follower in self.thread.followers.all():
            notify.send(self.profile.user, verb="posted", action_object=message,
                        target=self.thread, recipient=follower)

        return message

class FollowThreadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        self.profile = kwargs.pop("profile")
        super(FollowThreadForm, self).__init__(*args, **kwargs)

    def save(self):
        if self.profile.user in self.instance.followers.all():
            self.instance.followers.remove(self.profile.user)
            following = False
        else:
            self.instance.followers.add(self.profile.user)
            following = True
        self.instance.save()
        return following

class EditThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ("subject",)
        help_texts = {
            "subject": "",
            }

class DeleteMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ()

    def save(self):
        message = super(DeleteMessageForm, self).save()
        thread = message.thread
        message.delete()

        if thread.number_of_messages > 1:
            return thread

class EditMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("body",)
        help_texts = {
            "body": "",
            }

    def save(self):
        message = super(EditMessageForm, self).save()
        message.edited = True
        message.save()
