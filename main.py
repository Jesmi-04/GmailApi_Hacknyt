
from flask import Flask, request, url_for, redirect, render_template
import gmail_send

app = Flask(__name__)


@app.route('/')
def home_template():
    return render_template("index.html", content = "")

@app.route('/sendmail', methods=['POST', 'GET'])
def send_mail():
    gmail = gmail_send.SendGmail()
    to_email = request.form.get('to_mail')
    from_email = request.form.get('from_mail')
    subject = request.form.get('subject')
    body = request.form.get('body')

    to_email_address = to_email.split('\n')
    for i in to_email_address:
        gmail.send_mail(to_email=i, from_email=from_email, subject=subject, body=body)
    return render_template('index.html', content = 'Email Sent')



if __name__ == '__main__':
    app.run(debug = True)