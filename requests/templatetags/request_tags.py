'''
Project: Farnsworth

Author: Karandeep Singh Nagra
'''

from django import template

register = template.Library()

@register.filter
def count_votes(value):
	''' Return the net vote count for value, which is a Request. '''
	return value.upvotes.count() - value.downvotes.count()