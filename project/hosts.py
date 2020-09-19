from django_hosts import patterns, host

from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', 'rowan.urls.rowan', name='www'),
    host(r'challenges', 'project.urls', name='challenges'),
    host(r'wedding', 'wedding.urls.wedding', name='wedding'),
)
