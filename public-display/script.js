// Rejimni o‘zgartirish
document.getElementById("themeToggle").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const toggleBtn = document.getElementById("themeToggle");
    toggleBtn.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
    localStorage.setItem("theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
});

// Sahifa yuklanganda rejimni qayta tiklash
window.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    const toggleBtn = document.getElementById("themeToggle");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        toggleBtn.textContent = "☀️";
    }
});