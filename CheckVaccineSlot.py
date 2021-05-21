import requests
import time
import smtplib

configs = {
    "pin_cods": ["458990", "458001"], # List of pin codes of your Area
    "smtp_email":  "",  # Your Email ID
    "smtp_pass": "",  # Password of your Email ID
    "recipient": "",  # Recipient Email ID
    "api_url": f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=%s&date=%s",
    "hdr": {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
}


def send_mail(body, smtp_email, smtp_pass, recipient):
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    result = smtpserver.login(smtp_email, smtp_pass)
    if result[0] == 235:
        smtpserver.sendmail(smtp_email, recipient, body)
    print('Mail Sent #########')

print('####### Start Running')

while True:  # It will check in each Hour
    _date = time.strftime("%d/%m/%Y")
    for pin_code in configs['pin_cods']:
        with requests.session() as s:
            api = configs['api_url'] % (pin_code, _date)
            print(api)
            hdr = configs['hdr']
            res = s.get(api, headers=hdr)
            res = res.json()
            for center in res['centers']:
                for session in center['sessions']:
                    if (session['min_age_limit'] < 45) & (session['available_capacity'] > 0):
                        body = f"Subject: Congrats! You got a slot Alert! for %s" % (center['name'])
                        body = body + '\n' + 'Date- ' + _date
                        body = body + '\n' + 'Centre Name - ' + center['name']
                        body = body + '\n' + 'Centre Address - ' + center['address']
                        body = body + '\n' + 'Total Vaccine Doses - ' + str(session['available_capacity'])
                        body = body + '\n' + 'available capacity dose 1 - ' + str(session['available_capacity_dose1'])
                        body = body + '\n' + 'available capacity dose 2 - ' + str(session['available_capacity_dose2'])
                        body = body + '\n' + 'Click Here to book your slot Now - ' + 'https://www.cowin.gov.in/home'
                        body = body + '\n' + ' Regards, \n Kapil Chouhan \n www.about.me/kchouhan  '
                        send_mail(body, configs['smtp_email'], configs['smtp_pass'], configs['recipient'])

    time.sleep(100)