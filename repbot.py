#coding: utf-8

import vk
from random import randint as random
from time import sleep
from subprocess import call as cl
from datetime import datetime

api_group = vk.API(vk.AuthSession(access_token='f94a409b058107892d3677ae352c4ee76319857daa58a3312b9040cd19ddb0e25f0349d07cd47e96f088f'),v='5.80')
api_profile = vk.API(vk.AuthSession(access_token='d60e0a9b178c44e239855f0a2c44f67b89ec53b137b70974deab9648d4eec5971b81138590631995e10a5'),v='5.80')


def clear():
    a = cl('clear')
    a = cl('clear')


def longpoll():
    info = api_group.messages.getLongPollServer(need_pts='1', group_id='169970841')
    return {'ts': info['ts'], 'pts': info['pts']}


def getupd(lpinf):
    upds = api_group.messages.getLongPollHistory(ts=lpinf['ts'], pts=lpinf['pts'], lp_version='3')
    return upds['messages']['items']


def send(user_id, message):
    api_group.messages.send(user_id=user_id, message=message)


def repost(object, nums):
    ids = ['169976139', '169976170', '169976196', '169976274', '169976293',
           '169980485', '169980543', '169980587', '169980618', '169980637']
    n = 0
    for i in ids:
        print('Бот сделал репост на группу \033[33m%s\033[0m \033[36m%s\033[0m' % (i,datetime.now()))
        api_profile.wall.repost(object=object, group_id=i)
        sleep(nums[n])
        n += 1

clear()


def main():

    lpinf = longpoll()
    while(True):
        messages = getupd(lpinf)
        print('Бот получил обновление сообщений \033[36m%s\033[0m' % datetime.now())

        n = 0

        for i in messages:
            if i['out'] == '1':
                messages.pop(n)
            n += 1

        for msg in messages:
            try:
                msg['attachments'][0]['wall']
            except:
                send(msg['from_id'], 'Не удалось найти пост. Чтобы бот смог найти пост, '
                                     'просто сделайте репост этого поста боту в сообщения.')
                print('Бот не смог найти прикрепленную запись \033[36m%s\033[0m' % datetime.now())
            else:
                nums = []
                for i in range(0,10):
                    nums.append(random(3,10))

                send(msg['from_id'], 'Бот начал делать репосты. Действие займет %s секунд' % sum(nums))
                print('Бот начал делать репосты \033[36m%s\033[0m' % datetime.now())


                try:
                    mesa = 'wall%s_%s' %(msg['attachments'][0]['wall']['from_id'], msg['attachments'][0]['wall']['id'])
                    repost(mesa, nums)
                except Exception as ex:
                    print ex
                    send(msg['from_id'], 'Не удалось сделать репосты. Возможно, у '
                                         'бота появилась капча, или пост находится в закрытой группе.')
                    print('Боту не удалось сделать репосты \033[36m%s\033[0m' % datetime.now())
                    lpinf = longpoll()
                    continue
                else:
                    send(msg['from_id'], 'Бот сделал 10 репостов на указанной записи!')
                    print('Репосты сделаны \033[36m%s\033[0m' % datetime.now())
            sleep(2)

        lpinf = longpoll()
        sleep(2)


main()
