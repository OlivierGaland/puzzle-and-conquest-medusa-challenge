import time
from threading import Thread
from collections import deque
from copy import copy,deepcopy

UNKNOWN = ''
VOID = ' '

EMPTY_FLASK = None

class Flask(deque):
    def __init__(self,arr = None):
        super().__init__()
        if arr is not None:
            if len(arr) != 4: raise Exception('Wrong number of arguments')
            for i in range(0,4):
                if arr[i] is not VOID: self.push(arr[i]) 
                else: break

    @property
    def is_full(self):
        return len(self) == 4

    @property
    def is_empty(self):
        return len(self) == 0
    

    @property
    def same_color(self):
        color = None
        for i in self:
            if color is None : color = i
            elif color != i: return False
        return True    

    def push(self,a): 
        if len(self) >= 4: raise Exception('Stack Overflow')
        self.append(a)

    def __str__(self):
        ret = "|"
        for i in self:
            ret += str(i) if i != '' else '0' 
        return ret

class Factory:
    def __init__(self,inp):
        self.items = []
        self.history = list()
        for item in inp:
            self.items.append(Flask(item))
        self.validate()

    def validate(self):
        #print("VALIDATE")
        d = dict()
        for item in self.items:
            for c in item:
                if c in d.keys():
                    d[c] += 1
                else:
                    d[c] = 1

        print("INPUT "+str(d))
        self.is_count_valid(d)
        print("INITIAL POSSIBLE MOVES " + str(self.get_possible_moves()))

    def is_count_valid(self,items):
        for item in items:
            if items[item] != 4:
                raise Exception('Error in initial settings : '+str(item)+" = "+str(items[item]))


    def __str__(self):
        ret = ""
        i = 1
        for item in self.items:
            ret+=str(i)+': '+str(item)+'\n'
            i+=1

        for item in self.history:
            ret+=str(item[0]+1)+"=>"+str(item[1]+1)+" "

        return ret
    
    def solve(self,first_move = None):

        if self.is_win():
            print("WON !!!!!!")
            print(self)
            #print(self.history)
            exit(0)
            return

        if self.is_fail():
            print("FAIL !!!!!!")
            return

        possible_moves = self.get_possible_moves()
        #print(self.history)
        #print(possible_moves)

        # if len(possible_moves) == 0:
        #     print("NO MORE MOVE")
        #     print(self.history)
        #     print(possible_moves)
        #     exit(0)
        #     return

        i = 0
        for move in possible_moves:
            i+=1

            # tune initial move
            if first_move is not None:
                print(str(move)+" => "+str(len(possible_moves))+" possibles moves")
                if i < first_move: continue

            # discard loop moves
            if len(self.history) == 0 or not self.is_cycling(move):

                start = self.items[move[0]]
                end = self.items[move[1]]

                if end.is_empty and start.same_color: continue      # optimize, do not apply useless move : ex   AAA => Empty
                    #print("useless move : same color")
                    #print(self.items[move[0]])
                    #print(self.items[move[1]])
                    #pass

                #if len(self.history) > 0 and self.history[-1][0] == move[1] and self.history[-1][1] == move[0]: continue    # optimize , do not revert move
                    #print(str(self.history[-1])+" => "+str(move))
                if len(self.history) > 0:
                    #print("--------------")
                    #print(move)
                    cycle = False
                    for old_moves in reversed(self.history):
                        if old_moves[0] == move[1] and old_moves[1] == move[0]:
                            cycle = True   # revert move (cycle)
                            #print("cycle found")
                            break
                        elif move[0] == old_moves[0] or move[0] == old_moves[1]: break
                        elif move[1] == old_moves[0] or move[1] == old_moves[1]: break
                        #print (old_moves)
                    if cycle: continue

                tmp = deepcopy(self)
                tmp.swap(move[0],move[1])
                tmp.solve()

    def is_cycling(self,move): #TODO
        t = list()
        t.append(move)

        for i in range(0,len(self.history)):
            if self.history[-1-i] not in t: t.append(self.history[-1-i])
            elif t[0] == self.history[-1-i]: return True
            else: return False
            #else:
                #print("--------------0")
                #print(t)
                #print(self.history)
                #print("--------------1")
                #for j in range(0,len(t)):
                #    if 1+i+j >= len(self.history) or t[j] != self.history[-1-i-j]: return False
                #return True                

        return False

    def swap(self,start_idx,end_idx):
        self.history.append((start_idx,end_idx))
        t = self.items[start_idx].pop()
        self.items[end_idx].push(t)
        while not self.items[end_idx].is_full and not self.items[start_idx].is_empty and self.items[start_idx][-1] == t:
            self.items[end_idx].push(self.items[start_idx].pop())
        #print(self.history)

    def is_win(self):
        for flask in self.items:
            if flask.is_full:
                s = set()
                for item in flask: s.add(item)
                #print(len(s))
                if len(s) > 1: return False
            elif not flask.is_empty:
                return False
        return True

    def is_fail(self):
        if len(self.history) > len(self.items)*8: return True
        return False
        #for flask in self.items:

    def get_possible_moves(self):
        not_full = list()
        not_empty = list()
        possible_moves = list()
        for i in range(0,len(self.items)):
            if not self.items[i].is_empty: not_empty.append(i)
            if not self.items[i].is_full: not_full.append(i)
        #print('not full',not_full)
        #print('not empty',not_empty)
        for nf in not_full:
            for ne in not_empty:
                if nf != ne:
                    if self.items[nf].is_empty or self.items[nf][-1] == self.items[ne][-1]:

                        if (not self.items[nf].is_empty and self.items[nf][-1] == UNKNOWN) or self.items[ne][-1] == UNKNOWN:
                            pass
                        else:
                            possible_moves.append((ne,nf))

        #print('possible moves',possible_moves)
        return possible_moves


# Not working well yet : class is supposed to ease hidden tile reveal
class FactoryReveal(Factory):

    def is_count_valid(self,items):
        if items[UNKNOWN] != 0:
            for item in items:
                if item != UNKNOWN and items[item] > 4:
                    raise Exception('Error in initial settings : '+str(item)+" = "+str(items[item]))    
            return
        raise Exception('Error in initial settings : no UNKNOW item')    
    

    
    def solve(self,revealed,first_move = None):

        if revealed is None:
            revealed = list()
            for i in range(0,len(self.items)):
                revealed.append(False)
        else:
            for i in range(0,len(self.items)):
                if not self.items[i].is_empty and self.items[i][-1] == UNKNOWN:
                    revealed[i] = True

        possible_moves = self.get_possible_moves()
        #print(possible_moves)
        #exit(0)


        i = 0
        for item in revealed:
            if item: i+=1

        #if i > 0:
        if i > 1:
            j = 0
            for item in self.items:
                if not item.is_full: j+=1


            if j > 5:
            #if j > 3:
                ret = ""
                for item in self.history:
                    ret+=str(item[0]+1)+"=>"+str(item[1]+1)+" "
                print("Found solution : revealed "  + str(i) + " items, "+str(j)+" flasks are not full : "+ret)
                #print(self)
                return


        if len(possible_moves) == 0:
            return

        i = 0
        for move in possible_moves:
            i += 1

            # tune initial move
            if first_move is not None:
                print(str(move)+" => "+str(len(possible_moves))+" possibles moves")
                if i != first_move: continue            

            # discard loop moves
            if len(self.history) == 0 or not self.is_cycling(move):

                start = self.items[move[0]]
                end = self.items[move[1]]

                if end.is_empty and start.same_color: continue      # optimize, do not apply useless move : ex   AAA => Empty

                if len(self.history) > 0:
                    cycle = False
                    for old_moves in reversed(self.history):
                        if old_moves[0] == move[1] and old_moves[1] == move[0]:
                            cycle = True   # revert move (cycle)
                            break
                        elif move[0] == old_moves[0] or move[0] == old_moves[1]: break
                        elif move[1] == old_moves[0] or move[1] == old_moves[1]: break
                    if cycle: continue

                tmp = deepcopy(self)
                tmp_revealed = deepcopy(revealed)
                tmp.swap(move[0],move[1])
                tmp.solve(tmp_revealed)




def task(factory):
    print('Starting the task '+str(factory.history)+' ...')
    time.sleep(5)
    factory.solve()
    #print(f'The task {id} completed')



def solve_monothread(init,initial_move_index = None):
    f = Factory(init)
    f.solve(initial_move_index)

def solve_multithread(init):
    f = Factory(init)
    possible_moves = f.get_possible_moves()
    factory_list = dict()

    for i in range(0,len(possible_moves)//2):        # there should be 2 empty flasks : so get only first half of possible moves
        tmp = deepcopy(f)
        tmp.swap(possible_moves[i][0],possible_moves[i][1])
        possible_moves_tmp = tmp.get_possible_moves()
        for move in possible_moves_tmp:
            tmp2 = deepcopy(tmp)
            tmp2.swap(move[0],move[1])
            factory_list[str(tmp2.history)] = tmp2

    #print(len(factory_list))

    threads = []
    for f in factory_list.values():
        t = Thread(target=task, args=(f,))
        threads.append(t)
        t.start()

    # wait for the threads to complete
    for t in threads:
        t.join()



# A yellow, B red, C pink, D clear blue
# E dark green, F purple, G green, H dark blue
# I orange

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

# A purple , B orange , C clear blue , D pink
# E red , F dark red , G green , H dark blue
# I dark green , J yellow
INIT6A = [ ['A','B','C','B'],
          ['D','D','E','A'],
          ['D','F','G','H'],
          ['C','B','E','H'],
          ['C','F','H','E'],
          ['H','A','F','I'],

          ['I','J','I','G'],
          ['J','G','F','A'],
          ['J','E','G','B'],
          ['J','C','D','I'],
          EMPTY_FLASK,
          EMPTY_FLASK ]


# A green , B dark red , C dark green , D yellow
# E clear blue , F flesh , G orange , H purple
# I red , J dark blue , K pink

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


# A green , B red , C purple , D flesh
# E orange , F dark red , G dark pink , H blue
# I yellow , J pink , K dark green , L clear blue

INIT8A = [ ['K','G','A','B'],
          ['L','F','C','B'],
          ['I','D','L','D'],
          ['I','D','E','F'],
          ['I','K','G','A'],
          ['J','L','E','H'],

          ['L','J','H','E'],
          ['H','C','I','J'],
          ['B','K','F','E'],
          ['G','C','J','F'],
          ['K','C','B','H'],
          ['G','A','D','A'],

          EMPTY_FLASK,
          EMPTY_FLASK ]



# A dark blue , B green , C clear blue , D dark red
# E yellow , F dark green , G pink , H red
# I orange , J dark pink , K flesh , L grey
# M purple

INIT9A = [ ['I','L','F','A'],
          ['E','K','A','B'],
          ['D','F','J','C'],
          ['L','A','C','D'],
          ['I','B','M','E'],
          ['D','J','H','F'],

          ['C','M','J','G'],
          ['D','M','K','H'],
          ['B','L','A','G'],
          ['K','I','C','G'],
          ['E','H','G','B'],
          ['E','M','K','I'],

          ['H','L','J','F'],
          EMPTY_FLASK,
          EMPTY_FLASK ]

# A dark green, B dark blue , C orange , D purple
# E dark red , F green , G red , H grey
# I yellow , J flesh , K clear blue , L pink
# M dark pink , N dark purple

INIT10A = [ ['M','E','A','B'],
           ['N','H','C','D'],
           ['L','E','F','G'],
           ['H','I','G','A'],
           ['K','M','B','J'],
           ['M','I','D','K'],

           ['C','H','B','C'],
           ['J','K','F','E'],
           ['B','L','J','L'],
           ['M','H','C','A'],
           ['N','A','I','G'],
           ['N','F','D','J'],

           ['L','N','F','D'],
           ['G','I','E','K'],
           EMPTY_FLASK,
           EMPTY_FLASK ]

# Your code here 
#   define your INIT array 
#      note the bottom of the flask is at left side of array, top is at right 
#      use a single letter for each color, and EMPTY_FLASK if flask is empty
#
#   call :
#           solve_monothread   : try all moves in sequence (could take time if you are not lucky on the first move)
#        or solve_multithread  : will create a thread for each possible first move x second move (should be faster to solve as some first move have no solution)
#
#     solve_monothread(INIT5A)   : solve INIT5A trying moves in sequence
#     solve_monothread(INIT5A,3) : solve INIT5A with the 3th initial move as the first move
#     solve_multithread(INIT5A)  : solve INIT5A with multithreading (1 thread for each combination of fixed first and second move)
#
#   PREFER solve_multithread !

#solve_monothread(INIT5A,3)
solve_monothread(INIT5A,3)
#solve_multithread(INIT5A)

