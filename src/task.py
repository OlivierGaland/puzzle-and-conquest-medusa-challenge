import time
from threading import Thread,RLock
from copy import deepcopy
from og_log import LOG

from src.factory import Factory,FingerPrint

def task(factory,fingerprint):
    id = str(factory.history)
    print('Starting the task '+id+' ...')
    time.sleep(5)
    factory.solve(fingerprint)
    fingerprint.workers -= 1
    LOG.info('The task '+id+' is complete')


def monitor(fingerprint):
    LOG.info('Fingerprint count : '+str(len(fingerprint.items))+', discarded : '+str(fingerprint.discarded)+', workers : '+str(fingerprint.workers))
    while fingerprint.workers > 0:
        time.sleep(10)
        LOG.info('Fingerprint count : '+str(len(fingerprint.items))+', discarded : '+str(fingerprint.discarded)+', workers : '+str(fingerprint.workers))


def solve_monothread(init,initial_move_index = None):
    fp = FingerPrint()
    f = Factory(init)
    f.solve(initial_move_index,fp)

def solve_multithread(init):
    fp = FingerPrint()
    f = Factory(init,fp)

    possible_moves = f.get_possible_moves()
    factory_list = dict()

    for i in range(0,len(possible_moves)):       
        tmp = deepcopy(f)
        if tmp.swap(possible_moves[i][0],possible_moves[i][1],fp):
            possible_moves_tmp = tmp.get_possible_moves()
            for move in possible_moves_tmp:
                try:
                    tmp2 = deepcopy(tmp)
                    if tmp2.swap(move[0],move[1],fp):
                        factory_list[str(tmp2.history)] = tmp2
                except Exception as e:
                    LOG.warning('Error : '+str(e))

    fp.workers = 0

    threads = []
    for f in factory_list.values():
        t = Thread(target=task, args=(f,fp,))
        threads.append(t)
        fp.workers += 1
        t.start()

    LOG.info("All threads started : Count is "+str(len(threads)))


    m = Thread(target=monitor, args=(fp,))
    m.start()

    # wait for the threads to complete
    for t in threads:
        t.join()

    LOG.info("All threads finished : Count is "+str(len(threads)))

