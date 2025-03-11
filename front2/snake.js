const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const tileCount = 10;
const tileSize = canvas.width / tileCount;

let snake = [{ x: 2, y: 2 }];
let food = { x: 8, y: 8 };
let direction = { x: 0, y: 0 };
let score = 0;
let snake_speed = 2;

let isPaused = false; // Variable pour gérer l'état de pause

// Variables pour contrôler la fréquence de la boucle de jeu
let lastUpdate = 0;  // Temps de la dernière mise à jour
const targetFPS = 5;  // Nombre de FPS souhaité
const frameDelay = 1000 / targetFPS;  // Délai entre chaque frame en millisecondes

function gameLoop(timestamp) {
    if (!isPaused) {
        // Vérifier si le délai entre les frames est écoulé
        if (timestamp - lastUpdate >= frameDelay) {
            lastUpdate = timestamp;  // Mettre à jour le temps de la dernière frame
            update();
            sendGameState();
        }
    }
    draw();
    requestAnimationFrame(gameLoop);  // Continuer la boucle
}

function update() {
    const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

    // Vérifier les collisions avec les bords
    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
        resetGame();
        return;
    }

    // Vérifier les collisions avec le serpent lui-même
    for (let i = 1; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            resetGame();
            return;
        }
    }

    // Ajouter la nouvelle tête
    snake.unshift(head);

    // Vérifier si le serpent mange la nourriture
    if (head.x === food.x && head.y === food.y) {
        score++;
        //snake_speed += 1;
        placeFood();
    } else {
        // Retirer la queue si le serpent ne mange pas
        snake.pop();
    }
}

function draw() {
    // Effacer le canvas
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Afficher le score
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";    
    ctx.textAlign = "start"; // Réinitialiser l'alignement du texte
    ctx.fillText("Score: " + score, 10, 30);

     // Afficher la vitesse
     const speedText = "Snake Speed: " + Number(snake_speed * 0.131 * 3.6).toFixed(1) + " km/h";
     const textWidth = ctx.measureText(speedText).width; // Mesurer la largeur du texte
     const paddingRight = 10; // Espace entre le texte et le bord droit
     const speedTextX = canvas.width - textWidth - paddingRight; // Calculer la position X
     ctx.fillText(speedText, speedTextX, 30); // Afficher le texte à la position calculée

    // Afficher un message de pause si le jeu est en pause
    if (isPaused) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.5)"; // Fond semi-transparent
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "white";
        ctx.font = "40px Arial";
        ctx.textAlign = "center";
        ctx.fillText("PAUSED", canvas.width / 2, canvas.height / 2);
        ctx.textAlign = "start"; // Réinitialiser l'alignement du texte
    }

    // Dessiner le serpent
    ctx.fillStyle = "green";
    for (let segment of snake) {
        ctx.fillRect(segment.x * tileSize, segment.y * tileSize, tileSize, tileSize);
    }

    // Dessiner la nourriture
    ctx.fillStyle = "red";
    ctx.fillRect(food.x * tileSize, food.y * tileSize, tileSize, tileSize);

}

function placeFood() {
    food.x = Math.floor(Math.random() * tileCount);
    food.y = Math.floor(Math.random() * tileCount);
    // Vérifier que la nourriture ne se trouve pas sur le serpent
    for (let segment of snake) {
        if (food.x === segment.x && food.y === segment.y) {
            placeFood();
            return;
        }
    }

}

function resetGame() {
    snake = [{ x: 5, y: 5 }];
    direction = { x: 0, y: 0 };
    score = 0;
    snake_speed = 1;
    placeFood();
    console.log("Reset");
}

window.addEventListener("keydown", (e) => {
    if (e.key === "p" || e.key === "P") { // Si la touche "P" est pressée
        isPaused = !isPaused; // Basculer entre pause et reprise
        console.log(isPaused ? "Game paused" : "Game resumed");
    }
    switch (e.key) {
        case "ArrowUp":
            if (direction.y === 0) direction = { x: 0, y: -1 };
            break;
        case "ArrowDown":
            if (direction.y === 0) direction = { x: 0, y: 1 };
            break;
        case "ArrowLeft":
            if (direction.x === 0) direction = { x: -1, y: 0 };
            break;
        case "ArrowRight":
            if (direction.x === 0) direction = { x: 1, y: 0 };
            break;
    }
});

// Se connecter au serveur WebSocket
let socket = new WebSocket("ws://localhost:8000");

socket.onopen = () => {
    console.log("Connected to WebSocket server");
    gameLoop();
};

socket.onmessage = (event) => {
    const action = JSON.parse(event.data);
    console.log("Received action:", action);

    // Met à jour la direction du serpent en fonction de l'action reçue
    switch (action.direction) {
        case "UP":
            if (direction.y === 0) direction = { x: 0, y: -1 };
            break;
        case "DOWN":
            if (direction.y === 0) direction = { x: 0, y: 1 };
            break;
        case "LEFT":
            if (direction.x === 0) direction = { x: -1, y: 0 };
            break;
        case "RIGHT":
            if (direction.x === 0) direction = { x: 1, y: 0 };
            break;
    }
    waitingForAction = false; // Prêt à envoyer le prochain état
};

socket.onerror = (error) => {
    console.error("WebSocket error:", error);
};

socket.onclose = () => {
    console.log("WebSocket connection closed. Reconnecting...");
    // Réessayer de se connecter après un délai
    setTimeout(() => {
        socket = new WebSocket("ws://localhost:8000");
    }, 1000); // Réessayer après 1 seconde
};

// Fonction pour envoyer l'état du jeu au serveur
let waitingForAction = false;
function sendGameState() {
    if (socket.readyState === WebSocket.OPEN && !waitingForAction) { // Vérifie que la connexion est ouverte
        waitingForAction = true;
        const gameState = {
            snake: snake, 
            food: food,
            direction: direction,
            score: score
        };
        console.log("Sending game state:", gameState);
        socket.send(JSON.stringify(gameState));
    } else {
        console.warn("WebSocket is not open. Ready state:", socket.readyState);
    }
}

async function register(username, password) {
    const res = await fetch("http://localhost:3000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    alert(data.message);
}

async function login(username, password) {
    const res = await fetch("http://localhost:3000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (data.token) {
        localStorage.setItem("token", data.token);
        alert("Connexion réussie !");
    } else {
        alert("Erreur de connexion");
    }
}

placeFood();
gameLoop();


//cd Desktop
//cd "Snake V2"
//python3 -m venv venv    
//source venv/bin/activate