function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
     document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
}
function myFunction() {
document.getElementsByClassName("topnav")[0].classList.toggle("responsive");
}

document.addEventListener('DOMContentLoaded', function () {
    let navbar = document.querySelector(".navbar");
    let navLinks = document.querySelector(".nav-links");
    let menuOpenBtn = document.querySelector(".navbar .bx-menu");
    let menuCloseBtn = document.querySelector(".nav-links .bx-x");
  
    menuOpenBtn.onclick = function() {
        navLinks.style.left = "0";
    }
  
    menuCloseBtn.onclick = function() {
        navLinks.style.left = "-100%";
    }
  
    let htmlcssArrow = document.querySelector(".htmlcss-arrow");
    htmlcssArrow.onclick = function() {
        navLinks.classList.toggle("show1");
    }
  
    let jsArrow = document.querySelector(".js-arrow");
    jsArrow.onclick = function() {
        navLinks.classList.toggle("show3");
    }
  });
