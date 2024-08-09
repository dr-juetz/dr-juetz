import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    email = request.form['email']
    phone = request.form['phone']
    preferred_contact_time = request.form['preferred_contact_time']

    sender_email = 'mjuetz@gmx.de'
    receiver_email = 'mjuetz@gmx.de'
    password = 'gafto5-natgif-jiwJyz'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Neuer Kontaktformular-Eintrag'

    body = f"""
    Vorname: {first_name}
    Nachname: {last_name}
    E-Mail: {email}
    Telefonnummer: {phone}
    Bevorzugte Kontaktzeit: {preferred_contact_time}
    """
    message.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP('mail.gmx.net', 587) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return redirect('/thank-you')
    except Exception as e:
        return str(e)

@app.route('/thank-you')
def thank_you():
    return 'Vielen Dank für Ihre Nachricht! Wir werden uns bald bei Ihnen melden.'

if __name__ == '__main__':
    app.run(debug=True)
