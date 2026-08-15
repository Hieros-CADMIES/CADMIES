// ============================================================
// CADMIES — Main Application (v4)
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ---------- SPLASH SCREEN ----------
    const splash = document.getElementById('splash-overlay');
    const app = document.getElementById('app');

    setTimeout(() => {
        splash.classList.add('hidden');
        app.classList.remove('hidden');
    }, 4000);

    // ---------- NAVIGATION ----------
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
        window.scrollTo(0, 0);
    }

    document.querySelectorAll('[data-page]').forEach(el => {
        el.addEventListener('click', () => {
            const page = el.dataset.page;
            if (page && pages[page]) showPage(page);
        });
    });

    // ---------- CONCEPT DATA ----------
    let conceptsData = [];
    let domainCounts = {};
    let browseFilter = 'all';
    let browseSearchTerm = '';

    // CANONICAL 15 DOMAINS
    const canonicalDomains = [
        "Physics", "Philosophy", "Biology", "Mathematics", "Consciousness",
        "Chemistry", "Ethics", "Computer Science", "Psychology", "Spirituality",
        "Neuroscience", "Sociology", "Economics", "Ecology", "Medicine"
    ];

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

            // Build domain filters
            buildDomainFilters('browse-filters', 'browse-grid');

            // Render Browse grid
            renderBrowseConcepts();

            // Build domain list for dropdown
            buildDomainList();

            // Check map status
            checkMapStatus();

        } catch (err) {
            console.error('Error loading concepts:', err);
            document.getElementById('browse-count').textContent = 'Failed to load concepts';
            document.getElementById('stat-concepts').textContent = '?';
            document.getElementById('stat-domains').textContent = '?';
            document.getElementById('stat-relationships').textContent = '?';
            document.getElementById('browse-grid').innerHTML =
                '<p class="empty-text">Could not load concept data.</p>';
        }
    }

    // ---------- DOMAIN FILTERS ----------
    function buildDomainFilters(containerId, gridId) {
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
            renderBrowseConcepts('all');
        });
        container.appendChild(allBtn);

        const existingCanonical = canonicalDomains.filter(d => domainCounts[d] > 0);

        existingCanonical.forEach(domain => {
            const btn = document.createElement('button');
            btn.className = 'filter-btn';
            btn.dataset.filter = domain;
            btn.textContent = `${domain} (${domainCounts[domain]})`;
            btn.addEventListener('click', () => {
                container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderBrowseConcepts(domain);
            });
            container.appendChild(btn);
        });
    }

    // ---------- BROWSE CONCEPTS (Expandable Cards) ----------
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
            const rawDomain = c.domain || domain;
            const def = c.description || c.definition || 'No definition available.';
            const id = c.human_id || c.id || '';
            const cid = c.termCode || c.cid || '';

            // Relationships
            const rels = c.relationships || {};
            const relLabels = {
                builds_upon: 'Builds Upon',
                related_to: 'Related To',
                specializes: 'Specializes',
                contradicts: 'Contradicts'
            };
            let relHtml = '';
            for (const [key, label] of Object.entries(relLabels)) {
                const items = rels[key] || [];
                if (items.length > 0) {
                    const tags = items.map(item => {
                        const relTitle = item.title || item.id || item;
                        return `<span class="rel-tag rel-${key}">${escapeHtml(relTitle)}</span>`;
                    }).join('');
                    relHtml += `<div class="rel-group"><strong>${label}:</strong> ${tags}</div>`;
                }
            }

            // Extras
            let extrasHtml = '';
            if (c.extra) {
                if (c.extra.insight) {
                    extrasHtml += `<div class="extra-section"><strong>Core Insight:</strong> ${escapeHtml(c.extra.insight)}</div>`;
                }
                if (c.extra.poetic_version) {
                    extrasHtml += `<div class="extra-section poetic"><strong>Poetic Version:</strong><blockquote>${escapeHtml(c.extra.poetic_version)}</blockquote></div>`;
                }
                if (c.extra.mantra) {
                    extrasHtml += `<div class="extra-section mantra"><strong>Mantra:</strong> <em>"${escapeHtml(c.extra.mantra)}"</em></div>`;
                }
            }

            // Preview (first ~180 chars)
            const preview = def.substring(0, 180) + (def.length > 180 ? '…' : '');

            html += `
                <article class="concept-card" data-domain="${escapeHtml(domain)}" data-raw-domain="${escapeHtml(rawDomain)}" data-search="${escapeHtml(title.toLowerCase())} ${escapeHtml(domain.toLowerCase())} ${escapeHtml(id.toLowerCase())}">
                    <div class="card-header" onclick="this.parentElement.classList.toggle('expanded')">
                        <span class="domain-badge">${escapeHtml(domain)}</span>
                        <h4>${escapeHtml(title)}</h4>
                        <p class="definition-preview">${escapeHtml(preview)}</p>
                        <span class="expand-hint">Click to expand ↓</span>
                    </div>
                    <div class="card-detail">
                        <div class="definition-full">
                            <p>${escapeHtml(def)}</p>
                        </div>
                        ${extrasHtml}
                        <div class="relationships">
                            <h5>Relationships</h5>
                            ${relHtml || '<p class="no-rels">No relationships recorded yet.</p>'}
                        </div>
                        ${cid ? `<div class="cid-box"><strong>Permanent CID:</strong><br><code>${escapeHtml(cid)}</code></div>` : ''}
                    </div>
                </article>
            `;
        });

        grid.innerHTML = html;

        // === TRANSLATE.JS FIX: Retranslate newly injected concept cards ===
        if (typeof translate !== 'undefined') {
            setTimeout(function() {
                translate.execute();
            }, 100);
        }
    }

    // ---------- SEARCH (Browse) ----------
    document.getElementById('browse-search').addEventListener('input', function() {
        const search = this.value;
        const activeFilter = document.querySelector('#browse-filters .filter-btn.active');
        const filter = activeFilter ? activeFilter.dataset.filter : 'all';
        renderBrowseConcepts(filter, search);
    });

    // ---------- DOMAIN DROPDOWN ----------
    function buildDomainList() {
        const container = document.getElementById('domain-list');
        if (!container) return;

        const existingCanonical = canonicalDomains.filter(d => domainCounts[d] > 0);

        let html = '';
        existingCanonical.forEach(d => {
            html += `<span class="domain-tag" data-domain="${d}">${d} <span class="count">(${domainCounts[d]})</span></span>`;
        });
        container.innerHTML = html;

        container.querySelectorAll('.domain-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const domain = tag.dataset.domain;
                showPage('browse');
                const browseFilters = document.getElementById('browse-filters');
                browseFilters.querySelectorAll('.filter-btn').forEach(b => {
                    b.classList.toggle('active', b.dataset.filter === domain);
                });
                renderBrowseConcepts(domain, '');
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
                showPage('map');
            }

            else if (stat === 'license') {
                window.open('cc-license.html', '_blank', 'width=600,height=700,scrollbars=yes');
            }
        });
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
        showResult(`Concept "${concept.title}" (${concept.human_id}) ready for submission.`, 'success');
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
        chatStatus.textContent = 'Connecting to Dr. Mistral...';
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
            setTimeout(() => ctx.close(), 1000);
        } catch (e) {}
    };

    // ---------- INIT ----------
    loadConcepts();

});
