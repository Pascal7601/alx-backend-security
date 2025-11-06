from django.db import models

class RequestLog(models.Model):
    ip_adress = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ip_adress}: {self.path}"


class BlockedIp(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address