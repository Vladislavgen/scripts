import datetime
import requests
import os


def http_request_post(url, payload, headers=None, creds=None):

    if creds and headers:
        headers.update({'Content-Type': 'application/json'})
        print(url, creds.get('user'), creds.get('pass'))
        response = requests.post(url, headers=headers, json=payload, auth=(creds.get('user'), creds.get('pass')))
        print(response.text)
        return response.json()

    if headers:
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    else:
        response = requests.post(url, json=payload)
        return response.json()


def get_request_body(status, payment_method):

    time_zone = datetime.timedelta(minutes=180)
    gap = datetime.timedelta(minutes=30)



    request_body = {
        "report_params": {
            "date_type": "paid_at",
            "from": str((datetime.datetime.now() - time_zone - gap).strftime('%Y-%m-%d %H:%M')),
            "to": str((datetime.datetime.now() - time_zone).strftime('%Y-%m-%d %H:%M')),
            "status": str(status),
            "payment_method_type": str(payment_method),
            "time_zone": "UTC"}
    }
    return request_body


def get_transctions(url, creds):

    def get_ratio(success, failed):
        if failed + success == 0:
            ratio = 0
            return ratio

        ratio = float("{0:.2f}".format((success / (failed + success) * 100)))
        return ratio

    successful_count = 0
    failed_count = 0
    pending_count = 0
    payment_methods_info = {"credit_card": {
                                'successful': successful_count,
                                'failed': failed_count,
                                'pending': pending_count},

                            "alternative": {
                                'successful': successful_count,
                                'failed': failed_count,
                                'pending': pending_count},

                            "erip": {
                                'successful': successful_count,
                                'failed': failed_count,
                                'pending': pending_count},

                            "all": {
                                'successful': successful_count,
                                'failed': failed_count,
                                'pending': pending_count}
                            }

    headers = {'X-Api-Version': '3'}
    for method in ['credit_card', 'alternative', 'erip']:
        for status in ["successful", "failed", 'pending']:
            body = get_request_body(status, method)
            result = http_request_post(url, body, headers, creds)
            payment_methods_info['credit_card'][status] += result.get('transactions').get('count')
            payment_methods_info['all'][status] += result.get('transactions').get('count')

    body.update(payment_methods_info)

    for method in ['credit_card', 'alternative', 'erip']:
        ratio = get_ratio(payment_methods_info[method]['successful'], payment_methods_info[method]['failed'])
        body[method]['ratio'] = ratio
    return body


def get_transaction_report(url, creds):
    transaction_info = {
        'Time': '',
        'Description': '',
        'Amount': 0,
        'Currency': '',
        'PaymentGatewayName': '',
        'PaymentMethodType': '',
        'AdditionalData': {
            'Fraud': {
                'Rules': {
                    'show': ''}}},
        'Status': ''}

    headers = {'X-Api-Version': '3'}
    for method in ['credit_card', 'alternative', 'erip']:
        for status in ["successful", "failed"]:
            body = get_request_body(status, method)
            result = http_request_post(url, body, headers, creds)
            transaction_info['Time'] += result.get('transactions').get('count')
            transaction_info['all'][status] += result.get('transactions').get('count')
    pass
    return body


def send_notify(contacts, message):
    generate_message = f"Constantpos API. Total stats from {message.get('report_params').get('date_from')}  to {message.get('report_params').get('date_to')}: " \
              f"Accept amount: {message.get('all').get('successful_count')}\n" \
              f"Decline amount: {message.get('all').get('failed')}\n" \
              f"Accept ratio: {message.get('ratio')} %"

    url = f'https://api.telegram.org/bot{os.environ.get("TELEGRAM_BOT_TOKEN")}/sendMessage'
    for contact in contacts:
        telegram_json_body = {
          "chat_id": contact,
          "text": generate_message
        }
        http_request_post(url, telegram_json_body)

# url_1 = os.environ.get('URL_REPORTS')
url = os.environ.get('URL_COUNT')
creds = {'user': os.environ.get('BASIC_LOGIN'), 'pass': os.environ.get('BASIC_PASS')}
message = get_transctions(url, creds)
contacts = ['-457443920', '-452186474']

import sys
send_notify(sys.argv, message)