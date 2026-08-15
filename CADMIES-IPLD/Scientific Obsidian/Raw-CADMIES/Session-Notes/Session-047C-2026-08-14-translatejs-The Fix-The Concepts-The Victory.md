>⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
>unfiltered thoughts, and coded messages for fellow gardeners.
>For polished documentation, check Polished CADMIES or promote this note.

# Session 047C - 2026-08-14 - translatejs - The Fix, The Concepts, The Victory

## Soundtrack
The sound of a working translation. Italian laughter. Relief.

What Went Down
The Problem
After successfully deploying translate.js with the latest version (4.1.0), the concept cards loaded dynamically by app.js were not translating. The static content translated fine, but the concepts remained in English.

The Debugging Trail
Attempt 1: translate.listener.start()
We added translate.listener.start() to the HTML initialization, thinking it would monitor DOM changes and translate new content automatically. This broke translation entirely. The listener interfered with app.js.

Attempt 2: app.js retranslation fix
We added a call to translate.execute() in renderBrowseConcepts() after the concept cards were injected into the DOM. This worked initially but stopped working when the listener was added.

The breakthrough: Removing translate.listener.start() and keeping the simple translate.execute() approach fixed the issue. The concept cards now translate when they load.

The Fix
In index.html:

html
<script src="https://cdn.jsdelivr.net/gh/xnx3/translate/translate.js/translate.js"></script>
<script>
    translate.language.setLocal('english');
    translate.execute();
    // NO translate.listener.start() — it breaks everything
</script>
<script src="app.js"></script>
In app.js (renderBrowseConcepts function):

javascript
// === TRANSLATE.JS FIX: Retranslate newly injected concept cards ===
if (typeof translate !== 'undefined') {
    setTimeout(function() {
        translate.execute();
    }, 100);
}
The Result
Static content translates

Concept cards translate when they load

Button toggles dropdown

Language preference stored in localStorage

No console errors

What We Learned
translate.listener.start() is the enemy of dynamic content loading in this setup

The simple translate.execute() approach works if you call it after the new content is rendered

setTimeout(100) gives the DOM time to render before retranslating

Less is more — the listener added complexity and broke everything

Nuggets
"The listener broke it. We removed it. It works."

"Simple is better. Always."

"The concept cards translate now. Finally."

"Dr. Mistral speaks every language. The mycelium grows."

