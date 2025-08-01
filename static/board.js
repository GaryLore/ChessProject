
const board = document.getElementsByClassName("board")[0];
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
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