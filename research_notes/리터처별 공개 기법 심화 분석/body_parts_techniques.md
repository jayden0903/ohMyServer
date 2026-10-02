# Body-Part / Element-Specific Professional Retouching Techniques (non-generative, non-destructive)

Scope note: Research done 2026-10-02 from free public pages (Retouching Academy, PHLEARN, Fstoppers, KelbyOne Insider, Photoshop Essentials, Adobe Community, Pratik Naik's free PDF guide, etc.). Many "pro" sources (PHLEARN PRO, PhotoshopCAFE eye video, Retouching Academy highlight video, Fstoppers lip video) hide the exact numbers inside paywalled or video content; where that happened it is listed under Gaps. Numbers below are the publishers' starting values, not universal constants. All "measurable checks" that aren't directly quoted from a source are in the Inferences sections.

---

## Q0 (cross-cutting). Base tool settings and layer workflow that every element below relies on

### Takeaway
Pratik Naik's free guide gives the most concrete baseline: blank layers sampling "Current and Below", 0% hardness brushes, 1–3% flow for dodge & burn (2% default), 5–10% flow clone for gentle work, legacy healing algorithm, Median 2–4 for frequency separation, and Liquify pressure 5–10 / density 50. The workflow order is Clean (heal/clone) → Dodge & Burn → Frequency Separation (sparingly) → Color fix.

### Cited Findings
- Clone Stamp: hardness 0%, opacity 100%, Shape Dynamics unchecked, Build-up checked, work on a new layer; flow "05% to 10% to clone away something gently, and 20% and higher to clone things away quickly"; Sample = "Current and Below". — [Pratik Naik, Pratik's Retouching Guide (PDF)](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Healing Brush: hardness 0%, pen-pressure size Off, own layer, Normal blend mode, sample "Current and Below", "completely cover a blemish completely before letting the healing brush give you the results"; enable "Use legacy healing brush algorithm" in Preferences > Tools. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Spot Healing Brush only offers "sample all layers", so helper (black & white) layers must be turned off when using it or strokes come out "black and white and grainy". — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Clone "softening technique" for rough texture: 0% hardness, 5% flow, brush the size of the texture to be evened, sample in the same area, move a few pixels away and brush; "the overlap in texture will diffuse the area nicely." — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Dodge & burn (curves/mask method): 2% flow, 100% opacity, Shape Dynamics off; helper B&W layer on; zoom out to ~50–70% to judge larger areas; D&B first to even patchy tone (under eyes, next to mouth, forehead) before any frequency separation; brush tool 1–3% flow preferred. Eyedropper sample size 5×5 Average; brush Smoothing 0%. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- D&B self-check: toggle the layer; if too bright you went too far (paint back with opposite); if area outside the target brightens the brush is too big; if the edges stay dark the brush is too small. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Frequency separation (Pratik's action): Median radius 2–4 ("a range that makes the image look out of focus to the point where it would look like you just missed focus"); Low layer = color/light, High = texture, edit High with heal/clone set to "Current Layer"; use 8-bit vs 16-bit action variants. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Apply Image math: 16-bit = Add, Scale 2, Offset 0, Invert checked; 8-bit = Subtract, Scale 2, Offset 128, Invert unchecked; High layer set to Linear Light. — [ExpertPhotography / search summary](https://expertphotography.com/frequency-separation-photoshop); [Adobe Community thread](https://forums.adobe.com/thread/2484403)
- Color fix: blank layer in Color mode, sample good skin (5×5 avg), low flow / 100% opacity; if it looks wrong use Hue mode instead ("Hue won't change the saturation… Color will match the saturation as well"); try Color first, then Hue. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Liquify: only on a merged/visible solid layer; Forward Warp Brush Pressure 5–10, Density 50% to start; Reconstruct tool = undo brush; use "Show Backdrop" at reduced opacity to see how far you've moved; "Face Aware… can be abused easily, so adjust those sliders with caution." — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Julia Kuzmenko McKim (Retouching Academy): "I use healing brush 90% of the time for the skin"; frequency separation used sparingly as supplementary; Liquify used for symmetry of eyes, brows, lips, nose, chin, jawline. — [Retouching Academy, 7 Key Areas](https://retouchingacademy.com/7-key-areas-for-beauty-photography-retouching/)
- Fstoppers editorial workflow D&B: two Curves layers (one up, one down), black masks, brush "100% opacity and 3% flow" or "70% opacity and 1% flow". — [Fstoppers, Start to Finish Fashion Editorial Retouching Pt 1](https://fstoppers.com/business/start-finish-fashion-editorial-retouching-part-1-68367)
- Overlay D&B variant: 50% gray layer in Overlay, white/black brush at 5% flow. — [Fstoppers, Understanding the Human Eye](https://fstoppers.com/bts/understanding-human-eye-and-how-retouch-it-naturally-60235)

### Inferences
- For an agent: every correction should be a separate named layer (Heal, Clone, D&B-Dodge curve, D&B-Burn curve, Color, per-feature adjustment layers) so each can be opacity-scaled or masked after review — this is the common thread across all sources.
- Low flow (1–10%) with 100% opacity is the consensus pattern for painting masks: build-up gradually rather than one stroke at partial opacity.

### Gaps
- No free source gave fixed Curves point values for D&B dodge/burn layers; practitioners describe "slightly up/down" only.

---

## Q1. Eyes: sclera, iris (radial D&B, limbal ring, catchlights), lashes/brows, under-eye bags/dark circles

### Takeaway
Treat the sclera as a color-cast problem (remove red/yellow, shift slightly toward blue/cyan) rather than a brightness problem; keep some vessels and leave corners darker. Iris work is built-up low-flow D&B following the light direction, with a softly darkened limbal ring. Under-eye: lighten with Lighten-mode paint/heal at ~10% flow and reduced opacity, or a Curves color-match; never erase the lower-lid shadow.

### Cited Findings
**Sclera**
- Kristina Sherk: "I rarely brighten them"; instead remove veins, decrease red, tweak color toward blue (Color Balance layer: add Blue and Cyan), "on rare occasions, I'll brighten only the inside ring of the eye whites (closest to the iris)"; avoid whitening the corners to keep the eye three-dimensional. Over-brightened whites = sign #1 of over-retouching. — [KelbyOne Insider, Kristina Sherk – Top Three Signs of Over-Retouching](https://insider.kelbyone.com/top-three-signs-of-over-retouching-and-how-to-protect-yourself-by-kristina-sherk/)
- Scott Kelby (Lightroom): sclera brush Exposure +0.50 (half a stop); "overbrightening the whites of the eyes is one of the most common retouching mistakes" producing "alien eyes"; recommends under-retouching. — [KelbyOne Insider, Retouching Teeth, Hair and Eyes in Lightroom Classic](https://insider.kelbyone.com/retouching-teeth-hair-and-eyes-in-lightroom-classic-by-scott-kelby/)
- Lightroom Eye Sclera mask example: Exposure +0.40, Saturation −60. — [Markus Hagner Photography (June 2026)](https://markus-hagner-photography.com/how-to-whiten-teeth-and-brighten-eyes-in-lightroom-portrait-retouching/)
- Retouching Academy (Michael Woloszynowicz method): select sclera (lasso/pen/Quick Mask), Gaussian-blur the mask edge, Selective Color layer, adjust the **Neutrals** while watching the Info panel for the contaminating cast; keep some blood vessel detail. — [Retouching Academy, How To Brighten Eyes Naturally](https://retouchingacademy.com/how-to-brighten-eyes-naturally-in-photoshop/)
- "The key to restoring the whiteness of the Sclera is to treat the problem as a local color cast"; brightening risks eyes that "feel unnaturally bright relatively to the rest of the image". — [Fstoppers, How to Naturally Whiten Eyes](https://fstoppers.com/photoshop/how-naturally-whiten-eyes-photoshop-and-capture-one-42256)
- Pratik Naik: "Never brighten the eyes too much, remove pores completely, and remove characteristic marks about the person!" — [ePhotozine, Retouching Is Not About Blurring Or Airbrushing Skin](https://www.ephotozine.com/article/retouching-is-not-about-blurring-or-airbrushing-skin-27617)
- Fstoppers commenter flagged an example sclera as "almost glowing" — cautionary sign. — [Fstoppers, Understanding the Human Eye](https://fstoppers.com/bts/understanding-human-eye-and-how-retouch-it-naturally-60235)
- Photoshop procedure: new layer, Spot Healing to remove distractions (veins), select whites, Hue/Saturation layer with mask, raise Lightness subtly. — [Photoshop Training Channel, How To Whiten Eyes](https://photoshoptrainingchannel.com/how-to-whiten-eyes-in-photoshop/)

**Iris, limbal ring, catchlights**
- Overlay method: new layer 50% gray in Overlay (or 50% opacity), white brush at 5% flow to dodge, black to burn; or Dodge tool on Midtones/Highlights low flow, Burn on Shadows. — [Fstoppers, Understanding the Human Eye](https://fstoppers.com/bts/understanding-human-eye-and-how-retouch-it-naturally-60235)
- Iris "should NOT be equally bright throughout": brightest area is where light exits the iris (opposite the catchlight); the upper iris is shadowed by the lid. "Build up the highlights and shadows" — avoid single strokes. — [Fstoppers, Understanding the Human Eye](https://fstoppers.com/bts/understanding-human-eye-and-how-retouch-it-naturally-60235)
- Limbal ring: darken for depth but don't over-sharpen — "the limbus is naturally a bit unsharp"; adding contrast "with one or two brush strokes will result in an amateurish retouch"; most limbal rings have jagged inward points, so darken with a small brush and keep it imperfect. — [Fstoppers, Understanding the Human Eye](https://fstoppers.com/bts/understanding-human-eye-and-how-retouch-it-naturally-60235)
- Catchlights: brighten with tiny brush (~20–30 px), darken iris edge slightly; Color Dodge can brighten the secondary reflection opposite the pupil. — [PHLEARN Master Retouching Eyes (topic list)](https://phlearn.com/tutorial/master-retouching-eyes/) / [Northrup, Dynamic Eyes](https://northrup.photo/using-photoshop-to-create-dynamic-eyes/) (search-snippet level; full text not verified)

**Lashes and brows**
- Retouching Academy lash brush: round tip, hardness 50–85% (mostly 70%); Size Jitter with Fade — "Brush Size 6/Fade 100 for shorter hairs on the bottom eyelid", "Size 7/Fade 120 for longer bottom/shorter top", "Size 10/Fade 160 for longer hairs on the top eyelid"; Scattering is "an important setting" to mimic mascara-coated jagged lashes; Color Dynamics optional; Transfer can be off; add shadow below new lashes, then low-radius blur to match. Brows: paint three layers — bluish tones, deeper red/saturated, then shadows — and slightly blur. Warnings: "Don't rush" and "Less is more". — [Retouching Academy, Retouching Eyelashes and Eyebrows](https://retouchingacademy.com/retouching-eyelashes-and-eyebrows-in-beauty-portraits/)
- Lash cleanup: remove lashes going against the flow/overlapping, clean gaps between lashes, heal mascara blots (Spot Healing, D&B). — [Retouching Academy, How To Retouch Eyelashes and Eyebrows (search summary)](https://retouchingacademy.com/how-to-retouch-eyelashes-and-eyebrows-for-beauty-photographs/)

**Under-eye bags / dark circles**
- PHLEARN: lasso both under-eye areas, Quick Mask + Gaussian Blur 10–25 px (resolution-dependent) to feather; new layer in **Lighten** mode; brush hardness 0, **Flow 10%**; Alt-sample a lighter nearby skin tone (resample separately per eye/tone); lower layer opacity if too strong. Warns Generative Fill "tends to reshape the eye rather than just lighten the skin". — [PHLEARN, Eliminate Dark Circles](https://phlearn.com/tutorial/eliminate-dark-circles-under-eyes-in-photoshop/)
- Fstoppers Curves color-match: Curves layer, double-click the eyedropper (with the Curves icon selected, not the mask), pick target skin color from a good cheek area, click on the dark circle, invert mask, paint white at reduced flow — avoids pore-size mismatch from cloning cheek texture. — [Fstoppers, Simple Method to Fix Bags Under Eyes](https://fstoppers.com/photoshop/simple-method-fix-bags-under-eyes-and-mismatched-skin-tones-7977)
- Search-level consensus for heal/paint-in-Lighten: opacity typically 3–15% brush or reduce layer opacity until natural. — [Fstoppers dark circles](https://fstoppers.com/photoshop/how-fix-dark-circles-under-eyes-photoshop-651278); [DIYPhotography](https://www.diyphotography.net/remove-eye-bags-1-minute-photoshop/)
- The shadow under the lower lid is "a wanted shadow" — soften, don't eliminate. — [Fstoppers, Understanding the Human Eye](https://fstoppers.com/bts/understanding-human-eye-and-how-retouch-it-naturally-60235)
- Pratik lists under-eyes as a prime D&B zone (2% flow). — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)

### Inferences
- Color vs luminance: dark circles are usually both darker and cooler/purpler; use a Color/Hue-mode layer (Pratik) or Curves color-match (Fstoppers) for the hue component and Lighten/D&B for the luminance component, each on its own layer so either can be faded.
- Measurable checks an agent can run: (a) sclera luminance should stay below the brightest specular/catchlight and ideally below the brightest skin highlight; (b) sclera corners should remain darker than the area adjacent to the iris; (c) sclera chroma near-neutral to very slightly cool, not 255/255/255; (d) under-eye L* after correction should remain slightly below adjacent cheek L* (shadow preserved); (e) iris luminance should be asymmetric (lower in the upper third). These are derived from the qualitative rules above, not published thresholds.

### Gaps
- No free source gives a numeric ceiling for sclera brightness (e.g., L* or RGB max). Sherk/Kelby/Fstoppers give only qualitative limits.
- PhotoshopCAFE and PHLEARN PRO eye tutorials keep exact settings in paywalled video.

---

## Q2. Lips: lip line cleanup, texture preservation, color/saturation, lipstick bleed

### Takeaway
Lipstick bleed is removed by painting sampled skin color on a Color-mode layer (100% opacity, 6% flow) or on the low-frequency layer, then restoring texture with heal/clone at low flow. Lips have little clean texture to sample, so texture must be preserved/grafted carefully; dry/chapped lips are fixed with frequency-separation-style resurfacing.

### Cited Findings
- Bleed removal, method 1: blank layer, blend mode Color, brush opacity 100%, flow 6%, sample nearby skin, paint over stray lipstick. Method 2: frequency separation; blank layer above Low, 6% flow skin-color paint; then a blank layer above High and heal/clone at low flow to add skin texture back. — [Nina K Photography, How to remove a lipstick bleed](https://www.ninakphotography.com/how-to-remove-a-lipstick-bleed-in-photoshop/)
- "Unlike skin, you have very little to sample from… lips need proper texture to be believable" or they look "overly artificial and fake". — [Fstoppers, How to Retouch Lips](https://fstoppers.com/portraits/how-retouch-lips-photoshop-629276)
- Dry/chapped lips: Retouching Academy demonstrates a frequency-separation-based "Resurface" script (MUA Retouch panel). — [Retouching Academy, Fixing Dry or Chapped Lips](https://retouchingacademy.com/fixing-dry-or-chapped-lips-in-beauty-portrait-retouching/)
- Tools commonly used for lips: frequency separation, healing/clone, texture grafting, Pen Tool, Blend If; inverted High Pass for cracks; adding shine; defining lip line. — [Michael Woloszynowicz, How to Retouch Lips (search summary; page returned 503)](http://www.vibrantshot.com/how-to-retouch-lips-in-photoshop/)
- Fine-detail clone at 35% opacity, small soft brush, zoomed in; lip selection in Quick Mask with ~85% hardness brush, feather 1 px. — [search summary of Layers Magazine / Photoshop Roadmap lip tutorials](https://www.photoshoproadmap.com/how-to-change-lip-color-in-photoshop-5-methods-with-exact-color-matching/) (snippet-level, not verified in full)
- Symmetry of lips via Liquify is part of beauty retouching's "7 key areas". — [Retouching Academy, 7 Key Areas](https://retouchingacademy.com/7-key-areas-for-beauty-photography-retouching/)
- Hue/Sat redness correction must be masked away from lips "that should stay red". — [PHLEARN, Remove Redness From Skin](https://phlearn.com/tutorial/how-to-remove-redness-from-skin-in-photoshop/)

### Inferences
- Lip line: rebuild edge with clone at low flow from adjacent clean border, sampling Current & Below; do not hard-mask a vector edge (lip borders are naturally soft).
- Checks: lip vertical crease texture visible at 100% zoom; lip edge transition width similar to original (no 1-px hard edge); lip saturation change limited and hue unchanged unless client requests.

### Gaps
- No verified exact saturation/hue numbers for lip color enhancement from free primary sources; Fstoppers/Kayleigh June and Woloszynowicz content was video-only or unreachable.

---

## Q3. Teeth: whitening without going grey/blue, selective color, gaps and shape

### Takeaway
Remove yellow rather than add brightness: Hue/Sat Yellows Saturation about −60 to −80 plus small Master Lightness (+10 to +20), or Selective Color (Yellows/Whites: Cyan up, Yellow down). Never drag Yellows saturation fully left — teeth go dull/grey.

### Cited Findings
- Hue/Sat on lasso-masked teeth: Edit = Yellows, Saturation −80 (man, "most but not all" yellow) / −70 (woman); then Master Lightness +20 / +10; refine mask with 50% opacity brush; separate layers per person. Warning: dragging Saturation all the way left produces "teeth that look dull and lifeless"; keep "just enough yellow". — [Photoshop Essentials, How To Whiten Teeth](https://www.photoshopessentials.com/photo-editing/whiten-teeth/)
- Selective Color: Colors = Yellows, Cyan +10, Yellow −23 (adjust to how yellow); brush 50% opacity for individual teeth; avoid lips/gums; one person at a time; uses Hue/Sat + Selective Color + Curves layers. — [Cole's Classroom, How to Whiten Teeth](https://colesclassroom.com/how-to-easily-and-successfully-whiten-teeth-in-photoshop/)
- Kristina Sherk: over-whitened teeth = sign #2 of over-retouching; use Selective Color, Whites: increase Cyan, decrease Yellow; repeat in Yellows; invert mask and paint teeth only. — [KelbyOne Insider, Kristina Sherk](https://insider.kelbyone.com/top-three-signs-of-over-retouching-and-how-to-protect-yourself-by-kristina-sherk/)
- Scott Kelby Lightroom teeth brush: Saturation −62, Exposure +0.79. — [KelbyOne Insider, Scott Kelby](https://insider.kelbyone.com/retouching-teeth-hair-and-eyes-in-lightroom-classic-by-scott-kelby/)
- Teeth naturally have a yellow tint; too much saturation removal looks unrealistic. — [search summary, Adobe/Photoshop tutorials](https://www.adobe.com/creativecloud/photography/discover/how-to-whiten-teeth.html)

### Inferences
- "Grey/blue" failure = Yellows saturation near −100 or excess Cyan; check that corrected teeth retain a small positive b* (warm) value and remain darker than sclera highlights/catchlights; back teeth should stay darker than front teeth (depth).
- Gaps/shape: no free source with procedure; standard approach would be Liquify at low pressure or clone from adjacent tooth edges — not verified.

### Gaps
- No free, verifiable source on closing tooth gaps or reshaping teeth with exact settings.

---

## Q4. Skin by area: shine, wrinkles, redness, acne marks, nose pores, beard shadow, body skin

### Takeaway
Heal/clone blemishes on blank layers (healing 90% of the time), reduce rather than erase wrinkles (heal then 40–60% opacity, Lighten mode), fix redness with a range-narrowed Hue/Sat Reds layer painted in at ~20% flow, reduce shine with a sampled solid color + Blend If + opacity, and remove stubble with a Dust & Scratches pattern heal at 50–65% limited by Blend If. Pores must remain visible — their absence is the #1 sign of over-retouching.

### Cited Findings
**Shine / specular highlights**
- Retouching Academy (Dansky): Solid Color fill layer (sampled skin tone), Blend-If sliders to restrict to highlights, and Opacity to control strength; used on forehead, under-eye, chin, arm; reasons: skin looks oily or harsh shapes distract. — [Retouching Academy, How to Reduce Unwanted Highlights](https://retouchingacademy.com/how-to-reduce-unwanted-highlights-on-skin-when-retouching/)

**Wrinkles / fine lines**
- Healing brush on new layer, Sample All Layers, Aligned unchecked; layer blend mode Lighten; opacity "somewhere between 40% and 60%" (60% example); sample texture near the wrinkle; "just because you can do something doesn't mean you should." — [Photoshop Essentials, Remove Wrinkles](https://www.photoshopessentials.com/photo-editing/healing-brush/)
- Lightroom: heal at 100% then lower opacity to ~55% ("the wrinkle is there, but it's not nearly as intense"); goal "is not to remove them but to reduce their intensity". — [Lightroom Killer Tips, Realistically Retouch Wrinkles](https://lightroomkillertips.com/portrait-retouching-in-lightroom-part-4-realistically-retouch-wrinkles/)
- Neck lines: heal fully then lower layer/stroke opacity so original shows through. — [Evoto / search summary](https://blog.evoto.ai/how-to-remove-wrinkles-in-photoshop/)

**Redness / blotches**
- PHLEARN: Hue/Sat layer → Reds → eyedropper on reddest skin → narrow the range sliders → Saturation back to 0, Hue slightly right (toward orange), Lightness up a little → invert mask → paint white at Flow ~20% → Spot Heal leftovers. Warnings: not narrowing range affects all skin; not inverting mask shifts lips; full flow prevents gradual build-up. — [PHLEARN, Remove Redness From Skin](https://phlearn.com/tutorial/how-to-remove-redness-from-skin-in-photoshop/)
- Don't take Reds saturation far below 0 or skin goes grey. — [search summary incl. SLR Lounge / PetaPixel](https://www.slrlounge.com/how-to-easily-correct-red-blotchy-skin-in-photoshop/)
- Pratik's color-fix layer (Color, then Hue mode, low flow) also handles blotches and hands/body mismatch. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)

**Acne marks / blemishes / pores**
- "I use healing brush 90% of the time for the skin… sample similar texture." — [Retouching Academy, 7 Key Areas](https://retouchingacademy.com/7-key-areas-for-beauty-photography-retouching/)
- Pores: "If all of the pores are gone, then this is a big red flag… If the skin still has pores (for the most part), it means that the retouching has been done well." — [KelbyOne Insider, Kristina Sherk](https://insider.kelbyone.com/top-three-signs-of-over-retouching-and-how-to-protect-yourself-by-kristina-sherk/)
- Pratik: retouching should be "what a person looks like on their best day, realistic yet natural and full of visible skin texture"; remembers over-retouched images where "every single pore was almost not visible" looking "mannequin like". — [ePhotozine](https://www.ephotozine.com/article/retouching-is-not-about-blurring-or-airbrushing-skin-27617); [DIYPhotography](https://www.diyphotography.net/the-skin-is-the-star-in-these-make-up-free-beauty-portraits-by-pratik-naik/)
- Rough/enlarged pore texture (e.g., nose): clone softening at 5% flow, offset sampling a few px. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Mismatched pore size is a giveaway when cloning cheek texture onto under-eye areas. — [Fstoppers](https://fstoppers.com/photoshop/simple-method-fix-bags-under-eyes-and-mismatched-skin-tones-7977)

**Beard shadow**
- Duplicate layer → Filter > Noise > Dust & Scratches Radius ~4 px (until stubble disappears) → Edit > Define Pattern → undo filter → new layer, Healing Brush Source = Pattern, Aligned + Sample All Layers checked → short strokes → layer at 50%, raised to 65% for that image → Blend If (drag white "This Layer"/underlying slider left, Alt-split for smooth transition) to restrict to dark stubble and reveal original texture. — [Photoshop Essentials, Reducing 5 O'Clock Shadow](https://www.photoshopessentials.com/photo-editing/stubble/)
- Healing Brush in Lighten mode for facial/body hair removal. — [Retouching Academy, 7 Key Areas](https://retouchingacademy.com/7-key-areas-for-beauty-photography-retouching/)

**Body skin (arms, legs, cellulite, stretch marks) and policy**
- General workflow: low-frequency for color/tone, high-frequency for blemishes/texture, D&B on 50% gray Overlay to restore volume; "the single biggest mistake… is trying to fix color, texture, and light all at once with one tool." — [photoshoptutorial.com, Why Your Skin Retouching Looks Fake](https://photoshoptutorial.com/posts/why-your-skin-retouching-looks-fake-and-the-frequency-separation-workflow-that-f/)
- Pratik uses D&B (2% flow) across face "and body" to even patchy tones before FS. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Policy: France requires commercial (advertising) images whose model body shape was digitally made thinner or thicker to be labeled "photographie retouchée"; in force 1 Oct 2017; fine up to €37,500; editorial not covered. — [Global Legal Post](https://www.globallegalpost.com/news/fashion-companies-must-disclose-retouching-of-photographs-in-france-57838557); [NPR](https://www.npr.org/sections/thetwo-way/2017/09/30/554750939/france-aims-to-get-real-retouched-photos-of-models-now-require-label); [Retouching Academy](https://retouchingacademy.com/new-french-law-requires-label-for-retouched-images/)
- Getty Images/iStock stopped accepting creative content "depicting models whose body shapes have been retouched to make them look thinner or larger". — [Yahoo News](https://news.yahoo.com/getty-images-bans-retouched-photos-201919517.html)
- Fstoppers editorial retoucher: "my use of liquefy is NOT to make the model look thinner" — used for clothing fit. — [Fstoppers](https://fstoppers.com/business/start-finish-fashion-editorial-retouching-part-1-68367)

### Inferences
- For an agent, body-shape Liquify and cellulite/stretch-mark removal should be a policy flag (off by default, require client brief), given French labeling and Getty rules.
- Measurable checks: high-frequency energy (e.g., local std-dev of a high-pass at 1–3 px radius) in retouched skin regions should remain close to untouched reference skin; shine reduction should lower but not eliminate the specular peak (highlight still the brightest skin value); wrinkle regions should retain a visible but reduced luminance dip.

### Gaps
- Retouching Academy's exact Blend-If numbers and opacity for shine reduction are only in the video.
- No free primary source with step-by-step cellulite or stretch-mark settings was found.

---

## Q5. Hair: flyaways, filling gaps, frizz, shine/color, hairline, strand masking

### Takeaway
Clone in Darken mode to remove light strands over darker hair and Lighten mode for dark strands over light backgrounds/hair; Spot Heal Content-Aware for isolated strays against simple backgrounds; work at 100–200% zoom; leave some flyaways to avoid "helmet hair." Gaps are filled by copying a full section of hair, transforming it to match direction, and setting it to Darken.

### Cited Findings
- Clone Stamp in Darken mode affects lighter strands against darker hair; Lighten mode affects dark strands against lighter hair. — [Retouching Academy, 7 Key Areas](https://retouchingacademy.com/7-key-areas-for-beauty-photography-retouching/)
- Flyaways: zoom 100–200%; Clone opacity ~80–90%, Lighten blend mode (for dark strands on lighter backdrop), small soft brush; Smudge strength 30–50%; Spot Healing Content-Aware with brush slightly wider than the strand. Warnings: "helmet hair… looks fake"; cloning repeatedly from one source creates repeating patterns; "don't eliminate every single strand. A few natural flyaways actually make portraits look more realistic." — [Retouching Labs, How to Remove Flyaway Hair](https://retouchinglabs.com/how-to-remove-flyaway-hair-in-photoshop/)
- Surface Blur + mask method removes many flyaways at once because it respects edges beyond its threshold. — [Retouching Labs (search summary)](https://retouchinglabs.com/how-to-remove-flyaway-hair-in-photoshop/)
- Gap fill: lasso a full hair area larger than the gap, copy to a "Gap Fill" layer, transform/flip to match strand direction, set blend mode to Darken, mask in. — [search summary of hair-gap tutorials](https://medialoot.com/blog/how-to-retouch-hair-in-adobe-photoshop/) (page returned 403; snippet only)
- Scott Kelby Lightroom hair brush: Exposure −1.08, Whites +75 (darken overall, bring back highlights/shine). — [KelbyOne Insider](https://insider.kelbyone.com/retouching-teeth-hair-and-eyes-in-lightroom-classic-by-scott-kelby/)
- Fstoppers fringe (dress) gap fill: Stamp tool on blank layer, Current & Below, sample matching fringe, optional Magnetic Lasso selection to confine. — [Fstoppers](https://fstoppers.com/business/start-finish-fashion-editorial-retouching-part-1-68367)

### Inferences
- Hairline cleanup follows the same Darken/Lighten clone logic against forehead skin; frizz within the mass can be D&B'd/cloned along strand direction rather than blurred.
- Checks: no repeated-pattern clones (autocorrelation of cloned region); hair silhouette retains some irregular strands; strand direction continuity across filled gaps.

### Gaps
- No free verified source with exact hair-shine D&B or hair-color Hue/Sat values in Photoshop; Retouching Academy's hair course is paid.

---

## Q6. Hands and nails, neck/décolletage, ears

### Takeaway
Clean cuticles/surrounding skin with Spot Heal first, then repair nails with clone/heal at 10–30% flow from similar-luminance nail, or copy-transform a good nail section; lighten red/dark knuckles lightly (Dodge Midtones ≤13% exposure or a color-match layer). Neck lines: heal then reduce opacity. Match hand color to face with a Color/Hue-mode layer.

### Cited Findings
- Nails: spot heal cuticles first; extend polish edges with Clone Stamp; Liquify grown-out nails; work on separate layers. — [Photoshop Roadmap, How to Retouch Nails](https://www.photoshoproadmap.com/how-to-retouch-nails-in-photoshop-quick-beauty-techniques/)
- Nail repair: clone/heal sampling nail of similar luminosity/color at low flow 10–30%; or Pen-tool cut of good nail section, transform to extend, mask/clone/heal to blend; Dodge tool small brush, Range Midtones, Exposure ≤13% single pass to lighten. — [Ad Retouch Studio / Orms RetutPro (search summary)](https://adretouchstudio.com/how-to-fix-fingernails-in-photoshop/); [Orms blog](https://blog.ormsdirect.co.za/retutpro-retouching-nails-in-photoshop/)
- Hands a different color than the body: Pratik's Color-mode sampled layer, low flow. — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Neck/décolletage lines: heal/remove then lower opacity so lines remain partially. — [Evoto / search summary](https://blog.evoto.ai/how-to-remove-wrinkles-in-photoshop/); same 40–60% Lighten principle — [Photoshop Essentials](https://www.photoshopessentials.com/photo-editing/healing-brush/)

### Inferences
- Knuckle redness can reuse the PHLEARN Reds Hue/Sat technique masked to knuckles.

### Gaps
- No free authoritative source on ear retouching specifically (earlobe creases, redness, cartilage highlights) was found.

---

## Q7. Makeup: foundation edges, mascara clumps, eyeshadow cleanup, contour enhancement

### Takeaway
Makeup is cleaned with the same heal/clone/color-layer toolkit: heal mascara blots and against-the-flow lashes, rebuild lashes with a jitter/scatter brush, paint sampled skin color (Color mode, ~6% flow) over stray pigment, and use D&B to accentuate makeup and contour.

### Cited Findings
- Mascara: remove lashes against the flow/overlaps, clean gaps, heal mascara blots via Spot Healing, Shape Dynamics brush, D&B. — [Retouching Academy (search summary)](https://retouchingacademy.com/how-to-retouch-eyelashes-and-eyebrows-for-beauty-photographs/)
- Lash rebuild brush settings (Size Jitter/Fade 100–160, Scattering, hardness ~70%). — [Retouching Academy](https://retouchingacademy.com/retouching-eyelashes-and-eyebrows-in-beauty-portraits/)
- Stray pigment (applies to eyeshadow fallout/lipstick bleed): Color-mode layer, opacity 100%, flow 6%, sampled skin; restore texture with low-flow heal on high frequency. — [Nina K Photography](https://www.ninakphotography.com/how-to-remove-a-lipstick-bleed-in-photoshop/)
- Makeup asymmetry is fixed in the symmetry pass (Liquify); D&B used to "accentuate makeup and jewelry". — [Retouching Academy, 7 Key Areas](https://retouchingacademy.com/7-key-areas-for-beauty-photography-retouching/)
- Pratik separates D&B for evening tone from D&B for contouring ("I prefer doing this in another step"). — [Pratik's Retouching Guide](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Envato makeup-retouching overview exists (5 steps) but was not fetched in full. — [Tuts+ How to Retouch Makeup](https://photography.tutsplus.com/articles/how-to-perfectly-retouch-makeup-for-beauty-and-fashion-photography-in-five-steps--cms-27092)

### Inferences
- Foundation edge at jaw/hairline is a color-and-luminance step; fix on a low-frequency/Color layer with sampled neck/face tone and D&B, not by blurring.

### Gaps
- No free source with specific numbers for foundation-line blending or contour D&B intensity.

---

## Q8. Clothing/fabric and backgrounds (seamless paper, gradients, banding)

### Takeaway
Clothing: frequency separation (low blur radius relative to weave) + D&B to remove wrinkles while keeping weave texture; clone/heal lint and tags on blank layers. Backdrops: heal wrinkles, D&B with two Curves layers at 1–3% flow, then FS (small radius, e.g., 3 px) to smooth gradations. Banding is mostly a display/8-bit artifact; fix by working 16-bit and adding a small amount of noise (~2–3%).

### Cited Findings
- PHLEARN clothing course sections: change color, remove logos/marks, increase detail/dynamic range, D&B, remove wrinkles, remove/smooth undergarment lines; FS "for achieving a freshly-pressed look" while preserving texture. — [PHLEARN, How to Retouch Clothing & Fabric](https://phlearn.com/tutorial/how-to-retouch-clothing-fabric/)
- FS on fabric: blur middle (low) layer until fabric weave detail disappears. — [search summary of PathEdits / DPS clothing tutorials](https://digital-photography-school.com/remove-wrinkles-from-clothes-in-photoshop/)
- Backdrop: (1) Healing brush on blank layer, Current & Below, for paper wrinkles; (2) two Curves (up/down) with black masks, brush 100% opacity/3% flow or 70%/1%; (3) FS with small blur radius (3 px "relative to my file size") to smooth tone transitions — turn off the darkening curve when sampling. Tags removed with Magnetic Lasso + Stamp. — [Fstoppers, Fashion Editorial Retouching Pt 1](https://fstoppers.com/business/start-finish-fashion-editorial-retouching-part-1-68367)
- Banding: "If you're working with 16 bit data, any banding you see is in your display system"; most monitors are 8-bit or 6-bit+FRC; "The standard advice is to add a tiny bit of noise to break up the banding." — [Adobe Community, Dither and 16-bit won't fix gradient stepping](https://community.adobe.com/t5/photoshop-ecosystem-discussions/dither-and-16-bit-image-mode-won-t-fix-gradient-stepping/td-p/14223179)
- Add Noise ~2–3% to mask banding; enable Dither on gradients. — [Adobe Community, Photoshop CC gradient banding](https://community.adobe.com/t5/photoshop/photoshop-cc-gradient-banding/td-p/5886839) (search summary)

### Inferences
- Agent check for banding: on 8-bit export, examine the histogram of smooth backdrop regions for comb gaps / step edges; add monochromatic Gaussian noise until steps are not visible at 100%.

### Gaps
- No free source verified exact behavior of Photoshop's 16→8-bit conversion dither setting (Color Settings "Use Dither") — not confirmed in this research.
- No specific lint-removal procedure beyond generic clone/heal.

---

## Q9. Final steps: output-specific sharpening, grain/noise to unify texture, banding prevention

### Takeaway
Sharpen last, on a merged layer or Smart Object: Smart Sharpen (Remove: Lens Blur, Amount 150–200%, Radius 0.5–1 px for screen, 1–3 px for print, Reduce Noise ~10%, filter blend mode Luminosity) or High Pass in Overlay (radius 0.2–0.5 px web, 0.3–1.5 px print), masked away from skin. Add monochromatic Gaussian noise at low amounts (~2–3% for banding; up to ~8% to unify composites/retouched areas).

### Cited Findings
- Smart Sharpen: convert to Smart Object; Remove = Lens Blur; Amount 150–200% for most images; Radius 1–3 px for print (up to 4–5 with Lens Blur), 0.5–1 px for screen; Reduce Noise default 10% "often all you need"; set the smart filter blend mode to Luminosity to avoid color artifacts; too-high Radius creates "visible halos". Shadows/Highlights fade radius ~50 px. — [Photoshop Essentials, Smart Sharpen](https://www.photoshopessentials.com/photo-editing/using-smart-sharpen-for-the-best-image-sharpening-in-photoshop/)
- High Pass: Ctrl+Shift+Alt+E stamp merged, Filter > Other > High Pass, Overlay blend, adjust opacity; Radius web 0.2–0.5 px, print 0.3–1.5 px, out-of-focus rescue 2–6 px; sharpening is the final step. — [Damien Symonds, High Pass Filter Sharpening](https://www.damiensymonds.net/tut_hipass.html)
- Larger prints viewed at distance need more sharpening than small glossy prints; projection needs more than web. — [Photoshop Essentials, High Pass](https://www.photoshopessentials.com/photo-editing/sharpen-high-pass/) (search summary)
- Grain: Add Noise 2–8%, Gaussian, Monochromatic checked; ~8% monochromatic Gaussian used to unify composite images; optional 0.5 px Gaussian Blur on the noise layer for film-like softness. — [Aiarty](https://www.aiarty.com/edit-photo/add-grain-in-photoshop.htm); [ProEdu, Using Noise Patterns to Add Grain](https://proedu.com/blogs/news/mo-better-noise-using-noise-patterns-add-grain-image) (search summary)
- Banding: noise ~2–3%; work in 16-bit. — [Adobe Community](https://community.adobe.com/t5/photoshop/photoshop-cc-gradient-banding/td-p/5886839)

### Inferences
- Output mapping for an agent: web (≤2048 px long edge) → resize first, then Smart Sharpen ~100–150%, 0.5 px, Luminosity, masked to eyes/lashes/hair/lips/fabric; print → 1–2 px at output resolution. Check for halos by sampling luminance profile across a high-contrast edge (overshoot should be small and narrow).
- Grain should be added as a separate Overlay/Soft-Light noise layer after sharpening so it is not sharpened itself; amount should make retouched patches statistically match untouched skin noise.

### Gaps
- Greg Benz's web-resizing sharpening page returned empty content; no verified web-specific Smart Sharpen numbers from him.
- Search-snippet claim "web: Amount 100, Radius 1 px, Reduce Noise 10–20%, Lens Blur" could not be traced to a verified primary page ([AskTimGrey](https://asktimgrey.com/2015/02/12/smart-sharpen-settings/) not fetched) — treat as unverified.
