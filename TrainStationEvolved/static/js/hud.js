async function loadScreen(route){
    const res = await fetch(route);
    const html = await res.text();

    root = document.getElementById("modal-root");
    root.innerHTML = html;
}

async function closeTab() {
    root = document.getElementById("modal-root");
    root.innerHTML = "";
}

btnTrains = document.getElementById("btnTrains");
btnShop = document.getElementById("btnShop");
btnWarehouse = document.getElementById("btnWarehouse");
btnAchievements = document.getElementById("btnAchievements");
btnContracts = document.getElementById("btnContracts");

btnTrains.addEventListener("click", () => {
    loadScreen("/page/trains");
})