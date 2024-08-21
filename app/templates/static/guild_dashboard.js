let checkPeriod;
let checkPeriodLabel;

document.addEventListener("DOMContentLoaded", () => init());

function init() {
  checkPeriod = document.getElementById("checkPeriod");
  checkPeriod.addEventListener("input", () => {
    refreshForm();
  });

  checkPeriodLabel = document.getElementById("checkPeriodLabel");
  refreshForm();
}

function refreshForm() {
  checkPeriodLabel.innerText = checkPeriod.value + " min";
}
