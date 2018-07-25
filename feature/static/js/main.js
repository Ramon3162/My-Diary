function openNav() {
    let nav = document.getElementById("top-navigation");
    if (nav.className === "nav-links") {
        nav.className += " responsive";
    } else {
        nav.className = "nav-links";
    }
}

function confirmDelete() {
    confirm("Are you sure you want to delete this entry?")
}
