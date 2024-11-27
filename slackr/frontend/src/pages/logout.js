import http from "../utils/request.js";

// Remove all the uer info from localstorage and turns to login page
function logout(data) {
  http.post("/auth/logout", data).then((res) => {
    // Rasie error if res is null/undefined
    if (!(!res || res.error)) {
      Swal.fire({
        icon: 'success',
        title: 'Logout Successful',
        showConfirmButton: false,
        timer: 1500
      });
      localStorage.removeItem("token");
      localStorage.removeItem("userProfile")
      window.location.hash = "#login";
    }
  });
}

document.querySelector("#logoutBtn").addEventListener("click", function () {
  const email = document.querySelector("#loginEmail").value;
  const password = document.querySelector("#loginPassword").value;
  logout({ email, password });
});