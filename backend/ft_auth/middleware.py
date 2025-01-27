import rest_framework_simplejwt
from ft_user.models import CustomUser
from django.shortcuts import render, redirect
import jwt
import re
from django.http import HttpResponse
from backend.settings import JWT_SECRET_KEY
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class CustomAuthentication:
	def __init__(self, get_response):
		self.get_response = get_response
		self.API_URLS = [
			re.compile(r'^(.*)test_home/'),
			# re.compile(r'^(.*)user/'),
		]
		self.PUBLIC_URLS = [
			re.compile(r'^(.*)callback/'),
			re.compile(r'^(.*)test/'),
			re.compile(r'^(.*)/auth/otp/'),
			re.compile(r'^(.*)/admin/'),
		]
	def __call__(self, request):
		# print(f'url is {request.path_info}')
		path = request.path_info.lstrip('/')
		valid_urls = (url.match(path) for url in self.API_URLS)
		public = (url.match(path) for url in self.PUBLIC_URLS)
		request_user = request.user
		print(f'{request_user}, {path}')
		request.token = request.COOKIES.get('access_token')
		if any(public):
			print('public')
			return self.get_response(request)
		if any(valid_urls):
			if request_user == None or request_user.is_anonymous:
				print('here')
				return JsonResponse({'error': 'Anonymous User'}, status=401)
			if request_user.is_authenticated:
				try:
					token = request.token #이부분은 이후 Header에서 Authorization으로 받아오는 방식으로 바꿔야함
					payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256']) #이거는 try except으로 해야함. 사이닝 키로 유효성검사와 동시에 성공시 페이로드 리턴받아옴.
					user = CustomUser.objects.get(uid=payload['uid'])
					if user == request_user:
						return self.get_response(request)
					else:
						print('not same user')
						return JsonResponse({'error': 'Not Same User'}, status=401)
				except:
					if not token:
						print('empty token4')
						return JsonResponse({'error': 'Empty Token'}, status=401)
					if jwt.exceptions.ExpiredSignatureError:
						print('empty token3')
						return JsonResponse({'error': 'Expired Token'}, status=401)
					else:
						print('empty token2')
						return JsonResponse({'error': 'Invalid Token'}, status=401)
			else:
				print('empty token1')
				return JsonResponse({'error': 'not user authenticated'}, status=401)
		return self.get_response(request)

class InsertJWT(MiddlewareMixin):
	def process_request(self, request):
		authorization = request.headers.get('Authorization')
		if authorization:
			request.token = authorization.split(' ')[1]
		else:
			request.token = None
		return None
