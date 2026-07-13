/**
 * StadiumIQ — Crowd Dashboard JavaScript
 * Real-time crowd analytics with Chart.js
 */

let densityChart = null;
let historyChart = null;

const chartColors = [
    '#7c3aed', '#06d6a0', '#d4af37', '#f72585', '#4cc9f0',
    '#ff6b35', '#8338ec', '#3a86ff', '#fb5607', '#06d6a0'
];

document.addEventListener('DOMContentLoaded', () => {
    loadCrowdData();
    loadHistoryData();
    loadRecommendations();

    // Stadium selector
    const selector = document.getElementById('crowd-stadium-select');
    if (selector) {
        selector.addEventListener('change', () => {
            loadCrowdData();
            loadHistoryData();
            loadRecommendations();
        });
    }

    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadCrowdData();
        loadHistoryData();
    }, 30000);
});

async function loadCrowdData() {
    const stadiumId = document.getElementById('crowd-stadium-select').value;
    try {
        const res = await fetch(`/api/crowd/data?stadium_id=${stadiumId}`);
        const data = await res.json();

        // Update overall density
        const densityValue = document.getElementById('density-value');
        const totalPeople = document.getElementById('total-people');
        const densityRing = document.getElementById('density-ring');

        densityValue.textContent = data.overall_density;
        totalPeople.textContent = `${data.total_people.toLocaleString()} fans in stadium`;

        // Color the ring based on density
        let ringColor = 'var(--accent-cyan)';
        if (data.overall_density > 85) ringColor = 'var(--accent-pink)';
        else if (data.overall_density > 70) ringColor = 'var(--accent-gold)';

        densityRing.style.background = `conic-gradient(${ringColor} ${data.overall_density * 3.6}deg, rgba(255,255,255,0.05) 0deg)`;

        // Update zone cards
        updateZoneCards(data.zones);

        // Update bar chart
        updateDensityChart(data.zones);

    } catch (err) {
        console.error('Failed to load crowd data:', err);
    }
}

function updateZoneCards(zones) {
    const grid = document.getElementById('zones-grid');
    grid.innerHTML = '';

    zones.forEach((zone, i) => {
        const card = document.createElement('div');
        card.className = `glass-card zone-card zone-alert-${zone.alert_level}`;
        card.innerHTML = `
            <div class="zone-density">${zone.density}%</div>
            <div class="zone-name">${zone.zone}</div>
            <div class="zone-people">${zone.people_count.toLocaleString()} people</div>
            <div class="zone-bar">
                <div class="zone-bar-fill" style="width:${zone.density}%;background:${zone.color}"></div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function updateDensityChart(zones) {
    const ctx = document.getElementById('density-bar-chart');
    if (!ctx) return;

    const labels = zones.map(z => z.zone);
    const values = zones.map(z => z.density);
    const colors = zones.map(z => z.color);

    if (densityChart) {
        densityChart.data.labels = labels;
        densityChart.data.datasets[0].data = values;
        densityChart.data.datasets[0].backgroundColor = colors.map(c => c + '80');
        densityChart.data.datasets[0].borderColor = colors;
        densityChart.update('none');
    } else {
        densityChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Density %',
                    data: values,
                    backgroundColor: colors.map(c => c + '80'),
                    borderColor: colors,
                    borderWidth: 1,
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { color: '#94a3b8' },
                        grid: { color: 'rgba(255,255,255,0.05)' },
                    },
                    x: {
                        ticks: { color: '#94a3b8', font: { size: 10 }, maxRotation: 45 },
                        grid: { display: false },
                    }
                }
            }
        });
    }
}

async function loadHistoryData() {
    try {
        const res = await fetch('/api/crowd/history');
        const data = await res.json();
        const history = data.history;

        const ctx = document.getElementById('history-line-chart');
        if (!ctx) return;

        const labels = history.map(h => h.hour);
        const values = history.map(h => h.density);

        if (historyChart) {
            historyChart.data.labels = labels;
            historyChart.data.datasets[0].data = values;
            historyChart.update('none');
        } else {
            historyChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels,
                    datasets: [{
                        label: 'Crowd Density %',
                        data: values,
                        borderColor: '#7c3aed',
                        backgroundColor: 'rgba(124, 58, 237, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 3,
                        pointBackgroundColor: '#7c3aed',
                        pointBorderColor: '#a78bfa',
                        pointHoverRadius: 6,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: { color: '#94a3b8' },
                            grid: { color: 'rgba(255,255,255,0.05)' },
                        },
                        x: {
                            ticks: { color: '#94a3b8', font: { size: 10 }, maxRotation: 45 },
                            grid: { display: false },
                        }
                    }
                }
            });
        }
    } catch (err) {
        console.error('Failed to load history:', err);
    }
}

async function loadRecommendations() {
    const stadiumId = document.getElementById('crowd-stadium-select').value;
    const recText = document.getElementById('ai-rec-text');
    recText.innerHTML = '<div class="spinner" style="margin:8px 0"></div>';

    try {
        const res = await fetch(`/api/crowd/recommendations?stadium_id=${stadiumId}`);
        const data = await res.json();
        recText.textContent = data.recommendation;
    } catch (err) {
        recText.textContent = 'Unable to load recommendations.';
    }
}
