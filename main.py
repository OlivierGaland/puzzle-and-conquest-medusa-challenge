import time
from threading import Thread,RLock
from copy import deepcopy
from og_log import LOG

UNKNOWN = '?'
VOID = '0'

EMPTY_FLASK = [ VOID,VOID,VOID,VOID ]

class Flask(list):
    def __init__(self,arr = [ '0','0','0','0' ]):
        super().__init__()
        if len(arr) != 4: raise Exception('Wrong number of arguments')
        endFound = False
        for i in range(0,4):
            if endFound and arr[i] != VOID: raise Exception('Wrong filling of flask') 
            if arr[i] is VOID: endFound = True
            self.push(arr[i])

    @property
    def is_full(self):
        return self[3] != VOID

    @property
    def is_empty(self):
        return self[0] == VOID
    

    @property
    def same_color(self):
        color = self[0]
        for i in self:
            if i != color: return False
        return True
    
    def view_top(self):
        for i in reversed(range(0,len(self))):
            if self[i] != VOID:
                return self[i]
        return None

    def push(self,a): 
        for i in range(0,len(self)):
            if self[i] == VOID and a != VOID:
                self[i] = a
                return
        if len(self) < 4:
            self.append(a)
            return
        raise Exception('Stack Overflow')    
    
    def pop(self):
        for i in reversed(range(0,len(self))):
            if self[i] != VOID:
                ret = self[i]
                self[i] = VOID
                return ret
        raise Exception('Stack Underflow')

    def __str__(self):
        ret = "|"
        for i in self:
            ret += str(i) if i != '' else '0' 
        return ret
    
class FingerPrint():

    def __init__(self):
        self.items = []
        self.lock = RLock()
        self.discarded = 0

    def push(self,a): 
        if self.lock.acquire(True,10):
            if a not in self.items:
                self.items.append(a)
                self.lock.release()
                return True
            else:
                self.discarded += 1
                self.lock.release()
                return False
        else:
            raise Exception('Could not acquire lock')
        
    def __str__(self):
        return '\n'.join(self.items)

class Factory:
    def __init__(self,inp,fingerprint):
        self.items = []
        self.history = list()
        for item in inp:
            self.items.append(Flask(item))
        self.validate()
        if not fingerprint.push(self.get_fingerprint()):
            raise Exception('Fingerprint already exist : '+str(self.get_fingerprint()))

    def get_fingerprint(self):
        tmp = [ str(item) for item in self.items ] 
        tmp.sort()
        return ''.join(tmp)

    def validate(self):
        d = dict()
        for item in self.items:
            for c in item:
                if c in d.keys():
                    d[c] += 1
                else:
                    d[c] = 1

        LOG.info("Input : "+str(d))
        self.is_count_valid(d)
        LOG.info("Initial possible moves " + str(self.get_possible_moves()))

    def is_count_valid(self,items):
        for item in items:
            if items[item] != 4 and item != VOID:
                LOG.warning('Initial settings not balanced : '+str(item)+" = "+str(items[item]))


    def __str__(self):
        ret = ""
        i = 1
        for item in self.items:
            ret+=str(i)+': '+str(item)+'\n'
            i+=1

        for item in self.history:
            ret+=str(item[0]+1)+"=>"+str(item[1]+1)+" "

        return ret
    
    def solve(self,fingerprint):

        if self.is_win():
            LOG.info("Solution found : "+str(self.history))
            print(self)
            return

        if self.is_fail(): return

        possible_moves = self.get_possible_moves()

        for move in possible_moves:
            start = self.items[move[0]]
            end = self.items[move[1]]            

            if end.is_empty and start.same_color: continue      # optimize, do not apply useless move : ex   AAA => Empty

            tmp = deepcopy(self)
            if tmp.swap(move[0],move[1],fingerprint):
                tmp.solve(fingerprint)

    def swap(self,start_idx,end_idx,fingerprint):
        self.history.append((start_idx,end_idx))

        cfrom = self.items[start_idx].view_top()
        cto = self.items[end_idx].view_top()
        color = cfrom
        success = False

        while not self.items[end_idx].is_full and (cto is None or cfrom == cto):
            success = True
            self.items[end_idx].push(self.items[start_idx].pop())
            cto = cfrom
            cfrom = self.items[start_idx].view_top()
            if color != cfrom: break

        if success: return fingerprint.push(self.get_fingerprint())
        raise Exception('Impossible swap : '+str(self.items[start_idx])+" => "+str(self.items[end_idx]))


    def is_win(self):

        win = True
        for flask in self.items:
            if not flask.is_full and not flask.is_empty:
                win = False
                continue
            if not flask.same_color:
                win = False
                continue

        return win

    def is_fail(self):
        #if len(self.history) > len(self.items)*6: return True   # *8
        return False


    def get_possible_moves(self):
        not_full = list()
        not_empty = list()
        possible_moves = list()
        for i in range(0,len(self.items)):
            if not self.items[i].is_empty: not_empty.append(i)
            if not self.items[i].is_full: not_full.append(i)

        for nf in not_full:
            for ne in not_empty:
                if nf != ne:
                    if self.items[nf].is_empty or self.items[nf].view_top() == self.items[ne].view_top():

                        if (not self.items[nf].is_empty and self.items[nf].view_top() == UNKNOWN) or self.items[ne].view_top() == UNKNOWN:
                            pass
                        else:
                            possible_moves.append((ne,nf))

        return possible_moves



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



INIT2 = [ ['A','C','B','B'],
          ['A','C','A','B'],
          ['C','C','A','B'],
          EMPTY_FLASK,
          EMPTY_FLASK ]

INIT = [ ['A','A','B','B'],
          ['A','B','A','B'],
          EMPTY_FLASK,
          EMPTY_FLASK ]


INIT5A = [ ['A','B','C','B'],
          ['D','C','E','C'],
          ['D','F','B','G'],
          ['G','H','E','I'],
          ['F','I','F','G'],
          ['I','H','C','G'], 

          ['H','D','A','F'], 
          ['H','A','E','D'],
          ['A','E','B','I'],
          EMPTY_FLASK,
          EMPTY_FLASK ]

INIT7A = [ ['J','A','B','C'],
           ['K','C','A','D'],
           ['K','I','E','F'],
           ['J','C','F','D'],
           ['G','H','B','H'],
           ['J','A','B','C'],

           ['G','D','H','F'],
           ['G','E','I','F'],
           ['K','D','I','E'],
           ['K','J','E','I'],
           ['A','G','B','H'], 
           EMPTY_FLASK,
           EMPTY_FLASK ]

# A purple , B orange , C clear blue , D pink
# E red , F dark red , G green , H dark blue
# I dark green , J yellow
INIT6C = [ ['C','A','B','C'],
          ['G','F','D','E'],
          ['H','I','A','G'],
          ['F','A','J','B'],
          ['F','J','G','D'],
          ['B','H','I','D'],

          ['E','H','B','J'],
          ['I','H','D','E'],
          ['C','I','G','A'],
          ['E','F','J','C'],
          EMPTY_FLASK,
          EMPTY_FLASK,
          EMPTY_FLASK ]


# Your code here 
#   define your INIT array 
#      note the bottom of the flask is at left side of array, top is at right 
#      use a single letter for each color, and EMPTY_FLASK if flask is empty
#
#   call :
#           solve_monothread   : try all moves in sequence
#        or solve_multithread  : will create a thread for each possible first move x second move 
#                                (should be faster to solve as some first move have no solution)
#
#     solve_monothread(INIT5A)   : solve INIT5A trying moves in sequence
#     solve_multithread(INIT5A)  : solve INIT5A with multithreading (1 thread for each combination of fixed first and second move)
#
#   PREFER solve_multithread !

LOG.start()
solve_multithread(INIT6C)


