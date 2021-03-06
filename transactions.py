import datetime
import requests
import os

def http_request_post(url, payload, headers=None, creds=None):

    if creds and headers:
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url, headers=headers, json=payload, auth=(creds.get('user'), creds.get('pass')))
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
            "to": str((datetime.datetime.now() - datetime.timedelta(minutes=180)).strftime('%Y-%m-%d %H:%M')),
            "status": str(status),
            "payment_method_type": str(payment_method),
            "time_zone": "UTC"}
    }
    return request_body


def get_transctions(url, creds):
    successful_count = 10
    failed_count = 10
    payment_method = ("credit_card", "alternative")
    # transaction_status = ("successful", "failed")

    headers = {'X-Api-Version': '3'}
    for method in payment_method:
        result = http_request_post(url, get_request_body("successful", method), headers, creds)
        successful_count += result.get('transactions').get('count')

        result = http_request_post(url, get_request_body("failed", method), headers, creds)
        failed_count += result.get('transactions').get('count')

    message = {
        'date_from': (datetime.datetime.now() - datetime.timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M'),
        'date_to': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'successful_count': successful_count,
        'failed_count': failed_count,
        'ratio': float("{0:.2f}".format((successful_count / (failed_count + successful_count) * 100)))
    }
    return message


def send_notify(contacts, message):

    text_message = f"Constantpos API. Total stats from {message.get('date_from')}  to {message.get('date_to')}: " \
              f"Accept amount: {message.get('successful_count')}\n" \
              f"Decline amount: {message.get('failed_count')}\n" \
              f"Accept ratio: {message.get('ratio')} %"


    url = f'https://api.telegram.org/bot{os.environ.get("TELEGRAM_BOT_TOKEN")}/sendMessage'

    for contact in contacts:
        telegram_json_body = {
          "chat_id": contact,
          "text": text_message
        }
        print(telegram_json_body)
        http_request_post(url, telegram_json_body)


# url_1 = os.environ.get('URL_REPORTS')
url = os.environ.get('URL_COUNT')
creds = {'user': os.environ.get('BASIC_LOGIN'), 'pass': os.environ.get('BASIC_PASS')}
message = get_transctions(url, creds)
contacts = ['-457443920']

import sys
send_notify(sys.argv, message)