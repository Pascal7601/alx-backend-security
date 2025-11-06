from .models import RequestLog, BlockedIp
from django.http import HttpResponseForbidden

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