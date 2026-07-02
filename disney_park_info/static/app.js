const select = document.getElementById("park-select");
const summary = document.getElementById("summary");
const ridesList = document.getElementById("rides");
const errorEl = document.getElementById("error");

select.addEventListener("change", async () => {
  const parkKey = select.value;
  summary.textContent = "";
  ridesList.innerHTML = "";
  errorEl.textContent = "";

  if (!parkKey) {
    return;
  }

  const response = await fetch(`/api/status/${parkKey}`);
  const data = await response.json();

  if (!response.ok) {
    errorEl.textContent = data.error || "Failed to load park status.";
    return;
  }

  summary.textContent =
    `${data.park.name}: Open ${data.open_count} / Closed ${data.closed_count} ` +
    `- Average wait ${data.average_wait} min`;

  const maxWait = data.rides.reduce((max, ride) => Math.max(max, ride.wait_time), 0);

  for (const ride of data.rides) {
    const li = document.createElement("li");

    const waitEl = document.createElement("span");
    waitEl.className = "wait-time";
    waitEl.textContent = `${ride.wait_time} min`;

    const barEl = document.createElement("span");
    barEl.className = "bar";
    const widthPercent = maxWait ? Math.round((ride.wait_time / maxWait) * 100) : 0;
    barEl.style.width = `${widthPercent}%`;

    const nameEl = document.createElement("span");
    nameEl.textContent = ride.name;

    li.append(waitEl, barEl, nameEl);
    ridesList.appendChild(li);
  }
});
