/**
 * StadiumIQ — Stadium Map JavaScript
 * Interactive Leaflet.js stadium navigator
 */

let map;
let markers = [];
let currentStadiumId = 1;

// Category icons and colors
const categoryConfig = {
    food: { emoji: '🍔', color: '#06d6a0' },
    restroom: { emoji: '🚻', color: '#3a86ff' },
    exit: { emoji: '🚪', color: '#f72585' },
    medical: { emoji: '🏥', color: '#ff6b35' },
    merch: { emoji: '🛍️', color: '#d4af37' },
    accessibility: { emoji: '♿', color: '#7c3aed' },
    info: { emoji: 'ℹ️', color: '#4cc9f0' },
    other: { emoji: '📍', color: '#94a3b8' }
};

document.addEventListener('DOMContentLoaded', () => {
    initMap();
    setupFilters();
    setupStadiumSelector();
});

function initMap() {
    const selector = document.getElementById('stadium-selector');
    const option = selector.options[selector.selectedIndex];
    const lat = parseFloat(option.dataset.lat) || 40.8128;
    const lng = parseFloat(option.dataset.lng) || -74.0742;

    map = L.map('stadium-map', {
        zoomControl: true,
        scrollWheelZoom: true,
    }).setView([lat, lng], 16);

    // Dark map tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap © CARTO',
        maxZoom: 20,
    }).addTo(map);

    // Load initial stadium POIs
    loadPOIs(1);
}

function setupStadiumSelector() {
    const selector = document.getElementById('stadium-selector');
    selector.addEventListener('change', () => {
        const option = selector.options[selector.selectedIndex];
        const lat = parseFloat(option.dataset.lat);
        const lng = parseFloat(option.dataset.lng);
        const stadiumId = parseInt(selector.value);

        currentStadiumId = stadiumId;
        map.setView([lat, lng], 16, { animate: true });
        loadPOIs(stadiumId);
    });
}

function setupFilters() {
    const filters = document.querySelectorAll('.poi-filter');
    filters.forEach(btn => {
        btn.addEventListener('click', () => {
            filters.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const category = btn.dataset.category;
            filterMarkers(category);
        });
    });
}

async function loadPOIs(stadiumId) {
    try {
        const res = await fetch(`/api/stadium/${stadiumId}/pois`);
        const data = await res.json();
        const pois = data.pois;

        // Clear existing markers
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        // Add markers
        pois.forEach(poi => {
            const config = categoryConfig[poi.category] || categoryConfig.other;

            const icon = L.divIcon({
                html: `<div style="
                    background:${config.color};
                    width:32px;height:32px;
                    border-radius:8px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:16px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.3);
                    border:2px solid rgba(255,255,255,0.3);
                ">${config.emoji}</div>`,
                className: 'custom-marker',
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -20],
            });

            const marker = L.marker([poi.latitude, poi.longitude], { icon })
                .addTo(map)
                .bindPopup(`
                    <div style="font-family:Inter,sans-serif;min-width:200px;padding:4px">
                        <strong style="font-size:14px">${config.emoji} ${poi.name}</strong>
                        <p style="font-size:12px;color:#666;margin:6px 0">${poi.description}</p>
                        <div style="font-size:11px;color:#999">
                            📍 ${poi.floor} ${poi.is_accessible ? '| ♿ Accessible' : ''}
                        </div>
                    </div>
                `);

            marker._category = poi.category;
            markers.push(marker);
        });

        // Update POI list
        updatePOIList(pois);

    } catch (err) {
        console.error('Failed to load POIs:', err);
    }
}

function filterMarkers(category) {
    markers.forEach(marker => {
        if (category === 'all' || marker._category === category) {
            marker.setOpacity(1);
        } else {
            marker.setOpacity(0.15);
        }
    });

    // Also filter the list
    const items = document.querySelectorAll('.poi-item');
    items.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}

function updatePOIList(pois) {
    const list = document.getElementById('poi-list');
    list.innerHTML = '';

    pois.forEach(poi => {
        const config = categoryConfig[poi.category] || categoryConfig.other;
        const item = document.createElement('div');
        item.className = 'poi-item';
        item.dataset.category = poi.category;
        item.innerHTML = `
            <div class="poi-icon" style="background:${config.color}20;color:${config.color}">${config.emoji}</div>
            <div class="poi-info">
                <h4>${poi.name}</h4>
                <p>${poi.floor} ${poi.is_accessible ? '· ♿' : ''}</p>
            </div>
        `;

        item.addEventListener('click', () => {
            map.setView([poi.latitude, poi.longitude], 18, { animate: true });
            // Find and open the marker popup
            markers.forEach(m => {
                if (Math.abs(m.getLatLng().lat - poi.latitude) < 0.0001 &&
                    Math.abs(m.getLatLng().lng - poi.longitude) < 0.0001) {
                    m.openPopup();
                }
            });
        });

        list.appendChild(item);
    });

    lucide.createIcons();
}

async function getNavigation() {
    const destination = document.getElementById('nav-destination').value || 'nearest food court';
    const resultEl = document.getElementById('nav-result');
    const btn = document.getElementById('nav-btn');

    btn.innerHTML = '<div class="spinner" style="width:14px;height:14px;border-width:2px"></div> Finding...';

    try {
        const res = await fetch('/api/stadium/navigate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                destination,
                current_location: 'main entrance',
                stadium_id: currentStadiumId,
            })
        });
        const data = await res.json();
        resultEl.textContent = data.recommendation;
        resultEl.classList.add('active');
    } catch (err) {
        resultEl.textContent = 'Unable to get directions. Please try again.';
        resultEl.classList.add('active');
    }

    btn.innerHTML = '<i data-lucide="navigation" style="width:14px;height:14px"></i> Get Directions';
    lucide.createIcons();
}
