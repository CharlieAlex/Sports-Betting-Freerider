import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import BytesIO

def df_to_csv(df):
    with BytesIO() as buffer:
        df.to_csv(buffer, index=0)
        return buffer.getvalue()

class Gmail_machine:
    def __init__(self, target, during, data:dict[pd.DataFrame]):
        self.target = target
        self.during = during
        self.data = data
        self.sender_account = os.getenv('Sender_Account')
        self.sender_password = os.getenv('Sport_Lottery_Password')

    def data_to_html(self, col_name):
        return (self.data[col_name]
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
                    {self.data_to_html('mainpush')}
                    <br>
                    <br>
                    以下是所有人的預測結果：<br>
                    {self.data_to_html('total')}
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

    def mail_attach(self, col_name):
        attach_name = f'{col_name}_{self.target}_{self.during}.csv'
        part_attach = MIMEApplication(df_to_csv(self.data[col_name]))
        part_attach.add_header('Content-Disposition','attachment',filename=attach_name)
        return part_attach

    def message_content(self, receiver_account):
        msg = MIMEMultipart()
        msg["From"] = self.sender_account
        msg["To"] = receiver_account
        msg["Subject"] = f'運彩預測 {self.target} {self.during}'
        msg.attach(self.mail_content)
        msg.attach(self.mail_attach('prediction'))
        return msg

    def send_mail(self, receiver_account):
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465) #建立gmail連驗
        server.login(self.sender_account, self.sender_password)
        server.send_message(self.message_content(receiver_account))
        server.close()

if __name__ == '__main__':
    from datetime import date
    from dotenv import load_dotenv
    from config import rawdata_path, workdata_path
    load_dotenv('/Users/alexlo/Desktop/Project/Others/App_Setting/.env')

    target = 'NBA'
    during = date.today().strftime("%Y%m%d")
    test_account = os.getenv('Alex_Account')
    data = {
        'leaderboard': pd.read_csv(f'{rawdata_path}/leaderboard_{target}_20231125.csv'),
        'prediction': pd.read_csv(f'{rawdata_path}/prediction_{target}_20231125.csv'),
        'mainpush': pd.read_csv(f'{workdata_path}/mainpush_{target}_{during}.csv'),
        'total': pd.read_csv(f'{workdata_path}/total_{target}_{during}.csv'),
    }
    gmail_machine = Gmail_machine(target, during, data)
    gmail_machine.send_mail(test_account)