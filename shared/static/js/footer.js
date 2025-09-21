document.addEventListener("DOMContentLoaded", function () {
  const btn = document.querySelector(".show-footer");
  const hiddenBlock = document.querySelector(".footer-hidden");

  if (!btn || !hiddenBlock) return;

  btn.addEventListener("click", function () {
    hiddenBlock.classList.toggle("expanded");

    btn.textContent = hiddenBlock.classList.contains("expanded") ? "Show Less" : "Show More";
  });
});
