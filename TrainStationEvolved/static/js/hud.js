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
btnMaterials = document.getElementById("btnMats");

btnTrains.addEventListener("click", () => {
    loadScreen("/page/trains");
})
btnShop.addEventListener("click", () => {
    loadScreen("/page/shop");
})
btnWarehouse.addEventListener("click", () => {
    loadScreen("/page/warehouse");
})
btnMaterials.addEventListener("click", ()=>{
    loadScreen("/hud/tool/materials")
})

function updateXP(level, xp, xpNeeded) {
    document.getElementById("levelnumber").textContent = level
    const bar = document.getElementById("progressLevel");
    bar.max = xpNeeded;
    bar.value = xp;
}
function toggleScreen(tipo) {
    screenTrains = document.getElementById("trains");
    screenCargoWagons = document.getElementById("cargowagons");
    screenPassWagons = document.getElementById("passwagons");
    screenRawMats = document.getElementById("rawmats");
    screenFacMats = document.getElementById("facmats");

    if (tipo == "train") {
        screenTrains.classList.remove("hidden");
        screenCargoWagons.classList.add("hidden");
        screenPassWagons.classList.add("hidden");
    } else if (tipo == "cargo") {
        screenTrains.classList.add("hidden");
        screenCargoWagons.classList.remove("hidden");
        screenPassWagons.classList.add("hidden");
    } else if (tipo == "pass")  {
        screenTrains.classList.add("hidden");
        screenCargoWagons.classList.add("hidden");
        screenPassWagons.classList.remove("hidden");
    } else if (tipo == "raw")  {
        screenFacMats.classList.add("hidden");
        screenRawMats.classList.remove("hidden");
    } else if (tipo == "fac")  {
        screenRawMats.classList.add("hidden");
        screenFacMats.classList.remove("hidden");
    }
}