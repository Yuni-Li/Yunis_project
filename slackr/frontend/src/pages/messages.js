import http from "../utils/request.js";
import { clearDom, dataAndTime } from "../utils/helper.js";
import { getUserProfile } from "../utils/user.js";

export function fetchChannelMessage(channelId, start = 0) {
  window.__CHANNEL_MESSAGE_LOADED__ = false;
  http.get(`/message/${channelId}?start=${window.__MESSAGE_START__}`).then((msg) => {
    // Check if msg is empty or if there are no messages
    // Generate an empty msg text if there is no message in curren channel
    if (!msg || !msg.messages || msg.messages.length === 0 && window.__MESSAGE_START__ === 0) {
      createEmptyMsg();
    } else {
      createMessageList(msg);
      window.__CHANNEL_MESSAGE_LOADED__ = true;
    }
  });
}

/***************************************************************
                      Create Functions
***************************************************************/
// Generate a hello text if current channel has no msg
function createEmptyMsg() {
  const emptyMsg = document.createElement("div");
  const noMessage1 = document.createElement("p");
  const noMessage2 = document.createElement("p");
  const messageDom = document.getElementById("message-box");
  if (messageDom !== null) clearDom(messageDom);

  emptyMsg.className = "empty-msg";
  noMessage1.className = "no-message-channel";
  noMessage2.className = "no-message-channel";
  noMessage1.innerText = "👋 Welcome to the channel!"
  noMessage2.innerText = "Start your first message!"

  emptyMsg.appendChild(noMessage1);
  emptyMsg.appendChild(noMessage2);
  messageDom.appendChild(emptyMsg);
}

function createMessageList(messageList) {
  const messageDom = document.getElementById("message-box");
  // These 2 const are used to save the old scroll position
  const oldScrollTop = messageDom.scrollTop;
  const oldScrollHeight = messageDom.scrollHeight;

  const message = messageList.messages;

  if (messageDom !== null && window.__MESSAGE_START__ === 0) clearDom(messageDom);
  
  message.forEach((msg) => {
    const msgContainer = document.createElement("div");
    const msgAvatarContainer = document.createElement("div");
    const msgDetailsContainer = document.createElement("div");
    const msgSenderDetailsContainer = document.createElement("div");
    const msgLogo = document.createElement("img");
    const msgSender = document.createElement("div");
    const msgContent = document.createElement("div");
    const msgSendTime = document.createElement("div");

    const curUserProfile = getUserProfile();
    const curUserId = curUserProfile.id;

    const myMessage = curUserId === msg.sender;
    // const senderUserName = fetchUserProfile(msg.sender).name;
    // const senderUserAvatar = fetchUserProfile(msg.sender).image;

    // Generate class name 
    curUserId === msg.sender
    ? msgContainer.className = "msg-contianer my-msg"
    : msgContainer.className = "msg-container";
    msgAvatarContainer.className = "msg-avatar-container";
    msgDetailsContainer.className = "msg-details-container";
    msgSenderDetailsContainer.className = "msg-sender-detail-container";
    msgLogo.className = "msg-logo";
    msgSender.className = "msg-sender";
    msgContent.className = "msg-content";
    msgSendTime.className = "msg-send-time";

    // Generate innerText
    msgLogo.src = "images/defaultAvatar.png";
    msgSender.innerText = msg.sender;
    msgContent.innerText = msg.message;
    msgSendTime.innerText = dataAndTime(msg.sentAt);

    // Generate appendChild
    msgAvatarContainer.appendChild(msgLogo);
    msgSenderDetailsContainer.appendChild(msgSender);
    msgSenderDetailsContainer.appendChild(msgSendTime);
    msgDetailsContainer.appendChild(msgSenderDetailsContainer);
    msgDetailsContainer.appendChild(msgContent);

    // If msg is sent by cur user,
    // add msg details first because it should be locates on the left of the avatar
    if (!myMessage) {
      msgContainer.appendChild(msgAvatarContainer);
      msgContainer.appendChild(msgDetailsContainer);
    } else {
      msgContainer.appendChild(msgDetailsContainer);
      msgContainer.appendChild(msgAvatarContainer);
    }
    
    messageDom.appendChild(msgContainer);

    // If messageDom is not empty, add next msg at the top of the list
    if(messageDom.firstChild) {
      messageDom.insertBefore(msgContainer, messageDom.firstChild);
    } else {
        messageDom.appendChild(msgContainer);
    }
      
    // Always insert to the front because the lastest msg should be the lowest
    messageDom.children.length
    ? messageDom.insertBefore(msgContainer, messageDom.children[0])
    : messageDom.appendChild(msgContainer);

    // Only direct to the bottom if there is no scroll up to fetch more msg
    if (window.__MESSAGE_START__ === 0) newToBottom(messageDom);
  })

  // When loading a new msg list, 
  // the scrolling position of the page should remain unchanged at the current message.
  const newScrollHeight = messageDom.scrollHeight;
  const heightDifference = newScrollHeight - oldScrollHeight;
  messageDom.scrollTop = oldScrollTop + heightDifference;
}

/***************************************************************
                      Helper functions
***************************************************************/
// Load more message (a new group of message list)
document.getElementById("message-box").onscroll = function (index) {
  const { scrollTop } = index.target;
  if (scrollTop === 0 && window.__CHANNEL_MESSAGE_LOADED__) {
    window.__MESSAGE_START__ += 25;
    fetchChannelMessage(window.__ACTIVE_CHANNEL_ID__)
  }
}

// Insert new msg to the bottom if msgDetailsContainer is not empty
// And locates to the newest message when user opening the channel
function newToBottom(messageDom) {
  messageDom.scrollTop = messageDom.scrollHeight;
}
