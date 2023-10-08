class UsernameCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            response.set_cookie('username', request.user.username)
        elif 'username' in request.COOKIES:
            response.delete_cookie('username')

        return response
