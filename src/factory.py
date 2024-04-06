from threading import RLock
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

