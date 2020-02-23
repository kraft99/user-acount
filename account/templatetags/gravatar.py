# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import hashlib

from django.utils.http import urlencode, urlquote
from django import template

register = template.Library()

# @register.simple_tag()
# def get_gravatar_url(user, size, rating='g', default='identicon'):
#     url = "https://www.gravatar.com/avatar/"
#     hash = hashlib.md5(user.email.strip().lower().encode('utf-8')).hexdigest()
#     data = urlencode([('d', urlquote(default)),
#                       ('s', str(size)),
#                       ('r', rating)])
#     return "".join((url, hash, '?', data))

'''
@use in templates.

{% load gravatarr %}

<img class="profile-avatar" src="{% get_gravatar_url request.user size=200 %}" />

'''


@register.simple_tag()
def get_gravatar_url(email, size, rating='g', default='identicon'):
    url = "https://www.gravatar.com/avatar/"
    hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    data = urlencode([('d', urlquote(default)),
                      ('s', str(size)),
                      ('r', rating)])
    return "".join((url, hash, '?', data))


'''
@use in templates.

{% load gravatarr %}

<img class="profile-avatar" src="{% get_gravatar_url email size=200 %}" />
or 
<img class="profile-avatar" src="{% get_gravatar_url user.email size=200 %}" />

'''