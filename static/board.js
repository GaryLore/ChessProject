
const board = document.getElementsByClassName("board")[0];
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];//column
let selected = 0;
let fromMove = "";
let toMove = "";
let promotionPiece = "";
let ai_start="";
let ai_end="";
let pawnSelected = false;
let whiteTurn = true;
const moveSound = new Audio("../static/chess_sound.mp3");
const overlay = document.querySelector('#overlay');

for(let row = 8; row != 0; --row){
    for(let col = 0; col != 8; ++col){

        let square = document.createElement("div");
        square.classList.add('square');
        square.classList.add( (row+col)%2 === 0 ? "white" : "black");
        square.dataset.col = files[col];
        square.dataset.row = row;
        board.appendChild(square);

    }
}

document.querySelectorAll(".popup .pieces button").forEach(pieceButton => {
  pieceButton.addEventListener('click', () => {
    pieceSymbol = pieceButton.querySelector('img');
    console.log(pieceSymbol.alt)
    promotionPiece = pieceSymbol.alt;
    closePopUp();
  });
});

document.querySelectorAll('.square').forEach(square => {
  square.addEventListener('click', () => {
    console.log("before Click: " + selected);
    if(selected == 0){//no squares are selected so we assign first selected
      square.classList.toggle('selected');
      square.classList.toggle('first');
      fromMove = square.dataset.col + square.dataset.row;
      ++selected;
    }
    else if(promotionPiece !== ""){
      removeSelect();
    }
    else if(square.classList.contains("first")){
      square.classList.toggle('selected');
      square.classList.toggle('first');
      fromMove = "";
      --selected;
    }
    else if(square.classList.contains("second")){
      square.classList.toggle('selected');
      square.classList.toggle('second');
      toMove = "";
      --selected;
    }
    else if(fromMove === "" && toMove !== ""){ //means current square not selected, and second square has been selected
      square.classList.toggle('selected');
      square.classList.toggle('second');
      fromMove = square.dataset.col + square.dataset.row;
      ++selected;
    }
    else if(fromMove !== "" && toMove === ""){ //means current square not selected, and first square has been selected
      square.classList.toggle('selected');
      square.classList.toggle('second');
      toMove = square.dataset.col + square.dataset.row;
      ++selected;
      //check piece of first square make sure its pawn, and check if second square is in last rank
      if(toMove[1] === "8" && checkPawnSelected()){
        openPopUp();
      }
    }
    else if(fromMove !== "" && toMove !== ""){
      removeSelect();
      square.classList.toggle('selected');
      square.classList.toggle('first');
      fromMove = square.dataset.col + square.dataset.row;
      ++selected;
    }
    console.log("After Click: " + selected);
  });
});

document.querySelector('.close').addEventListener('click', () => {
  closePopUp(true);  
});

window.onload = sendState;

async function sendState() {
  let response = await fetch("/update_state");

  if (!response.ok) {
      console.error("Server returned error:", response.status);
      return;
  }

  //contains only squares which has pieces 
  let data = await response.json();

  //resets the board everytime
  let squareDivs = document.querySelectorAll('.square')
  for(let div of squareDivs){
    div.innerHTML = "";
  }

  let board_info = data["board"];
  //fills in the squares that are actually not full, goes throu
  for(let key in board_info){
    let col = key[0];
    let row = key[1];
    let piece = board_info[key];
    console.log('[data-col="'+col+'"][data-row="'+row+'"]');
    let div = document.querySelector('[data-col="'+col+'"][data-row="'+row+'"]');

    if (isUpper(piece)){
      piece = piece.toLowerCase();

      if(piece === "k" && data['check'] && whiteTurn)
        div.classList.toggle("CHECK");

      div.innerHTML = `<img src="../static/img/_${piece}.svg" alt="${piece.toUpperCase()}">`;
    }
    else{

      if(piece === "k" && data['check'] && !whiteTurn)
        div.classList.toggle("CHECK");

      div.innerHTML = `<img src="../static/img/${piece}.svg" alt="${piece}">`;
    }
  }
  let title = document.querySelector("h1 a");

  console.log()
  if(data['end']) {

    console.log(data["winner"])
    switch (data['winner']) {
      case "WHITE":
        title.innerText = "White Wins";
        break;
      case "BLACK":
        title.innerText = "Black Wins";
        break;
      default:
        title.innerText = "Draw";
        break; 
  }
  }

  console.log(data);
}

async function submitMove(params) {
  if(selected == 2){
    console.log("SubmitMove Function entered");
    let response = await fetch("/submit_move", {
    method: "POST",
    headers: { "Content-Type": "application/json" }, // Necessary here
    body: JSON.stringify({ move: `${fromMove}${toMove}${promotionPiece}` }),
    });//uses await because we need to ensure its completly done before we update our current state

    let boardResponse = await response.json();
    //checks if network request was ok and checks if it was legal move or not
    console.log(fromMove);
    console.log(toMove);
    console.log(response.ok);
    console.log(boardResponse['success']);
    //await sleep(2000);
  
    removeSelect();

    if(response.ok && boardResponse['success']){
      console.log("SEND STATE IS ENTERED");
      //await sleep(2000);
      whiteTurn = !whiteTurn;//alternates turns
      removeCheck(false);//only removes check if there was a check highlighed square if it was check before
      await sendState();

    removeAISelect();
    let ai_success = await aiMove();
    if(ai_success){
      whiteTurn = !whiteTurn;
      await removeCheck();
      await sendState();
    }
    else{
      console.log("AI ERROR")
    }
    }
  }
  else{
    removeSelect(1);
  }
}

async function removeCheck(AI = true){
  let kingSquare = document.getElementsByClassName("CHECK");
      if(kingSquare.length === 1){

        if (AI)
          await sleep(500);//slight delay before red goes away because AI removes instantly we want to see it
        kingSquare[0].classList.toggle("CHECK");
      }
}

async function aiMove(){
  console.log("AIMove Function entered");
  let response = await fetch("/ai_move");
  let boardResponse = await response.json();

  if(response.ok){
    moveSound.currentTime = .3;
    moveSound.play();
    ai_start = boardResponse['fromMove'];
    ai_end = boardResponse['toMove'];
    
    let square1 = document.querySelector(`[data-col="${ai_start[0]}"][data-row="${ai_start[1]}"]`);
    let square2 = document.querySelector(`[data-col="${ai_end[0]}"][data-row="${ai_end[1]}"]`);

    square1.classList.toggle('ai_selected');
    square2.classList.toggle('ai_selected');
    return true;
  }
  return false;
}

function removeSelect(num = 2){
  
  fromMove = "";
  toMove = "";
  promotionPiece = "";
  selected = 0;
  let selectedSquares = document.getElementsByClassName("selected");
  console.log("LENGTH")
  console.log(selectedSquares.length)

  //only toggles 2 if there is two selected else only toggles 1
  if(num == 2){
    selectedSquares[0].classList.remove('first','second'); //we tell it to remove either because we dont know which one it has
    selectedSquares[0].classList.remove('selected');
  }

  selectedSquares[0].classList.remove('first','second'); //important to do this before selected so the element isnt removed from live list
  selectedSquares[0].classList.remove('selected');
}

function removeAISelect(){

  let square1 = null;
  let square2 = null;
  if(ai_start.length){//if length is zero then that means we havnt assigned ai_start or ai_end yet
    square1 = document.querySelector(`[data-col="${ai_start[0]}"][data-row="${ai_start[1]}"]`);
    square2 = document.querySelector(`[data-col="${ai_end[0]}"][data-row="${ai_end[1]}"]`);
  }

  if(square1){//not null then will run, if squar1 is not null then square2 must also not be null
    square1.classList.toggle('ai_selected');
    square2.classList.toggle('ai_selected');
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function isUpper(character) {
    if (character === character.toUpperCase()) {
        return true;
    } 
    else {
        return false;
    }
}

function openPopUp(){//only open if two squares selected and second square selected is promotion rank with pawn
  let popup = document.querySelector('.popup');
  popup.classList.add("active");
  overlay.classList.add("active");
}

function closePopUp(clickX = false){
  let popup = document.querySelector('.popup');
  popup.classList.remove("active");
  overlay.classList.remove("active");

  if(clickX){//if x was clicked person changed their mind and doesnt want to promote
    removeSelect();
  }
}

function checkPawnSelected(){
  let file = fromMove[0];
  let rank = fromMove[1];
  let pieceSelected = document.querySelector(`[data-col="${file}"][data-row="${rank}"]`);

  if (pieceSelected && pieceSelected.firstElementChild.alt === "P" ){
    return true;
  }
  return false;
}