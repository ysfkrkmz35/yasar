document.addEventListener("DOMContentLoaded", function() {
  var toggleButton = document.getElementById("sidebarToggle");
  var sidebar = document.getElementById("sidebar");
  var content = document.getElementById("content");

  toggleButton.addEventListener("click", function() {
    if (!sidebar.classList.contains("hiddenSidebar")) {
      // Sidebar görünüyorsa gizle: 250px sola kaydır
      sidebar.classList.add("hiddenSidebar");
      sidebar.style.transform = "translateX(-250px)";
      content.style.marginLeft = "0";
    } else {
      // Gizliyse göster: sıfırlayın
      sidebar.classList.remove("hiddenSidebar");
      sidebar.style.transform = "translateX(0)";
      content.style.marginLeft = "250px";
    }
  });
});
