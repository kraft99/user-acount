from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext



# class HttpResponseNotFound(HttpResponse):
#     def __init__(self, request):
#         super(HttpResponseNotFound, self).__init__(
#             content=render_to_string('404.html', context_instance=RequestContext(request)),
#             status=404
#         )


# class HttpResponseInternalServerError(HttpResponse):
#     def __init__(self, request):
#         super(HttpResponseIntServerError, self).__init__(
#             content=render_to_string('500.html', context_instance=RequestContext(request)),
#             status=500
#         )

# class HttpResponseUnauthorized(HttpResponse):
#     def __init__(self, request):
#         if request.user.is_authenticated():
#             super(HttpResponseUnauthorized, self).__init__(
#                 content=render_to_string('403.html', context_instance=RequestContext(request)),
#                 status=403
#             )
#         else:
#             super(HttpResponseUnauthorized, self).__init__(
#                 content=render_to_string('401.html', context_instance=RequestContext(request)),
#                 status=401
#             )
