'''
Project: Farnsworth

Author: Karandeep Singh Nagra
'''

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db import models

from utils.funcs import convert_to_url
from base.models import UserProfile

class Manager(models.Model):
    '''
    The Manager model.  Contains title, incumbent, and duties.
    '''
    title = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=255,
        help_text="The title of this management position.",
        )
    url_title = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        help_text="The unique URL key for this manager. Autogenerated from custom interface.",
        )
    incumbent = models.ForeignKey(
        UserProfile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The incumbent for this position.",
        )
    semester_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=settings.DEFAULT_WORKSHIFT_HOURS,
        help_text="Number of hours this manager receives during the fall and spring.",
        )
    summer_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=settings.DEFAULT_WORKSHIFT_HOURS,
        help_text="Number of hours this manager receives during the summer.",
        )
    compensation = models.TextField(
        blank=True,
        null=True,
        help_text="The compensation for this manager.",
        )
    duties = models.TextField(
        blank=True,
        null=True,
        help_text="The duties of this manager.",
        )
    email = models.EmailField(
        blank=True,
        null=True,
        max_length=255,
        help_text="The e-mail address of this manager.",
        )
    president = models.BooleanField(
        default=False,
        help_text="Whether this manager has president privileges (edit managers, bylaws, etc.).",
        )
    workshift_manager = models.BooleanField(
        default=False,
        help_text="Whether this manager has workshift manager privileges (assign workshifts, etc.).",
        )
    active = models.BooleanField(
        default=True,
        help_text="Whether this is an active manager position (visible in directory, etc.).",
        )

    def __unicode__(self):
        return self.title

    def is_manager(self):
        return True

    def __init__(self, *args, **kwargs):
        if "title" in kwargs:
            kwargs.setdefault("url_title", convert_to_url(kwargs["title"]))
        super(Manager, self).__init__(*args, **kwargs)

class RequestType(models.Model):
    '''
    A request type to specify relevant managers and name.
    '''
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        help_text="Name of the request type.",
        )
    url_name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        help_text="Unique URL key for this manager.  Autogenerated from custom interface.",
        )
    managers = models.ManyToManyField(
        Manager,
        help_text="Managers to whom this type of request is made.",
        )
    enabled = models.BooleanField(
        default=True,
        help_text="Whether this type of request is currently accepted. Toggle this to off to temporarily disable accepting this type of request.",
        )
    glyphicon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Glyphicon for this request type (e.g., cutlery).  Check Bootstrap documentation for more info.",
        )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def is_requesttype(self):
        return True

    def __init__(self, *args, **kwargs):
        if "name" in kwargs:
            kwargs.setdefault("url_name", convert_to_url(kwargs["name"]))
        super(RequestType, self).__init__(*args, **kwargs)

    def get_view_url(self):
        return reverse("managers:requests", kwargs={"requestType": self.url_name})

class Request(models.Model):
    '''
    The Request model.  Contains an owner, body, post_date, change_date, and relevant
    manager.
    '''
    owner = models.ForeignKey(
        UserProfile,
        blank=False,
        null=False,
        help_text="The user who made this request.",
        )
    body = models.TextField(
        blank=False,
        null=False,
        help_text="The body of this request.",
        )
    post_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The date this request was posted.",
        )
    change_date = models.DateTimeField(
        auto_now=True,
        help_text="The last time this request was modified.",
        )
    request_type = models.ForeignKey(
        RequestType,
        blank=False,
        null=False,
        help_text="The type of request this is.",
        )
    OPEN = 'O'
    CLOSED = 'C'
    FILLED = 'F'
    EXPIRED = 'E'
    STATUS_CHOICES = (
        (OPEN, "Open"),
        (CLOSED, "Closed"),
        (FILLED, "Filled"),
        (EXPIRED, "Expired"),
        )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OPEN,
        help_text="Status of this request."
        )
    number_of_responses = models.PositiveSmallIntegerField(
        default=0,
        help_text="The number of responses to this request.",
        )
    upvotes = models.ManyToManyField(
        UserProfile,
        blank=True,
        help_text="Up votes for this request.",
        related_name="up_votes",
        )
    followers = models.ManyToManyField(
        User,
        blank=True,
        help_text="Users following this request.",
        related_name="request_followers",
        )
    private = models.BooleanField(
        default=False,
        help_text="Only show this request to the manager, other members cannot view it.",
        )

    def __unicode__(self):
        return "{0.name} request by {1.owner}".format(self.request_type, self)

    @property
    def filled(self):
        return self.status == self.FILLED

    @property
    def open(self):
        return self.status == self.OPEN

    @property
    def closed(self):
        return self.status == self.CLOSED

    @property
    def expired(self):
        return self.status == self.EXPIRED

    class Meta:
        ordering = ['-post_date']

    def is_request(self):
        return True

    def get_view_url(self):
        return reverse("managers:view_request", kwargs={"request_pk": self.pk})

class Response(models.Model):
    '''
    The Response model.  A response to a request.  Very similar to Request.
    '''
    owner = models.ForeignKey(
        UserProfile,
        blank=False,
        null=False,
        help_text="The user who posted this response."
        )
    body = models.TextField(
        blank=False,
        null=False,
        help_text="The body of this response."
        )
    post_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The date this response was posted."
        )
    request = models.ForeignKey(
        Request,
        blank=False,
        null=False,
        help_text="The request to which this is a response."
        )
    manager = models.BooleanField(
        default=False,
        help_text="Whether this is a relevant manager response."
        )
    CLOSED = 'C'
    REOPENED = 'O'
    FILLED = 'F'
    EXPIRED = 'E'
    NONE = 'N'
    ACTION_CHOICES = (
        (NONE, "None"),
        (CLOSED, "Mark closed"),
        (REOPENED, "Mark open"),
        (FILLED, "Mark filled"),
        (EXPIRED, "Mark expired"),
    )
    action = models.CharField(
        max_length=1,
        choices=ACTION_CHOICES,
        default=NONE,
        help_text="A mark action (e.g., 'Marked closed'), if any."
        )

    def __unicode__(self):
        return self.owner.user.get_full_name()

    def display_action(self):
        if self.action != self.NONE:
            return '<div class="text-center"><hr style="width: 75%; margin-top: 0; margin-bottom: 0;" /></div><div class="field_wrapper text-info">Action: {0}</div>'.format(
                self.get_action_display()
                )
        return ""

    class Meta:
        ordering = ['post_date']

    def is_response(self):
        return True

class Announcement(models.Model):
    '''
    Model for manager announcements.
    '''
    manager = models.ForeignKey(
        Manager,
        blank=False,
        null=False,
        help_text="The manager who made this announcement.",
        )
    incumbent = models.ForeignKey(
        UserProfile,
        blank=False,
        null=False,
        help_text="The incumbent who made this announcement.",
        )
    body = models.TextField(
        blank=False,
        null=False,
        help_text="The body of the announcement.",
        )
    post_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The date this announcement was posted.",
        )
    pinned = models.BooleanField(
        default=False,
        help_text="Whether this announcment should be pinned permanently.",
        )
    change_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The last time this request was modified.",
        )

    def __unicode__(self):
        return self.incumbent.user.get_full_name()

    class Meta:
        ordering = ['-post_date']

    def is_announcement(self):
        return True
