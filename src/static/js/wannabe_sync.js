async function syncWannabe() {
  const loadingIndicator = document.getElementById("loading-indicator");

  const syncStats = document.getElementById("sync-stats");
  const statNewUsers = document.getElementById("stat-new-users");
  const statUpdatedUsers = document.getElementById("stat-updated-users");
  const statNewCrews = document.getElementById("stat-new-crews");
  const statUpdatedCrews = document.getElementById("stat-updated-crews");
  const statDeletedUsers = document.getElementById("stat-deleted-users");

  const errorBlock = document.getElementById("error-block");
  const errorMessage = document.getElementById("error-message");

  loadingIndicator.classList.remove("hidden");
  // add hidden classes again if user clicks the button multiple times
  syncStats.classList.add("hidden");
  errorBlock.classList.add("hidden");

  const response = await fetch("sync_start");
  if (response.ok) {
    const data = await response.json();
    statNewUsers.textContent = data.new_users;
    statUpdatedUsers.textContent = data.updated_users;
    statNewCrews.textContent = data.new_crews;
    statUpdatedCrews.textContent = data.updated_crews;
    statDeletedUsers.textContent = data.deleted_users;
    syncStats.classList.remove("hidden");
  } else {
    if (response.status === 500) errorMessage.textContent = "Noe gikk galt på serveren.";
    else try {
      const errorData = await response.json();
      errorMessage.textContent = errorData.message || "En feil oppsto.";
    } catch {
      errorMessage.textContent = "En ukjent feil oppsto.";
    }
    errorBlock.classList.remove("hidden");
  }

  loadingIndicator.classList.add("hidden");
}
