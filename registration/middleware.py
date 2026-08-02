from django.http import HttpResponseForbidden

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
            if not ip:
                ip = request.META.get('REMOTE_ADDR')

            allowed_ips = [
                '127.0.0.1',
                '::1',
                '217.199.148.249',
            ]

            if ip not in allowed_ips:
                return HttpResponseForbidden('''
                    <html>
                    <body style="
                        background: #1a1a2e;
                        color: white;
                        text-align: center;
                        padding: 100px;
                        font-family: Arial;">
                        <h1 style="color: #e94560;">⛔ Access Denied</h1>
                        <p>Admin access is restricted to the tournament organizer only.</p>
                        <a href="/" style="color: #e94560;">← Go Back to Registration</a>
                    </body>
                    </html>
                ''')

        response = self.get_response(request)
        return response