import http from "../utils/request.js";
import { fetchUserProfile } from '../utils/user.js';
import { fetchChannelList } from "./channel.js";

// Add the token to localstorage and turns to channel page
function login(data) {
  http.post("/auth/login", data).then((res) => {
    // Rasie error if res is null/undefined
    if (!(!res || res.error)) {
      Swal.fire({
        icon: 'success',
        title: 'Login Successful',
        showConfirmButton: false,
        timer: 1500
      });
      localStorage.setItem("token", res.token);
      window.location.hash = "#channel";
      fetchUserProfile(res.userId);
      fetchChannelList();
    };
  });
}

document.querySelector("#loginBtn").addEventListener("click", function () {
  const email = document.querySelector("#loginEmail").value;
  const password = document.querySelector("#loginPassword").value;
  login({ email, password });
})