from wxpy import *
from db import GroupLog, PersonLog, TemplateImportHandle
from nlp import common_response, emotion_recognize
from emotion_classifier import emotion_recognition
from utils import *
from function_api import weather_response
import re


def create_robot():
    bot = Bot(console_qr=True)
    # groups = bot.groups().search('测试')
    friends = bot.friends()
    admins_name = ['吴金晶']
    admins = []
    # for admin_name in admins_name:
    #     admin = bot.friends().search(admin_name)[0]
    #     admins.append(admin)

    @bot.register(msg_types=FRIENDS)
    def auto_accept_friends(msg):
        print('test')
        new_friend = bot.accept_friend(msg.card)
        new_friend.send('想和小z聊天直接发消息就行了，消息前缀为#就进入情感识别模式，消息前缀为&就进入调教模式，'
                        '想查询天气可以发送"天气：城市名"，什么都不加就是普通聊天模式，如果有疑问可以发送help查看帮助')

    # 聊天群里的消息在这里处理
    @bot.register(admins, msg_types=TEXT, except_self=False)
    def get_message2(msg):
        sender = msg.sender.name
        receiver = msg.receiver.name
        sender_name = msg.member.name
        sender_id = msg.sender.wxid
        if sender_id == 2442638283:
            group_name = receiver
        else:
            group_name = sender
        content = msg.text
        msg_time = msg.create_time.strftime("%Y-%m-%d %H:%M:%S")
        is_at = str(msg.is_at)
        dic = {'group_name': group_name,
               'sender_name': sender_name,
               'content': content,
               'msg_time': msg_time,
               'if_at': is_at}
        GroupLog.insert(dic)
        result = _user_content_process(content)
        if result['type'] == 'normal':
            answer = common_response(result['data'])
            if answer == 'no result':
                answer = '小Z还不知道怎么回答这个问题，教教小Z吧。格式是: &问题？答复\n比如：&你的名字叫什么？小Z'
        elif result['type'] == 'emotion_recognize':
            answer = emotion_recognize(content)
            emotion = emotion_recognition
            answer = answer + '\n*************\n' + emotion
        elif result['type'] == 'help':
            answer = result['data']
        elif result['type'] == 'learning_pattern':
            conversition = [result['data']['question'], result['data']['answer']]
            template_import_handle = TemplateImportHandle()
            insert_result = template_import_handle.insert_conversition(conversition)
            if insert_result == 'success':
                answer = '小Z已经成功学习此问题了，快来试试吧！'
            else:
                answer = '抱歉，学习过程出了些问题，请联系主人解决'
        print(answer)
        msg.reply(answer)

    # 私聊消息在这里处理
    @bot.register(friends, except_self=False)
    def reply_my_friend(msg):
        sender_name = msg.sender.name
        receiver_name = msg.receiver.name
        content = msg.text
        msg_time = msg.create_time.strftime("%Y-%m-%d %H:%M:%S")
        dic = {'sender_name': sender_name,
               'receiver_name': receiver_name,
               'content': content,
               'msg_time': msg_time}
        PersonLog.insert(dic)
        result = _user_content_process(content)
        if result['type'] == 'normal':
            answer = common_response(result['data'])
            if answer == 'no result':
                answer = '小Z还不知道怎么回答这个问题，教教小Z吧。格式是: &问题？答复\n比如：&你的名字叫什么？小Z'
        elif result['type'] == 'emotion_recognize':
            answer = emotion_recognize(content)
            emotion = emotion_recognition(content)
            answer = answer + '\n*************\n' + emotion
        elif result['type'] == 'help':
            answer = result['data']
        elif result['type'] == 'function_pattern':
            data = result['data']
            answer = weather_response(data)
            if answer == 'no city!':
                answer = '小Z目前不能查询到这个城市的天气信息'
        elif result['type'] == 'learning_pattern':
            conversition = [result['data']['question'], result['data']['answer']]
            template_import_handle = TemplateImportHandle()
            insert_result = template_import_handle.insert_conversition(conversition)
            if insert_result == 'success':
                answer = '小Z已经成功学习此问题了，快来试试吧！'
            else:
                answer = '抱歉，学习过程出了些问题，请联系主人解决'
        print('回复为: {}'.format(answer))
        msg.reply(answer)

    # 管理员消息在这里处理
    @bot.register(admins, msg_types=TEXT)
    def get_message1(msg):
        sender_name = msg.sender.name
        receiver_name = msg.receiver.name
        content = msg.text
        msg_time = msg.create_time.strftime("%Y-%m-%d %H:%M:%S")
        dic = {'sender_name': sender_name,
               'receiver_  name': receiver_name,
               'content': content,
               'msg_time': msg_time}
        PersonLog.insert(dic)
        print(dic)
        result = _admin_content_process(content)
        msg.reply(result['data'])

    embed()


def _admin_content_process(content):
    content = ''.join(content.split())
    help_msg = re.match('^help$', content)

    if help_msg:
        help_msg = ''
        result = {'type': 'help',
                  'data': help_msg}
        return result


def _user_content_process(content):
    content = ''.join(content.split())
    help_msg = re.match('^help$', content)
    learning_pattern = re.match('^&(?P<question>.+)？(?P<answer>.+)', content)
    emotion_model = re.match('^#', content)
    function = re.match('^天气：(?P<city>.+)', content)
    if emotion_model:
        content = content.strip('#')
        result = {'type': 'emotion_recognize',
                  'data': content}
    elif learning_pattern:
        question = learning_pattern.groupdict()['question']
        answer = learning_pattern.groupdict()['answer']
        date_dict = {'question': question,
                     'answer': answer}
        result = {'type': 'learning_pattern',
                  'data': date_dict}
    elif function:
        key = function.groupdict()['city']
        result = {'type': 'function_pattern',
                  'data': key}
    elif help_msg:
        help_msg = ('小Z暂时有4个功能，普通聊天，学习模式，情感识别，天气查询。\n'
                    '1.消息前缀为#则为情感识别命令，小Z将识别#后面句子的情感。\n'
                    '2.消息前缀为&即为调教命令，此时可以教小Z说话，调教的格式是: &问题？答复\n'
                    ' 比如：&你的名字叫什么？小Z\n'
                    ' (注意，这里的问号为中文字符)\n'
                    '3.天气查询命令为 "天气：城市名"\n' 
                    ' 比如：天气：武汉\n'
                    '（注意，这里的冒号为中文字符）\n'
                    '4.什么都不加就是普通模式')
        result = {'type': 'help',
                  'data': help_msg}
    else:
        result = {'type': 'normal',
                  'data': content}
    return result


if __name__ == "__main__":
    create_robot()