const API_BASE = '/api';
let powerChart = null;

async function fetchMachines() {
  const res = await fetch(`${API_BASE}/machines`);
  const data = await res.json();
  const sel = document.getElementById('machineSelect');
  sel.innerHTML = '<option value="">All</option>';
  data.forEach(m => {
    const opt = document.createElement('option');
    opt.value = m.machine_id;
    opt.textContent = `${m.name} (${m.location || 'NA'})`;
    sel.appendChild(opt);
  });
  return data;
}

async function fetchLatest() {
  const res = await fetch(`${API_BASE}/readings/latest`);
  return await res.json();
}

async function fetchAlerts() {
  const res = await fetch(`${API_BASE}/alerts`);
  return await res.json();
}

function renderLatestTable(rows) {
  const tbody = document.querySelector('#latestTable tbody');
  tbody.innerHTML = '';
  rows.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${r.name}</td><td>${r.voltage.toFixed(1)}</td><td>${r.current.toFixed(2)}</td><td>${r.power.toFixed(1)}</td><td>${r.energy_kwh.toFixed(4)}</td><td>${new Date(r.timestamp).toLocaleString()}</td>`;
    tbody.appendChild(tr);
  });
}

function renderAlerts(alerts) {
  const ul = document.getElementById('alertsList');
  ul.innerHTML = '';
  alerts.forEach(a => {
    const li = document.createElement('li');
    li.textContent = `[${new Date(a.alert_time).toLocaleString()}] Machine ${a.machine_id}: ${a.message}`;
    ul.appendChild(li);
  });
}

function initChart() {
  const ctx = document.getElementById('powerChart').getContext('2d');
  powerChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: []
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Power (W)' } },
        x: { title: { display: true, text: 'Time' } }
      }
    }
  });
}

function updateChartWithLatest(rows) {
  const labels = rows.map(r => new Date(r.timestamp).toLocaleTimeString());
  // if multiple machines, create dataset per machine
  powerChart.data.labels = labels;
  powerChart.data.datasets = rows.map((r, idx) => ({
    label: r.name,
    data: [r.power], // for simple dashboard we just use single value; can be extended to moving window
    fill: false,
  }));
  powerChart.update();
}

async function refreshAll() {
  const latest = await fetchLatest();
  renderLatestTable(latest);
  renderAlerts(await fetchAlerts());
  if (!powerChart) initChart();
  updateChartWithLatest(latest);
}

document.getElementById && (async () => {
  await fetchMachines();
  await refreshAll();
  document.getElementById('refreshBtn').addEventListener('click', refreshAll);
  setInterval(refreshAll, 10000); // auto-refresh every 10s
})();
