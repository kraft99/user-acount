import uuid
import socket

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


# def get_client_ip(request):
#     ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
#     if ip:
#         return ip.split(",")[0].strip()
#     return request.META.get("REMOTE_ADDR", None)


def visitor_ip_address(request):
	x_forwarded_for = request.META.get('HTTP_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def is_valid_ip_address(ip = None):
	if not ip is None:
		try:
			socket.inet_aton(ip)
			ip_valid = True
		except (AttributeError,socket.error):
			return False
		return ip_valid



def activation_token():
	token_ = str(uuid.uuid4()).replace('-','')
	return urlsafe_base64_encode(force_bytes(token_))

'''
Guide.

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text

mssg = 'hello universe'

encode_mssg = urlsafe_base64_encode(force_bytes(mssg))

`aGVsbG8gdW5pdmVyc2U` 


decode_mssg = force_text(urlsafe_base64_decode(encode_mssg))

`hello universe`

'''

