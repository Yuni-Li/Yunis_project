import http from "../utils/request.js";
import { clearDom, dataAndTime } from "../utils/helper.js";
import { getUserProfile } from "../utils/user.js";
import { fetchChannelMessage } from "./messages.js";

export function fetchChannelList() {
  http.get("/channel").then((res) => {
    createChannelList(res.channels);
    switchChannel();
  });
}

export function fetchChannelDetail(channelId) {
  http.get(`/channel/${channelId}`).then((detail) => {
    createChannelHeader({
      ...detail,
      id: channelId,
    });
  });
}

/***************************************************************
                        Create Channel
***************************************************************/
// Show create channel modal
const createChannelModal = new bootstrap.Modal(document.getElementById("createChannelModal"));

document.getElementById("createChannelBtn").addEventListener("click", function () {
  createChannelModal.show();
});

document.querySelector(".close-create-btn").addEventListener("click", function () {
  createChannelModal.hide();
});

document.querySelector("#createChannel").onclick = function () {
  const curChannelName = document.querySelector("#channelName").value;
  const description = document.querySelector("#channelDescription").value;
  const _private = document.querySelector("#channelPraviteCheck").checked;
  const createChannelModal = new bootstrap.Modal("#createChannelModal");

  // Raise error if not enter channel name or descriptionn
  // The default value of private is false
  if (!curChannelName) {
    Swal.fire({
      icon: 'error',
      title: 'Invalid inut',
      text: 'Please provide a name for new channel',
    })
    return;
  }

  if (!description) {
    Swal.fire({
      icon: 'error',
      title: 'Invalid inut',
      text: 'Please provide a description',
    })
    return;
  }
 
  http.post("/channel", { 
    name: curChannelName, 
    private: _private, 
    description,
  })
  .then((res) => {
    if (res && res.channelId) {
      Swal.fire({
        icon: 'success',
        title: 'Channel has been created',
        showConfirmButton: false,
        timer: 1500
      })
      createChannelModal.hide();
      fetchChannelList();
    };
  });
};

/***************************************************************
                        Switch Channel
***************************************************************/
function switchChannel() {
  document.querySelectorAll(".channel-item").forEach((item) => {
    // If clicked channel is not current active channel
    // Remove the "active-channel" from the list to set the channel to not active
    item.onclick = function () {
      if (item.classList.contains("unjoined")) {
        Swal.fire({
          icon: 'error',
          title: 'No permission',
          text: 'Join in to access the channel message',
        })
        return;
      }

      if (!item.classList.contains("active-channel")) {
        document.querySelectorAll(".channel-item").forEach((iterItem) => {
          iterItem.classList.remove("active-channel");
        })
      }
      // Set current clicked channel to active channel
      item.classList.add("active-channel");
      const curChannelId = Number(item.id.split("_")[2]);

      window.__ACTIVE_CHANNEL_ID__ = curChannelId;
      fetchChannelDetail(curChannelId);
      fetchChannelMessage(curChannelId);
    }
  })
}

/***************************************************************
                      Show Channel Profile
***************************************************************/
function createChannalProfile(detail) {
  const { name, creator, priv, description, createdAt, members } = detail;
  const channelProfileDom = document.getElementById("channelProfileBody");
  if (channelProfileDom !== null) clearDom(channelProfileDom);

  // Create elements
  const channelName = document.createElement("p");
  const channelCreatorId = document.createElement("p");
  const channelPrivate = document.createElement("p");
  const channelDescrip = document.createElement("p");
  const channelCreatedTime = document.createElement("p");
  const channelMembers = document.createElement("p");

  // Generate class name 
  channelName.className = "channal-profile-name";
  channelCreatorId.className = "channal-profile-creator";
  channelPrivate.className = "channal-profile-priv";
  channelDescrip.className = "channal-profile-descrip";
  channelCreatedTime.className = "channal-profile-create-time";
  channelMembers.className = "channal-profile-members";

  // Convert createTime from ISO string to spcific format
  const createTime = dataAndTime(createdAt);
  const privacy = detail.private;

  // Generate innerText
  channelName.innerText = `Name: ${name}`;
  channelCreatorId.innerText = `Creator Id:  ${creator}`;
  channelPrivate.innerText = `Private:  ${privacy}`;
  channelDescrip.innerText = `Description:  ${description}`;
  channelCreatedTime.innerText = `Create Time:  ${createTime}`;
  channelMembers.innerText = `Members:  ${members}`;

  // Generate appendChild
  channelProfileDom.appendChild(channelName);
  channelProfileDom.appendChild(channelDescrip);
  channelProfileDom.appendChild(channelCreatorId);
  channelProfileDom.appendChild(channelCreatedTime);
  channelProfileDom.appendChild(channelMembers);
  channelProfileDom.appendChild(channelPrivate);

}

/***************************************************************
                      Show Channel Profile
***************************************************************/
function createChannalMembers(detail) {
  const memberId = detail.members;
  const memberList = document.createElement("div");
  const channelMembersDom = document.getElementById("channelMembersBody");
  if (channelMembersDom !== null) clearDom(channelMembersDom);

  memberList.className = "channel-member-list";
  memberList.innerText = memberId;
  
  channelMembersDom.appendChild(memberList);
}  

/***************************************************************
                      Create Functions
***************************************************************/
const showChannelProfileModal = new bootstrap.Modal("#channelProfileModal");
const showChannelMemberModal = new bootstrap.Modal("#channelMembersModal")

document.querySelector(".close-channel-profile").onclick = function () {
  showChannelProfileModal.hide()
}
document.querySelector(".close-channel-members").onclick = function () {
  showChannelProfileModal.hide()
}

function createChannelList(channelList, channelId) {
  const listDom = document.getElementById("channel-list");
  const userProfile = getUserProfile();
  const userId = userProfile.id;
  clearDom(listDom);

  // Filter out channels that user already been joined
  const joinedChannels = channelList.filter((channel) => 
    channel.members.includes(userId)
  );

  const targetChannelId = channelId || joinedChannels[0].id;
  // Get current active channel
  window.__ACTIVE_CHANNEL_ID__ = targetChannelId;
  const unjoinedChannels = channelList.filter(
    (channel) => !channel.members.includes(userId)
  );

  // Generation for joined channels
  joinedChannels.forEach((channel) => {
    const channelDom = document.createElement("div");
    const channelLeftDom = document.createElement("div");
    const channelRightDom = document.createElement("div");
    const privChannelLogo = document.createElement("i");
    const channelLogo = document.createElement("div");
    const channelTitle = document.createElement("p");
    const channelPrivacy = channel.private;

    const active = channel.id === targetChannelId;
    channelDom.id = `channel_list_${channel.id}`;

    channelDom.className = active
      ? "joined channel-item active-channel"
      : "joined channel-item";
    channelLeftDom.className = "channel-left-dom";
    channelRightDom.className = "channel-right-dom";
    privChannelLogo.className = "bi bi-person-lock"
    channelLogo.className = "channel-logo";
    channelTitle.className = "channel-title";

    channelLogo.style.background = randomColor();
    channelLogo.innerText = channel.name[0];
    channelTitle.innerText = channel.name;

    channelLeftDom.appendChild(channelLogo);
    channelLeftDom.appendChild(channelTitle);
    // Add privacy logo to private channel
    if (channelPrivacy) channelRightDom.appendChild(privChannelLogo);
    channelDom.appendChild(channelRightDom);
    channelDom.appendChild(channelLeftDom);

    listDom.appendChild(channelDom);
  });

  // Generation for unjoined channels
  unjoinedChannels.forEach((channel) => {
    const channelDom = document.createElement("div");
    const channelListLeft = document.createElement("div");
    const channelListRight = document.createElement("div");
    const channelLogo = document.createElement("div");
    const channelTitle = document.createElement("h3");
    const joinbtn = document.createElement("button");

    const active = channel.id === targetChannelId;
    channelDom.id = `channel_list_${channel.id}`;

    channelDom.className = active
      ? "unjoined channel-item active-channel"
      : "unjoined channel-item";
    channelListLeft.className = "channel-list-left";
    channelListRight.className = "channel-list-right";
    channelLogo.className = "channel-logo";
    channelTitle.className = "channel-title";
    joinbtn.className = "btn btn-light btn-sm join-btn";

    channelLogo.style.background = randomColor();
    channelLogo.innerText = channel.name[0];
    channelTitle.innerText = channel.name;
    // Add a join button to unjoined channel
    joinbtn.innerText = "Join";
  
    channelListLeft.appendChild(channelLogo);
    channelListLeft.appendChild(channelTitle);
    channelListRight.appendChild(joinbtn);
    channelDom.appendChild(channelListLeft);
    channelDom.appendChild(channelListRight);
    listDom.appendChild(channelDom);
  });

  fetchChannelDetail(targetChannelId);
  fetchChannelMessage(targetChannelId);
}


function createChannelHeader(detail) {
  const headerDom = document.getElementById("channel-right-header");

  if (headerDom !== null) clearDom(headerDom);

  const headerLeft = document.createElement("div");
  const channelLogo = document.createElement("div");
  // Channel logo backgound color in the channel title should be the same in the channel list
  const channelListLogo = document.querySelector(`#channel_list_${detail.id} .channel-logo`);
  const channelTitle = document.createElement("p");
  const headerRight = document.createElement("div");

  // Channel header left container (logo and channel name)
  headerLeft.className = "header-left-container";
  channelLogo.className = "header-left-logo"; 
  channelTitle.className = "header-left-title";
  headerRight.className = "header-right-container";

  channelLogo.style.background = channelListLogo.style.background;
  channelLogo.innerText = detail.name[0];
  channelTitle.innerText = detail.name;

  // Different generation for mobile and pc
  if (window.__MOBILE__) {
    // Place all icon(functions) in a dropdown list
    const dropDownContainer = document.createElement("div");
    const dropDownMenu = document.createElement("ul");
    const dropDownBtn = document.createElement("a");

    // Channel header right container (icons)
    const infoIcon = document.createElement("li");
    const peopleIcon = document.createElement("li");
    const editIcon = document.createElement("li");
    const inviteIcon = document.createElement("li");
    const leaveIcon = document.createElement("li");

    dropDownBtn.className = "btn btn-light dropdown-toggle";
    dropDownBtn.setAttribute("data-bs-toggle", "dropdown");
    dropDownBtn.setAttribute("aria-expanded", "false");
    dropDownBtn.innerText = "...";

    // Generate class name
    dropDownContainer.className = "dropdown";
    dropDownMenu.className = "dropdown-menu";
    infoIcon.className = "dropdown-item";
    peopleIcon.className = "dropdown-item";
    editIcon.className = "dropdown-item";
    inviteIcon.className = "dropdown-item";
    leaveIcon.className = "dropdown-item";
    createChannalProfile(detail);
    infoIcon.onclick = function () {
      createChannalProfile(detail);
      showChannelProfileModal.show();
    }

    // Generate innerText
    infoIcon.innerText = "Channel Information";
    peopleIcon.innerText = "Members";
    editIcon.innerText = "Edit Channel";
    inviteIcon.innerText = "Invite User";
    leaveIcon.innerText = "Leave Channel";

    // Generate appendChild
    dropDownMenu.appendChild(infoIcon);
    dropDownMenu.appendChild(peopleIcon);
    dropDownMenu.appendChild(editIcon);
    dropDownMenu.appendChild(inviteIcon);
    dropDownMenu.appendChild(leaveIcon);
    dropDownContainer.appendChild(dropDownMenu);
    dropDownContainer.appendChild(dropDownBtn);
    headerRight.appendChild(dropDownContainer);

  } else {
    // Channel header right container (icons)
    const infoIcon = document.createElement("i");
    const peopleIcon = document.createElement("i");
    const editIcon = document.createElement("i");
    const inviteIcon = document.createElement("i");
    const leaveIcon = document.createElement("i");

    // Generate class name, these class names are from bootstrap icons
    // Source url: https://icons.getbootstrap.com/
    infoIcon.className = "bi bi-info-circle";
    peopleIcon.className = "bi bi-people";
    editIcon.className = "bi bi-pencil-square";
    inviteIcon.className = "bi bi-person-plus";
    leaveIcon.className = "bi bi-box-arrow-right";

    // Functionalities of icons
    createChannalProfile(detail);
    infoIcon.onclick = function () {
      createChannalProfile(detail);
      showChannelProfileModal.show();
    }

    createChannalMembers(detail);
    peopleIcon.onclick = function () {
      createChannalMembers(detail);
      showChannelMemberModal.show();
    }

    // Generate appendChild
    headerRight.appendChild(infoIcon);
    headerRight.appendChild(peopleIcon);
    headerRight.appendChild(editIcon);
    headerRight.appendChild(inviteIcon);
    headerRight.appendChild(leaveIcon);
  }

  // Generate appendChild
  headerLeft.appendChild(channelLogo);
  headerLeft.appendChild(channelTitle);
  headerDom.appendChild(headerLeft);
  headerDom.appendChild(headerRight);

}

/***************************************************************
                      Helper functions
***************************************************************/
function randomColor() {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return `rgb(${r},${g},${b})`;
}