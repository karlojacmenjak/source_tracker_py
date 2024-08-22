let checkPeriodRange;
let checkPeriodLabel;
let serverListDiv;
let serverList;

document.addEventListener("DOMContentLoaded", () => init());

function init() {
  checkPeriodRange = document.getElementById("checkPeriod");
  checkPeriodRange.addEventListener("input", () => {
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
    let server = txtServerData.value.trim();

    try {
      parseGameServerInput(server);
      serverList.push(server);
      txtServerData.value = "";
      refreshForm();
    } catch (error) {
      alert(error.message);
    }
  });

  let btnSave = document.getElementById("btnSave");
  btnSave.addEventListener("click", async () => {
    try {
      await saveData();
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
  if(!regFull.test(data)) {
    throw new Error("Invalid format for game server. Expected format is address:PORT. Actual value: " + data);
  }
  let result = data.split(":");

  let address = result[0].trim();
  let port = result[1].trim();

  let regDomain = /[a-zA-Z0-9\-\_]+(\.[a-zA-Z0-9\-\_]+)*/gm;
  let regaddress4 = /\d+\.\d+\.\d+\.\d+/gm;

  if (!address.match(regDomain) && !address.match(regaddress4)) {
    throw new Error("Invalid format for game server address. Expected value is either domain or addressv4 address. Actual value: " + data);
  }

  return { address: address, port: port };
}

function refreshForm() {
  checkPeriodLabel.innerText = checkPeriodRange.value + " min";

  serverListDiv.innerHTML = "";

  for (let i = 0; i < serverList.length; i++) {
    let divListItem = document.createElement("div");
    divListItem.className = "list-item";

    let input = document.createElement("input");
    input.type = "text";
    input.spellcheck = "false";
    input.placeholder = "address:port";
    input.value = serverList[i];
    input.addEventListener("input", () => {
      serverList[i] = input.value;
    });

    let btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn-icon";
    btn.innerHTML = '<img src="/static/icon-xmark.png"/>';
    btn.addEventListener("click", () => removeServerItem(i));

    divListItem.append(input);
    divListItem.append(btn);

    serverListDiv.append(divListItem);
  }
}

async function saveData() {
  let rbStatusEnabled = document.getElementById("statusEnabled");

  let botEnabled = rbStatusEnabled.checked;
  let checkPeriod = checkPeriodRange.value;
  let servers = [];

  for (let i = 0; i < serverList.length; i++) {
    servers.push(parseGameServerInput(serverList[i].trim()));
  }

  let body = {
    enable_features: botEnabled,
    check_period: checkPeriod,
    game_server_list: servers,
  };

  await postData(body);
}

async function postData(data) {
  let headers = new Headers();
  headers.set("Content-Type", "application/json");

  let guildId = document.querySelector("meta[data-guild-id]").getAttribute("data-guild-id");
  let url = "/v1/dashboard/" + guildId + "/settings";

  await fetch(url, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(data),
    headers: headers,
  });
}
