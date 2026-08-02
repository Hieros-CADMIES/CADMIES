// ============================================================
// CADMIES — Main Application (v2)
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ---------- SPLASH SCREEN ----------
    const splash = document.getElementById('splash-overlay');
    const app = document.getElementById('app');

    setTimeout(() => {
        splash.classList.add('hidden');
        app.classList.remove('hidden');
    }, 4000);

    // ---------- SIDEBAR NAVIGATION ----------
    const navBtns = document.querySelectorAll('.nav-btn');
    const pages = {
        dashboard: document.getElementById('page-dashboard'),
        mistral: document.getElementById('page-mistral'),
        browse: document.getElementById('page-browse'),
        add: document.getElementById('page-add'),
        map: document.getElementById('page-map')
    };

    function showPage(pageId) {
        Object.values(pages).forEach(p => p.classList.remove('active'));
        if (pages[pageId]) pages[pageId].classList.add('active');
        navBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.page === pageId);
        });
        document.getElementById('main-content').scrollTop = 0;
    }

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            showPage(btn.dataset.page);
        });
    });

    document.querySelectorAll('[data-page]').forEach(el => {
        el.addEventListener('click', () => {
            const page = el.dataset.page;
            if (page && pages[page]) showPage(page);
        });
    });

    // ---------- CONCEPT DATA ----------
    let conceptsData = [];
    let domainCounts = {};
    let currentDashboardFilter = 'all';
    let dashboardSearchTerm = '';

    async function loadConcepts() {
        try {
            const res = await fetch('concepts.json');
            if (!res.ok) throw new Error('Failed to load concepts');
            const data = await res.json();

            if (data['@graph']) {
                conceptsData = data['@graph'];
            } else if (Array.isArray(data)) {
                conceptsData = data;
            } else {
                conceptsData = [data];
            }

            domainCounts = {};
            conceptsData.forEach(c => {
                const d = c.canonical_domain || c.domain || 'Unknown';
                domainCounts[d] = (domainCounts[d] || 0) + 1;
            });

            // Update stats
            document.getElementById('stat-concepts').textContent = conceptsData.length;
            document.getElementById('stat-domains').textContent = Object.keys(domainCounts).length;

            let relCount = 0;
            conceptsData.forEach(c => {
                if (c.relationships) {
                    Object.values(c.relationships).forEach(arr => {
                        if (Array.isArray(arr)) relCount += arr.length;
                    });
                }
            });
            document.getElementById('stat-relationships').textContent = relCount;

            document.getElementById('browse-count').textContent =
                `${conceptsData.length} concepts in the mycelium`;

            // Build domain filters (both Dashboard and Browse)
            const canonicalDomains = [
                "Physics", "Philosophy", "Biology", "Mathematics", "Consciousness",
                "Chemistry", "Ethics", "Computer Science", "Psychology", "Spirituality",
                "Neuroscience", "Sociology", "Economics", "Ecology", "Medicine"
            ];

            // Render both grids
            renderDashboardConcepts();
            renderBrowseConcepts();

            // Domain list for dropdown
            buildDomainList();

            // Check map status
            checkMapStatus();

        } catch (err) {
            console.error('Error loading concepts:', err);
            document.getElementById('browse-count').textContent = '❌ Failed to load concepts';
            document.getElementById('stat-concepts').textContent = '?';
            document.getElementById('stat-domains').textContent = '?';
            document.getElementById('stat-relationships').textContent = '?';
            document.getElementById('dashboard-grid').innerHTML =
                '<p class="error-text">Could not load concept data.</p>';
            document.getElementById('browse-grid').innerHTML =
                '<p class="error-text">Could not load concept data.</p>';
        }
    }

    // ---------- DOMAIN FILTERS ----------
    function buildDomainFilters(containerId, gridId, isDashboard) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = '';

        const allBtn = document.createElement('button');
        allBtn.className = 'filter-btn active';
        allBtn.dataset.filter = 'all';
        allBtn.textContent = `All (${conceptsData.length})`;
        allBtn.addEventListener('click', () => {
            container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            allBtn.classList.add('active');
            if (isDashboard) {
                currentDashboardFilter = 'all';
                renderDashboardConcepts();
            } else {
                renderBrowseConcepts('all');
            }
        });
        container.appendChild(allBtn);

        const sortedDomains = Object.keys(domainCounts).sort();
        sortedDomains.forEach(domain => {
            const btn = document.createElement('button');
            btn.className = 'filter-btn';
            btn.dataset.filter = domain;
            btn.textContent = `${domain} (${domainCounts[domain]})`;
            btn.addEventListener('click', () => {
                container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                if (isDashboard) {
                    currentDashboardFilter = domain;
                    renderDashboardConcepts();
                } else {
                    renderBrowseConcepts(domain);
                }
            });
            container.appendChild(btn);
        });
    }

    // ---------- DASHBOARD CONCEPTS ----------
    function renderDashboardConcepts() {
        const grid = document.getElementById('dashboard-grid');
        const search = document.getElementById('dashboard-search');
        const term = search ? search.value.toLowerCase().trim() : '';

        let filtered = conceptsData;
        if (currentDashboardFilter !== 'all') {
            filtered = filtered.filter(c =>
                (c.canonical_domain || c.domain) === currentDashboardFilter
            );
        }
        if (term) {
            filtered = filtered.filter(c => {
                const title = (c.name || c.title || '').toLowerCase();
                const def = (c.description || c.definition || '').toLowerCase();
                const id = (c.human_id || c.id || '').toLowerCase();
                return title.includes(term) || def.includes(term) || id.includes(term);
            });
        }

        if (filtered.length === 0) {
            grid.innerHTML = '<p class="empty-text">No concepts match your criteria.</p>';
            return;
        }

        let html = '';
        filtered.forEach(c => {
            const title = c.name || c.title || 'Untitled';
            const domain = c.canonical_domain || c.domain || 'Unknown';
            const def = c.description || c.definition || 'No definition available.';
            const id = c.human_id || c.id || '';

            html += `
                <div class="concept-card" data-id="${id}">
                    <h4>${escapeHtml(title)}</h4>
                    <div class="card-domain">${escapeHtml(domain)}</div>
                    <div class="card-definition">${escapeHtml(def.substring(0, 180))}${def.length > 180 ? '…' : ''}</div>
                </div>
            `;
        });

        grid.innerHTML = html;
        grid.querySelectorAll('.concept-card').forEach(card => {
            card.addEventListener('click', () => {
                const id = card.dataset.id;
                const concept = conceptsData.find(c => (c.human_id || c.id) === id);
                if (concept) openDetail(concept);
            });
        });
    }

    // ---------- BROWSE CONCEPTS ----------
    let browseFilter = 'all';
    let browseSearchTerm = '';

    function renderBrowseConcepts(filter, search) {
        filter = filter || browseFilter;
        search = (search !== undefined) ? search : browseSearchTerm;
        browseFilter = filter;
        browseSearchTerm = search;

        const grid = document.getElementById('browse-grid');
        let filtered = conceptsData;

        if (filter !== 'all') {
            filtered = filtered.filter(c =>
                (c.canonical_domain || c.domain) === filter
            );
        }
        if (search && search.trim()) {
            const term = search.toLowerCase().trim();
            filtered = filtered.filter(c => {
                const title = (c.name || c.title || '').toLowerCase();
                const def = (c.description || c.definition || '').toLowerCase();
                const id = (c.human_id || c.id || '').toLowerCase();
                return title.includes(term) || def.includes(term) || id.includes(term);
            });
        }

        if (filtered.length === 0) {
            grid.innerHTML = '<p class="empty-text">No concepts match your criteria.</p>';
            return;
        }

        let html = '';
        filtered.forEach(c => {
            const title = c.name || c.title || 'Untitled';
            const domain = c.canonical_domain || c.domain || 'Unknown';
            const def = c.description || c.definition || 'No definition available.';
            const id = c.human_id || c.id || '';

            html += `
                <div class="concept-card" data-id="${id}">
                    <h4>${escapeHtml(title)}</h4>
                    <div class="card-domain">${escapeHtml(domain)}</div>
                    <div class="card-definition">${escapeHtml(def.substring(0, 180))}${def.length > 180 ? '…' : ''}</div>
                </div>
            `;
        });

        grid.innerHTML = html;
        grid.querySelectorAll('.concept-card').forEach(card => {
            card.addEventListener('click', () => {
                const id = card.dataset.id;
                const concept = conceptsData.find(c => (c.human_id || c.id) === id);
                if (concept) openDetail(concept);
            });
        });
    }

    // ---------- SEARCH (Dashboard) ----------
    document.getElementById('dashboard-search').addEventListener('input', function() {
        renderDashboardConcepts();
    });

    // ---------- SEARCH (Browse) ----------
    document.getElementById('browse-search').addEventListener('input', function() {
        const search = this.value;
        const activeFilter = document.querySelector('#browse-filters .filter-btn.active');
        const filter = activeFilter ? activeFilter.dataset.filter : 'all';
        renderBrowseConcepts(filter, search);
    });

    // ---------- DETAIL MODAL ----------
    const modal = document.getElementById('detail-modal');
    const modalClose = document.querySelector('.modal-close');

    function openDetail(concept) {
        const title = concept.name || concept.title || 'Untitled';
        const domain = concept.canonical_domain || concept.domain || 'Unknown';
        const type = concept.type || 'Concept';
        const def = concept.description || concept.definition || 'No definition available.';
        const mantra = concept.mantra || '';
        const poetic = concept.poetic_version || '';
        const axioms = concept.axioms || [];
        const relationships = concept.relationships || {};
        const metadata = concept.metadata || {};
        const cid = concept.termCode || concept.cid || '';

        document.getElementById('detail-title').textContent = title;

        let badges = `
            <span style="background:#4F46E5;color:#fff;">${escapeHtml(domain)}</span>
            <span style="background:#6366F1;color:#fff;">${escapeHtml(type)}</span>
        `;
        document.getElementById('detail-badges').innerHTML = badges;
        document.getElementById('detail-definition').textContent = def;

        const mantraEl = document.getElementById('detail-mantra');
        if (mantra) {
            mantraEl.innerHTML = `<div class="detail-section"><h5>Mantra</h5><p><em>"${escapeHtml(mantra)}"</em></p></div>`;
        } else {
            mantraEl.innerHTML = '';
        }

        const poeticEl = document.getElementById('detail-poetic');
        if (poetic) {
            poeticEl.innerHTML = `<div class="detail-section"><h5>Poetic Version</h5><p><em>"${escapeHtml(poetic)}"</em></p></div>`;
        } else {
            poeticEl.innerHTML = '';
        }

        const axiomsEl = document.getElementById('detail-axioms');
        if (axioms && axioms.length > 0) {
            let list = axioms.map(a => `<li>${escapeHtml(a)}</li>`).join('');
            axiomsEl.innerHTML = `<div class="detail-section"><h5>Core Truths</h5><ul>${list}</ul></div>`;
        } else {
            axiomsEl.innerHTML = '';
        }

        const relEl = document.getElementById('detail-relationships');
        let relHtml = '';
        const relLabels = {
            builds_upon: 'Builds Upon',
            related_to: 'Related To',
            contradicts: 'Contradicts'
        };
        for (const [key, label] of Object.entries(relLabels)) {
            const items = relationships[key] || [];
            if (items.length > 0) {
                const list = items.map(i => `<li>${escapeHtml(i.title || i.id || i)}</li>`).join('');
                relHtml += `<div class="detail-section"><h5>${label}</h5><ul>${list}</ul></div>`;
            }
        }
        relEl.innerHTML = relHtml;

        const metaEl = document.getElementById('detail-metadata');
        let metaHtml = '';
        if (metadata.created) metaHtml += `<p><strong>Created:</strong> ${escapeHtml(metadata.created)}</p>`;
        if (metadata.creator) metaHtml += `<p><strong>Creator:</strong> ${escapeHtml(metadata.creator)}</p>`;
        if (metadata.certainty_score !== undefined) metaHtml += `<p><strong>Certainty:</strong> ${metadata.certainty_score}</p>`;
        if (metadata.license) metaHtml += `<p><strong>License:</strong> ${escapeHtml(metadata.license)}</p>`;
        if (metadata.genesis) metaHtml += `<p><strong>Genesis:</strong> ${escapeHtml(metadata.genesis)}</p>`;
        if (metaHtml) {
            metaEl.innerHTML = `<div class="detail-section"><h5>Metadata</h5>${metaHtml}</div>`;
        } else {
            metaEl.innerHTML = '';
        }

        const diffEl = document.getElementById('detail-difficulty');
        const diff = concept.difficulty_levels || {};
        let diffHtml = '';
        for (const [level, text] of Object.entries(diff)) {
            if (text) diffHtml += `<div class="detail-section"><h5>${level.charAt(0).toUpperCase() + level.slice(1)}</h5><p>${escapeHtml(text)}</p></div>`;
        }
        diffEl.innerHTML = diffHtml;

        document.getElementById('detail-cid').innerHTML = cid ?
            `<div class="detail-section"><h5>CID</h5><p style="font-family:monospace;font-size:12px;color:#64748B;word-break:break-all;">${escapeHtml(cid)}</p></div>` :
            '';

        modal.classList.remove('hidden');
    }

    modalClose.addEventListener('click', () => modal.classList.add('hidden'));
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });

    // ---------- DOMAIN DROPDOWN ----------
    function buildDomainList() {
        const container = document.getElementById('domain-list');
        if (!container) return;
        const sorted = Object.keys(domainCounts).sort();
        let html = '';
        sorted.forEach(d => {
            html += `<span class="domain-tag" data-domain="${d}">${d} <span class="count">(${domainCounts[d]})</span></span>`;
        });
        container.innerHTML = html;
        container.querySelectorAll('.domain-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const domain = tag.dataset.domain;
                // Navigate to Browse page with filter
                showPage('browse');
                // Set filter in Browse
                const browseFilters = document.getElementById('browse-filters');
                browseFilters.querySelectorAll('.filter-btn').forEach(b => {
                    b.classList.toggle('active', b.dataset.filter === domain);
                });
                renderBrowseConcepts(domain, '');
                // Close dropdown
                document.getElementById('domain-dropdown').classList.add('hidden');
            });
        });
    }

    // ---------- STAT CARDS ----------
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('click', function(e) {
            const stat = this.dataset.stat;

            if (stat === 'concepts') {
                showPage('browse');
                // Reset filters
                document.querySelectorAll('#browse-filters .filter-btn').forEach(b => {
                    b.classList.toggle('active', b.dataset.filter === 'all');
                });
                renderBrowseConcepts('all', '');
            }

            else if (stat === 'domains') {
                const dropdown = document.getElementById('domain-dropdown');
                dropdown.classList.toggle('hidden');
            }

            else if (stat === 'relationships') {
                document.getElementById('rel-modal').classList.remove('hidden');
            }

            else if (stat === 'license') {
                document.getElementById('license-display').classList.remove('hidden');
            }

            // ORCID is handled by the link inside the card
        });
    });

    // ---------- RELATIONSHIP MODAL ----------
    document.getElementById('rel-modal-btn').addEventListener('click', () => {
        document.getElementById('rel-modal').classList.add('hidden');
        showPage('map');
    });

    document.getElementById('rel-modal').addEventListener('click', function(e) {
        if (e.target === this) this.classList.add('hidden');
    });

    // ---------- LICENSE DISPLAY ----------
    document.getElementById('license-close').addEventListener('click', () => {
        document.getElementById('license-display').classList.add('hidden');
    });

    document.getElementById('license-display').addEventListener('click', function(e) {
        if (e.target === this) this.classList.add('hidden');
    });

    // ---------- MAP STATUS ----------
    async function checkMapStatus() {
        const statusEl = document.getElementById('map-status');
        try {
            const res = await fetch('mycelium_map.html', { method: 'HEAD' });
            if (res.ok) {
                statusEl.innerHTML = '<span class="status-dot online">●</span> Map file found — ready to launch';
            } else {
                statusEl.innerHTML = '<span class="status-dot offline">●</span> Map file not found. Run the map generator.';
            }
        } catch {
            statusEl.innerHTML = '<span class="status-dot offline">●</span> Map file not found. Run the map generator.';
        }
    }

    document.getElementById('map-launch').addEventListener('click', () => {
        window.open('mycelium_map.html', '_blank');
    });

    // ---------- ADD CONCEPT ----------
    document.getElementById('add-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const concept = {
            human_id: document.getElementById('add-human-id').value.trim(),
            title: document.getElementById('add-title').value.trim(),
            definition: document.getElementById('add-definition').value.trim(),
            domain: document.getElementById('add-domain').value,
            type: document.getElementById('add-type').value,
            mantra: document.getElementById('add-mantra').value.trim(),
            poetic_version: document.getElementById('add-poetic').value.trim(),
            axioms: document.getElementById('add-axioms').value.split('\n').filter(s => s.trim()),
            genesis: document.getElementById('add-genesis').value.trim(),
            builds_upon: document.getElementById('add-builds').value.split(',').filter(s => s.trim()),
            related_to: document.getElementById('add-related').value.split(',').filter(s => s.trim()),
            contradicts: document.getElementById('add-contradicts').value.split(',').filter(s => s.trim()),
            beginner: document.getElementById('add-beginner').value.trim(),
            intermediate: document.getElementById('add-intermediate').value.trim(),
            expert: document.getElementById('add-expert').value.trim(),
        };

        if (!concept.human_id || !concept.title || !concept.definition) {
            showResult('Please fill in Human ID, Title, and Definition.', 'error');
            return;
        }

        concept.human_id = concept.human_id.toLowerCase().replace(/[^a-z0-9_]/g, '_');
        showResult(`✅ Concept "${concept.title}" (${concept.human_id}) ready for submission.`, 'success');
        console.log('Concept data:', concept);
    });

    document.getElementById('add-form').addEventListener('reset', function() {
        document.getElementById('add-result').classList.add('hidden');
    });

    function showResult(message, type) {
        const el = document.getElementById('add-result');
        el.textContent = message;
        el.className = type === 'error' ? 'error' : '';
        el.classList.remove('hidden');
    }

    // ---------- CHAT ----------
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatDisplay = document.getElementById('chat-display');
    const chatStatus = document.getElementById('chat-status');

    function addChatMessage(role, text) {
        const div = document.createElement('div');
        div.className = `chat-message ${role}`;
        const label = role === 'user' ? 'You:' : 'Dr. Mistral:';
        div.innerHTML = `<span class="msg-label">${label}</span><span class="msg-text">${escapeHtml(text)}</span>`;
        chatDisplay.appendChild(div);
        chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }

    async function sendChatMessage() {
        const query = chatInput.value.trim();
        if (!query) return;
        chatInput.value = '';
        addChatMessage('user', query);

        const thinkingDiv = document.createElement('div');
        thinkingDiv.className = 'chat-message assistant';
        thinkingDiv.innerHTML = `<span class="msg-label">Dr. Mistral:</span><span class="msg-text"><em>Thinking...</em></span>`;
        chatDisplay.appendChild(thinkingDiv);
        chatDisplay.scrollTop = chatDisplay.scrollHeight;

        chatSend.disabled = true;
        chatStatus.textContent = '⏳ Connecting to Dr. Mistral...';
        chatStatus.style.color = '#F59E0B';

        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            const responses = [
                "Bonjour, mon ami! That's a fascinating question. Let me consult the library for you...",
                "Ah, c'est une bonne question! The mycelium has knowledge on this. Let me think...",
                "Here's what the mycelium knows about that. The connections are subtle but profound.",
                "I recall something from the stacks. The librarian Willie would know this one too.",
            ];
            const reply = responses[Math.floor(Math.random() * responses.length)];
            thinkingDiv.innerHTML = `<span class="msg-label">Dr. Mistral:</span><span class="msg-text">${escapeHtml(reply)}</span>`;
            chatStatus.textContent = '🟢 Connected to Dr. Mistral';
            chatStatus.style.color = '#10B981';
            if (window.chirp) window.chirp();
        } catch (err) {
            thinkingDiv.innerHTML = `<span class="msg-label">Dr. Mistral:</span><span class="msg-text"><em>Désolé, mon ami. I'm having trouble connecting. Please try again.</em></span>`;
            chatStatus.textContent = '🔴 Connection error';
            chatStatus.style.color = '#EF4444';
            console.error('Chat error:', err);
        }
        chatSend.disabled = false;
    }

    chatSend.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

    // ---------- UTILITY ----------
    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    window.chirp = function() {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            for (let i = 0; i < 5; i++) {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.frequency.value = 800 + i * 200;
                gain.gain.value = 0.08;
                osc.start(ctx.currentTime + i * 0.08);
                osc.stop(ctx.currentTime + i * 0.08 + 0.05);
            }
        } catch (e) {}
    };

    // ---------- INIT ----------
    loadConcepts();

});
