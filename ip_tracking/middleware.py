from .models import RequestLog, BlockedIp
from django.http import HttpResponseForbidden
import requests
from django.core.cache import cache

def print_request_middleware(get_response):

    def middleware(request):
        try:
            ip_addr = request.META["REMOTE_ADDR"]
            path = request.path
            if ip_addr and path:
                if BlockedIp.objects.filter(ip_address=ip_addr).exists():
                    return HttpResponseForbidden("Your Ip ADRESS has been blocked")
                log = RequestLog.objects.create(
                    ip_adress=ip_addr,
                    path=path
                )
                log.save()
        except Exception as e:
            print("Exception", e)

        print("before caling the view")
 
        response = get_response(request)

        return response
    return middleware

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure IPBlockMiddleware ran first to attach client_ip, or re-fetch it
        ip = getattr(request, 'client_ip', request.META.get('REMOTE_ADDR'))

        # 1. Check Cache
        cache_key = f"geo_{ip}"
        geo_data = cache.get(cache_key)

        # 2. If Cache Miss, Call API
        if not geo_data:
            try:
                # Using ip-api.com for demonstration (free for non-commercial use)
                response = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
                if response.status_code == 200 and response.json().get('status') == 'success':
                    data = response.json()
                    geo_data = {
                        'country': data.get('country'),
                        'city': data.get('city')
                    }
                    # 3. Set Cache for 24 hours (86400 seconds)
                    cache.set(cache_key, geo_data, timeout=86400)
            except requests.RequestException:
                # Fail silently if API is down so standard requests don't break
                geo_data = {}

        # 4. Create Log Entry
        RequestLog.objects.create(
            ip_address=ip,
            country=geo_data.get('country') if geo_data else None,
            city=geo_data.get('city') if geo_data else None
        )

        return self.get_response(request)