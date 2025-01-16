from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Load initial data for the library"

    def handle(self, *args, **options):
        try:
            call_command("loaddata", "initial_data.json")
            self.stdout.write(self.style.SUCCESS("Data loaded successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading data : {str(e)}"))
