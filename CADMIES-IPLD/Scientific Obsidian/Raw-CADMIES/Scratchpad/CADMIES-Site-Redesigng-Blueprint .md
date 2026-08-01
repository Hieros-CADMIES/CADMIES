# CADMIES Site Redesign — Blueprint

1. Overview
Goal: Transform the current data dashboard into a polished, research-grade web presence that mirrors the Tkinter GUI design while remaining fast, clean, and minimalist.

Current state: Single-page concept grid with stats bar. Functional but lacks narrative and structure.

Target state: Single-page app with sidebar navigation, DeepSeek color palette, splash screen, and five core views.

2. Color Palette (DeepSeek)
Role	Color	Hex
Primary	Indigo	#4F46E5
Secondary	Navy	#1E1B4B
Accent	Light Indigo	#6366F1
Background	Surface	#F8FAFC
Background Alt	Light Gray	#F1F5F9
Card Background	White	#FFFFFF
Text Primary	Dark	#0F172A
Text Secondary	Gray	#475569
Subtle Border	Light Gray	#E2E8F0
Success	Green	#10B981
Warning	Amber	#F59E0B
Error	Red	#EF4444

3. Splash Screen
Purpose: Brief brand intro, sets the tone.

Design:

Full-screen overlay on page load

Navy (#1E1B4B) background

Sprout emoji (🌱) above title

"CADMIES" in white, bold, large

"Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem" in indigo (#4F46E5)

"Welcome to the digital mycelium. Welcome to the Deep." in white

Whale emoji (🐋) at bottom

Behavior:

3-5 second display

Fades out smoothly

Reveals main site underneath

CSS-only animation (no heavy assets)

4. Layout Structure
Single-page app with fixed sidebar:

text
┌─────────────┬──────────────────────────────────────┐
│  SIDEBAR    │         CONTENT AREA                │
│  (fixed)    │                                      │
│             │                                      │
│  🌱 CADMIES │   (Page content goes here)           │
│             │                                      │
│  📌         │                                      │
│  Dashboard  │                                      │
│             │                                      │
│  👩‍🏫       │                                      │
│  Dr. Mistral│                                      │
│             │                                      │
│  📚         │                                      │
│  Browse     │                                      │
│             │                                      │
│  ➕         │                                      │
│  Add        │                                      │
│             │                                      │
│  🕸️         │                                      │
│  Map        │                                      │
│             │                                      │
│  🐋         │                                      │
│  (footer)   │                                      │
└─────────────┴──────────────────────────────────────┘
Sidebar width: 220px
Content area: Remaining width
Responsive: Sidebar collapses to top nav on mobile (or hamburger menu)

5. Pages
5.1 Dashboard (📌)
Purpose: Welcome + at-a-glance stats + quick actions

Content:

Welcome message: "Welcome to the digital mycelium. Welcome to the Deep."

Stat cards: Concept count, Domain count, Relationship count, Willie version

Quick action buttons:

"👩‍🏫 Ask Dr. Mistral a Question"

"➕ Add a New Concept"

5.2 Dr. Mistral (👩‍🏫)
Purpose: Chat interface with Dr. Amanda Mistral

Content:

Chat display area (scrollable)

Controls:

Model selector: TinyLlama (Fast) / Mistral (Deep)

Tone selector: helpful / scholarly / casual

Max concepts: 5 / 10 / 20 / All

Input field + Send button

Welcome message from Dr. Mistral

Note: Uses Ollama API, same as Tkinter version.

5.3 Browse Library (📚)
Purpose: Searchable, filterable concept cards

Content:

Search bar (filters cards in real-time)

Domain filter pills (15 canonical domains)

Concept cards in grid (title, domain, definition preview)

Click card → detail popup/modal with:

Full definition

Mantra

Poetic version

Relationships (Builds Upon, Related To, Contradicts)

Metadata (created, creator, certainty)

Difficulty levels (beginner/intermediate/expert)

Human ID + CID

5.4 Add Concept (➕)
Purpose: Form for submitting new concepts

Content:

Required fields: Human ID, Title, Definition, Domain, Type, Subdomain

Optional fields: Mantra, Poetic Version, Axioms, Relationships, Genesis

Difficulty levels: Beginner / Intermediate / Expert

Preview panel (updates as you type)

Submit button → saves JSON to source_concepts/

Reset button

5.5 Mycelium Map (🕸️)
Purpose: Launch the interactive map

Content:

Brief description of the map

Status: "Map file found" or "Map file not found"

Launch button → opens mycelium_map.html in new tab

Technical note about browser requirements

6. Implementation Phases
Phase	What	Effort
1	Splash screen + color palette swap	Low
2	Sidebar layout + navigation	Low-Medium
3	Dashboard page	Low
4	Browse Library (concept cards + search/filter)	Medium
5	Dr. Mistral chat (Ollama integration)	Medium
6	Add Concept form	Medium
7	Map launch page	Low
8	Mobile responsiveness	Medium1. Architecture Overview
text
┌──────────────────────────────────────────────────────────────────────┐
│                    DIGITAL OCEAN DROPLET                            │
│                    (hierion-ubuntu-nyc1-929)                       │
│                                                                     │
│  ┌─────────────┐    ┌─────────────────────────────────────────┐    │
│  │   Nginx     │    │     Static Site (HTML/CSS/JS)           │    │
│  │  (Port 80)  │───▶│     - Splash screen                     │    │
│  │  (Port 443) │    │     - Sidebar navigation                │    │
│  └─────────────┘    │     - Dashboard                         │    │
│          │          │     - Browse Library                    │    │
│          │          │     - Add Concept form                  │    │
│          │          │     - Map launch page                   │    │
│          │          └─────────────────────────────────────────┘    │
│          │                                                          │
│          │  ┌─────────────────────────────────────────────────┐    │
│          │  │   API Proxy (Node/Flask) — Port 5000           │    │
│          │  │   - Receives chat requests from frontend       │    │
│          │  │   - Forwards to Paperspace via SSH tunnel      │    │
│          │  │   - Returns responses to frontend              │    │
│          │  └─────────────────────────────────────────────────┘    │
│          │                                                          │
│          └──────────────────────┬───────────────────────────────────┘
│                                 │ (SSH tunnel or API call)
└─────────────────────────────────┼───────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    PAPERSPACE GRADIENT                              │
│                    (cadmies-ipld notebook)                         │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │   Ollama API (Port 11434)                                  │    │
│  │   - Dr. Mistral model loaded                              │    │
│  │   - Accepts /api/generate requests                        │    │
│  │   - Uses GPU (A4000) for inference                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │   Blockstore                                                │    │
│  │   - Concepts                                                │    │
│  │   - Relationships                                           │    │
│  │   - Index                                                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
2. Component Responsibilities
Component	Location	Purpose
Static Site	Droplet	Serves HTML/CSS/JS to visitors
Splash Screen	Droplet	CSS overlay, 3-5 second intro
Sidebar	Droplet	Navigation between pages
Browse Library	Droplet	Renders concept cards from JSON
Add Concept	Droplet	Form, saves JSON locally on droplet
Map	Droplet	Launches mycelium_map.html in new tab
API Proxy	Droplet	Forwards chat requests to Paperspace
Ollama/Dr. Mistral	Paperspace	GPU inference for chat
Blockstore	Paperspace	Source of truth for concepts
3. API Proxy (Droplet)
Purpose: Bridge between frontend (browser) and Paperspace's Ollama API.

Why we need it:

Browser can't call Paperspace directly (CORS, firewall, auth)

Proxy handles authentication and routing

Single endpoint for frontend to call

Proxy endpoints:

Endpoint	Method	Purpose
/api/chat	POST	Send message to Dr. Mistral
/api/health	GET	Check if Paperspace is reachable
Proxy implementation options:

Flask (Python) — Simple, matches existing Python stack

Node/Express — Lightweight, good for proxy

Nginx reverse proxy — Directly route to Paperspace (if network allows)

Recommendation: Flask proxy running on droplet. Minimal code, easy to debug.

4. Frontend → API Flow
text
1. User types message in Dr. Mistral chat
2. Frontend sends POST to /api/chat on droplet
3. Droplet proxy forwards to Paperspace Ollama API
4. Paperspace generates response (GPU)
5. Response flows back through proxy to frontend
6. Frontend displays response
Timeout consideration: Ollama on GPU can take 5-30 seconds. Frontend should show "thinking" state.

5. Files to Create/Update (Droplet)
File	Location	Purpose
index.html	/var/www/project-hierion/	Single-page app
style.css	/var/www/project-hierion/	DeepSeek palette + layout
app.js	/var/www/project-hierion/	Page switching, API calls
splash.css	/var/www/project-hierion/	Splash screen overlay
proxy.py	/home/Project/Hierion/proxy/	Flask API proxy
proxy.service	/etc/systemd/system/	Systemd service for proxy
nginx.conf	/etc/nginx/sites-available/	Update to serve new site
6. Nginx Configuration Update
Current: Serves docs/index.html as static site.
Updated: Serves same, plus proxies /api/ to Flask proxy.

nginx
# Static site
location / {
    root /var/www/project-hierion;
    try_files $uri $uri/ /index.html;
}

# API proxy
location /api/ {
    proxy_pass http://127.0.0.1:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 60s;
}
7. Paperspace Connection Options
Option	Method	Complexity
SSH Tunnel	ssh -L 11434:localhost:11434 user@paperspace	Low
API Proxy	Flask on droplet calls Paperspace via HTTP	Medium
Reverse SSH	Paperspace opens tunnel to droplet	Medium
Recommendation: SSH tunnel from droplet to Paperspace. Simple, secure, reliable.

Command (on droplet):

bash
ssh -f -N -L 11434:localhost:11434 user@<paperspace-ip>
8. Deployment Plan
Phase 1: Static Site (droplet only)

Splash screen

Sidebar navigation

Dashboard

Browse Library (from concepts.json)

Add Concept (local save)

Map launch page

Phase 2: API + Paperspace Connection

SSH tunnel established

Flask proxy running on droplet

Dr. Mistral chat connected to Paperspace

Phase 3: Polish + Refinement

Mobile responsiveness

Error handling

Performance tuning

9. Questions to Decide
SSH tunnel: Do you want to set it up manually, or use a tool like autossh for auto-reconnect?

Proxy auth: Do we need API keys or is internal-only enough?

Paperspace uptime: What happens if the notebook goes to sleep? (auto-shutdown after 6 hours)

Fallback: If Paperspace is offline, should chat show a message or use a local fallback model?

10. Quick Commands
Start SSH tunnel (droplet):

bash
ssh -f -N -L 11434:localhost:11434 user@paperspace-ip
Test Ollama via tunnel:

bash
curl http://localhost:11434/api/generate -d '{"model":"dr-mistral","prompt":"Hello"}'
Start proxy:

bash
cd /home/Project/Hierion/proxy
python proxy.py
7. Files to Create/Update
File	Action
index.html	Replace with new single-page app
style.css	DeepSeek palette + sidebar layout
app.js	Page switching, search, filters
splash.css	Splash screen overlay
dashboard.html (template)	Stats + quick actions
mistral.html (template)	Chat interface
browse.html (template)	Concept cards + filter
add.html (template)	Form + preview
map.html (template)	Map launch page
8. Technical Notes
No build tools needed — plain HTML/CSS/JS

Ollama API runs locally on port 11434

Concept data from concepts.json (already generated)

Map remains a separate HTML file, opens in new tab

No authentication — public-facing site

9. Questions to Decide
Splash screen: Do we want it to appear on every visit, or just first visit of the session?

Mobile: Hamburger menu or collapsible sidebar?

Dr. Mistral: Should she have a different avatar/icon than Willie?

Browse Library: Infinite scroll or pagination?
