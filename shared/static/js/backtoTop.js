// Back to Top Button Functionality
document.addEventListener("scroll", function () {
  const backToTopButton = document.getElementById("backToTop");

  // Show the button after scrolling 300px
  if (window.scrollY > 300) {
    backToTopButton.classList.add("show");
  } else {
    backToTopButton.classList.remove("show");
  }
});

// Scroll to the top when the button is clicked
const backToTopButton = document.getElementById("backToTop");
backToTopButton.addEventListener("click", function() {
  window.scrollTo({ top: 0, behavior: "smooth" });
});