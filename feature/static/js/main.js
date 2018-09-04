const openNav = () => {
    let nav = document.getElementById("top-navigation");
    if (nav.className === "nav-links") {
        nav.className += " responsive";
    } else {
        nav.className = "nav-links";
    }
}
