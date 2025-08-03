
const board = document.getElementsByClassName("board")[0];
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];//column
let selected = 0;

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
    if(selected < 2 && !square.classList.contains('selected')){
        square.classList.toggle('selected');
        ++selected;
    }
    else if(square.classList.contains('selected')){
            square.classList.toggle('selected');
            --selected;
    }
  });
});

window.onload = sendState;

async function sendState(params) {
  let response = await fetch("/update_state");

  if (!response.ok) {
      console.error("Server returned error:", response.status);
      return;
  }

  let data = await response.json();

  //resets the board everytime
  let squares = document.querySelectorAll('.square')
  for(let div in squares){
    div.innerHTML = ""
  }

  //fills in the squares that are actually not full
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

async function makeMove(params) {
  
}

function isUpper(character) {
    if (character === character.toUpperCase()) {
        return true;
    } 
    else {
        return false;
    }
}