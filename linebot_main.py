# Import Packages
from function.config import during_list, img_url_dict, help_text
from function.linebot_config import *
from main import *
import re
from linebot.models import (
    MessageEvent, TextSendMessage, TextMessage, StickerSendMessage,
    MessageAction, TemplateSendMessage, ButtonsTemplate,
    )

def linebot_main(target, during, target_num, *mail_accounts):
    key_path_linebot = '/etc/secrets/sport-lottery-database.json'

    if re.match(r'^yesterday|.*daysAgo$', during):
        result_main(target, during, target_num, is_gc=True, key_path=key_path_linebot)
        return '已完成結果搜集，請前往雲端工作表查看'
    if (during not in during_list):
        return '資料時間範圍有誤，請輸入 help 查看指令格式'
    for account in mail_accounts:
        if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', account):
            return f'{account} 格式有誤，請輸入 help 查看指令格式'
    print('參數確認完畢')

    taipei_timezone = pytz.timezone('Asia/Taipei')
    today = datetime.now(taipei_timezone).strftime('%Y%m%d')
    leaderboard, prediction = main(target, during, target_num, is_gc=True)
    print('爬蟲完畢')

    output = Output_maker(leaderboard, prediction)
    data = {
        'leaderboard': leaderboard,
        'prediction': prediction,
        'mainpush': output.mainpush_summary,
        'total': output.total_summary
    }
    print('資料整理完畢')

    gmail_machine = Gmail_machine(target, today, data)
    if not mail_accounts:
        gmail_machine.send_mail(os.getenv('Bro_Account'))
    else:
        [gmail_machine.send_mail(account) for account in mail_accounts]
    print('寄送郵件完畢')

    board_sheet, pred_sheet, total_sheet, mainpush_sheet = open_gsheet(
        key_path='/etc/secrets/sport-lottery-database.json',
        database_url=database_url,
    )
    append_dataframe(data['leaderboard'], board_sheet, target, during)
    append_dataframe(data['prediction'], pred_sheet, target, during)
    append_dataframe(data['mainpush'].pipe(add_rank), mainpush_sheet, target, during)
    append_dataframe(data['total'].pipe(add_rank), total_sheet, target, during)
    print('資料儲存完畢')

    if data['total']['game'].isna().any():
        return '有對戰資料缺漏，請前往雲端工作表查看'

    return '已完成爬蟲，請前往收信'

def time_template(command):
    msg = TemplateSendMessage(
        alt_text='ButtonsTemplate',
        template=ButtonsTemplate(
            thumbnail_image_url=img_url_dict[command],
            title=command,
            text='請選擇主推榜時間範圍',
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
    target = rm_list[0]

    try:
        if (target in alliance_dict.keys()):
            if (len(rm_list) == 1):
                sent_message = time_template(target)
            elif (len(rm_list) == 2):
                sent_message = TextSendMessage(text='少輸入一個參數，請輸入 help 查看指令格式')
            elif (len(rm_list) >= 3):
                result_text = linebot_main(*rm_list)
                sent_message = TextSendMessage(text=result_text)
        elif (target == 'help'):
            sent_message = TextSendMessage(text=help_text)
        else:
            sent_message = StickerSendMessage(package_id='6359', sticker_id='11069851')
    except Exception as e:
        sent_message = TextSendMessage(text=str(e))

    line_bot_api.reply_message(event.reply_token, sent_message)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)