from og_log import LOG
from src.factory import EMPTY_FLASK
from src.task import solve_multithread,solve_monothread


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




INIT7D = [ ['A','B','C','D'],
           ['C','A','B','E'],
           ['F','G','A','H'],
           ['H','I','J','E'],
           ['K','D','J','E'],
           ['K','H','J','I'],

           ['F','G','C','D'],
           ['C','I','B','K'],
           ['G','D','E','H'],
           ['J','F','I','K'],
           ['F','G','A','B'],
           EMPTY_FLASK,
           EMPTY_FLASK ]
# BFJ
# INIT8D = [ ['A','B','A','C'],
#            ['D','B','E','F'],
#            ['D','G','H','F'],
#            ['C','F','I','H'],       
#            ['C','J','G','D'],
#            ['B','?','H','K'],

#            ['H','?','J','I'],
#            ['A','L','A','D'],
#            ['K','E','L','K'],
#            ['I','C','E','K'],
#            ['?','G','I','L'],
#            ['J','G','L','E'],  
#            EMPTY_FLASK,
#            EMPTY_FLASK ]

INIT8D = [ ['A','B','A','C'],
           ['D','B','E','F'],
           ['D','G','H','F'],
           ['C','F','I','H'],       
           ['C','J','G','D'],
           ['B','J','H','K'],

           ['H','B','J','I'],
           ['A','L','A','D'],
           ['K','E','L','K'],
           ['I','C','E','K'],
           ['F','G','I','L'],
           ['J','G','L','E'],  
           EMPTY_FLASK,
           EMPTY_FLASK ]

INIT9D = [ ['A','B','C','D'],
           ['E','F','D','G'],
           ['H','D','I','J'],
           ['K','B','J','I'],
           ['L','H','M','F'],
           ['G','A','G','E'],

           ['L','B','D','A'],
           ['M','L','H','G'],
           ['L','C','M','K'],
           ['B','H','F','M'],
           ['I','F','C','A'],
           ['J','K','J','E'],

           ['K','I','C','E'],
           EMPTY_FLASK,
           EMPTY_FLASK ]

INIT0D = [ ['A','B','C','A'],
           ['D','E','F','G'],
           ['H','F','E','I'],
           ['C','A','H','J'],
           ['K','G','L','H'],
           ['J','D','H','G'],

           ['F','I','M','F'],
           ['K','A','N','L'],
           ['M','J','I','M'],
           ['K','M','C','E'],
           ['C','L','K','I'],
           ['N','B','G','J'],

           ['E','N','B','D'],
           ['B','N','D','L'],
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
solve_multithread(INIT0D)


