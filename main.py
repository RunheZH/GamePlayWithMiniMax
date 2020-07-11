from random import randint
from lib import Constants
from player import Player, State

class Pit:
    def __init__(self, numStones, is_player1=True, is_pocket=False):
        self.numStones = numStones
        self.is_player1 = is_player1
        self.is_pocket = is_pocket

    def setNumStones(self, newNumStones):
        self.numStones = newNumStones

    def setToPlayer2(self):
        self.is_player1 = False

    def setToPlayer1(self):
        self.is_player1 = True

    def setIsPocket(self, newBool):
        self.is_pocket = newBool

    def putInAStone(self):
        self.numStones = self.numStones + 1

    def getNumStones(self):
        return self.numStones

    def getIsPlayer1(self):
        return self.is_player1

    def getIsPocket(self):
        return self.is_pocket

def initGame(board, p1, p2, num_stones):
    # reset
    #board = []
    for i in range(Constants.NUM_PITS):
        board.append(Pit(num_stones))

    # by default, all pits belong to player 1
    p1.setPits(Constants.P1_PITS)
    p1.setPockets(Constants.P1_POCKETS)
    p2.setOppoPockets(Constants.P1_POCKETS)
    p2.setOppoPits(Constants.P1_PITS)

    for i in Constants.P1_POCKETS:
        board[i].setNumStones(0)
        board[i].setIsPocket(True)

    p2.setPits(Constants.P2_PITS)
    p2.setPockets(Constants.P2_POCKETS)
    p1.setOppoPockets(Constants.P2_POCKETS)
    p1.setOppoPits(Constants.P2_PITS)
    
    for i in Constants.P2_POCKETS:
        board[i].setToPlayer2()
        board[i].setNumStones(0)
        board[i].setIsPocket(True)

def printBoard(board):
    print("            \033[1;34;17m|   " +
          str(board[Constants.P2_POCKETS[0]].getNumStones()) + "   |")

    print("            | " + str(board[Constants.P2_PITS[0]].getNumStones()) +
          " | " + str(board[Constants.P2_PITS[1]].getNumStones()) +
          " |")
    print("            | " + str(board[Constants.P2_PITS[2]].getNumStones()) +
          " | " + str(board[Constants.P2_PITS[3]].getNumStones()) +
          " |")

    print("\033[1;31;17m|   | " + str(board[Constants.P1_PITS[0]].getNumStones()) +
          " | " + str(board[Constants.P1_PITS[1]].getNumStones()) +
          " | " + str(board[Constants.P1_PITS[2]].getNumStones()) +
          " |\033[1;34;17m " + str(board[Constants.P2_PITS[4]].getNumStones()) +
          " \033[1;31;17m| " + str(board[Constants.P1_PITS[3]].getNumStones()) +
          " | " + str(board[Constants.P1_PITS[4]].getNumStones()) +
          " |   |")

    print("\033[1;31;17m| " + str(board[Constants.P1_POCKETS[0]].getNumStones()) + " |"
          "                       " +
          "| " + str(board[Constants.P1_POCKETS[1]].getNumStones()) + " |")

    print("|   | " + str(board[Constants.P1_PITS[5]].getNumStones()) +
          " | " + str(board[Constants.P1_PITS[6]].getNumStones()) +
          " |\033[1;34;17m " + str(board[Constants.P2_PITS[5]].getNumStones()) +
          "\033[1;31;17m | " + str(board[Constants.P1_PITS[7]].getNumStones()) +
          " | " + str(board[Constants.P1_PITS[8]].getNumStones()) +
          " | " + str(board[Constants.P1_PITS[9]].getNumStones()) +
          " |   |")

    print("\033[1;34;17m            | " + str(board[Constants.P2_PITS[6]].getNumStones()) +
          " | " + str(board[Constants.P2_PITS[7]].getNumStones()) +
          " |")
    print("            | " + str(board[Constants.P2_PITS[8]].getNumStones()) +
          " | " + str(board[Constants.P2_PITS[9]].getNumStones()) +
          " |")

    print("            |   " +
          str(board[Constants.P2_POCKETS[1]].getNumStones()) + "   |\033[0m")

def updateBoard(board, move):
    for i in range(len(board)):
        board[i].setNumStones(move.getBoard()[i])

def isOutOfMoves(board, pits):
    for pit in pits:
        if not board[pit].getNumStones() == 0:
            return False
    return True

def startGameCvC():
    board = []
    player_1 = Player(1)
    player_2 = Player(2)
    p1_nodes = 0
    p2_nodes = 0

    print("\033[1;31;17mPlayer 1\033[0m uses the Mini-Max Algorithm.")
    print("\033[1;34;17mPlayer 2\033[0m uses the Alpha-Beta Algorithm.")

    #num_stones = randint(1, Constants.MAX_STONES)
    num_stones = Constants.NUM_STONES
    initGame(board, player_1, player_2, num_stones)
    printBoard(board)

    rand = randint(0, 1)
    if rand == 0:
        print("\033[1;31;17mPlayer 1\033[0m makes the first move.")
    else:
        print("\033[1;34;17mPlayer 2\033[0m makes the first move.")

    while rand == 0:
        if isOutOfMoves(board, Constants.P1_PITS):
            print("\033[1;31;17mPlayer 1\033[0m is out of moves, skip to player 2:")
        else:
            move, node_count = player_1.minimax_decision(board)
            #move, node_count = player_1.alpha_beta_search(board)
            p1_nodes = p1_nodes + node_count
            print("\033[1;31;17mPlayer 1\033[0m chose to move the stones in pit #" +
                str(move.getPitIndex()) + ":")
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

        if isOutOfMoves(board, Constants.P2_PITS):
            print(
                "\033[1;34;17mPlayer 2\033[0m is out of moves, skip to player 1:")
        else:
            #move, node_count = player_2.minimax_decision(board)
            move, node_count = player_2.alpha_beta_search(board)
            p2_nodes = p2_nodes + node_count
            print("\033[1;34;17mPlayer 2\033[0m chose to move the stones in pit #" +
                str(move.getPitIndex()) + ":")
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

    while rand == 1:
        if isOutOfMoves(board, Constants.P2_PITS):
            print("\033[1;34;17mPlayer 2\033[0m is out of moves, skip to player 1:")
        else:
            #move, node_count = player_2.minimax_decision(board)
            move, node_count = player_2.alpha_beta_search(board)
            p2_nodes = p2_nodes + node_count
            print("\033[1;34;17mPlayer 2\033[0m chose to move the stones in pit #" +
                  str(move.getPitIndex()) + ":")
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

        if isOutOfMoves(board, Constants.P1_PITS):
            print(
                "\033[1;31;17mPlayer 1\033[0m is out of moves, skip to player 2:")
        else:
            move, node_count = player_1.minimax_decision(board)
            #move, node_count = player_1.alpha_beta_search(board)
            p1_nodes = p1_nodes + node_count
            print("\033[1;31;17mPlayer 1\033[0m chose to move the stones in pit #" +
                  str(move.getPitIndex()) + ":")
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

    p1_score = board[Constants.P1_POCKETS[0]].getNumStones() + board[Constants.P1_POCKETS[1]].getNumStones()
    p2_score = board[Constants.P2_POCKETS[0]].getNumStones() + board[Constants.P2_POCKETS[1]].getNumStones()

    if  p1_score > p2_score:
        print("\033[1;31;17mPlayer 1\033[0m Won!")
    elif p2_score > p1_score:
        print("\033[1;34;17mPlayer 2\033[0m Won!")
    else:
        print("It's a tie!")

    print("\033[1;31;17mPlayer 1\033[0m searched " + str(p1_nodes) + " nodes.")
    print("\033[1;34;17mPlayer 2\033[0m searched " + str(p2_nodes) + " nodes.")

def isValidPit(board, pit_index, pit_list):
    if pit_index in pit_list:
        if not board[pit_index].getNumStones() == 0:
            return True
    return False

def startGamePvC():
    board = []
    player_1 = Player(1)
    player_2 = Player(2)
    p2_nodes = 0
    alg_choice = -1
    valid_choice = False

    while not valid_choice:
        print("Please choose an algorithm that the computer should use:")
        print("1 - Mini-Max")
        print("2 - Alpha-Beta")
        alg_choice = int(input())
        if alg_choice == 1:
            print("\033[1;31;17mThe Computer\033[0m uses the Mini-Max Algorithm.")
            valid_choice = True
        elif alg_choice == 2:
            print("\033[1;34;17mThe Computer\033[0m uses the Alpha-Beta Algorithm.")
            valid_choice = True
        else:
            print("Invalid choice. Please type 1 or 2.")
            valid_choice = False

    #num_stones = randint(1, Constants.MAX_STONES)
    num_stones = Constants.NUM_STONES
    initGame(board, player_1, player_2, num_stones)
    printBoard(board)

    rand = randint(0, 1)
    if rand == 0:
        print("\033[1;31;17mThe player\033[0m makes the first move.")
    else:
        print("\033[1;34;17mThe Computer\033[0m makes the first move.")

    while rand == 0:
        if isOutOfMoves(board, Constants.P1_PITS):
            print(
                "\033[1;31;17mThe player\033[0m is out of moves, skip to the Computer:")
        else:
            pit_choice = -1
            pit_valid = False
            while not pit_valid:
                print("\033[1;31;17mThe player\033[0m's turn. Please choose a pit.")
                pit_choice = int(input())
                if isValidPit(board, pit_choice, Constants.P1_PITS):
                    pit_valid = True
                else:
                    print("Invalid choice, please try again.")

            print("\033[1;31;17mThe player\033[0m chose to move the stones in pit #" +
                  str(pit_choice) + ":")

            move = State(None, 0, pit_choice, board[pit_choice].getNumStones(), None)
            tempBoard = []
            for i in range(len(board)):
                tempBoard.append(board[i].getNumStones())
            newBoard = player_1.updateBoard(move, tempBoard)
            move.setBoard(newBoard)
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

        if isOutOfMoves(board, Constants.P2_PITS):
            print(
                "\033[1;34;17mThe Computer\033[0m is out of moves, skip to the player:")
        else:
            print("\033[1;34;17mThe Computer\033[0m's turn.")
            if alg_choice == 1:
                move, node_count = player_2.minimax_decision(board)
            elif alg_choice == 2:
                move, node_count = player_2.alpha_beta_search(board)
            p2_nodes = p2_nodes + node_count
            print("\033[1;34;17mThe Computer\033[0m chose to move the stones in pit #" +
                  str(move.getPitIndex()) + ":")
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

    while rand == 1:
        if isOutOfMoves(board, Constants.P2_PITS):
            print(
                "\033[1;34;17mThe Computer\033[0m is out of moves, skip to the player:")
        else:
            print("\033[1;34;17mThe Computer\033[0m's turn.")
            if alg_choice == 1:
                move, node_count = player_2.minimax_decision(board)
            elif alg_choice == 2:
                move, node_count = player_2.alpha_beta_search(board)
            p2_nodes = p2_nodes + node_count
            print("\033[1;34;17mThe Computer\033[0m chose to move the stones in pit #" +
                  str(move.getPitIndex()) + ":")
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

        if isOutOfMoves(board, Constants.P1_PITS):
            print(
                "\033[1;31;17mThe player\033[0m is out of moves, skip to the Computer:")
        else:
            pit_choice = -1
            pit_valid = False
            while not pit_valid:
                print(
                    "\033[1;31;17mThe player\033[0m's turn. Please choose a pit.")
                pit_choice = int(input())
                if isValidPit(board, pit_choice, Constants.P1_PITS):
                    pit_valid = True
                else:
                    print("Invalid choice, please try again.")

            print("\033[1;31;17mThe player\033[0m chose to move the stones in pit #" +
                  str(pit_choice) + ":")

            move = State(None, 0, pit_choice,
                         board[pit_choice].getNumStones(), None)
            tempBoard = []
            for i in range(len(board)):
                tempBoard.append(board[i].getNumStones())
            newBoard = player_1.updateBoard(move, tempBoard)
            move.setBoard(newBoard)
            updateBoard(board, move)
            printBoard(board)

        if isOutOfMoves(board, Constants.P1_PITS) and isOutOfMoves(board, Constants.P2_PITS):
            break

    p1_score = board[Constants.P1_POCKETS[0]].getNumStones(
    ) + board[Constants.P1_POCKETS[1]].getNumStones()
    p2_score = board[Constants.P2_POCKETS[0]].getNumStones(
    ) + board[Constants.P2_POCKETS[1]].getNumStones()

    if p1_score > p2_score:
        print("\033[1;31;17mThe Player\033[0m Won!")
    elif p2_score > p1_score:
        print("\033[1;34;17mThe Computer\033[0m Won!")
    else:
        print("It's a tie!")

startGameCvC()
#startGamePvC()
