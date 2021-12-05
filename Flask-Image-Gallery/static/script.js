
function myfunction(element) {
  console.log("1");
  document.getElementById("img01").src = element.src;

  document.getElementById("img02").src = element.src.replaceAll('cdn', 'results');

  // document.getElementById("img01").src = "./results/" + path;
  document.getElementById("modal01").style.display = "block";
}
