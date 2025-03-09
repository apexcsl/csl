document.addEventListener("DOMContentLoaded", function () {
  const profileBtn = document.getElementById("profileBtn");
  const profileDropdown = document.getElementById("profileDropdown");

  if (profileBtn) {
      profileBtn.addEventListener("click", function () {
          profileDropdown.style.display = profileDropdown.style.display === "block" ? "none" : "block";
      });

      // Cierra el menú si el usuario hace clic fuera de él
      document.addEventListener("click", function (event) {
          if (!profileBtn.contains(event.target) && !profileDropdown.contains(event.target)) {
              profileDropdown.style.display = "none";
          }
      });
  }
});
