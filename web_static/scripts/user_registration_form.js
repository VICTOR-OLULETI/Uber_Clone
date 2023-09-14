  const form = document.getElementById("myForm");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const fullnameInput = document.getElementById("fullname");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!isValidEmail(emailInput.value)) {
      alert("Invalid email format");
      return;
    }
    if (!fullnameInput.value.trim()) {
      alert("Full Name is required");
      return;
    }
    if (passwordInput.value.length < 6) {
      alert("Password must be at least 6 characters long");
      return;
    }
    alert("Form submitted successfully!");
    // You can also send the form data to a server here
  });

  function isValidEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
  }