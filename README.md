# puzzle-and-conquest-medusa-challenge
Python script to help solving medusa challenge in mobile game puzzle and conquest.

This script will help solving this challenge in this mobile game : 
 - you have several flasks with different color tiles, you need to end with flasks having same color tiles

Start :
![image](https://github.com/OlivierGaland/puzzle-and-conquest-medusa-challenge/assets/26048157/465dc112-4765-4814-8157-7fac95cf67bf)

End (almost finished) :
![image](https://github.com/OlivierGaland/puzzle-and-conquest-medusa-challenge/assets/26048157/c4c1e854-7d73-4bfd-a1f9-ec73446c0c9f)

How to use it :
- Get the python script
- Add inside an array describing the mapping of the flasks
- Add inside the call to solve the enigma
- Run the script and wait

Example :

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

solve_multithread(INIT5A)
