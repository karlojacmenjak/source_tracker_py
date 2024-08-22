let checkPeriod;
let checkPeriodLabel;
let serverListDiv;
let serverList;

document.addEventListener("DOMContentLoaded", () => init());

function init() {
  checkPeriod = document.getElementById("checkPeriod");
  checkPeriod.addEventListener("input", () => {
    refreshForm();
  });

  checkPeriodLabel = document.getElementById("checkPeriodLabel");

  serverListDiv = document.getElementById("serverList");
  serverList = [];

  let serverListItems = serverListDiv.querySelectorAll("div.list-item");
  for (var item of serverListItems) {
    serverList.push(item.querySelector("input").value);
  }

  let txtServerData = document.getElementById("txtServerData");
  let btnAddServer = document.getElementById("btnAddServer");

  btnAddServer.addEventListener("click", () => {
    let server = txtServerData.value;

    try {
      server = parseGameServerInput(server);

      serverList.push(server);
      txtServerData.value = "";
      refreshForm();
    } catch (error) {
      alert(error.message);
    }
  });

  refreshForm();
}

function removeServerItem(index) {
  let serverListNew = [];
  for (let i = 0; i < serverList.length; i++) {
    if (i != index) serverListNew.push(serverList[i]);
  }

  serverList = serverListNew;
  refreshForm();
}

function parseGameServerInput(data) {
  data = data.trim();

  let regFull = /([a-zA-Z0-9\-\_\.]+)\s*:\s*(\d+)/gm;
  let result = data.matchAll(regFull).toArray()[0];

  if (result == undefined) {
    throw new Error("Invalid format for game server. Expected format is IP:PORT. Actual value: " + data);
  }

  let ip = result[1].trim();
  let port = result[2].trim();

  let regDomain = /[a-zA-Z0-9\-\_]+(\.[a-zA-Z0-9\-\_]+)*/gm;
  let regIp4 = /\d+\.\d+\.\d+\.\d+/gm;

  if (!ip.match(regDomain) && !ip.match(regIp4)) {
    throw new Error("Invalid format for game server ip. Expected value is either domain or IPv4 address. Actual value: " + data);
  }

  return ip + ":" + port;
}

function refreshForm() {
  checkPeriodLabel.innerText = checkPeriod.value + " min";

  let serverListHtml = "";
  for (let i = 0; i < serverList.length; i++) {
    serverListHtml += `
    <div class="list-item">
      <input type="text" spellcheck="false" placeholder="ip:port" value="${serverList[i]}" />
      <button type="button" onclick="removeServerItem(${i})" class="btn-icon"><img src="/static/icon-xmark.png" /></button>
    </div>
    `;
  }

  serverListDiv.innerHTML = serverListHtml;
}
