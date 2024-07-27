from django.core.management.base import BaseCommand
import helpers
from django.conf import settings


VENDOR_STATICFILES = {
    "flowbite.min.css":"https://cdn.jsdelivr.net/npm/flowbite@2.4.1/dist/flowbite.min.css",
    "flowbite.min.js":"https://cdn.jsdelivr.net/npm/flowbite@2.4.1/dist/flowbite.min.js"
}



STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("DOWNLOADING vendor static files")
        completed_urls = []
        for name,url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_sucess  = helpers.download_to_local(url,out_path)

            if dl_sucess:
                completed_urls.append(url)

            else:
                self.stdout.write(self.style.ERROR(f'failed to download {url}'))


        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS("Successfully updated vendor static files.")
            )
        else:
            self.stdout.write(
                self.style.WARNING("some files are not updated")
            )

            


        
