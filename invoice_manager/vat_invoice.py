from wand.image import Image
from wand.color import Color
from manager.models import Invoice
from datetime import datetime
from huaweicloud_ocr_sdk.HWOcrClientToken import HWOcrClientToken
from invoice_manager.settings import IMPORT_PATH, INVOICES_PATH

username = "fgh15975300"
password = "858833crc"
domain_name = "fgh15975300"  # If the current user is not an IAM user, the domain_name is the same as the username.
region = "cn-north-4"  # cn-north-1,cn-east-2 etc.
req_uri = "/v1.0/ocr/vat-invoice"
ocrClient = HWOcrClientToken(domain_name, username, password, region)


def ocr(invoice_path):
    option = {}
    try:
        img = Image(blob=invoice_path.read_bytes(), resolution=300)
        img.format = 'png'
        img.background_color = Color("white")
        img.alpha_channel = 'remove'

        img.save(filename='/data/invoice/invoices/test.png')

        img_bytes = img.make_blob()

        response = ocrClient.request_ocr_service_base64(req_uri, img_bytes, option)
        if response.status_code != 200:
            print("Status code:" + str(response.status_code) + "\ncontent:" + response.text)
            return None
        return response.json()["result"]
    except ValueError as e:
        print(e)


def invoice():
    for invoice_path in IMPORT_PATH.iterdir():
        if invoice_path.is_file() and invoice_path.suffix == ".pdf":
            invoice_data = ocr(invoice_path)
            if invoice_data:
                print(invoice_data)
                invoice = Invoice(
                    id=invoice_data["number"],
                    description="、".join([item["name"] for item in invoice_data["item_list"]]),
                    create_date=get_crate_date(invoice_data["issue_date"]),
                    company_name=invoice_data["buyer_name"],
                    company_id=invoice_data["buyer_id"],
                    price=get_price(invoice_data["total"]),
                )

                # 判断抬头和税号是否正确
                if invoice.company_id != "91350212MA34NYU13R" or invoice.company_name != "厦门万里目成长科技有限公司":
                    print(f"{invoice_path.name} 税号或税号与配置中的不符，已跳过")
                    continue
                invoice_path.rename(INVOICES_PATH / f"{invoice.id}.pdf")
                invoice.save()


def get_crate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y年%m月%d日")
    except Exception:
        return datetime.now()


def get_price(total_str):
    try:
        return float(total_str.replace("￥", ""))
    except Exception:
        return 0.0
