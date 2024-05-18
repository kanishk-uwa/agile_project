CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ranking INTEGER NOT NULL,
    matches_won INTEGER NOT NULL,
    image_url TEXT NOT NULL
);

-- Insert some sample data
INSERT INTO players (name, ranking, matches_won, image_url) VALUES
('Player 1', 1, 100, 'https://via.placeholder.com/50'),
('Player 2', 2, 90, 'https://via.placeholder.com/50'),
('Player 3', 3, 85, 'https://via.placeholder.com/50'),
('Player 4', 4, 80, 'https://via.placeholder.com/50'),
('Player 5', 5, 75, 'https://via.placeholder.com/50');