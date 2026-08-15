> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session - 048 - 2026-08-10 - One for the record.

## After doing some work and some communicating with VMX regarding the Matadisco project, I asked DeepSeek to provide one more message.

DeepSeek provided the message and i was not happy with it.

So, this is what I, The Gardener, told DeepSeek:
```
ok, not that concise.

we read his most recent comment, we added an image and redid the preview code, everything worked, we noticed that the records still did not load, we noticed a behavior in the browser/viewer,  where the images displayed were different, we realized this was because the viewer is a "live" viewer, we realized we need a library type viewer for cadmies records, we realized we already had that via the site/library, we realized that is good for the public but that for the scientist and academia we should have a matadisco-cadmies viewer which pulls from the same source as the site library. wheeew, lol. now write that neatly. =)
```

To that, DeepSeek returned with and provided:
```
Following up on the preview test — we added a PNG image to one of our records and re-published, but it still doesn't appear in the viewer.

We noticed the viewer streams records live in the console, and only those with eo and stac fields show up on the page. Our records have preview but not those fields, so they don't render.

We also realized the viewer is a live stream, not a library browser. Our records were already in the network, but by the time we opened the viewer, they weren't "live" anymore. So even if they were renderable, they wouldn't show up unless published while the page is open.

That distinction made us step back and think about what we actually need. For the general public, we already have the CADMIES gateway — a library-style interface that pulls from our concepts JSON. For scientists and academics, we think a Matadisco-CADMIES viewer makes sense — a specialized portal that pulls from the same source data but is designed for discovery and querying in a decentralized context.

So the next step is building a viewer for CADMIES records that can pull from the network, rather than relying on a live stream. We'll likely reuse the same concepts JSON as the source, so no double work.

Curious if you have any thoughts on that approach or if others have run into similar considerations with the viewer.
```

And that, mon ami, is why I, a real human, use DeepSeek to do the writing for me. =)

So, I hope this dimisses once and for all any concerns that this project and all of this work is being done by bots for shady reasons, lol. It is most definitely not. =)

Namaste to you, reading this right now. =)
