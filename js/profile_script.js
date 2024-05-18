// Sample data for demonstration purposes
const profileData = {
    username: "JohnDoe",
    profilePic: "john-doe-profile-pic.jpg",
    totalGames: 50,
    gamesWon: 30,
    winPercentage: 60
};

const leaderboardData = [
    { username: "Alice", wins: 25 },
    { username: "Bob", wins: 20 },
    { username: "Charlie", wins: 18 },
    // More leaderboard data...
];

// Function to populate profile information
function populateProfile() {
    document.getElementById("username").textContent = profileData.username;
    document.getElementById("profile-pic").src = profileData.profilePic;
    document.getElementById("total-games").textContent = profileData.totalGames;
    document.getElementById("games-won").textContent = profileData.gamesWon;
    document.getElementById("win-percentage").textContent = `${profileData.winPercentage}%`;
}

// Function to populate leaderboard
function populateLeaderboard() {
    const leaderboardList = document.getElementById("leaderboard-list");
    leaderboardData.forEach(entry => {
        const li = document.createElement("li");
        li.textContent = `${entry.username} - ${entry.wins} wins`;
        leaderboardList.appendChild(li);
    });
}

// Function to simulate editing profile (replace with actual functionality)
function editProfile() {
    alert("Edit Profile functionality is not implemented yet.");
}

// Populate profile and leaderboard on page load
window.onload = function() {
    populateProfile();
    populateLeaderboard();
};
