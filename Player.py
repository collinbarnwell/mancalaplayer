# File: Player.py
# Author(s) names AND netid's:
# Date: 
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board, "max"), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board, "max")
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board, "max")
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board, "min")
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board, "min")
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board, mValue):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
            """ Choose a move with alpha beta pruning.  Returns (score, move) """
            move = -1
            array1=[-INFINITY, INFINITY]#holds alpha and beta
            score = -INFINITY
            turn = self
            for m in board.legalMoves(self):

                if ply == 0:
                    return (self.score(board, "max"), m)
                if board.gameOver():
                    return (-1, -1)  # Can't make a move, the game is over
                nb = deepcopy(board)

                nb.makeMove(self, m)

                opp = Player(self.opp, self.type, self.ply)
                s = opp.abminValue(nb, ply-1, turn, array1)

                if s > score:

                    move = m
                    score = s

            return score, move

    def abmaxValue(self, board, ply, turn, array):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        array2=[array[0],array[1]]
        if board.gameOver():
            return turn.score(board, "max")
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:

                return turn.score(board, "max")

            opponent = Player(self.opp, self.type, self.ply)

            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.abminValue(nextBoard, ply-1, turn, array)
            if s > score:
                score = s
            if score >= array2[1]:
                return score
            if array2[0]<score:
                array2[0]=score
        return score

    def abminValue(self, board, ply, turn, array):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        array2=[array[0],array[1]]
        if board.gameOver():
            return turn.score(board, "min")
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board, "min")
            opponent = Player(self.opp, self.type, self.ply)
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.abmaxValue(nextBoard, ply-1, turn, array)

            if s < score:
                score = s
            if score <= array2[0]:
                return score
            if array2[1]>score:
                array2[1]=score
        return score

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class crb331(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def compareToExtra(self, board, originalVal, originalMove):
        """Evaluates potential of moves that will earn an extra move"""
        # look at possible moves that will earn an extra turn
        # evaluate board from each of those, add 2 to val
        cups = board.getPlayersCups(self)
        bestMove = originalMove
        bestVal = originalVal

        for m in board.legalMoves(self):
            if 7 - m != cups[6 - m]:
                continue

            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)

            # check how well taking extra move sets you up (+2 for extra open space and mancala + 1)
            newVal, x = self.alphaBetaMove(nextBoard, self.ply)
            if newVal + 2 >= bestVal:
                print "we found somethin good!"
                bestVal = newVal + 2
                bestMove = m

        return (bestVal, bestMove)

    def score(self, board, mTurn):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        print "Calling score in MancalaPlayer"
        #return board.boardScore( self.num )
        k=0
        # if you have an empty cup and the opponent's corresponding cup is not empty,
        # check to see if you can end in that cup to steal their stone if it's your turn.
        # Do the corresponding thing if it's their turn.
        if(mTurn == "min"):
            for x in range(0,6):
                if  board.getPlayersCups(self.num)[x]==0 and board.getPlayersCups(self.opp)[5-x] !=0:
                    for y in range(0,x):
                     if board.getPlayersCups(self.num)[y]+ y == x:
                        k += board.getPlayersCups(self.opp)[5-x] + 1
        else:
            for x in range(0,6):
                if  board.getPlayersCups(self.opp)[x]==0 and board.getPlayersCups(self.num)[5-x] !=0:
                    for y in range(0,x):
                     if board.getPlayersCups(self.opp)[y]+ y == x:
                        k -= board.getPlayersCups(self.num)[5-x] + 1
        
            
        
##        if board.getPlayersCups(self.num)[x]+x==5:#extra move might be there
##            k=k+1
        k += (board.boardScore(self.num) - board.boardScore(self.opp))
        if board.boardScore(self.num)>24:#changed board score
            k+= 1000.0
        if board.hasWon(self.num):
            k+= 1000.0
        if board.hasWon(self.opp) or board.boardScore(self.opp)>24:
            k=0.0
        return k

