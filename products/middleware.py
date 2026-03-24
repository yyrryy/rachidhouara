from django.shortcuts import redirect

class AdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and not user.groups.filter(name='admin').exists():
            return redirect('main:logoutuser')

        response = self.get_response(request)
        return response
