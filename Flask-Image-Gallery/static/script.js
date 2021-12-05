// function clicked_img(img,fp){
//           console.log(img.src);

//           var top=document.getElementById('top')

//           top.src = img.src;

//           top.hidden=false;


//           if (img.naturalWidth<screen.width*0.6 && img.naturalHeight<screen.height*0.6) {

//             top.width=img.naturalWidth;
//             top.height=img.naturalHeight;

//           } else {

//             top.width=screen.width*0.6;
//             top.height=img.naturalHeight/img.naturalWidth*top.width;

//           }

//           document.getElementById('close').hidden = false;
//  }


// function do_close(){
//   document.getElementById('top').hidden=true;
//   document.getElementById('close').hidden=true;
// }


// document.getElementsByClassName("image").forEach((item) => {
//   console.log("11");
//   item.addEventListener("click", (event) => {
//     alert("hehe");
//     const image = event.target.getAttribute("data-src");
//     event.target.setAttribute("src", image);
//   });
// });
function myfunction(element) {
  console.log("1");
  // document.getElementById("img01").src = element.src;
  document.getElementById("img01").src = "./results/6173736574732f696d616765732f436c6f7365446574656374526573756c74302e6a7067";
  document.getElementById("modal01").style.display = "block";
}
