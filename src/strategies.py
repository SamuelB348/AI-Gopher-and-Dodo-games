from utils import *

State = Board
Strategy = Callable[[State, Player], Action]


def minmax(grid: State, depth: int, player: Player) -> float:
    if depth == 0 or grid.final(player):
        return grid.evaluate_v1(player)
    if player == R:
        best_value = float("-inf")
        for legal in grid.legals(player):
            grid.play(player, legal)
            v = minmax(grid, depth-1, B)
            grid.undo(player, legal)
            best_value = max(best_value, v)
        return best_value
    else:  # minimizing player
        best_value = float("inf")
        for legal in grid.legals(player):
            grid.play(player, legal)
            v = minmax(grid, depth-1, R)
            grid.undo(player, legal)
            best_value = min(best_value, v)
        return best_value


def minmax_actions(grid: State, player: Player, depth: int) -> tuple[float, list[Action]]:
    if depth == 0 or grid.final(player):
        return grid.evaluate_v1(player), []
    if player == R:
        best_value = float("-inf")
        best_legals: list[Action] = []
        for legal in grid.legals(player):
            grid.play(player, legal)
            v = minmax(grid, depth-1, B)
            grid.undo(player, legal)
            if v > best_value:
                best_value = v
                best_legals = [legal]
            elif v == best_value:
                best_legals.append(legal)
        return best_value, best_legals
    else:  # minimizing player
        best_value = float("inf")
        best_legals = []
        for legal in grid.legals(player):
            grid.play(player, legal)
            v = minmax(grid, depth-1, R)
            grid.undo(player, legal)
            if v < best_value:
                best_value = v
                best_legals = [legal]
            elif v == best_value:
                best_legals.append(legal)
        return best_value, best_legals


def strategy_minmax_random(grid: State, player: Player) -> Action:
    list_moves: list[Action] = minmax_actions(grid, player, 5)[1]
    return random.choice(list_moves)


def alphabeta(grid: State, depth: int, a: float, b: float, player: Player) -> float:
    if depth == 0 or grid.final(player):
        return grid.evaluate_v1(player)
    if player == R:
        best_value = float('-inf')
        for legal in grid.legals(player):
            grid.play(player, legal)
            best_value = max(best_value, alphabeta(grid, depth-1, a, b, B))
            grid.undo(player, legal)
            a = max(a, best_value)
            if a >= b:
                break  # β cut-off
        return best_value
    else:  # minimizing player
        best_value = float('inf')
        for legal in grid.legals(player):
            grid.play(player, legal)
            best_value = min(best_value, alphabeta(grid, depth-1, a, b, 2))
            grid.undo(player, legal)
            b = min(b, best_value)
            if a >= b:
                break  # α cut-off
        return best_value


def alphabeta_actions(grid: State, player: Player, depth: int) -> tuple[float, list[Action]]:
    if depth == 0 or grid.final(player):
        return grid.evaluate_v1(player), []
    if player == R:
        best_value = float('-inf')
        best_legals: list[Action] = []
        for legal in grid.legals(player):
            grid.play(player, legal)
            v = alphabeta(grid, depth-1, float('-inf'), float('inf'), B)
            grid.undo(player, legal)
            if v > best_value:
                best_value = v
                best_legals = [legal]
            elif v == best_value:
                best_legals.append(legal)
        return best_value, best_legals
    else:  # minimizing player
        best_value = float('inf')
        best_legals = []
        for legal in grid.legals(player):
            grid.play(player, legal)
            v = alphabeta(grid, depth-1, float('-inf'), float('inf'), R)
            grid.undo(player, legal)
            if v < best_value:
                best_value = v
                best_legals = [legal]
            elif v == best_value:
                best_legals.append(legal)
        return best_value, best_legals


def strategy_alphabeta_random(grid: State, player: Player) -> Action:
    actions = alphabeta_actions(grid, player, 3)
    list_moves: list[Action] = actions[1]
    # print(actions[0])
    return random.choice(list_moves)


def strategy_brain(board: Board, player: Player) -> Action:
    print("à vous de jouer: ", end="")
    start_q = int(input("start q :"))
    start_r = int(input("start r :"))
    end_q = int(input("end q :"))
    end_r = int(input("end r :"))
    depart = Hex(start_q, start_r)
    arrive = Hex(end_q, end_r)

    while (depart, arrive) not in board.legals(player):
        print("Coup illégal !")
        start_q = int(input("start q :"))
        start_r = int(input("start r :"))
        end_q = int(input("end q :"))
        end_r = int(input("end r :"))
        depart = Hex(start_q, start_r)
        arrive = Hex(end_q, end_r)

    return depart, arrive


def strategy_random(board: Board, player: Player) -> Action:
    return random.choice(board.legals(player))


def strategy_first_legal(board: Board, player: Player) -> Action:
    return board.legals(player)[0]


def dodo(strategy_rouge: Strategy, strategy_bleu: Strategy, size: int) -> Score:
    b = start_board(size)
    # b.pplot2()
    while True:
        s = strategy_rouge(b, 1)
        b.play(1, s)
        if b.final(2):
            return -1
        s = strategy_bleu(b, 2)
        b.play(2, s)
        if b.final(1):
            return 1
