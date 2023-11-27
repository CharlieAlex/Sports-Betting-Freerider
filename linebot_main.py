# Import Packages
from function.config import *
from function.linebot_config import *
from main import *
from linebot.models import (
    MessageEvent, TextSendMessage,
    TextMessage, StickerSendMessage,
    )

def linebot_main(target, during, target_num):
    print('開始爬蟲!')
    today = date.today().strftime("%Y%m%d")
    leaderboard, prediction = main(target, during, target_num)
    print('爬蟲完畢')
    output = Output_maker(leaderboard, prediction)
    data = {
        'leaderboard': leaderboard,
        'prediction': prediction,
        'mainpush': output.mainpush_summary,
        'total': output.total_summary
    }
    gmail_machine = Gmail_machine(target, today, data)
    gmail_machine.send_mail(os.getenv('Alex_Account'))
    gmail_machine.send_mail(os.getenv('Bro_Account'))
    print('寄送郵件完畢!')

@handler.add(MessageEvent, message=TextMessage)
def echo_text(event):
    received_message = event.message.text
    rm_list = received_message.split()
    try:
        if rm_list[0] == 'Start':
            if (rm_list[1] in alliance_dict.keys()) & (rm_list[2] in during_list):
                linebot_main(rm_list[1], rm_list[2], rm_list[3])
                sent_message = TextSendMessage(text='已完成爬蟲，請前往收信')
            else:
                sent_message = TextSendMessage(text='指令有誤，請重新輸入以下格式: Start NBA thismonth 15')
        else:
            sent_message = StickerSendMessage(package_id='6359', sticker_id='11069851')
    except Exception as e:
        sent_message = TextSendMessage(text=str(e))

    line_bot_api.reply_message(event.reply_token, sent_message)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)