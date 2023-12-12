# Import Packages
from function.config import *
from function.linebot_config import *
from main import *
from linebot.models import (
    MessageEvent, TextSendMessage, TextMessage, StickerSendMessage,
    MessageAction, TemplateSendMessage, ButtonsTemplate,
    )

def linebot_main(target, during, target_num):
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
    gmail_machine.send_mail(os.getenv('Alex_Account'))
    gmail_machine.send_mail(os.getenv('Bro_Account'))
    print('寄送郵件完畢!')

def time_template(command):
    img_url_dict = {
        'NBA':'https://media.cnn.com/api/v1/images/stellar/prod/160204121559-nba-slam-dunk-23.jpg?q=x_4,y_0,h_1934,w_3437,c_crop/w_800',
        'Soccer':'https://img1.wsimg.com/isteam/ip/062f8e95-2657-40ed-a40a-acb450331c62/8-20200926-IMG_5064.jpg/:/cr=t:26.49%25,l:33.91%25,w:64.94%25,h:48.72%25/rs=w:1240,h:620,cg:true,m',
        'NHL':'https://help.viaplay.com/wp-content/uploads/capture-3-1024x576.png',
    }
    return (
        TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url=img_url_dict[command],
                title=command,
                text='請選擇以下時間範圍',
                actions=[
                    MessageAction(label='上月', text=f'{command} lastmonth 30'),
                    MessageAction(label='本月', text=f'{command} thismonth 30'),
                    MessageAction(label='本週', text=f'{command} thisweek 30'),
                ]
            )
        )
    )

@handler.add(MessageEvent, message=TextMessage)
def echo_text(event):
    received_message = event.message.text
    rm_list = received_message.split()
    target = rm_list[0].upper()

    try:
        if target in ('NBA', '足球', 'NHL冰球') & len(rm_list) == 1:
            time_template(target)
            sent_message = ''
        elif target in alliance_dict.keys() & len(rm_list) == 3:
            during_, target_num_ = rm_list[1], int(rm_list[2])
            if (during_ in during_list):
                linebot_main(target, during_, target_num_)
                sent_message = TextSendMessage(text='已完成爬蟲，請前往收信')
            else:
                sent_message = TextSendMessage(text='指令有誤，請重新輸入以下格式: NBA thismonth 15')
        else:
            sent_message = StickerSendMessage(package_id='6359', sticker_id='11069851')
    except Exception as e:
        sent_message = TextSendMessage(text=str(e))

    line_bot_api.reply_message(event.reply_token, sent_message)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)