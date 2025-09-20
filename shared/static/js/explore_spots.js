document.addEventListener("DOMContentLoaded", function () {
  // For each button, toggle its image color on hover/focus
  document.querySelectorAll(".explore-btn").forEach(function (btn) {
    const spot = btn.getAttribute("data-spot");
    const section = btn.closest(".spot-image-section");
    btn.addEventListener("mouseenter", function () {
      section.classList.add("active");
    });
    btn.addEventListener("mouseleave", function () {
      section.classList.remove("active");
    });
    btn.addEventListener("focus", function () {
      section.classList.add("active");
    });
    btn.addEventListener("blur", function () {
      section.classList.remove("active");
    });
  });
});