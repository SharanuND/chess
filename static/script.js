const socket = io();
let gameId = null;
let playerColor = null;
let selectedPiece = null;
let validMoves = [];

// Chess piece Unicode characters
const PIECES = {
    'white': {
        'king': '♔',
        'queen': '♕',
        'rook': '♖',
        'bishop': '♗',
        'knight': '♘',
        'pawn': '♙'
    },
    'black': {
        'king': '♚',
        'queen': '♛',
        'rook': '♜',
        'bishop': '♝',
        'knight': '♞',
        'pawn': '♟'
    }
};

function createGame() {
    gameId = Math.random().toString(36).substring(2, 8);
    playerColor = 'white';
    socket.emit('create_game', { game_id: gameId, color: playerColor });
}

function joinGame() {
    gameId = document.getElementById('game-id').value;
    if (gameId) {
        socket.emit('join_game', { game_id: gameId });
    }
}

function initializeBoard() {
    const board = document.querySelector('.chess-board');
    board.innerHTML = '';
    
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.className = `square ${(row + col) % 2 === 0 ? 'white' : 'black'}`;
            square.dataset.row = row;
            square.dataset.col = col;
            square.addEventListener('click', handleSquareClick);
            board.appendChild(square);
        }
    }
}

function updateBoard(board) {
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        const row = parseInt(square.dataset.row);
        const col = parseInt(square.dataset.col);
        const piece = board[row][col];
        
        if (piece) {
            square.innerHTML = `<div class="piece">${PIECES[piece.color][piece.type]}</div>`;
        } else {
            square.innerHTML = '';
        }
    });
}

function handleSquareClick(event) {
    const square = event.target.closest('.square');
    if (!square) return;
    
    const row = parseInt(square.dataset.row);
    const col = parseInt(square.dataset.col);
    
    if (selectedPiece) {
        // Try to move the selected piece
        if (isValidMove(row, col)) {
            socket.emit('make_move', {
                game_id: gameId,
                from_pos: [selectedPiece.col, selectedPiece.row],
                to_pos: [col, row],
                color: playerColor
            });
        }
        clearSelection();
    } else {
        // Select a piece
        const piece = document.querySelector(`.square[data-row="${row}"][data-col="${col}"] .piece`);
        if (piece) {
            selectedPiece = { row, col };
            square.classList.add('selected');
            // TODO: Show valid moves
        }
    }
}

function isValidMove(row, col) {
    // TODO: Implement move validation
    return true;
}

function clearSelection() {
    selectedPiece = null;
    document.querySelectorAll('.square').forEach(square => {
        square.classList.remove('selected', 'valid-move');
    });
}

// Socket event handlers
socket.on('game_created', (data) => {
    gameId = data.game_id;
    playerColor = data.color;
    document.getElementById('game-setup').style.display = 'none';
    document.getElementById('game-board').style.display = 'block';
    document.getElementById('current-game-id').textContent = gameId;
    document.getElementById('player-color').textContent = playerColor;
    initializeBoard();
    updateBoard(data.board);
});

socket.on('game_joined', (data) => {
    gameId = data.game_id;
    playerColor = data.color;
    document.getElementById('game-setup').style.display = 'none';
    document.getElementById('game-board').style.display = 'block';
    document.getElementById('current-game-id').textContent = gameId;
    document.getElementById('player-color').textContent = playerColor;
    initializeBoard();
    updateBoard(data.board);
});

socket.on('move_made', (data) => {
    updateBoard(data.board);
    document.getElementById('current-turn').textContent = data.current_turn.charAt(0).toUpperCase() + data.current_turn.slice(1);
}); 