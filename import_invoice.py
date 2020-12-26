import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoice_manager.settings')
django.setup()

from invoice_manager.vat_invoice import invoice
from invoice_manager.job import invoice_from_email_job

if __name__ == '__main__':
    invoice()
