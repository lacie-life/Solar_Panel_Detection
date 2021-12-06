
function do_clicked(element) {
  console.log("1");
  document.getElementById("img00").src = element.src;
  
  // document.getElementById("img01").src = './results/6173736574732f726573756c74735c70726f636573732d6c6f6164696e672d74656d706c6174652d766563746f722d32303635373633322e6a7067';
  // var x  = document.getElementById("img01");
  // x.style.height = "300px";
  // x.style.marginTop = "120px";
  // document.getElementById("img01").src = "./results/" + path;
  document.getElementById("modal00").style.display = "block";
  document.getElementById("loader").style.display = "block";

}

function do_process() {
  console.log("1");
  document.getElementById("loader").style.display = "none";
  document.getElementById("img01").src = document.getElementById("img00").src.replaceAll('cdn', 'results');
  var x  = document.getElementById("img01");
  x.style.height = "550px";
  x.style.marginTop = "0px";
  x.style.display = "block";
  
  document.getElementById("modal00").style.display = "block";

}

function do_close(){
  document.getElementById("modal00").style.display = "none";
  document.getElementById("loader").style.display = "none";
  var x  = document.getElementById("img01").style.display = "none";
}

