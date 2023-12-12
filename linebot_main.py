# Import Packages
from function.config import *
from function.linebot_config import *
from main import *
import re
from linebot.models import (
    MessageEvent, TextSendMessage, TextMessage, StickerSendMessage,
    MessageAction, TemplateSendMessage, ButtonsTemplate,
    )

def linebot_main(target, during, target_num, *mail_accounts):
    print('開始爬蟲!')
    today = date.today().strftime("%Y%m%d")
    leaderboard, prediction = main(target, during, target_num, is_gc=True)
    print('爬蟲完畢')
    output = Output_maker(leaderboard, prediction)
    data = {
        'leaderboard': leaderboard,
        'prediction': prediction,
        'mainpush': output.mainpush_summary,
        'total': output.total_summary
    }
    gmail_machine = Gmail_machine(target, today, data)
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not mail_accounts:
        gmail_machine.send_mail(os.getenv('Alex_Account'))
        gmail_machine.send_mail(os.getenv('Bro_Account'))
    else:
        for account in mail_accounts:
            if re.fullmatch(email_pattern, account):
                gmail_machine.send_mail(account)
    print('寄送郵件完畢!')

def time_template(command):
    msg = TemplateSendMessage(
        alt_text='ButtonsTemplate',
        template=ButtonsTemplate(
            thumbnail_image_url=img_url_dict[command],
            title=command,
            text='請選擇以下時間範圍',
            actions=[
                MessageAction(label='上月', text=f'{command} lastmonth 30'),
                MessageAction(label='本月', text=f'{command} thismonth 30'),
                MessageAction(label='上週', text=f'{command} lastweek 30'),
                MessageAction(label='本週', text=f'{command} thisweek 30'),
            ]
        )
    )
    return msg

@handler.add(MessageEvent, message=TextMessage)
def echo_text(event):
    received_message = event.message.text
    rm_list = received_message.split()
    target = rm_list[0].upper()

    try:
        if target == 'HELP':
            sent_message = TextSendMessage(
                text='''請輸入以下格式進行爬蟲: 目標 資料範圍 爬取數量
                e.g. NBA thismonth 15
                目標包含: NBA, 歐洲職籃, 韓國職籃, 中國職籃, 日本職籃, 澳洲職籃, 澳洲職棒, 足球, NHL冰球, 俄羅斯冰球, 賽馬, 美式足球。
                資料範圍包含: lastmonth, thismonth, lastweek, thisweek, season。
                爬取數量範圍: 1~30，如果有開放預測的人不足，則會爬取所有開放預測的人。
                '''
            )
        elif (target in ['NBA', '足球', 'NHL冰球']) & (len(rm_list) == 1):
            sent_message = time_template(target)
        elif (target in alliance_dict.keys()) & (len(rm_list) == 3):
            during_, target_num_ = rm_list[1], int(rm_list[2])
            if (during_ in during_list):
                linebot_main(target, during_, target_num_)
                sent_message = TextSendMessage(text='已完成爬蟲，請前往收信')
            else:
                sent_message = TextSendMessage(text='指令有誤，請輸入 help 查看指令格式')
        else:
            sent_message = StickerSendMessage(package_id='6359', sticker_id='11069851')
    except Exception as e:
        sent_message = TextSendMessage(text=str(e))

    line_bot_api.reply_message(event.reply_token, sent_message)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)