let playerText = document.getElementById('playerText');
let boxes = Array.from(document.getElementsByClassName('box'));
let winnerIndicator = getComputedStyle(document.body).getPropertyValue('--winning-color');

// Get the current user ID from the hidden div
const userData = document.getElementById('user-data');
const currentUser = userData.getAttribute('data-user-id');

const O_TEXT = "O";
const X_TEXT = "X";
let currentPlayer = X_TEXT;
let spaces = Array(9).fill(null);

const startGame = () => {
    boxes.forEach(box => box.addEventListener('click', boxClicked));
}

function boxClicked(e) {
    const id = e.target.id;

    if (!spaces[id] && !playerHasWon()) {
        spaces[id] = currentPlayer;
        e.target.innerText = currentPlayer;

        submitMove(id, currentPlayer);

        if (playerHasWon()) {
            playerText.innerHTML = `${currentPlayer} has won!`;
            let winningBlocks = playerHasWon();
            winningBlocks.map(box => boxes[box].style.backgroundColor = winnerIndicator);

            // Send game result to backend
            sendResult(currentPlayer === X_TEXT ? 'win' : 'loss');
        } else if (spaces.every(space => space !== null)) {
            playerText.innerHTML = "It's a draw!";
            sendResult('draw');
        } else {
            currentPlayer = currentPlayer === X_TEXT ? O_TEXT : X_TEXT;
            playerText.innerHTML = `${currentPlayer}'s Turn`;
        }
    }
}

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

function playerHasWon() {
    for (const condition of winningCombos) {
        let [a, b, c] = condition;
        if (spaces[a] && spaces[a] === spaces[b] && spaces[a] === spaces[c]) {
            return [a, b, c];
        }
    }
    return false;
}

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

startGame();
