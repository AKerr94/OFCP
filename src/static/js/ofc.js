// Perform initial setup
setupGame();

function setupGame() {
	console.log("OFCP Game " + game_id);

	var button = document.getElementById('playButton');
	var buttonClicks = 0;
	button.onclick = function() {
		buttonClicks++;
		alert("Game " + game_id + ": Button pressed " + buttonClicks + " times.")
	}
}
