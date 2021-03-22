import datetime
import json
import os
from flask import Flask, request
import yagmail
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)

roads = {
    '1': {
        'name': 'Gudauri Kobi Magistral',
        'last_update': datetime.datetime.now()
    }
}


def update_available(road):
    last_update = road['last_update']
    return datetime.timedelta(minutes=1) < (datetime.datetime.now() - last_update)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/update', methods=['POST', ])
def info_update():
    request_info = json.loads(request.data)
    road = roads[request_info['roadId']]
    if not update_available(road):
        return json.dumps({
            'message': "Informaciis gamogzavna sheidzleba mxolod 1 wutshi ertxel, gtxovt cadot mogvianebit"
        }), 403
    road['last_update'] = datetime.datetime.now()
    notify_admin(road['name'])
    return json.dumps({
        'message': "Informaciis migebulia"
    }), 200


def notify_admin(road):
    subject = "Information update"
    message = "Hello, a request has come in to check situation on {road}".format(road=road)
    send_mail(subject, message)


def send_mail(subject, message):
    sender_email = os.environ['SENDER_MAIL']
    sender_email_password = os.environ['SENDER_MAIL_PASSWORD']
    receiver_email = os.environ['RECEIVER_MAIL']
    yag = yagmail.SMTP(sender_email, sender_email_password)
    yag.send(
        to=receiver_email,
        subject=subject,
        contents=message,
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, host='0.0.0.0', debug=True)

