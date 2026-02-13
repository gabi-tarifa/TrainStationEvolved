function buyItem(type, id) {
    fetch("/api/shop/buy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type, id })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) return

        updateGold(data.new_gold)
        updateXP(data.level, data.xp, data.xp_needed)

        if (data.leveled_up) {
            showLevelUp(data.levels_gained)
        }
    })
}
function updateGold(newGold) {
    document.getElementById("btnGold").textContent = newGold
    currentGold = document.getElementById("btnGold").textContent;
    document.querySelectorAll(".btnBuy").forEach(btn => {
        const price = parseInt(btn.dataset.price)

        if (currentGold < price) {
            btn.disabled = true
            btn.classList.add("disabled")
        } else {
            btn.disabled = false
            btn.classList.remove("disabled")
        }
    })
}
