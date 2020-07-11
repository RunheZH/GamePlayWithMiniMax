from random import randint
from lib import Constants

class Player:
    def __init__(self, player):
        self.player = player
        self.pits = []
        self.pockets = []
        self.oppo_pits = []
        self.oppo_pockets = []

    # Beginning of Mini-Max
    def minimax_decision(self, board):
        max_value = -1
        temp_board = []
        node_count = 0

        for i in board:
            temp_board.append(i.getNumStones())
        
        next_pit = None

        for pit_index in self.pits:
            if temp_board[pit_index] == 0:
                continue
            temp_state = self.get_state(pit_index, temp_board)
            op_value, nd_count = self.mm_find_mini_value(temp_state, temp_board)
            node_count = node_count + nd_count
            if op_value > max_value:
                max_value = op_value
                next_pit = temp_state
            elif op_value == max_value:
                rand = randint(0, 1)
                if rand == 0:
                    next_pit = temp_state

        # make next available move
        if next_pit is None:
            for i in self.pits:
                if not temp_board[i] == 0:
                    next_pit = self.get_state(i, temp_board)
                    new_board = self.updateBoard(next_pit, temp_board)
                    next_pit.setBoard(new_board)
                    next_pit.setNumStones(0)
                    break
        return next_pit, node_count

    def mm_find_max_value(self, state, board):
        node_count = 1
        if state.getDepth() >= Constants.MAX_DEPTH:
            return state.getDiff(), node_count

        value = - Constants.MAX_STONES * Constants.NUM_PITS
        # self
        temp_board = self.updateBoard(state, board)
        state.setBoard(temp_board)
        state.setNumStones(0)
        for p_ind in self.pits:
            if temp_board[p_ind] == 0:
                continue
            temp_val, nd_count = self.mm_find_mini_value(self.get_state(p_ind, temp_board, state), temp_board)
            value = max(value, temp_val)
            node_count = node_count + nd_count

        if value == - Constants.MAX_STONES * Constants.NUM_PITS:
            value = state.getDiff()
        return value, node_count

    def mm_find_mini_value(self, state, board):
        node_count = 1
        if state.getDepth() >= Constants.MAX_DEPTH:
            return state.getDiff(), node_count

        value = Constants.MAX_STONES * Constants.NUM_PITS
        # oppo
        temp_board = self.updateBoard(state, board)
        state.setBoard(temp_board)
        state.setNumStones(0)
        for p_ind in self.oppo_pits:
            if temp_board[p_ind] == 0:
                continue
            temp_val, nd_count = self.mm_find_max_value(self.get_state(p_ind, temp_board, state), temp_board)
            value = min(value, temp_val)
            node_count = node_count + nd_count

        if value == Constants.MAX_STONES * Constants.NUM_PITS:
            value = state.getDiff()
        return value, node_count

    def get_state(self, pit_index, board, parent=None):
        self_points = 0
        oppo_points = 0
        for i in self.pockets:
            self_points = self_points + board[i]
        for i in self.oppo_pockets:
            oppo_points = oppo_points + board[i]

        if parent:
            depth = parent.getDepth() + 1
        else:
            depth = 0
        return State(parent, depth, pit_index, board[pit_index], board, self_points, oppo_points)

    def updateBoard(self, state, board):
        newBoard = []
        # copy over
        for i in range(len(board)):
            newBoard.append(board[i])
        num_stones = state.getNumStones()
        newBoard[state.getPitIndex()] = 0
        for i in range(num_stones):
            # TODO: jump opponent's pockets
            pit_index = (state.getPitIndex() + i + 1) % Constants.NUM_PITS
            # put a stone in a pit
            newBoard[pit_index] = newBoard[pit_index] + 1

        return newBoard
    
    # End of Mini-Max

    # Beginning of Alpha-Beta
    def alpha_beta_search(self, board):
        max_value = -1
        temp_board = []
        node_count = 0

        for i in board:
            temp_board.append(i.getNumStones())

        next_pit = None

        for pit_index in self.pits:
            if temp_board[pit_index] == 0:
                continue
            temp_state = self.get_state(pit_index, temp_board)
            op_value, nd_count = self.ab_find_mini_value(
                temp_state, temp_board, - Constants.MAX_STONES * Constants.NUM_PITS, Constants.MAX_STONES * Constants.NUM_PITS)
            node_count = node_count + nd_count
            if op_value > max_value:
                max_value = op_value
                next_pit = temp_state
            elif op_value == max_value:
                rand = randint(0, 1)
                if rand == 0:
                    next_pit = temp_state

        # make next available move
        if next_pit is None:
            for i in self.pits:
                if not temp_board[i] == 0:
                    next_pit = self.get_state(i, temp_board)
                    new_board = self.updateBoard(next_pit, temp_board)
                    next_pit.setBoard(new_board)
                    next_pit.setNumStones(0)
                    break
        return next_pit, node_count

    def ab_find_max_value(self, state, board, a, b):
        node_count = 1
        if state.getDepth() >= Constants.MAX_DEPTH:
            return Constants.NUM_STONES * Constants.NUM_PITS / 2 - state.getSelfPoints(), node_count

        value = - Constants.MAX_STONES * Constants.NUM_PITS
        # self
        temp_board = self.updateBoard(state, board)
        state.setBoard(temp_board)
        state.setNumStones(0)
        for p_ind in self.pits:
            if temp_board[p_ind] == 0:
                continue
            temp_val, nd_count = self.ab_find_mini_value(self.get_state(p_ind, temp_board, state), temp_board, a, b)
            value = max(value, temp_val)
            node_count = node_count + nd_count
            if value >= b:
                return value, node_count
            a = max(a, value)

        if value == - Constants.MAX_STONES * Constants.NUM_PITS:
            value = Constants.NUM_STONES * Constants.NUM_PITS / 2 - state.getSelfPoints()
        return value, node_count

    def ab_find_mini_value(self, state, board, a, b):
        node_count = 1
        if state.getDepth() >= Constants.MAX_DEPTH:
            return Constants.NUM_STONES * Constants.NUM_PITS / 2 - state.getSelfPoints(), node_count

        value = Constants.MAX_STONES * Constants.NUM_PITS
        # oppo
        temp_board = self.updateBoard(state, board)
        state.setBoard(temp_board)
        state.setNumStones(0)
        for p_ind in self.oppo_pits:
            if temp_board[p_ind] == 0:
                continue
            temp_val, nd_count = self.ab_find_max_value(self.get_state(p_ind, temp_board, state), temp_board, a, b)
            value = min(value, temp_val)
            node_count = node_count + nd_count
            if value <= a:
                return value, node_count
            b = min(b, value)

        if value == Constants.MAX_STONES * Constants.NUM_PITS:
            value = Constants.NUM_STONES * Constants.NUM_PITS / 2 - state.getSelfPoints()
        return value, node_count
    
    # End of Alpha-Beta

    def setPits(self, pit_list):
        self.pits = pit_list
    
    def setPockets(self, pocket_list):
        self.pockets = pocket_list

    def setOppoPits(self, oppo_pit_list):
        self.oppo_pits = oppo_pit_list

    def setOppoPockets(self, oppo_pocket_list):
        self.oppo_pockets = oppo_pocket_list
    
    def getPits(self):
        return self.pits
    
    def getPockets(self):
        return self.pockets
    
    def getOppoPockets(self):
        return self.oppo_pockets

class State:
    def __init__(self, parent, depth, pit_index, num_stones, board, self_points=-1, oppo_points=-1):
        self.parent = parent
        self.depth = depth
        self.pit_index = pit_index
        self.num_stones = num_stones
        self.board = board
        self.self_points = self_points
        self.oppo_points = oppo_points

    def getDepth(self):
        return self.depth
    
    def getDiff(self):
        return self.self_points - self.oppo_points

    def getNumStones(self):
        return self.num_stones

    def getPitIndex(self):
        return self.pit_index
    
    def getBoard(self):
        return self.board
    
    def getSelfPoints(self):
        return self.self_points
    
    def setNumStones(self, newNum):
        self.num_stones = newNum

    def setSelfPoints(self, newPoints):
        self.self_points = newPoints

    def setOppoPoints(self, newPoints):
        self.oppo_points = newPoints
    
    def setBoard(self, newBoard):
        self.board = newBoard
