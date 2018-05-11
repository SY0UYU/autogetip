"""
# AUTHOR SY0UYU
# UPDATE 18-5-6
# Version 1.0.0
"""
# !\usr\bin\env python3
import requests
import smtplib
import time
import os
from email.mime.text import MIMEText
from email.header import Header


def get_file(file_path=r"/home/pi/get_mail.conf"):
    if os.path.exists(file_path):
        return open(file_path, "r+")
    print(" 'get_mail.conf' 文件不存在！")


def is_online():
    if os.system("ping -c 4 -W 8.8.8.8"):
        return False
    return True


def is_ipaddr_change(ip):
    conf = get_file()
    tmp = conf.readlines()
    conf.close()
    if ip != tmp[0].split(' ')[-1].replace("\n", ""):
        return True
    return False


def update_conf(ip):
    conf = get_file()
    tmp = conf.readlines()
    tmp[0] = 'OLDIP = ' + ip + "\n"
    conf.seek(0)
    conf.truncate()
    for pot in range(len(tmp)):
        conf.write(tmp[pot])


def get_ip_addr():
    url = r'http://2017.ip138.com/ic.asp'
    r = requests.get(url)
    ip = r.text[r.text.find("[") + 1: r.text.find("]")]
    return ip


def seed_mail(ip):
    sender = 'PI@pi.com'
    receivers = ['you@email.com']
    message = MIMEText(ip, 'plain', 'utf-8')
    message['From'] = Header('From', 'utf-8')
    message['To'] = Header('To', 'utf-8')
    subject = 'Python mail'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpobj = smtplib.SMTP('localhost')
        smtpobj.sendmail(sender, receivers, message.as_string())
        print("Email send over")
    except smtplib.SMTPException:
        print("ERROR:can't send email")


if __name__ == '__main__':
    time.sleep(10)
    if is_online():
        new_ip = get_ip_addr()
        if is_ipaddr_change(new_ip):
            update_conf(new_ip)
            seed_mail(new_ip)
        else:
            print("ip未改变！")
    else:
        os.system("sudo bash /home/pi/reboot.sh")
