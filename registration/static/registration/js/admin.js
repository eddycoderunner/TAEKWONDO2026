const playerList = document.getElementById("playerList");


function loadPlayers() {
    const players = JSON.parse(localStorage.getItem("players")) || [];
    displayPlayers(players);
}
function displayPlayers(players) {
    playerList.innerHTML = "";

    if (players.length === 0) {
        playerList.innerHTML = "<p style='color:white'>No players registered</p>";
        return;
    }

    players.forEach((player, index) => {
        const div = document.createElement("div");
        div.classList.add("card");
        div.innerHTML = `
            <div class="card-header">
                <h3>${player.name}</h3>
                <span class="badge">${player.gender}</span>
            </div>
            <div class="card-body">
                <p>Age: ${player.age}</p>
                <p>Club: ${player.club}</p>
                <p>Weight: ${player.weight}</p>
                <p>Nationality: ${player.nationality}</p>
        </div>
        <div class="card-footer">
            <button onclick="deletePlayer(${index})" class="delete-btn">Delete</button>
        </div>
        `;
        playerList.appendChild(div);
    });
}
function deletePlayer(index) {
    let players = JSON.parse(localStorage.getItem("players")) || [];
    players.splice(index, 1);
    localStorage.setItem("players", JSON.stringify(players));
    loadPlayers();
}
searchInput.addEventListener("input", function () {
    const value = this.value.toLowerCase();
    const players = JSON.parse(localStorage.getItem("players")) || [];

    const filtered = players.filter(player =>
        player.name.toLowerCase().includes(value) ||
        player.club.toLowerCase().includes(value)
    );
    displayPlayers(filtered);
});
loadPlayers();
