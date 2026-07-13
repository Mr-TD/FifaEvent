/**
 * StadiumIQ — Schedule JavaScript
 * Match filtering and AI previews
 */

document.addEventListener('DOMContentLoaded', () => {
    setupFilters();
});

function setupFilters() {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;
            const cards = document.querySelectorAll('.schedule-match-card');

            cards.forEach(card => {
                const stage = card.dataset.stage;
                const status = card.dataset.status;

                if (filter === 'all') {
                    card.style.display = '';
                } else if (filter === 'completed' || filter === 'scheduled' || filter === 'live') {
                    card.style.display = (status === filter) ? '' : 'none';
                } else {
                    card.style.display = (stage === filter) ? '' : 'none';
                }
            });
        });
    });
}

async function loadPreview(matchId) {
    const container = document.getElementById(`preview-${matchId}`);
    const spinner = document.getElementById(`preview-spinner-${matchId}`);
    const btn = document.getElementById(`preview-btn-${matchId}`);

    // Toggle if already loaded
    if (container.classList.contains('active') && !spinner) {
        container.classList.remove('active');
        return;
    }

    container.classList.add('active');
    container.innerHTML = '<div class="spinner" style="margin:8px auto"></div>';

    try {
        const res = await fetch(`/api/match/${matchId}/preview`);
        const data = await res.json();
        container.textContent = data.preview;
    } catch (err) {
        container.textContent = 'Unable to load preview. Please try again.';
    }

    btn.innerHTML = '<i data-lucide="sparkles" style="width:14px;height:14px"></i> Hide Preview';
    lucide.createIcons();
}
