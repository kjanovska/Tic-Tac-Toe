import random
from copy import deepcopy


class Player:
    sign = ''

    def __init__(self, sign):
        self.sign = sign


class Human(Player):
    sign = ''

    def __init__(self, sign):
        super().__init__(self)
        self.sign = sign

    @staticmethod
    def move(self, board, sign):
        # tell player to input a number and return it if that position is empty
        try:
            position = int(input("Input a number from 0 to 24 where you want to play: "))
        except ValueError:
            position = int(input("Invalid number! Try again: "))
        while board[position] != ' ':
            try:
                position = int(input("Invalid number! Try again: "))
            except ValueError:
                position = int(input("Invalid number! Try again: "))

        return position


class AI(Player):
    sign = ''

    def __init__(self, sign):
        super().__init__(self)
        self.sign = sign

    @staticmethod
    def move(self, board, sign):
        print("AI on turn")
        position = AI.minimax(self, board, sign)
        print("move here: " + str(position))
        return position

    @staticmethod
    def first_move():
        position = random.randint(0, 24)
        return position

    def minimax(self, board, sign):
        layer = 0
        value = float("-inf")
        biggest_child = []
        child_no = 1
        for child in AI.successors(board, sign):
            max_val = AI.max_value(self, child, sign, layer, float("-inf"), float("inf"))
            print("child number " + str(AI.find_changed_position(board, child)) + ": " + str(max_val))
            if max_val > value:
                biggest_child = child
                value = max_val
            if AI.is_best_solution(self, board, child):
                return AI.find_changed_position(board, child)
            child_no += 1
        print("max value: " + str(value))
        return AI.find_changed_position(board, biggest_child)

    def max_value(self, state, sign, layer, alpha, beta):
        if AI.is_terminal(state) or layer >= 4:
            return AI.utility(state, sign, layer)
        value = float("-inf")
        for child in AI.successors(state, sign):
            if value != float("-inf"):
                value = max(value, AI.min_value(self, child, 'O', layer + 1, alpha, beta))
            else:
                value = max(value, AI.min_value(self, child, 'O', layer + 1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, state, sign, layer, alpha, beta):
        if AI.is_terminal(state) or layer >= 4:
            return AI.utility(state, sign, layer)
        value = float("inf")
        for child in AI.successors(state, sign):
            if value != float("inf"):
                value = min(value, AI.max_value(self, child, 'X', layer + 1, alpha, beta))
            else:
                value = min(value, AI.max_value(self, child, 'X', layer + 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def is_best_solution(self, board, possible_best):
        max_o_together = 0
        max_x_together = 0
        loss_cases = [['O', 'O', ' ', 'O'], ['O', ' ', 'O', 'O'], [' ', 'O', 'O', 'O'], ['O', 'O', 'O', ' ']]
        almost_loss_case = ['O', ' ', 'O']
        for square in {0, 1, 5, 6, 10, 11, 15, 16, 20, 21}:  # rows
            for case in loss_cases:
                if [board[square], board[square + 1], board[square + 2], board[square + 3]] == case:
                    if [possible_best[square], possible_best[square + 1], possible_best[square + 2], possible_best[square + 3]] != case:
                        return True  # == find a possible_best which eliminates loss case
                if [board[square], board[square + 1], board[square + 2]] == almost_loss_case:
                    if [possible_best[square], possible_best[square + 1], possible_best[square + 2]] != almost_loss_case:
                        return True
        for square in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}:  # columns
            for case in loss_cases:
                if [board[square], board[square + 5], board[square + 10], board[square + 15]] == case:
                    if [possible_best[square], possible_best[square + 5], possible_best[square + 10], possible_best[square + 15]] != case:
                        return True
                if [board[square], board[square + 5], board[square + 10]] == almost_loss_case:
                    if [possible_best[square], possible_best[square + 5], possible_best[square + 10]] != almost_loss_case:
                        return True
        for square in {0, 1, 5, 6}:  # left diagonal
            for case in loss_cases:
                if [board[square], board[square + 6], board[square + 12], board[square + 18]] == case:
                    if [possible_best[square], possible_best[square + 6], possible_best[square + 12], possible_best[square + 18]] != case:
                        return True
                if [board[square], board[square + 6], board[square + 12]] == almost_loss_case:
                    if [possible_best[square], possible_best[square + 6], possible_best[square + 12]] != almost_loss_case:
                        return True
        for square in {3, 4, 8, 9}:  # right diagonal
            for case in loss_cases:
                if [board[square], board[square + 4], board[square + 8], board[square + 12]] == case:
                    if [possible_best[square], possible_best[square + 4], possible_best[square + 8], possible_best[square + 12]] != case:
                        return True
                if [board[square], board[square + 4], board[square + 8]] == almost_loss_case:
                    if [possible_best[square], possible_best[square + 4], possible_best[square + 8]] != almost_loss_case:
                        return True
        return False

    @staticmethod
    def successors(state, sign):
        successor_array = []
        for i in range(25):
            if state[i] == ' ':
                new_child = deepcopy(state)
                new_child[i] = sign
                successor_array.append(new_child)
        return successor_array

    @staticmethod
    def change_sign(sign):
        if sign == 'X':
            return 'O'
        else:
            return 'X'

    @staticmethod
    def is_full(state):
        for i in range(25):
            if state[i] == ' ':
                return False
        return True

    @staticmethod
    def is_terminal(state):
        if check_winner(state) != "NO WINNER":
            return True
        return AI.is_full(state)

    @staticmethod
    def row_advantage(state):
        range1 = {0, 5, 10, 15, 20}
        line_type = "ROWS"
        return AI.check_sign_count(state, range1, line_type)


    @staticmethod
    def column_advantage(state):
        range1 = {0, 1, 2, 3, 4}
        line_type = "COLUMNS"
        return AI.check_sign_count(state, range1, line_type)

    @staticmethod
    def diagonal_advantage(state):
        x_o = []
        range1 = {0, 1, 5, 6}
        line_type = "LEFT_D"
        most_together_x = AI.check_sign_count(state, range1, line_type)[0]
        most_together_o = AI.check_sign_count(state, range1, line_type)[1]

        range1 = {3, 4, 8, 9}
        line_type = "RIGHT_D"
        most_together_x += AI.check_sign_count(state, range1, line_type)[0]
        most_together_o += AI.check_sign_count(state, range1, line_type)[1]

        x_o.append(most_together_x)
        x_o.append(most_together_o)
        return x_o

    @staticmethod
    def check_sign_count(state, range1, line_type):
        x_o = []
        most_together_x = 0
        most_together_o = 0
        for line in range1:
            x_together = 0
            o_together = 0
            if line_type == "COLUMNS":
                range2 = {line, line + 5, line + 10, line + 15, line + 20}
            elif line_type == "ROWS":
                range2 = range(line, line + 5)
            elif line_type == "LEFT_D":
                range2 = {line, line + 6, line + 12, line + 18}
            else:
                range2 = {line, line + 4, line + 8, line + 12}
            for line_pos in range2:
                if line_pos > line:
                    if state[line_pos] == 'O' and state[line_pos - 1] == 'O':
                        o_together += 1
                    elif state[line_pos] == 'X' and state[line_pos - 1] == 'X':
                        x_together += 1
                    else:
                        if x_together > 0:
                            most_together_x += pow(10, x_together - 1)  # 1 -> 10^(1-1) == 1
                        if o_together > 0:
                            most_together_o += pow(10, o_together - 1)
                        o_together = 0
                        x_together = 0
                else:
                    if line_pos == 'X':
                        x_together += 1
                    elif line_pos == 'O':
                        o_together += 1

                if x_together > 0:
                    most_together_x += pow(10, x_together - 1)  # 1 -> 10^(1-1) == 1
                if o_together > 0:
                    most_together_o += pow(10, o_together - 1)

                o_together = 0
                x_together = 0

        x_o.append(most_together_x)
        x_o.append(most_together_o)
        return x_o


    @staticmethod
    def player_advantage(state, layer):  # heuristic evaluation function

        score = AI.row_advantage(state)[0]
        score -= AI.row_advantage(state)[1]  # because both are positive, but i need to substract o score
        score += AI.column_advantage(state)[0]
        score -= AI.column_advantage(state)[1]
        score += AI.diagonal_advantage(state)[0]
        score -= AI.diagonal_advantage(state)[1]

        if score > 100:
            return score - layer*100
        elif score > 10:
            return score - layer*10
        elif score < -10:
            return score + layer
        elif score < -100:
            return score + layer*10
        else:
            return score

    @staticmethod
    def utility(state, sign, layer):
        points = 0
        if check_winner(state) == "DRAW":
            return 0
        if not AI.is_terminal(state):
            return AI.player_advantage(state, layer)
        elif check_winner(state) == 'X':
            points += 1000 - layer*100
            return points
        elif check_winner(state) == 'O':
            points += -1000 + layer*100
            return points
        else:
            return 0

    @staticmethod
    def find_changed_position(board, child):
        for pos in range(len(board)):
            if board[pos] != child[pos]:
                return pos


def check_winner(state):
    for row in {0, 1, 5, 6, 10, 11, 15, 16, 20, 21}:
        if state[row] != ' ':
            same_signs_in_row = True
            for row_pos in range(row, row + 4):
                if state[row_pos] != state[row]:
                    same_signs_in_row = False
            if same_signs_in_row:
                return state[row]

    for column in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}:
        if state[column] != ' ':
            same_signs_in_column = True
            for column_pos in {column, column + 5, column + 10, column + 15}:
                if state[column_pos] != state[column]:
                    same_signs_in_column = False
            if same_signs_in_column:
                return state[column]

    for left_diagonal in {0, 1, 5, 6}:
        if state[left_diagonal] != ' ':
            same_signs_in_diagonal = True
            for diag_pos in {left_diagonal, left_diagonal + 6, left_diagonal + 12, left_diagonal + 18}:
                if state[diag_pos] != state[left_diagonal]:
                    same_signs_in_diagonal = False
            if same_signs_in_diagonal:
                return state[left_diagonal]

    for right_diagonal in {3, 4, 8, 9}:
        if state[right_diagonal] != ' ':
            same_signs_in_diagonal = True
            for diag_pos in {right_diagonal, right_diagonal + 4, right_diagonal + 8, right_diagonal + 12}:
                if state[diag_pos] != state[right_diagonal]:
                    same_signs_in_diagonal = False
            if same_signs_in_diagonal:
                return state[right_diagonal]

    if AI.is_full(state):
        return "DRAW"
    else:
        return "NO WINNER"


class Game:
    board = []
    winner = None

    def __init__(self):
        self.board = self.create_empty_board()
        self.winner = None

    @staticmethod
    def create_empty_board():
        return [' ' for position in range(25)]

    def print_board(self):
        square_number = 0
        print('\n|-------------|')
        for square in self.board:
            print('|' + square, end="|")
            if square_number in {4, 9, 14, 19, 24}:
                print('\n|-------------|')
            square_number += 1

if __name__ == '__main__':
    game = Game()
    game.create_empty_board()
    game.print_board()
    ai_player = AI('X')
    human_player = Human('O')

    position_to_move = ai_player.first_move()
    game.board[position_to_move] = 'X'
    player_on_turn = human_player

    while game.winner is None:
        game.print_board()
        position_to_move = player_on_turn.move(player_on_turn, game.board, player_on_turn.sign)
        print(int(position_to_move))
        game.board[position_to_move] = player_on_turn.sign

        if player_on_turn == human_player:
            player_on_turn = ai_player
        else:
            player_on_turn = human_player

        if check_winner(game.board) == 'X' or check_winner(game.board) == 'O':
            print("WINNER")
            game.winner = check_winner(game.board)
            game.print_board()
        elif check_winner(game.board) == 'DRAW':
            print("DRAW")
            game.winner = check_winner(game.board)
            game.print_board()
