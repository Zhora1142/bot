#coding: utf-8
import vk
from Queue import Queue
from threading import Thread
from time import sleep

global messagess
messagess = Queue()


def msgs():

    api_group = vk.API(vk.AuthSession(access_token='f94a409b058107892d3677ae352c4ee76319857daa58a3312b9040cd19ddb0e25f0349d07cd47e96f088f'), v='5.80')
    inf = api_group.messages.getLongPollServer(need_pts='1', group_id='169970841')
    inf = {'ts': inf['ts'], 'pts': inf['pts']}

    while True:
        upds = api_group.messages.getLongPollHistory(ts=inf['ts'], pts=inf['pts'], lp_version='3')
        msg = upds['messages']['items']
        n = 0
        for i in msg:
            if i['out'] == '1':
                msg.pop(n)
            n += 1
        if msg is not []:
            messagess.put(msg)
        inf = api_group.messages.getLongPollServer(need_pts='1', group_id='169970841')
        inf = {'ts': inf['ts'], 'pts': inf['pts']}
        sleep(1)


def main():

    getmsg = Thread(target=msgs, args=())
    getmsg.setDaemon(True)
    getmsg.start()

    while True:
        print messagess.get()
        sleep(1)

main()