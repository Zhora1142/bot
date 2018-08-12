#coding: utf-8
import vk
from Queue import Queue
from threading import Thread
from time import sleep
from subprocess import call
from random import randint as random
from datetime import datetime

global messagess
messagess = Queue()

global api_group
api_group = vk.API(vk.AuthSession(access_token='f94a409b058107892d3677ae352c4ee76319857daa58a3312b9040cd19ddb0e25f0349d07cd47e96f088f'), v='5.80')

global api_profile
api_profile = vk.API(vk.AuthSession(access_token='d60e0a9b178c44e239855f0a2c44f67b89ec53b137b70974deab9648d4eec5971b81138590631995e10a5'),v='5.80')

def clear():

    a = call('clear')
    a = call('clear')

def repost(object, nums):
    sleep(10)
    ids = ['169976139', '169976170', '169976196', '169976274', '169976293',
           '169980485', '169980543', '169980587', '169980618', '169980637']
    n = 0
    for i in ids:
        print('Бот сделал репост на группу \033[33m%s\033[0m \033[36m%s\033[0m [%s]' % (i,datetime.now(),n+1))
        api_profile.wall.repost(object=object, group_id=i)
        sleep(nums[n])
        n += 1

def send(user_id, message):

    api_group.messages.send(user_id=user_id, message=message)

def get_messages():

    inf = api_group.messages.getLongPollServer(need_pts='1', group_id='169970841')
    inf = {'ts': inf['ts'], 'pts': inf['pts']}

    while True:
        upds = api_group.messages.getLongPollHistory(ts=inf['ts'], pts=inf['pts'], lp_version='3')
        msg = upds['messages']['items']
        income_mes = []
        for i in msg:
            if i['out'] == 0:
                income_mes.append(i)
        if income_mes is not []:
            for c in income_mes:
                messagess.put(c)
        inf = api_group.messages.getLongPollServer(need_pts='1', group_id='169970841')
        inf = {'ts': inf['ts'], 'pts': inf['pts']}
        sleep(1)


def main():

    print '\033[33m======\033[36mБот начал работу\033[33m======\033[0m'
    getmsg = Thread(target=get_messages, args=())
    getmsg.start()

    while True:
        msgs = messagess.get()
        print('Бот получил сообщение \033[36m%s\033[0m' % datetime.now())

        if msgs == []:
            continue

        try:
            msgs['attachments'][0]['wall']
        except:
            send(msgs['from_id'], 'Не удалось найти пост. Чтобы бот смог найти пост, '
                                 'просто сделайте репост этого поста боту в сообщения.')
            print('Бот не смог найти прикрепленную запись \033[36m%s\033[0m' % datetime.now())
        else:
            nums = []
            for a in range(0, 10):
                nums.append(random(1, 5))

            time = sum(nums) + 10
            send(msgs['from_id'], 'Бот начал делать репосты. Действие займет %s секунд' % time)
            print('Бот начал делать репосты \033[36m%s\033[0m' % datetime.now())

            try:
                mesa = 'wall%s_%s' % (msgs['attachments'][0]['wall']['from_id'], msgs['attachments'][0]['wall']['id'])
                repost(mesa, nums)
            except Exception as ex:
                print ex
                send(msgs['from_id'], 'Не удалось сделать репосты. Возможно, у '
                                     'бота появилась капча, или пост находится в закрытой группе.')
                print('Боту не удалось сделать репосты \033[36m%s\033[0m' % datetime.now())
                continue
            else:
                send(msgs['from_id'], 'Бот сделал 10 репостов на указанной записи!')
                print('Репосты сделаны \033[36m%s\033[0m' % datetime.now())
        sleep(1)

clear()
main()