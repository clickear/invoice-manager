import json
import re

from werobot import WeRoBot

robot = WeRoBot(enable_session=False,
                token='test',
                APP_ID='wxa78d83051c37f20b',
                APP_SECRET='9966a363619f49ab247e0d234eb352c8',
                ENCODING_AES_KEY='zTPfDoFmMdXpMazPp20Rw2e086MJIZ3EQQHli4BjkI3')

from invoice_manager.job import invoice_from_email_job
from invoice_manager.vat_invoice import invoice

@robot.filter("job")
def hello(message):
    unread_count = invoice_from_email_job()
    return '未读邮件' + str(unread_count)

@robot.filter("import")
def import_invoice(message):
    invoice()
    return '执行成功'
