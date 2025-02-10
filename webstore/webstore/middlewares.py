from django.utils.translation import get_language_from_request
from django.shortcuts import redirect
from django.utils.translation import activate

class LanguageRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':
            return redirect('/ru/')
        return self.get_response(request)

class LanguageMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = self.request.GET.get('lang')
        if lang:
            activate(lang)
            request.session['django_language'] = lang
        return self.get_response(request)