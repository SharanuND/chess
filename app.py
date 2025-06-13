from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, async_mode='eventlet')

# Store active games
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_game')
def create_game(data):
    game_id = data.get('game_id')
    player_color = data.get('color')
    
    if game_id not in games:
        games[game_id] = {
            'board': initialize_board(),
            'players': {'white': None, 'black': None},
            'current_turn': 'white'
        }
    
    games[game_id]['players'][player_color] = request.sid
    join_room(game_id)
    
    emit('game_created', {
        'game_id': game_id,
        'color': player_color,
        'board': games[game_id]['board']
    })

@socketio.on('join_game')
def join_game(data):
    game_id = data.get('game_id')
    if game_id in games:
        # Assign the remaining color
        available_color = 'black' if games[game_id]['players']['white'] else 'white'
        games[game_id]['players'][available_color] = request.sid
        join_room(game_id)
        
        emit('game_joined', {
            'game_id': game_id,
            'color': available_color,
            'board': games[game_id]['board']
        }, room=game_id)

@socketio.on('make_move')
def make_move(data):
    game_id = data.get('game_id')
    from_pos = data.get('from_pos')
    to_pos = data.get('to_pos')
    player_color = data.get('color')
    
    if game_id in games and games[game_id]['current_turn'] == player_color:
        # Update the board
        piece = games[game_id]['board'][from_pos[1]][from_pos[0]]
        games[game_id]['board'][to_pos[1]][to_pos[0]] = piece
        games[game_id]['board'][from_pos[1]][from_pos[0]] = None
        
        # Switch turns
        games[game_id]['current_turn'] = 'black' if player_color == 'white' else 'white'
        
        # Broadcast the move to all players in the game
        emit('move_made', {
            'from_pos': from_pos,
            'to_pos': to_pos,
            'board': games[game_id]['board'],
            'current_turn': games[game_id]['current_turn']
        }, room=game_id)

def initialize_board():
    # Initialize an empty 8x8 board
    board = [[None for _ in range(8)] for _ in range(8)]
    
    # Set up pawns
    for x in range(8):
        board[1][x] = {'type': 'pawn', 'color': 'black'}
        board[6][x] = {'type': 'pawn', 'color': 'white'}
    
    # Set up other pieces
    piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for x, piece_type in enumerate(piece_order):
        board[0][x] = {'type': piece_type, 'color': 'black'}
        board[7][x] = {'type': piece_type, 'color': 'white'}
    
    return board

if __name__ == '__main__':
    socketio.run(app, debug=True) 