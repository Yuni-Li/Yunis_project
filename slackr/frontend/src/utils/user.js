import http from "../utils/request.js";

// Fetch user profile and store the profile to local storage
export function fetchUserProfile(id) {
  http.get(`/user/${id}`).then((res) => {
    const userProfile = {
      ...res,
      id,
    };
    localStorage.setItem("userProfile", JSON.stringify(userProfile));
  });
}

// Get user profile in localstorage
export function getUserProfile() {
  const userProfile = localStorage.getItem("userProfile");
  if (!userProfile) return null;
  return JSON.parse(userProfile);
}