# High-End Retouching: Workflows, Philosophies, and Quality Standards (beauty / fashion / advertising)

Scope note: These notes target an AI agent that retouches using only traditional non-destructive methods (curves, masks, dodge & burn, healing/clone, frequency separation, color grading, crop/rotate). Research was done October 2026 with roughly 20 search/fetch calls. Many top retouchers teach mainly through paid video courses (CreativeLive, Fstoppers store, PRO EDU, The Portrait Masters, X-Rite webinars). Those courses are not transcribed publicly, so some named retouchers have thin coverage here (see the Gaps sections).

---

## 1. Step-by-step workflows of known high-end retouchers (order of operations, layer stacks, file setup)

### Takeaway
Every documented pro workflow follows the same skeleton:
1. Raw/global correction (exposure, white balance, lens corrections, crop with room to spare).
2. Cleanup with healing/clone on separate pixel layers.
3. Corrective ("micro") dodge & burn with Curves adjustment layers and masks.
4. Contouring ("macro") dodge & burn.
5. Local color correction of skin.
6. Color grading.
7. Shape work (liquify), then sharpening and grain at the very end, for output.

Pixel layers sit at the bottom and adjustment layers above them, with no stamping or rasterizing above adjustments. 16-bit is used when there are subtle gradations or the work is editorial/commercial.

### Cited Findings

**Michael Woloszynowicz (Vibrant Shot) — the most fully documented public workflow (Capture One blog)**
- Four macro stages: (1) tethered capture into Capture One Pro, (2) raw processing in Capture One, (3) skin retouching in Photoshop, (4) output through a PSD round-trip back into Capture One. — [Capture One blog: Portrait & beauty retouching workflow](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Tethered-stage goal: "achieving a look that as closely resembles the final output as is possible – excluding of course the actual skin retouching portion." — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Raw settings he gives:
  - Avoid the Contrast slider. Use Levels/Curves instead, pulling the shadow and highlight handles inward to stretch the histogram.
  - Use the shadow/highlight sliders sparingly on portraits.
  - Overexpose by 1/3 stop if needed for shadow detail, then pull highlights back in software.
  - Set white balance from a gray card first, then refine exposure, because the two interact.
  - Clarity ("natural" mode): portrait values should "typically be under 6 or 7"; at the final round-trip stage use "1–4" for mid-tone contrast.
  
  — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Skin-tone uniformity sliders: keep adjustments minimal and "refrain from pushing this too far as it can start to blend lip tones, clothing or other makeup colors." Strong saturation uniformity flattens the face. — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Make drastic white-balance or look decisions in the raw file, not on the PSD: "if I'm going for a very cool look, it's best to do so in the raw file rather than off the PSD in Photoshop." — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Raw-stage cleanup: lens corrections (remove vignettes, fix keystone) for a "clean neutral look." Crop with "wiggle room" for multiple output ratios (4×5 for Instagram and magazines). Crop away unneeded areas in advance "to save yourself the time of retouching that area." — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Bit depth: export to Photoshop in **16-bit for editorial, commercial, or images with subtle gradations**, and 8-bit otherwise. — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Photoshop order:
  1. Cleanup (healing brush / clone stamp: blemishes, stray hairs, sensor spots).
  2. Optional subject extraction.
  3. Corrective dodge & burn with Curves adjustment layers and masks, to smooth tonal transitions.
  4. Contouring dodge & burn (also Curves plus masks).
  5. Color correction of mismatched skin tones (Hue/Saturation and Selective Color with feathered masks).
  6. Color grading.
  
  — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Layer-stack rules:
  - "Perform all your raster/pixel based adjustments at the outset on separate layers."
  - Put all adjustment layers above the raster layers.
  - Avoid stamping or rasterizing above adjustment layers, so client changes don't force rework.
  - "The key thing to focus on within your workflow is flexibility."
  
  — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Finishing is done on output variants, not the master PSD:
  - Grain goes on the final output, not the base PSD. Zoom in close to judge it. Use more grain for black and white, and vary it by output size.
  - Sharpening: start at 100% zoom, then scale back. Judge it with "Recipe Proofing" (an on-screen preview of the export settings).
  - Clone a variant before applying a print ICC profile.
  - Example outputs: editorial print 8.5×11 at 300 dpi TIFF with a specific profile; Instagram 4×5 at 2048 px long edge JPG; agency portfolio 9×12 at 300 dpi.
  
  — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Series consistency: apply the grade to the first image, copy it across the other looks, then fine-tune. Print contact sheets to check on paper. — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Dodge & burn "almost always precedes color grading" in his workflow. — [search summary of Fstoppers/Vibrant Shot course listing](https://fstoppers.com/product/color-grade-beauty-fashion-and-portrait-retouching-michael-woloszynowicz)

**Pratik Naik (Solstice Retouch)**
- Order for fashion/beauty:
  1. Skin cleanup (healing and clone first).
  2. Dodging and burning "to even out transitions."
  3. Color correction of skin tone issues.
  4. Liquify and sharpening, kept for the final stages.
  
  — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- He describes a "very clean and simple" stack: one base layer plus multiple blank and adjustment layers. The same interview reports he **avoids frequency separation**. — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- He prefers raw files as input. He switches to TIFF when a client often asks for changes. He works with a stylus. — [Richard Waine interview](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
- His CreativeLive course syllabus lists: Camera Raw → beauty image → Healing Brush → Content-Aware → Dodge & Burn → Frequency Separation → Color Correction → Contouring → Sharpening → Color Toning. He also sells actions that build an initial "game plan" layer set (adjustment layers, masks, curves) in one click. — [CreativeLive course listing via search](https://www.creativelive.com/class/art-business-high-end-retouching-pratik-naik/lessons/retouching-workflow-fashion)

**Julia Kuzmenko McKim (Retouching Academy / Master Beauty Photography)**
- Before retouching begins:
  - Rate and compare the set: "most likely it's not your best images that the world ends up seeing if you don't have a proper rating."
  - Raw-process in Lightroom, non-destructively, with Virtual Copies and synced settings for a cohesive set.
  - Use the Shadows/Highlights and Whites/Blacks sliders to optimize tonal range before any pixel work.
  
  — [Master Beauty Photography: "My Beauty Retouching Workflow — Before Retouching Even Begins (Part III)"](https://masterbeautyphotography.com/my-beauty-retouching-workflow-before-retouching-even-begins-part-iii/)
- After raw: assess the whole image and its details, then retouch skin, makeup and hair. — [search summary of her interview/eBook pages](https://121clicks.com/tutorials/digital-photo-retouching-beauty-fashion-portrait-photography-ebook/)
- Color space and bit depth: according to search-result summaries of her writing, she "prefers to work in sRGB and 8-bit whenever possible" depending on final use and image content. Her Beauty Actions include frequency separation presets for both 8- and 16-bit. This conflicts with the common "always 16-bit ProPhoto" advice. — [search summary, Master Beauty Photography color management article](https://masterbeautyphotography.com/color-theory-color-management-for-digital-photography/) (not directly fetched; treat as moderately reliable)
- The Retouching Academy Beauty Retouch Panel (v5) structures work into five phases: Initial Cleanup → Skin & Tone Work → Detail Refinement → Adding/Adjusting Elements → Quality Control & Export. — [Retoucher of the Year blog on RA panel v5](https://retoucheroftheyear.com/blog/ra-beauty-retouch-panel-v5)
- The RA Professional Skin Retouching course sequence: raw processing → basic cleanup → frequency separation → dodge & burn, both local "Micro" and global "Contouring" → color corrections. Teaching emphasis is on avoiding destructive changes and organizing PSDs. — [Retouching Academy: Professional Skin Retouching](https://retouchingacademy.com/product/skin-retouching/)

**Natalia Taffarel**
- Dodge & burn method: two Curves adjustment layers, one brightening the midtones and one darkening them, each with an inverted (black) mask. She paints white on each mask to dodge or burn. She explains the reasoning behind each step, not only the steps (X-Rite webinar, D&B at about 38 minutes). — [Fstoppers: Natalia Taffarel shows techniques and workflow](https://fstoppers.com/post-production/professional-retoucher-natalia-taffarel-shows-us-her-techniques-and-workflow-4773)

**Amy Dresser**
- Workflow: a quick first pass to find dust and acne, then basic color adjustments and small changes, with no non-realistic manipulation. She reportedly spends **about 80% of her time on dodge & burn** and uses Curves for color. — [FixThePhoto review summarizing Dresser](https://fixthephoto.com/amy-dresser-retouching-review.html) (secondary source)
- She sculpts with shadows and highlights and evens skin tone "rather than clipping someone's body into a smaller silhouette." — [FixThePhoto review](https://fixthephoto.com/amy-dresser-retouching-review.html)
- She describes her process as "relatively simple": remove distractions, then pull channels up and down to explore color directions. — [Brian Smith / PhotoShelter webinar page](https://briansmith.com/retoucher-amy-dresser-photoshelter-interview/)

**Frequency separation settings (where it is used)**
- 16-bit Apply Image for the high-frequency layer: Layer = low-frequency (blurred) copy, Channel RGB, **Invert checked, Blending Add, Scale 2, Offset 0**.
- 8-bit: **Invert unchecked, Subtract, Scale 2, Offset 128**.
- Set the texture layer to **Linear Light**.
- A Gaussian blur "radius of 6 is acceptable" for the color/low layer, adjusted per image so blemishes disappear without losing detail.

— [Retouching Academy: Simplifying Skin Retouching With Frequency Separation (Anita Sadowska)](https://retouchingacademy.com/simplifying-skin-retouching-with-frequency-separation/)
- Warnings in the same tutorial: patching from overly smooth areas makes skin "look too waxy or flat," and heavy low-frequency color correction can "overly blur the final product." — [Retouching Academy](https://retouchingacademy.com/simplifying-skin-retouching-with-frequency-separation/)

**Dodge & burn layer mechanics (common practice)**
- Two Curves layers (brighten / darken), each with a black inverted mask, painted with a soft white brush at **about 1–4% flow**. — [search summary of RetouchPRO / PSDVault / SLR Lounge D&B tutorials](https://www.slrlounge.com/how-to-micro-dodge-burn-skin-in-adobe-photoshop/)

### Inferences
- Canonical order for the agent, consistent across Woloszynowicz, Naik, RA, and Dresser:
  1. Global raw/base correction (WB, exposure, lens, crop with margin).
  2. Cleanup with healing/clone on empty "sample all layers" pixel layers.
  3. Optional frequency separation, only for color/tone blotches.
  4. Micro dodge & burn.
  5. Macro/contour dodge & burn.
  6. Local color correction (skin redness/yellow, eye whites, teeth).
  7. Global color grade.
  8. Liquify, if allowed.
  9. Output sharpening and grain, per output size, on a copy.
- Keep pixel layers at the bottom and adjustments on top, and never stamp above adjustments. That way any stage can be revised without redoing later ones.
- Frequency separation is optional or contested at the top end (Naik reportedly avoids it). An agent should treat it as a tool for low-frequency color/tone blotches, not as a skin "smoother."

### Gaps
- I found no publicly accessible, transcribed workflows from **Viktor Fejes, Sef McCullough, Calvin Hollywood, or Aaron Nace/PHLEARN** in this session. Their methods live mainly in paid video courses. Nothing specific is attributed to them here.
- I did not access Scott Kelby's *Professional Portrait Retouching Techniques* or Katrin Eismann's *Photoshop Restoration & Retouching* directly.
- Layer **naming conventions** were not documented in any fetched source. Common community practice ("Cleanup", "D&B Micro", "D&B Macro", "Color", "Grade", "Sharpen", grouped into folders) is unverified here.
- ProPhoto RGB vs Adobe RGB as working space: no fetched primary source states a top retoucher's explicit choice. McKim reportedly prefers sRGB/8-bit when output allows, and Woloszynowicz prescribes 16-bit for editorial/commercial work.

---

## 2. Deciding what to remove vs keep; working with briefs and art directors

### Takeaway
Top retouchers remove what is distracting or temporary: blemishes, stray hairs, dust, sensor spots, redness, color mismatches. They keep identity-defining features such as moles, freckles, and character lines unless the brief says otherwise. The guiding question is "does this help the image's message?", and the brief or art director's markup has final say on scope.

### Cited Findings
- Naik's goal is to make subjects appear "the way I remember them in person, which is usually their definable features without anything that takes away from it." He finds targets by "zooming in and out and seeing what stands out and catches my eye." — [Richard Waine interview](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
- Naik's boundaries: never excessively brighten eyes, completely remove pores, or eliminate characteristic facial marks, *unless it's beauty or fashion work*. "If it's meant to be realistic, keep the adjustments realistic." — [Richard Waine interview](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
- Naik calls himself "skin obsessed." He deliberately **preserves color variation in skin to convey humanity**, departing from the traditional evening-out approach, but only when that fits the client's vision. — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- Client communication (Naik): he prefers **marked-up JPGs indicating focus areas or written lists**. "Retouchers are like robots in the sense that we can do most things, as long as you feed the information in properly." He prefers working directly with photographers. — [Richard Waine interview](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
- Amy Dresser's motto: don't make an image perfect. Keep the character and remove whatever distracts, to help the message. Her method is like "polishing marble with your pinky," taking away the minimum amount possible. — [FixThePhoto review summarizing Dresser](https://fixthephoto.com/amy-dresser-retouching-review.html); see also [Fstoppers: Amy Dresser on the various intentions of retouching](https://fstoppers.com/video/retoucher-amy-dresser-speaks-about-various-intentions-retouching-4478)
- The Getty Images 2017 creative policy bans body-shape changes but still allows changes to hair color, nose shape, skin and blemishes. This is an industry signal for where the "acceptable" line sits. — [Refinery29](https://www.refinery29.com/en-us/2017/09/174162/getty-ban-digitally-altered-photos-slimmed-models); [Digital Trends](https://www.digitaltrends.com/photography/getty-bans-photoshopped-bodies-in-stock/)

### Inferences
- Agent rule set:
  - **Remove** temporary or distracting features: active blemishes, scratches, bruises, stray and flyaway hairs crossing the face, dust/lint, sensor spots, under-eye discoloration (reduce, don't erase), makeup flaws, and redness.
  - **Keep** permanent identity features (moles, freckles, scars, natural asymmetry, expression lines) unless the brief explicitly calls for full beauty polish.
  - **Reduce rather than remove** wrinkles and under-eye bags: lower contrast, don't erase.
- Scope should depend on genre:
  - Portrait/editorial: minimal.
  - Beauty/cosmetics: maximal skin polish, but texture is always preserved.
  - Fashion: garments and silhouette receive equal attention.
- Without a brief, default to "realistic" (Naik) and the minimum-removal principle (Dresser).

### Gaps
- No primary source in this session gave a formal written brief template or art-director round structure (for example, number of revision rounds). The guidance on markups and lists comes from Naik only.

---

## 3. How they evaluate their own work (zoom, flip, step away, toggle, compare, output size)

### Takeaway
Pros check their work in several ways:
- Alternate zoom levels: 100% or more for cleanup, fit-to-screen or output size for the overall gestalt.
- Toggle layers and groups against the original.
- Use temporary "helper/check" layers (grayscale, solarize, midrange-peak, negative) to reveal blotches and dodge & burn errors.
- Proof at final output settings.
- Hold a personal standard above client approval.

### Cited Findings
- Naik finds problems by "zooming in and out and seeing what stands out and catches my eye." — [Richard Waine interview](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
- Naik's standard for "finished": "Usually the job isn't over when the client is happy, it keeps going till I am happy." — [The Retouchist interview](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- Naik also says to work efficiently: "Do what you're there to do, and move on." — [Richard Waine interview](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
- Helper layers (Scott Valentine via KelbyOne Insider):
  - **Solarization:** a Curves layer with about 4 points at roughly 1/4 intervals, alternately dragged up and down. It exaggerates blemishes and reveals healing, cloning, and dodge & burn artifacts.
  - **Midrange peak:** a Curves layer with the midpoint dragged up and the top-right anchor pulled down, with the white slider moved slightly left and the black slider slightly right. It shows gradient smoothness and is "best for skin texture evaluation."
  - **Luminosity:** a Solid Color fill at Saturation 0%, Brightness 50%, in **Color** blend mode. It removes color so you see only luminance during dodge & burn.
  - **Negative:** an inverted Curves layer. It reveals harsh transitions and over-corrections. Toggle it periodically rather than leaving it on.
  - Group all helpers and toggle the group to see cumulative progress.
  
  — [KelbyOne Insider: Using Helper Layers When Retouching (Scott Valentine)](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)
- The dodge & burn check from the same tutorial cluster: toggle the D&B layer on and off every few minutes. "If the difference is dramatic, you've gone too far — the goal is for the image to feel it has great light, not to see the brushwork." A temporary Black & White adjustment layer above the D&B makes tonal shifts easier to see. — [search summary of photoshoptutorial.com D&B articles](https://photoshoptutorial.com/posts/dodge-and-burn-in-photoshop-the-manual-shading-technique-that-makes-retouching-l/)
- Woloszynowicz:
  - Judge sharpening first at 100%, then scale back.
  - Use recipe/soft proofing to preview final output, including sharpening and print ICC profiles.
  - Zoom in close to judge grain.
  - Print contact sheets to verify color consistency across a series.
  
  — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Kristina Sherk's heuristic: if the skin "still has pores (for the most part), it means that the retouching has been done well." Across sources the idea recurs: if the first thing you notice is the retouching, it has gone too far. — [KelbyOne Insider: Top Three Signs of Over-Retouching (Kristina Sherk)](https://insider.kelbyone.com/top-three-signs-of-over-retouching-and-how-to-protect-yourself-by-kristina-sherk/)
- Retouching Academy (Kendra Paige) names a **disproportionate amount of detail** as a failure. Perfecting some areas while neglecting others creates imbalance, so evaluation must cover the whole frame evenly. — [Retouching Academy: Six Mistakes to Avoid While Retouching](https://retouchingacademy.com/six-mistakes-to-avoid-while-retouching/)

### Inferences
- An automated evaluation loop for the agent:
  1. Compare before and after at fit-to-screen and at the intended output size.
  2. Inspect at 100% (and 200% for cleanup seams).
  3. Run solarize, luminosity (desaturated), and negative checks for dodge & burn blotches and healing seams.
  4. Confirm pores are still visible across all skin regions.
  5. Check that texture is consistent between areas.
  6. Check that the dodge & burn toggle difference is subtle.
  7. Check that detail is evenly distributed across the frame.
- "Finished" means:
  - Every item in the brief is done.
  - No artifact is visible at output size.
  - No retouching is noticeable at first glance.
  - Helper-layer checks show smooth transitions.
  - Images in a series are consistent.

### Gaps
- Flipping the canvas horizontally (a standard practice for resetting the eye) and "stepping away" were not explicitly sourced from a named top retoucher in this session.

---

## 4. Recognized signs of over-retouching and the trend toward natural retouching

### Takeaway
The canonical tells are:
- loss of pores and texture (plastic or waxy skin);
- glowing, "radioactive" eye whites and over-saturated, over-dodged irises;
- over-whitened gray or textureless teeth;
- flat faces from ignoring 3D light;
- "sticker-like" makeup features;
- anatomically impossible reshaping (missing knuckles, knees, ribs);
- over-saturated "Cheetos orange" skin;
- uneven levels of detail across the frame.

The industry direction (2017 onward, backed by laws and brand policies) is toward visible texture, preserved identity features, and no body-shape changes.

### Cited Findings
- **Eye whites:** the tell is "eye whites that have been brightened to the point of looking radioactive." The fix:
  - Remove veins with clone or heal.
  - Reduce red contamination.
  - Shift yellow toward blue with Color Balance in Highlights mode: add Cyan/Blue, reduce Red/Yellow.
  - Brighten only the inner area near the iris, avoiding the corners, so the eyeball's shading and 3D form stay intact.
  
  — [KelbyOne Insider (Kristina Sherk)](https://insider.kelbyone.com/top-three-signs-of-over-retouching-and-how-to-protect-yourself-by-kristina-sherk/)
- **Teeth:** correct the color instead of brightening. Use Selective Color: in Whites, add a little Cyan and remove nearly all Yellow; repeat in Yellows. Mask to the teeth only. — [KelbyOne Insider (Kristina Sherk)](https://insider.kelbyone.com/top-three-signs-of-over-retouching-and-how-to-protect-yourself-by-kristina-sherk/)
- **Skin:** "If all of the pores are gone, then this is a big red flag, and it screams over-retouching." — [KelbyOne Insider (Kristina Sherk)](https://insider.kelbyone.com/top-three-signs-of-over-retouching-and-how-to-protect-yourself-by-kristina-sherk/)
- Retouching Academy's six mistakes (Kendra Paige):
  1. Texture loss: "pores vanish, hairs blur together… your subject has been rendered into plastic."
  2. Eyes and teeth losing realism: the iris should not be "overly saturated with color, nor… appear to glow due to intense dodging"; over-whitened teeth turn "gray and unappealing."
  3. Failing to think in 3D: flat images, with eyebrows and lips looking "sticker-like."
  4. Distorted shapes: "missing knuckles, knees, and ribs," or "bad Photoshop plastic surgery."
  5. Over-saturation: pushing saturation "from 0 to 100 will turn most skin… straight to Cheetos orange."
  6. Disproportionate detail across the image.
  
  — [Retouching Academy: Six Mistakes to Avoid While Retouching](https://retouchingacademy.com/six-mistakes-to-avoid-while-retouching/)
- Frequency separation misuse: waxy or flat skin from patching smooth areas, and blur from heavy low-frequency correction. — [Retouching Academy FS tutorial](https://retouchingacademy.com/simplifying-skin-retouching-with-frequency-separation/)
- Raw-stage over-processing (Woloszynowicz):
  - Over-pushed skin-tone uniformity blends lip, makeup and clothing colors and flattens the face.
  - Clarity above about 6–7 is too much for portraits.
  - Over-sharpening looks harsh.
  
  — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- Natural-retouching philosophy at the top end:
  - Naik keeps skin color variation "to convey humanity" and never fully removes pores outside beauty/fashion work. — [The Retouchist](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin); [Richard Waine](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
  - Dresser takes away "the minimum amount" and sculpts with light instead of slimming silhouettes. — [FixThePhoto](https://fixthephoto.com/amy-dresser-retouching-review.html)
- Brand trend:
  - CVS "Beauty Mark" (launched 2018) watermarks imagery not "materially altered." It defines material alteration as changes to shape, size, proportion, skin or eye color.
  - CVS reported that more than 80% of beauty images across its roughly 8,000 stores appeared without material alteration.
  
  — [CVS Health press release](https://www.cvshealth.com/news/pharmacy/cvs-pharmacy-launches-first-campaign-featuring-unaltered-beauty.html); [Forbes 2020](https://www.forbes.com/sites/laurendebter/2020/10/08/cvs-now-labels-all-photoshopped-images-in-its-beauty-aisle-while-other-stores-are-still-covering-up/) (figures as summarized in search results)

### Inferences
Concrete over-retouching tests the agent can run:
- High-frequency energy in skin areas compared with the original. A large drop means texture was lost.
- Halo detection along high-contrast edges after dodge & burn or curves.
- Eye-white luminance and saturation compared with the surrounding skin. Eye whites should never clip to pure white and should keep a gradient toward the corners.
- Teeth checks: no clipping, luminance not far above the eye whites, some texture kept.
- Skin saturation and hue within a plausible range.
- Background lines near any warped area should stay straight.
- Texture scale should match between healed and unhealed regions, with no patched-in texture of the wrong size.

### Gaps
- No quantitative thresholds from a named pro (for example, "eye whites never above L=x"). Numbers like these would have to be calibrated empirically.
- Liquify-induced background warping is widely cited informally, but no named-pro source was fetched for it in this session.

---

## 5. Time per image and task prioritization

### Takeaway
Pratik Naik reports **15 minutes to 2 hours per image**, scaling with resolution and the realism target. Pros prioritize by impact: global fixes and cleanup first, then dodge & burn (the bulk of the time), then color, with finishing last. They aim for even detail across the frame rather than perfecting one area.

### Cited Findings
- Naik: 15 min to 2 h depending on complexity. **100 MP files that require pixel-perfect work** differ from **30 MP files that "should stay more realistic."** — [Richard Waine interview](https://richardwainephotography.com/blog/interview-with-a-retoucher-spotlight-on-pratik-naik/)
- Amy Dresser spends about 80% of her time on dodge & burn. — [FixThePhoto](https://fixthephoto.com/amy-dresser-retouching-review.html) (secondary)
- Woloszynowicz:
  - Efficiency is "just as important as the quality of your final image."
  - Push as much as possible to tethered and raw stages so Photoshop time goes to skin.
  - Crop early so unused areas are never retouched.
  - Copy grades across a series.
  
  — [Capture One blog](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)
- McKim: rate and select before retouching, and sync raw settings across Virtual Copies, so effort goes only to the strongest frames. — [Master Beauty Photography Part III](https://masterbeautyphotography.com/my-beauty-retouching-workflow-before-retouching-even-begins-part-iii/)
- Distributing effort evenly is part of quality, since disproportionate detail is listed as a mistake. — [Retouching Academy](https://retouchingacademy.com/six-mistakes-to-avoid-while-retouching/)

### Inferences
- Compute budget for the agent:
  - Most effort on dodge & burn and transitions.
  - Moderate effort on cleanup.
  - Light effort on color grade.
  - Scale detail effort to the intended output resolution. Billboard or 100 MP beauty needs pixel-level work. Web or social at 2048 px long edge needs less micro-work and more realism.

### Gaps
- No sourced per-genre breakdown (for example, beauty close-up vs full-length fashion vs ad composite) beyond Naik's range.

---

## 6. Ethics and industry norms (body reshaping, disclosure laws)

### Takeaway
Legal and industry lines center on **body shape/size changes**, and in Norway also skin and facial features. Skin cleanup, blemish removal, and color changes are generally exempt.
- **France** (2017; extended to influencers in 2023) requires "photographie retouchée" labels on commercial images with altered body silhouettes.
- **Norway** (since 1 July 2022) requires a standardized "retusjert person" label on ads where body size, shape or skin has been altered.
- **Getty** (2017) bans body-shape retouching in creative content.
- **CVS** labels unaltered beauty imagery.

### Cited Findings
- **France (law effective 1 Oct 2017):**
  - Commercial photos of models digitally altered to look thinner or thicker must carry "photographie retouchée."
  - Skin smoothing, blemish removal, and hair color changes are excluded.
  - Fine: at least €37,500, or 30% of advertising costs.
  
  — [Retouching Academy: New French Law Requires Label](https://retouchingacademy.com/new-french-law-requires-label-for-retouched-images/); [NPR](https://www.npr.org/sections/thetwo-way/2017/09/30/554750939/france-aims-to-get-real-retouched-photos-of-models-now-require-label)
- **France (2023):** labeling of filtered or retouched influencer images became mandatory, with reports of possible jail time for non-compliance. — [Hypebeast](https://hypebeast.com/2023/3/france-labeling-influencers-filtered-retouched-photos-mandatory-info); [Springtide Magazine](https://springtidemag.com/2023/03/30/influencers-in-france-could-face-jail-time-for-not-labelling-digitally-altered-photos/) (details not verified from the law text)
- **Norway (Marketing Control Act amendment adopted June 2021, in force 1 July 2022):**
  - Ads containing retouched images or videos of people must be labeled.
  - The trigger is a body with modified size, shape or skin, whether altered digitally or physically before the shot.
  - The label is a round "retusjert person" mark covering about 7% of the image area, placed top left by default, with contrast against the background. In video it must stay visible throughout.
  
  — [CLP law firm](https://www.clp.no/en/news/new-requirements-for-labelling-of-retouched-photos-back-and-forth-by-the-consumer-authority-what-is-the-current-status); [search summary incl. advokats.no / It's Nice That](https://www.itsnicethat.com/news/norway-ministry-of-children-and-family-affairs-marketing-act-advertising-300621)
- **Norway guidance revision (August 2022):**
  - After backlash, the Consumer Authority narrowed the scope to edits that create body-image pressure.
  - Labeling triggers: changes to body shape, size or skin, facial features (shape or size of eyes, teeth, eyebrows, lashes), and hair shape or size.
  - Exempt: brightness, contrast, shadows and temperature that create no body-image pressure; color changes to hair, teeth, eyes, brows, lashes or body hair; retouching of non-human elements; removing a second person.
  
  — [CLP law firm](https://www.clp.no/en/news/new-requirements-for-labelling-of-retouched-photos-back-and-forth-by-the-consumer-authority-what-is-the-current-status)
- **Israel (2012):** models need a minimum BMI of 18.5 and medical certificates, and ads must clearly disclose digital alterations. **UK:** the ASA rules case by case under the BCAP Code; for example, a 2011 ruling found a L'Oréal airbrushed ad misleading. **US:** the Truth in Advertising Act of 2016 was proposed and asked the FTC to evaluate digital alteration; it is not law. — [Berkeley Journal of International Law](https://www.berkeleyjournalofinternationallaw.com/post/photo-edit-law-is-it-time-for-an-international-norm)
- **Getty Images (from 1 Oct 2017):** contributors may not submit creative content showing models whose body shapes were retouched to look thinner or larger. Hair color, nose shape, skin and blemish edits remain allowed. — [Refinery29](https://www.refinery29.com/en-us/2017/09/174162/getty-ban-digitally-altered-photos-slimmed-models); [Digital Trends](https://www.digitaltrends.com/photography/getty-bans-photoshopped-bodies-in-stock/)
- **CVS Beauty Mark:** a watermark for images not materially altered (shape, size, proportion, skin, eye color). About 600 influencers have shared unaltered imagery since 2018. — [CVS Health](https://www.cvshealth.com/news/pharmacy/cvs-pharmacy-launches-first-campaign-featuring-unaltered-beauty.html)
- **Practitioner norm:** Dresser sculpts with light and shadow rather than slimming silhouettes. — [FixThePhoto](https://fixthephoto.com/amy-dresser-retouching-review.html)

### Inferences
Agent policy:
- Default to **no body-shape or size changes and no facial-feature reshaping**. If a brief requests it, flag the disclosure obligations (France and Norway labels, Getty prohibition).
- Skin cleanup, tonal work, and color changes are legally low-risk in France. In Norway, skin alteration in **advertising** can trigger labeling under the original rule; the narrowed August 2022 guidance hinges on "body-image pressure."
- Log every edit category (cleanup, skin texture, shape, color) so the result can be checked against labeling requirements.

### Gaps
- I could not verify the exact current (2026) text of the Norwegian guidance or the French 2023 influencer law (Loi n° 2023-451). Penalty details for Norway were not confirmed from primary sources.
- I found no source on whether any further EU-level rules on retouching disclosure took effect by 2026.
