import http from "../utils/request.js";

function register(data) {
  http.post("/auth/register", data).then((res) => {
    if (!(!res || res.error)) {
      Swal.fire({
        icon: 'success',
        title: 'Registration Success',
        showConfirmButton: false,
        timer: 1500
      })
      localStorage.setItem("token", res.token);
      window.location.hash = "#login";
    }
  })
}

document.querySelector("#registerBtn").addEventListener("click", function () {
  const email = document.querySelector("#registerEmail").value;
  const userName = document.querySelector("#registerName").value;
  const password = document.querySelector("#registerPassword1").value;
  const confirmPassword = document.querySelector("#registerPassword2").value;

  // Return error messge if email format is invalid
  if (!isValidEmail(email)) {
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Invalid email format',
    });
    return;
  }

  if (userName && password && confirmPassword) {
    if (password !== confirmPassword) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: "Password don't match",
      });
    } else {
      register({ email, userName, password });
    }
  } else {
    Swal.fire({
      icon: 'error',
      title: 'Please input all the information',
    });
  }
})

// Helper function to check email format
function isValidEmail(email) {
  const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  return regex.test(email);
}