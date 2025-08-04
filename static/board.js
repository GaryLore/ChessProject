
const board = document.getElementsByClassName("board")[0];
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];//column
let selected = 0;
let fromMove;
let toMove;

for(let row = 8; row != 0; --row){
    for(let col = 0; col != 8; ++col){

        let square = document.createElement("div");
        square.classList.add('square');
        square.classList.add( (row+col)%2 === 0 ? "black" : "white");
        square.dataset.col = files[col];
        square.dataset.row = row;
        board.appendChild(square);

    }
}

document.querySelectorAll('.square').forEach(square => {
  square.addEventListener('click', () => {
    console.log(selected);
    if(selected < 2 && !square.classList.contains('selected')){//not contains selected and below 2 selected
        square.classList.toggle('selected');
        if(selected == 0){
          fromMove = square.dataset.col + square.dataset.row;
        }
        else{
          toMove = square.dataset.col + square.dataset.row;
        }
        ++selected;
    }
    else if(square.classList.contains('selected')){//contains selected, we dont need to check if less than 2 doesnt matter, by this code it has to be
        square.classList.toggle('selected');
        if(selected == 2){
          toMove = "";
        }
        else{//gotta either be one or two selected
          fromMove = "";
        }
        --selected;
            
    }
    else{ //not contains selected and equal to 2 or above(in essence will only be 2), all these are mutually exclusive
        removeSelect();
        square.classList.toggle('selected');
        ++selected;
        fromMove = square.dataset.col + square.dataset.row;//always gonna be zero so no need to check what selected is
    }
  });
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

  //fills in the squares that are actually not full, goes throu
  for(let key in data){
    let col = key[0];
    let row = key[1];
    let piece = data[key];
    console.log('[data-col="'+col+'"][data-row="'+row+'"]');
    let div = document.querySelector('[data-col="'+col+'"][data-row="'+row+'"]');

    if (isUpper(piece)){
      piece = piece.toLowerCase();
      div.innerHTML = '<img src="../static/img/' + piece + '_.png"'  + 'alt="Chess piece">';
    }
    else{
      div.innerHTML = '<img src="../static/img/' + piece + '.png"'  + 'alt="Chess piece">';
    }

  }
  console.log(data);
}

async function submitMove(params) {
  
  console.log("SubmitMove Function entered");
  let response = await fetch("/submit_move", {
  method: "POST",
  headers: { "Content-Type": "application/json" }, // Necessary here
  body: JSON.stringify({ move: `${fromMove}${toMove}` }),
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
    await sendState();

    let ai_success = await aiMove();
    if(ai_success){
      await sendState();
    }
    else{
      console.log("AI ERROR")
    }
  }
}

async function aiMove(){
  console.log("AIMove Function entered");
  let response = await fetch("/ai_move");
  let boardResponse = await response.json();

  if(response.ok){
    return true;
  }
  return false;
}

function removeSelect(){
  fromMove = "";
  toMove = "";
  selected = 0;
  let selectedSquares = document.getElementsByClassName("selected");
  console.log("LENGTH")
  console.log(selectedSquares.length)
  selectedSquares[0].classList.toggle('selected');
  selectedSquares[0].classList.toggle('selected');
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