# Publicly Shared Retouching Techniques of Pratik Naik, Natalia Taffarel, and Julia Kuzmenko McKim (second, deeper pass)

Scope note: Only freely accessible pages were used. Several primary sources were not reachable: ModelMayhem forum threads returned 403 or Cloudflare 1005, Pratik's Tumblr blog returned 429, YouTube redirected to a captcha, the Wacom "Color Master" Taffarel page returned 404, and the SLR Lounge Capture One article returned 404. The richest new primary source found is **"Pratik's Retouching Guide"**, a free PDF from The Portrait Masters (https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf), referred to below as "Pratik PDF".

---

## Pratik Naik (Solstice Retouch): exact procedures, settings, layer structure, color, hair/background

### Takeaway
Pratik's free PDF gives exact settings for every tool and a fixed 4-stage order: Cleaning (heal/clone) → D&B (with B&W helper on, zoom 50–70%) → Frequency Separation (Median 2–4) → Color Fix (blank layer in Color mode, then Hue mode). He favors one base layer plus many blank and adjustment layers, uses FS only lightly, and deliberately leaves some color variation in skin. His plugins automate this exact stack, including 11 named help layers. A Capture One link exists only through a webinar description.

### Cited Findings

**Order of operations (stated several times)**
- Interview order: "the overall cleanup of the skin is my general starting point. Anything with the healing and cloning brush goes first", then "dodging and burning till any transitions are evened out", then "I tackle any color issues on the skin by evening that up", and "I leave liquifying and sharpening till the end." — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- Layer philosophy: "I don't use things like frequency seperation very much so I have one base layer, and lots of blank layers and adjustment layers to get to my end goal where it's easily adjustable." — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- PDF workflow: (1) CLEANING FOLDER (healing layer plus Clone layer) → (2) DODGE AND BURN → (3) FREQUENCY SEPARATION → (4) COLOR FIX ("this part becomes the final step"). He starts every image with his "Retouching Setup" action. — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Darker-skin case study: (1) heal and clone the most prominent bumps, and "gently clone a few partially to pull back on how intense some areas are without removing them completely"; (2) D&B "to even out transitions"; (3) balance colors, removing overly saturated areas. "The mindset is keeping the elements that can be minimized, while keeping her natural texture." — [Retouchist: Retouching Darker Skin Tones](http://retouchist.net/blog-1/before-and-after-retouching-darker-skin-tones)

**Global tool rules (PDF)**
- On all retouch layers, set Sample to **"Current and Below"** for the brush, clone and healing tools ("!!!" in original). Work on new layers in **Normal** blend mode so a mask, the eraser or opacity can pull work back. — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- **Healing Brush:** hardness 0%. Pen pressure for Size **Off**. "Sample using the option or alt key and completely cover a blemish completely before letting the healing brush give you the results". Turn on "Use legacy healing brush algorithm" (Preferences > Tools). — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- **Spot Healing Brush warning:** turn help layers OFF first. Spot heal only has "sample all layers", so it picks up the B&W helper and makes "brush strokes black and white and grainy". — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- **Clone Stamp:** hardness 0%, opacity 100%, Shape Dynamics unchecked, Build-up checked. Flow **5–10% "to clone away something gently"** and **20%+ to clone things away quickly**. — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- **Clone "Softening Technique"** for rough texture that must match surrounding skin: 0% hardness, **5% flow**, brush size = size of the texture being evened. "I sample in the same area, move my mouse a few pixels away, and begin brushing. The overlap in texture will diffuse the area nicely." — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- **Brush tool:** hardness 0%, opacity 100%, Shape Dynamics off, Build-up on, **Smoothing 0%**. Eyedropper Sample Size **5×5 Average** so you sample an area, not one pixel. — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)

**Dodge & burn specifics beyond the first pass**
- D&B on brush layers: **1–3% flow** in general, and **"I use a 2% flow, and 100% opacity"** in the workflow section. Shape Dynamics unchecked so pressure doesn't change size: "I personally don't find it very accurate when retouching." — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- **Zoom 50–70%** during D&B, "so that you focus on the larger areas that need to be evened out." — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Two purposes for D&B. (a) Even out "dark or light areas that produce patchy tones across the face and body". (b) Contouring, "where you add dimension", which he does "in another step if it's required" (contouring is a separate pass). — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Typical target areas for corrective dodging: "under the eyes, next to the mouth, on the forehead". D&B is done **before** FS "because it will make smoothing transitions a lot easier." — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Self-check rules (codifiable):
  - **Overshoot:** if a dodged area "gets too bright, that means you went too far". Press X for a black brush and paint back over to undo a few strokes.
  - **Brush-size diagnosis by toggling the layer:** if the area *outside* the target also brightens, the brush is too big. If the *edges* of the target stay as dark as before, the brush is too small.
  - Keep a **black-and-white helper layer** on "because I want to see the tonality."
  — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- **"Negative dodge and burn"** is a term Lance Nicoll says he "first heard from fellow retoucher Pratik Naik". It means minimizing distracting highlights and shadows and smoothing transitional values, while *preserving* form-defining light such as nose width and cheekbone height. Nicoll's settings: two Curves layers (lighten/darken) with black masks, white brush, flow 2–3%, opacity 100%, hardness 0–10%. Toggle undo/redo to verify that shadows *disappear* rather than appear. — [Fstoppers, Lance Nicoll](https://fstoppers.com/commercial/dramatic-beauty-tutorial-part-4-what-negative-dodge-and-burn-73214)

**Frequency separation (Pratik's version)**
- Use the 8-bit or 16-bit FS action to match the document. Use a **"Median" range between 2 to 4**, "a range that makes the image look out of focus to the point where it would look like you just missed focus." — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Low layer = "color and light detail". High layer = texture, edited with healing or clone set to **"Current Layer"** ("If it's set to anything else, it will not work"). A separate **"Brush" layer** evens transitions at **2% flow / 100% opacity**, or with clone set to "Current and Below". The action can be run more than once per image. — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)

**Skin color consistency (Color Fix)**
- Use a blank layer named "Color". "Sample a good skin tone, and then brush over an area you want to match… low flow and 100% opacity so it brushes in slowly." Typical problems: "discoloration from the retouching process" or "the hands may be a different color than the body". — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- Blend-mode decision rule: use **Color first, then Hue** if it doesn't look right. "Hue won't change the saturation of the original image. 'Color' will match the saturation as well." — [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)
- He deliberately leaves "a lot of color variations in the skin intentionally to illustrate a more human element". — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)

**Liquify (end-stage)**
- Run it only on a merged "Merge Visible" layer.
- Forward Warp **Brush Pressure 5–10**, **Density 50%** to start.
- Use Reconstruct as the "undo brush".
- Lower "Show Backdrop" opacity to see "how far you have gone, and how far you can go".
- Use the Smooth tool for wonky strokes.
- Face-Aware sliders "can be abused easily".
— [Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)

**What his plugins automate (a proxy for his process)**
- The Infinite Retouch "Create" button builds "healing layers, dodge and burn layers, color correction, and a wide variety of help layers". One reviewer's customized stack had 26 layers.
- The **11 help layers** are: Invert, Luminosity, Multiply Curve, Level, Contrast Curve, Solar Curve, Color, Hue, Saturation, Shadow Warning, Highlight Warning. Luminosity plus Multiply/Contrast Curve finds blemishes, and Solar Curve finds dust.
- The panel can auto-select the right layer and brush for each FS step.
- It also has a custom sharpening algorithm and "Holy Grain" (grain from high-res film scans).
— [Fstoppers review of Infinite Retouch](https://fstoppers.com/reviews/review-infinite-retouch-portrait-editing-plugin-610653); [Retouchist toolkit overview](http://retouchist.net/blog-1/retouching-toolkit-overview)
- **Infinite Color** (color grading, co-developed with Conny Wallstrom):
  - Generates stacks of **Curves, Color Balance, Selective Color, Gradient Map, and Color Lookup** layers.
  - "Harmonize" builds a **triadic** scheme "based on the highlights in the image, which will allow for harmonious mid-tones and shadows".
  - Has intensity/opacity controls, per-layer shuffle and toggles, and stacking of looks.
  - Naik: "Finding a direction is often the hardest part about color grading."
  — [Fstoppers review of Infinite Color](https://fstoppers.com/review/fstoppers-review-infinite-color-panel-246208); [Infinite Color site](https://infinitecolorpanel.com/)

**Capture One**
- Search-result summaries of an SLR Lounge/Capture One webinar describe:
  - Using the Skin Tone **Uniformity** tab to match skin tones "to provide a more harmonious gradation".
  - Favorite tools: the Advanced Color Editor ("push and pull colors of a specific region"), Color Balance "for overall feel", and the Luma curve (contrast without saturation change).
  - Building with layers, inverted masks, variants and presets.
  The page itself returned 404, so this is snippet-only. — [SLR Lounge (snippet)](https://www.slrlounge.com/pratik-naiks-color-workflow-capture-one/)
- Capture One's generic Skin Tone uniformity procedure (by Phase One staff, **not Naik**):
  1. Mask the skin, avoiding hair, lips and eyes.
  2. Pick the skin tone with the picker.
  3. Use "Span full saturation range" and widen the hue range.
  4. Set Smoothness to max for saturated images.
  5. Set **Uniformity up to 1.0**.
  6. Fine-tune Hue, Saturation and Lightness.
  — [Capture One blog, Christian Grüner](https://www.captureone.com/blog/get-uniform-skintones)

**Judgment and "eye"**
- "Never brighten the eyes too much, remove pores completely, and remove characteristic marks". Study admired retouchers by focusing "on what details they've kept rather than what they've removed. Subtleties are the element of beauty that we all seem to want to get rid of." — [Retouchist / Portrait Masters summaries via search](http://retouchist.net/blog-1/before-and-after-retouching-darker-skin-tones) (quote surfaced in search snippets of Pratik's material; verify against original)
- "the job isn't over when the client is happy, it keeps going till I am happy." — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)

### Inferences
- An agent replicating Pratik should build this stack bottom-up: Base → Healing (blank, Current & Below) → Clone (blank) → D&B Dodge/Burn curves → [contour curves, optional separate pass] → FS Low/High (Median 2–4) + "Brush" blank layer → "Color" blank layer (Color mode, then Hue mode) → Merge-visible for Liquify → sharpen/grain. Put help layers (B&W/luminosity, solar curve, saturation check) above everything, and switch them off for any sample-all tool.
- His FS is narrow (Median 2–4 px). It handles small-scale tone only, and large transitions are fixed earlier by D&B.
- His "partial clone" (reduce, don't remove) and "Color then Hue" rules are concrete, automatable decisions.

### Gaps
- No free source found giving Pratik's explicit hair or background procedures, beyond the clone layer being used "to remove annoying items in the environment" ([Pratik PDF](https://theportraitmasters.com/wp-content/uploads/2019/11/Pratiks-Retouching-Guide-PDF-download.pdf)).
- No retrievable transcript of his Capture One webinars or CreativeLive free segments (YouTube was captcha-blocked). Exact curve shapes for his D&B curves and his contouring pass were not found in free sources.
- His Tumblr review of Taffarel's "Art of Dodge and Burn" could not be fetched (429).

---

## Natalia Taffarel: D&B philosophy, transitions, skin color, hair

### Takeaway
Very little free technical material from Taffarel is currently retrievable. Her depth is in paid DVDs and webinars (X-Rite webinar, "Art of Dodge & Burn", "Beauty & Hair Retouching High End Techniques"). What survives freely: two-curves D&B, a preference for curves/soft light over overlay because of color shift, using the separate D&B masks to drive saturation fixes, a color-matching training exercise, and her philosophy of polishing and removing distractions rather than reshaping.

### Cited Findings
- **D&B method:** two Curves layers, one lightening and one darkening the midtones, both masks inverted, painting with a white brush. She prefers 50% gray Soft Light or two curves, and avoids **Overlay** because it "tends to shift colors more". Overlay gives stronger contrast but discoloration, Soft Light gives less contrast and less color shift, and curves give "far less colour shift". — [Search-engine summary attributed to Fstoppers/ModelMayhem pages](https://fstoppers.com/post-production/professional-retoucher-natalia-taffarel-shows-us-her-techniques-and-workflow-4773). **Caveat:** a direct fetch of the Fstoppers page found only the embedded X-Rite webinar and comments, no written settings. The text likely comes from the ModelMayhem thread ["Natalia Taffarel dropping some DNB Knowledge"](https://www.modelmayhem.com/forums/post/745300/1), which returned 403/1005 and could not be verified.
- **Saturation fix tied to D&B masks:** one stated advantage of separate lighten/darken curves is "having two separate masks that can be applied to different saturation layers", because D&B leaves colors "too saturated or not saturated enough". — same unverified snippet source as above ([ModelMayhem](https://www.modelmayhem.com/forums/post/745300/1))
- **Alternative highlight technique (snippet):** paint white subtly on blank layers, or use Select > Color Range on bright highlights and paint white over the selection, blurring or feathering if transitions are harsh. — [same snippet source](https://fstoppers.com/post-production/professional-retoucher-natalia-taffarel-shows-us-her-techniques-and-workflow-4773) (unverified)
- **X-Rite webinar:** the Fstoppers post says it "showcases some of Natalia's techniques and workflow" and the "mentality and reasoning". A commenter notes her D&B masks look "like monsters", meaning very extensive, dense mask painting. — [Fstoppers](https://fstoppers.com/post-production/professional-retoucher-natalia-taffarel-shows-us-her-techniques-and-workflow-4773)
- **Color training exercise** attributed to her: match a random color three times, using Curves, Selective Color, and Hue/Saturation in turn. — [Search summary referencing Marco Verna's blog](https://marcoverna.studio/blog/2020/8/28/mastering-color-adjustment-levels-exercise) (secondary)
- **Workshop scope** (third-party notes, CS4 era): teeth whitening and straightening, lip redefinition, nose reshaping, eye sharpening, makeup application/removal, "skintone creation and variation", "hair correction and redesign", background, and lighting. She showed it is achievable "with a mouse", and explains "why they are used or why not or when". — [Kris Gironella notes](https://krisgironella.wordpress.com/2011/01/08/natalia-taffarel-high-end-beauty-fashion-retouching-workshop/)
- **Philosophy:**
  - "our job is not to make celebrities prettier; we rarely make people thinner, taller or better looking. What we do is polish the image and get rid of distractions". "Keep it realistic; we try to enjoy looking at textures, deep colours and interesting composition." — [Creative Bloq (via search snippet)](https://www.creativebloq.com/photoshop/taffarel-51411756)
  - "a neurotic, detail maniac, control freak who thinks beauty is shown solely through the details." "Everything has a hidden beauty and it's my job to unleash it."
  - Her printing-family background means "many of the filters that are used in the Photoshop are based on the analogue methods."
  — [OmniPixLab interview](http://omnipixlab.com/en/2014/natalia-tafarel-2/)

### Inferences
- For replication, "Taffarel-style" means: curves-based D&B (not overlay) for minimal hue shift; extensive, high-coverage masks (the "monster masks"); then a dedicated saturation correction keyed to each D&B mask (desaturate burn areas, resaturate dodge areas). Color matching is done with Curves, Selective Color or Hue/Sat as interchangeable tools.

### Gaps
- No free, verifiable source gave Taffarel's brush flow/opacity numbers, helper-layer settings, her "transitions" definition, hair-retouching procedure (flyaways, hair color/shine), or skin color correction steps. These live in paid DVDs ("Art of Dodge and Burn", "Beauty & Hair Retouching High End Techniques") and the X-Rite webinar video, none of which have accessible transcripts.
- The ModelMayhem Q&A threads where she posted technical answers are blocked (403 / Cloudflare 1005), and the Wayback Machine is not fetchable from this environment.
- The Wacom "Color Theory Basics with Natalia Taffarel" page is 404.

---

## Julia Kuzmenko McKim (Retouching Academy): beauty workflow, helper layers, D&B, color, bit depth

### Takeaway
Julia has the most free, well-documented material. It covers:
- The light-physics rules behind D&B.
- Tablet and brush settings.
- Curves setup (keep curves near default), at Opacity 3–5% in her own method or flow 1–3% in the micro-transition article.
- The 50% gray **Color**-mode visual aid (preferred over B&W/Channel Mixer).
- Clipped color-correction layers after D&B.
- An explicit local vs. global D&B split, by zoom 60–200% vs. large strokes.
- FS settings with an empty heal layer between the frequencies.
- Process habits: raw-first, zoom out often, toggle layers.

The brief's premise of an "8-bit sRGB stance" is **contradicted** by her own article: she recommends working in **16 bits/channel**.

### Cited Findings

**D&B theory and decision rules**
- Local D&B evens small patches. Global D&B refines overall shadows, highlights and shape. — [Fstoppers Part 1](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-1-fundamentals-9261)
- Light rules (usable as checks):
  - Highlights sit where direct light hits the surface closest to the light.
  - Midtone rule: "within the area of transitional light the surface further away from the light source cannot be brighter than the surface closer to it".
  - Core shadows cannot exceed transitional-light brightness.
  - Reflected light adds volume and is "often overlooked".
  - "Luminosity inconsistencies" are read by the brain as bumps and hollows.
  — [Fstoppers Part 1](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-1-fundamentals-9261)
- Prerequisite knowledge list: anatomy for artists, physical light distribution, light/shadow in visual arts, current makeup trends, beauty/fashion trends. "knowing how to dodge and burn in Photoshop isn't going to make your work better. Improving your vision, taste…" — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)

**Setup and brush settings**
- Small tablet (e.g., Intuos small), pen mode mapped to the screen, pen tip feel "softest".
- Brush: Spacing **25%**; Shape Dynamics Size Jitter 0%, Control = Pen Pressure, **Minimum Diameter 50%**; Airbrush **OFF**.
- Opacity vs flow: Julia prefers lowering **Opacity** with Flow 100% (lifting the pen between strokes). Woloszynowicz/Naik lower **Flow** with Opacity 100%. "it depends on your style".
— [Fstoppers Part 2](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-2-setting-good-start-9262)
- If using native Dodge/Burn tools: Exposure **1–10%**, **Protect Tones ON**, range set per Shadows/Midtones/Highlights, on a 50% gray Soft Light layer. Afterwards add a Hue or Color mode layer to fix over-saturation. — [Fstoppers Part 2](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-2-setting-good-start-9262)
- Curves D&B: name the layers "Dodge"/"Burn" with black masks. "You don't want to pull the Curves too far away from their default position because then even with the lowest brush Opacity/Flow your brush strokes will be too intense." Brush **Opacity 3–5%**, soft, build up with many strokes. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- Zoom split: **local D&B with "tiny dots/lines at 60–200% zoom"**, global sculpting with large soft strokes. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)

**Helper / visual-aid layers**
- Preferred: a **50% gray layer in Color blend mode** above the D&B curves, which gives accurate luminosity without color. The older Channel Mixer Monochrome or Black & White adjustment can "show false targets". — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- Micro-transition setup: a **darkening/contrast Curves** layer plus a **50% gray Color-mode** layer as the visual aid. The Beauty Retouch Panel's "Visual Aid" button automates darkening plus desaturation. — [Retouching Academy: Micro Transitions](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)

**Micro transitions**
- Definition: "caused by the slightest shift or divot on the surface of the skin".
- Brush: Opacity 100%, **Flow 1–3%**, **Hardness 0–30%**, size "slightly smaller than blemish OR approximately same size".
- Dodge the darker micro-patches, burn the lighter ones, and **vary zoom levels** (don't stay fully in or fully out).
- "Over smoothing" is "the number one culprit of poor retouching".
— [Retouching Academy: Micro Transitions](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)

**Color after D&B**
- Clip Hue/Saturation, Selective Color, or a Color-mode layer to the D&B curves to fix "dodged areas appearing desaturated, burned areas appearing over-saturated, hue shifts". — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)

**Frequency separation** (Retouching Academy article with Julia's notes; the main author may be a guest)
- Layers: "texture" over "color". Gaussian Blur radius **6** (or as needed), and Julia notes Median "creates cleaner outer edges".
- Apply Image, **16-bit**: Layer color, RGB, Invert ON, **Add**, 100%, Scale 2, Offset 0.
- Apply Image, **8-bit**: Invert OFF, **Subtract**, Scale 2, Offset 128.
- Texture layer set to Linear Light. Patch tool on texture, avoiding pulling from overly smooth areas.
- Color layer: brush Opacity 100%, **Flow 4–6%**, sampling neighboring tones.
- Tip: put an **empty layer between color and texture** for healing.
— [Retouching Academy FS](https://retouchingacademy.com/simplifying-skin-retouching-with-frequency-separation/)

**Bit depth (corrects the brief's premise)**
- "Work in the 16 bits/channel color mode to avoid banding". Masterfile is a 16-bit PSD. 8-bit is acceptable only for client previews, for filters that are unavailable in 16-bit, or for downsized images without gradients. Deliver print as TIFF with no compression. A JPEG saved from 16-bit is actually 8-bit. The article does not address sRGB vs Adobe RGB. — [Retouching Academy: Bit Depth](https://retouchingacademy.com/qualities-of-digital-images-bit-depth/)

**Process and judgment habits**
- Refine the Raw (brightness/contrast) in Lightroom or Capture One before Photoshop. Stop pixel-peeping: view the whole face regularly and zoom in only for small details. Frequently toggle layers. Fix deviations with layer opacity, masks, or a mask on a group.
- Over-retouching list: over-brightened eye whites and teeth, over-contouring, over-sharpening, Liquify without anatomy knowledge, over-polished skin.
- Calibrate taste against cosmetics advertising (Sephora, magazines). Calibrate the monitor regularly (Spyder X Elite).
— [JKM: 5 Common Retouching Mistakes](https://juliakuzmenko.com/5-common-retouching-mistakes/)
- Her actions became the RA "Beauty Retouch" panel (v5, with AI-assisted features, which are not relevant here). — [Search summary of RA Lab / juliakuzmenko.com](https://retouchingacademylab.com/)

### Inferences
- Julia's stack for agent replication:
  - Raw global correction first.
  - Healing (empty layer, or FS with an empty heal layer between).
  - Dodge/Burn curves near default.
  - Clipped Hue/Sat or Selective Color per D&B layer.
  - Global sculpt curves as a separate pass.
  - Visual aids on top: a darkening curve plus 50% gray Color mode.
  - Work in 16-bit.
- Her "farther-from-light cannot be brighter than closer-to-light" rule is a testable constraint. An agent could check luminance gradients along surface normals relative to the key light direction.

### Gaps
- Her JKM blog "updated workflow" series (Part III "before retouching even begins") pages fetched without the actual steps. The detailed workflow articles were not retrieved.
- No exact curve point values were published, only "slightly" up or down.
- The opacity values conflict across her articles: Part 3 gives 3–5% opacity, while the Micro Transitions article gives flow 1–3% at opacity 100%. Both are valid in her framing ("depends on your style").

---

## What the three say distinguishes elite from average retouching (visible qualities)

### Takeaway
All three converge on the same visible markers:
- Texture and pores are preserved, with no over-smoothing.
- Transitions are even at both micro and macro scale, without flattening form-defining light.
- Natural color variation is retained, but there are no blotches or D&B-induced saturation shifts.
- Restraint on eyes, teeth, contour, sharpening and liquify.
- The subject still looks like themselves.

### Cited Findings
- **Pratik:**
  - Keeps characteristic marks, pores and natural eye brightness. Learn by noticing "what details they've kept rather than what they've removed". — [Pratik material via search summary](http://retouchist.net/blog-1/before-and-after-retouching-darker-skin-tones)
  - Leaves deliberate skin color variation for "a more human element". — [Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
  - Minimizes rather than removes ("keeping the elements that can be minimized"). — [Retouchist darker skin](http://retouchist.net/blog-1/before-and-after-retouching-darker-skin-tones)
- **Julia:**
  - "Over smoothing" is "the number one culprit of poor retouching". — [RA Micro Transitions](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
  - Over-whitened eyes and teeth, over-contouring, over-sharpening, liquify without anatomy, and over-polishing mark amateur work. — [JKM 5 mistakes](https://juliakuzmenko.com/5-common-retouching-mistakes/)
  - Vision and taste matter more than technique. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- **Taffarel:** "polish the image and get rid of distractions", not reshape. "Beauty is shown solely through the details". — [Creative Bloq](https://www.creativebloq.com/photoshop/taffarel-51411756); [OmniPixLab](http://omnipixlab.com/en/2014/natalia-tafarel-2/)
- **Negative D&B (Naik's term):** remove distracting highlights and shadows while keeping those that define structure (nose width, cheekbone height). — [Fstoppers, Nicoll](https://fstoppers.com/commercial/dramatic-beauty-tutorial-part-4-what-negative-dodge-and-burn-73214)

### Inferences
- An agent's QA checklist could include:
  1. Is high-frequency texture energy on skin preserved vs. the original?
  2. Are there no new halos or patchiness at 50–70% zoom (Pratik's working zoom)?
  3. Is D&B saturation drift corrected (burned areas not oversaturated, dodged areas not grey)?
  4. Do eye whites and teeth stay below "bright white" and keep their natural shading?
  5. Are identity-defining marks and form shadows intact?
  6. Does the luminance ordering obey the light-direction rule?

### Gaps
- None of the three give numeric thresholds for "too bright" eye whites or teeth, or for allowable saturation variance. These remain visual judgments in all free sources found.
