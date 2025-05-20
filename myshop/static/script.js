document.addEventListener("DOMContentLoaded", () => {
  const modal     = document.getElementById("loginModal");
  const userIcon  = document.querySelector(".user-icon");
  const loginBtn  = document.getElementById("loginBtn");
  const closeBtn  = document.querySelector(".close");

  console.log("userIcon:", userIcon);
  console.log("loginBtn:", loginBtn);


  
  function openModal() {
    modal.style.display = "flex";
  }

  if (userIcon)  userIcon.addEventListener("click", openModal);
  if (loginBtn)  loginBtn.addEventListener("click", openModal);

  if (closeBtn) {
    closeBtn.addEventListener("click", () => modal.style.display = "none");
  }

  window.addEventListener("click", e => {
    if (e.target === modal) modal.style.display = "none";
  });
});

const form = document.getElementById('loginForm');
if (form) {
  form.addEventListener('submit', e => {
    console.log('📝 Submitting login form…');
  });
}
