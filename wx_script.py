from wxpy import *
from db import GroupLog, PersonLog
from nlp import response


def create_robot():
    bot = Bot(console_qr=True)
    tuling = Tuling(api_key='1f92a19ef3284da1aec98b590c46690b')
    groups = bot.groups()
    friends = bot.friends()
    xiache = bot.groups().search('有梦就去追')[0]
    yatou = bot.friends().search('丫头')[0]

    @bot.register(groups, msg_types=TEXT, except_self=False)
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
        print(dic)
        GroupLog.insert(dic)
        answer = response(content)
        print(answer)

    @bot.register(friends, msg_types=TEXT, except_self=False)
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
        answer = response(content)
        print(answer)

    @bot.register([xiache, yatou], except_self=False)
    def reply_my_friend(msg):
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
        answer = response(content)
        msg.reply(answer)

    embed()


if __name__ == "__main__":
    create_robot()
