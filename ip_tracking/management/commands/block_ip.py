# ip_tracking/management/commands/block_ip.py
from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIp

class Command(BaseCommand):
    help = 'Add an IP address to the blocklist'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')

    def handle(self, *args, **options):
        ip = options['ip_address']
        obj, created = BlockedIp.objects.get_or_create(ip_address=ip)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip}'))
        else:
            self.stdout.write(self.style.WARNING(f'IP {ip} is already in the blocklist'))