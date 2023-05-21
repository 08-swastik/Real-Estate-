// add sticky navigation bar

// activate the hamburger menu and mobile navigation
document.addEventListener("DOMContentLoaded", function() {
    const hamb = document.querySelector(".hamb");
    const nav = document.querySelector(".nav-mobile");
    hamb.addEventListener("click", function() {
      hamb.classList.toggle("active");
      nav.classList.toggle("active");
    });
  });

