import os
import pandas as pd
from .config import rawdata_path, workdata_path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

load_dotenv('/Users/alexlo/Desktop/Project/Others/App_Setting/.env')

class Gmail_machine:
    def __init__(self, target, during):
        self.target = target
        self.during = during
        self.sender_account = os.getenv('Sender_Account')
        self.sender_password = os.getenv('Sport_Lottery_Password')

    @property
    def total_pred_table(self):
        os.chdir(workdata_path)
        return (pd
            .read_csv(f'total_{self.target}_{self.during}.csv')
            .to_html(index=False)
            .replace('\n', '')
        )

    @property
    def mainpush_pred_table(self):
        os.chdir(workdata_path)
        return (pd
            .read_csv(f'mainpush_{self.target}_{self.during}.csv')
            .to_html(index=False)
            .replace('\n', '')
        )

    @property
    def mail_content(self):
        str_ = f'''
                <html>
                <head></head>
                <body>
                    <p>
                    Hey, Bro!<br>
                    今天的預測來摟！<br>
                    <br>
                    <br>
                    以下是只計算主推的預測結果：<br>
                    {self.mainpush_pred_table}
                    <br>
                    <br>
                    以下是所有人的預測結果：<br>
                    {self.total_pred_table}
                    <br>
                    <br>
                    附件是抓到的原始數據。<br>
                    <br>
                    <br>
                    <br>
                    Best Regards,<br>
                    Your Bro<br>
                    </p>
                </body>
                </html>
            '''
        return MIMEText(str_, "html", "utf-8")

    def mail_attach(self, file_path):
        part_attach = MIMEApplication(open(file_path,'rb').read())
        part_attach.add_header('Content-Disposition','attachment',filename=file_path) #為附件命名
        return part_attach

    def message_content(self, receiver_account):
        msg = MIMEMultipart()
        msg["From"] = self.sender_account
        msg["To"] = receiver_account
        msg["Subject"] = f'運彩預測 {self.target} {self.during}'
        msg.attach(self.mail_content)

        os.chdir(rawdata_path)
        msg.attach(self.mail_attach(f'prediction_{self.target}_{self.during}.csv'))
        # msg.attach(self.mail_attach(f'leaderboard_{self.target}_{self.during}.csv'))
        # os.chdir(workdata_path)
        # msg.attach(self.mail_attach(f'mainpush_{self.target}_{self.during}.csv'))
        # msg.attach(self.mail_attach(f'total_{self.target}_{self.during}.csv'))
        return msg

    def send_mail(self, receiver_account):
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465) #建立gmail連驗
        server.login(self.sender_account, self.sender_password)
        server.send_message(self.message_content(receiver_account))
        server.close()

if __name__ == '__main__':
    from datetime import date

    target = 'NBA'
    during = date.today().strftime("%Y%m%d")
    test_account = os.getenv('Alex_Account')
    gmail_machine = Gmail_machine(target, during)
    gmail_machine.send_mail(test_account)