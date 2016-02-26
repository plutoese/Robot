# coding=UTF-8

import threading
from time import sleep, ctime


class PersonalThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.res = None

    def get_result(self):
        return self.res

    def run(self):
        self.res = self.func(*self.args)

if __name__ == '__main__':

    loops = [4,2,6]

    def loop(nloop, nsec):
        print('start loop ',nloop,' at: ',ctime())
        sleep(nsec)
        print('loop ',nloop,' done at: ',ctime())
        return nloop

    print('starting at: ',ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = PersonalThread(func=loop,args=(i,loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()
        print(threads[i].get_result())

    print('all DONE at: ',ctime())















