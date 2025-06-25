from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

board = [" "] * 9
current_player = "X"

def check_winner(b):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for line in wins:
        if b[line[0]] == b[line[1]] == b[line[2]] != " ":
            return b[line[0]]
    return None

def is_draw(b):
    return " " not in b and check_winner(b) is None

def minimax(b, is_maximizing):
    winner = check_winner(b)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_draw(b):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                val = minimax(b, False)
                b[i] = " "
                best = max(best, val)
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                val = minimax(b, True)
                b[i] = " "
                best = min(best, val)
        return best

def ai_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board
    data = request.get_json()
    index = data["index"]

    if board[index] == " " and not check_winner(board) and not is_draw(board):
        board[index] = "X"
        winner = check_winner(board)
        draw = is_draw(board)

        if not winner and not draw:
            ai_move()
            winner = check_winner(board)
            draw = is_draw(board)

        return jsonify(board=board, winner=winner, draw=draw, current_player="X")
    return jsonify(error="Invalid move"), 400

@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = [" "] * 9
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
