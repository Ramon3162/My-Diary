function openNav() {
    var x = document.getElementById("top-navigation");
    if (x.className === "nav-links") {
        x.className += " responsive";
    } else {
        x.className = "nav-links";
    }
}
