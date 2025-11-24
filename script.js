let ws = new WebSocket("ws://localhost:6789");

ws.onopen = () => {
  document.getElementById("status").innerText = "Connected ✅";
};

ws.onclose = () => {
  document.getElementById("status").innerText = "Disconnected ❌";
};

ws.onmessage = (event) => {
  let chat = document.getElementById("chat");
  chat.innerHTML += `<div>${event.data}</div>`;
  chat.scrollTop = chat.scrollHeight;
};

const input = document.getElementById("input");

document.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && input.value !== "") {
    ws.send(input.value);
    input.value = "";
  }
});

