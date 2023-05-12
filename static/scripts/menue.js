/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function navbarToggle() {
    var x = document.getElementById("myTopnav");
    setResponsiveClass(x, "topnav")
}

/* Toggle search bar */
function searchbarToggle() {
    var x = document.getElementById("mobSearchBox");
    setResponsiveClass(x, "mob-search-wrapper")
}

function setResponsiveClass(x, t) {
    var elements = document.getElementsByClassName("responsive");
    for (var i = 0; i < elements.length; i++) {
        if (x !== elements[i]) {
            elements[i].classList.remove("responsive");
        }
    }
    if (x.className === t) {
        x.className += " responsive";
    } else {
        x.className = t;
    }
}