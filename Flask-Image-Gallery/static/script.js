
function do_clicked(element) {
  console.log("1");
  document.getElementById("img00").src = element.src;

  document.getElementById("img01").src = './results/6173736574732f726573756c74732f73637265656e73686f742e706e67';
  // document.getElementById("img01").src = "./results/" + path;
  document.getElementById("modal00").style.display = "block";

}

function do_process() {
  console.log("1");

  document.getElementById("img01").src = document.getElementById("img00").src.replaceAll('cdn', 'results');

  document.getElementById("modal00").style.display = "block";

}

function do_close(){
  document.getElementById("modal00").style.display = "none";

}

