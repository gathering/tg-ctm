
async function startWannabeSync() {
    document.getElementById("loading-gif").style.display = "block";
    const response = await fetch('/api/sync');
    const data = await response.json();
    return data;
}

async function triggerWannabeSync() {
    await startWannabeSync().then(data => {
        document.getElementById("loading-gif").style.display = "none";
        document.getElementById("sync-stats").style.display = "block";
        document.getElementById("new_users").innerHTML = data['new_users']
        document.getElementById("new_crews").innerHTML = data['new_crews']
    });
}
