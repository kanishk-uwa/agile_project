// Get the player text element
let playerText = document.getElementById('playerText');

// Get all the boxes and convert them to an array
let boxes = Array.from(document.getElementsByClassName('box'));

// Get the winning color from CSS
let winnerIndicator = getComputedStyle(document.body).getPropertyValue('--winning-color');

// Get the current user ID from the hidden div
const userData = document.getElementById('user-data');
const currentUser = userData.getAttribute('data-user-id');

// Define text for players
const O_TEXT = "O";
const X_TEXT = "X";

// Set the current player to X
let currentPlayer = X_TEXT;

// Initialize the game board spaces
let spaces = Array(9).fill(null);

// Start the game by adding event listeners to each box
const startGame = () => {
    boxes.forEach(box => box.addEventListener('click', boxClicked));
}

// Handle box click events
function boxClicked(e) {
    const id = e.target.id;

    // Check if the space is empty and no player has won yet
    if (!spaces[id] && !playerHasWon()) {
        // Mark the space with the current player's symbol
        spaces[id] = currentPlayer;
        e.target.innerText = currentPlayer;

        // Submit the move to the backend
        submitMove(id, currentPlayer);

        // Check if the current player has won
        if (playerHasWon()) {
            playerText.innerHTML = `${currentPlayer} has won!`;
            let winningBlocks = playerHasWon();
            winningBlocks.map(box => boxes[box].style.backgroundColor = winnerIndicator);

            // Send game result to backend
            sendResult(currentPlayer === X_TEXT ? 'win' : 'loss');
        } else if (spaces.every(space => space !== null)) {
            // Check if it's a draw
            playerText.innerHTML = "It's a draw!";
            sendResult('draw');
        } else {
            // Switch to the other player
            currentPlayer = currentPlayer === X_TEXT ? O_TEXT : X_TEXT;
            playerText.innerHTML = `${currentPlayer}'s Turn`;
        }
    }
}

// Define the winning combinations
const winningCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
];

// Check if a player has won
function playerHasWon() {
    for (const condition of winningCombos) {
        let [a, b, c] = condition;
        if (spaces[a] && spaces[a] === spaces[b] && spaces[a] === spaces[c]) {
            return [a, b, c];
        }
    }
    return false;
}

// Submit the move to the backend
function submitMove(id, currentPlayer) {
    fetch('/submit_move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: window.gameId,  // Ensure you pass the correct game ID
            move_number: id,
            position: currentPlayer
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message);
        } else {
            console.error(data.error);
        }
    });
}

// Send the game result to the backend
function sendResult(result) {
    fetch('/update_results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            result: result,
            user_id: currentUser
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message);
            window.location.href = data.redirect;
        } else {
            console.error(data.error);
        }
    });
}

// Start the game when the script is loaded
startGame();
