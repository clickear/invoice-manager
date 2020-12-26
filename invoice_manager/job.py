import datetime
import io
import os
import requests
import re


from invoice_manager.vat_invoice import invoice

from bs4 import BeautifulSoup

from imbox import Imbox
from invoice_manager.settings import IMBOX_HOST, IMBOX_USERNAME, IMBOX_PWD, IMPORT_PATH
from manager.models import Email


def invoice_from_email_job():
    imbox = Imbox(IMBOX_HOST,
                  username=IMBOX_USERNAME,
                  password=IMBOX_PWD,
                  ssl=True,
                  ssl_context=None)
    unread_messages = imbox.messages(unread=True)
    print('未读邮件数量:', len(unread_messages))

    downloaded = False
    for uid, message in unread_messages:
        email = Email(id=uid,
                      subject=message.subject,
                      content=getHtmlFromEmailMessage(message))

        print('获取到未读', message)
        try:
            if email.subject.find('发票') >= 0:
                cur_download = download_invoice(message, email)
                downloaded = cur_download or downloaded
        except Exception as e:
            print(e)
            continue
        email.save()
        imbox.mark_seen(uid)
    if downloaded:
        invoice()

    return len(unread_messages)

def getHtmlFromEmailMessage(message):
    if message.body and message.body['html'] and len(message.body['html']) > 0:
        return message.body['html'][0]
    return ''


def download_invoice(message, email):
    if message and len(message.attachments) > 0:
        for attachment in message.attachments:
            print(attachment)
            download(attachment['content'], attachment['filename'])
            return True
    else:
        return parse(email.subject, email.content)


def download(content, filename):
    if filename.find('.pdf') == -1:
        filename += '.pdf'

    filename = str(IMPORT_PATH) + '/' + filename
    print('下载邮件:', filename)
    if isinstance(content, io.BytesIO):
        with open(filename, "wb") as f:
            f.write(content.getbuffer())
    else:
        with open(filename, "wb") as f:
            f.write(content)


def parse(subject, html_page):
    invoice_link = None
    soup = BeautifulSoup(html_page, 'html.parser')
    for link in soup.findAll('a'):
        href = link and link['href']
        if href and href.find('fpmail') >= 0:
            invoice_link = href
            break
    if invoice_link:
        r = requests.get(invoice_link, allow_redirects=True)
        filename = getFilename_fromCd(r.headers.get('content-disposition'))
        if not filename:
            filename = subject + '.pdf'
        download(r.content, filename)
        return True


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


if __name__ == "__main__":
    invoice_from_email_job()
