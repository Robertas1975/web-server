import os
from flask import Flask, render_template, url_for, send_from_directory
from flask import request, redirect

def submit_email(name_='Anonymous',email_from="robke69@gmail.com", subject = "Default", message = "Empty"):
    import smtplib
    from email.message import EmailMessage
    from string import Template
    from pathlib import Path
    #html_body = Template(Path('./email_body.html').read_text())
    email = EmailMessage()
    email['from'] = name_.strip()
    email['to'] = 'robertas.mockus.75@gmail.com'
    email['subject'] = subject
    email.set_content(message + ' Email from ' + email_from)
    #email.set_content(html_body.substitute(
    #    {'name': 'Robertas', 'email_address': 'lottery_board@gmail.com', 'phone_number': '+180025455524',
    #     'date': '1st October, 2021'}), 'html')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('robke69@gmail.com', 'Langas69+')
        smtp.send_message(email)
    return
    pass

def save_submission_to_file(name_='Anonymous',email_from="robke69@gmail.com", subject = "Default", message = "Empty"):
    from pathlib import Path
    file_to_save = '.\submitted_data.txt'
    file_to_save_path = Path(file_to_save)
    if file_to_save_path.exists():
        with open(file_to_save, mode='a') as output_file:
            output_file.write(f'\n{name_}:{email_from}:{subject}:{message.strip()}')
        return 'Line is appended.'
    else:
        return 'File not found.'
    pass

def save_submission_to_csv(name_='Anonymous',email_from="robke69@gmail.com", subject = "Default", message = "Empty"):
    import csv
    from pathlib import Path
    file_to_save = '.\submitted_data.csv'
    file_to_save_path = Path(file_to_save)
    if file_to_save_path.exists():
        with open(file_to_save, mode='a', newline='') as output_csv:
            csv_writer = csv.writer(output_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([name_,email_from,subject,message])
    pass

app = Flask(__name__)
print(__name__)

@app.route('/<string:page>')
def page(page):
    return render_template(page)

@app.route('/submitted', methods=['POST','GET'])
def submit_contact_me():
    if request.method == 'POST':
        dictionary_ = request.form.to_dict()
        for i in dictionary_.keys():
            if i == 'name': name_ = dictionary_.get(i)
            if i == 'email': email = dictionary_.get(i)
            if i == 'subject': subject = dictionary_.get(i)
            if i == 'message': message = dictionary_.get(i)
        submit_email(str(name_), str(email), str(subject), message)
        message = message.replace('\r\n',' ')
        save_submission_to_file(str(name_), str(email), str(subject), message)
        save_submission_to_csv(str(name_), str(email), str(subject), message)
        return render_template('/thankyou.html', name=name_)
    else:
        return 'Something went wrong...'
    pass
