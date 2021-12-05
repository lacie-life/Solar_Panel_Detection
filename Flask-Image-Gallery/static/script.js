
function myfunction(element) {
  console.log("1");
  document.getElementById("img00").src = element.src;

  // document.getElementById("img01").src = "./results/" + path;
  document.getElementById("modal00").style.display = "block";

  document.getElementById('process').hidden = false;
}

function do_process() {
  console.log("1");
  document.getElementById("img01").src = document.getElementById("img00").src;

  document.getElementById("img02").src = element.src.replaceAll('cdn', 'results');

  // document.getElementById("img01").src = "./results/" + path;
  document.getElementById("modal01").style.display = "block";
}

