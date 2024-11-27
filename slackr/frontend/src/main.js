import { BACKEND_PORT } from './config.js';
// A helper you may want to use when uploading new images to the server.
import { fileToDataUrl } from './helpers.js';
import { fetchChannelList } from './pages/channel.js';

window.addEventListener('resize', checkAndUpdateMobileStatus);

function loadingPage() {
  const loading = document.getElementById("loading-page");
  setTimeout(() => {
    loading.style.display = "none";
  }, 600);
}

function initPage() {
  loadingPage();
  window.__MESSAGE_START__ = 0;
  checkAndUpdateMobileStatus();

  if (window.__MOBILE__) document.body.classList.add("mobile");
}

// Set all page to display none
// Then change the target page type to display block
function showPage(pageType) {
  const pages = document.querySelectorAll(`.page`);
  pages.forEach(page => page.style.display = "none");
  if (pageType === "channel") {
    document.querySelector(`.page.${pageType}-container`).style.display = "flex";
    fetchChannelList();
  } else {
    document.querySelector(`.page.${pageType}-container`).style.display = "block";
  }
}

// Listen hash change
window.onhashchange = function () {
  const hash = window.location.hash;
  const isLogin = checkLogin();

  // Back to login page if user is not online and 
  // tends to visit the page other than login and register (i.e. channel page)
  if (!isLogin && hash !== "#login" && hash !== "#register") {
    window.location.hash = "#login";
    showPage("login");
  } else {
    switch (hash) {
      case "#channel":
        showPage("channel");
        break;
      case "#login":
        showPage("login");
        break;
      case "#register":
        showPage("register")
    }
  }
}

window.onload = () => {
  initPage();
  window.onhashchange()
};


/***************************************************************
                    Helper Check functions
***************************************************************/
function checkLogin() {
  return (localStorage.getItem("token") !== null && localStorage.getItem("token") !== "null");
}

function checkMobile() {
  return window.innerWidth < 600;
}

function checkAndUpdateMobileStatus() {
  // Check if mobile
  const isMobile = checkMobile();
  if (isMobile) {
    document.body.classList.add("mobile");
  } else {
    document.body.classList.remove("mobile");
  }
  // Update global variable
  window.__MOBILE__ = isMobile;
}