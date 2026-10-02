# High-End Skin Retouching: Dodge & Burn, Check Layers, Frequency Separation, Texture, Healing/Cloning (Implementation-Oriented Notes)

Scope note: Facts in "Cited Findings" carry a source. Implementation formulas and code mappings in "Inferences" are my own derivations (standard image math) and are marked as such. Several SEO-style sites (photoshoptutorial.com, clippingexpertasia, fixthephoto, etc.) surfaced in searches; I used them only where they agreed with primary/pro sources and flag them as lower-confidence.

## Dodge & Burn: curves vs 50% gray, brush settings, micro vs macro, color-shift control

### Takeaway
Pros use either two Curves adjustment layers (one brightened "Dodge", one darkened "Burn", each with a black mask painted in with white) or a single 50% gray layer in Soft Light/Overlay; the curves method is the high-end default because the effect strength is set by the curve and the mask is a pure 0..1 weight map. Brush: soft (0-30% hardness), Opacity 100% with Flow 1-5% (or Opacity 3-5%), brush slightly smaller than the transition being fixed. Color shifts are controlled by putting the curves in Luminosity blend mode and/or clipping a Hue/Sat or Color-mode correction to them.

### Cited Findings
**Curves method construction**
- Two Curves adjustment layers: "Dodge" = curve pulled slightly up in the midtones, "Burn" = curve pulled slightly down; each gets a black (inverted, Ctrl/Cmd+I) layer mask; paint white on the mask to reveal. — [Fstoppers / Julia Kuzmenko McKim, D&B Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281); [KelbyOne helper-layers summary via search](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)
- McKim: don't pull the curves far from default "because then even with the lowest brush Opacity/Flow your brush strokes will be too intense." No numeric curve points given (qualitative only). — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- Setting the D&B curve layers to Luminosity blend mode avoids hue shifts; one tip is to adjust the Green channel curve rather than RGB (search-snippet claim; check context). — [Fstoppers Part 3 (search summary)](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- McKim notes that brightening/darkening shifts hues ("chances are their hues will shift") and recommends correcting afterwards with Hue/Saturation, Selective Color, or Color-blend-mode layers clipped to the D&B curves. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- Michael Woloszynowicz's stack: 3-7 layers per image; the basic version is corrective Dodge (lighten), corrective Burn (darken), plus a helper layer that removes color and amplifies luminosity shifts. A Capture One helper-layer variant quoted in search snippets: Saturation -100, Exposure -0.1, RGB curve point Input 146 -> Output 115 (snippet only; I could not open the full page to confirm). — [Vibrant Shot: D&B with Capture One Pro 20](http://www.vibrantshot.com/dodging-and-burning-with-capture-one-pro-20/)

**50% gray method**
- A new layer filled with 50% gray in Soft Light is invisible until painted; paint white to dodge, black to burn. Soft Light is described as lightening/darkening "without reducing saturation". — [PHLEARN D&B](https://phlearn.com/tutorial/how-to-dodge-and-burn-in-photoshop/); [Noble Desktop](https://blog.nobledesktop.com/learn/photoshop/nondestructive-dodging-burning) (search summaries)
- Blend If on a D&B layer: on the "Underlying Layer" slider, Alt/Option-drag to split the handle and move it inward so dodging fades out of shadows and survives only where the base is already light; an unsplit handle gives a harsh, gritty edge. — [photoshoptutorial.com (lower-confidence source)](https://photoshoptutorial.com/posts/why-dodge-and-burn-is-still-the-best-retouching-tool-youre-probably-using-wrong/)

**Brush settings**
- McKim: brush Opacity about 3-5%, soft brush, build up gradually. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- Micro D&B (Retouching Academy): Opacity 100%, Flow 1-3%, Hardness 0-30%, size slightly smaller than the blemish (some match its size), soft white brush. — [Retouching Academy, Micro Transitions](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
- Pratik Naik: leaves Opacity at 100% and lowers Flow so intensity builds up without lifting the stylus. Common: Flow 1-3%, brush matched to the size of the dark patch, zoom 100%+, and change zoom often (only zoomed in misses the large forms, only zoomed out misses the details). — [SLR Lounge: Micro D&B](https://www.slrlounge.com/how-to-micro-dodge-burn-skin-in-adobe-photoshop/)
- Flow 1-5% is the commonly preferred range. — [Fstoppers Part 3 (search summary)](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)

**Micro vs macro (what is being evened)**
- Local/micro D&B: "tiny dots and lines" at 60-200% zoom to even out skin values. Global/macro D&B: large soft strokes for sculpting and adding dimension. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)
- Micro transitions are "small shadows and highlights" from skin-surface irregularities, not facial anatomy. Most are darker patches, so the work is mostly dodging, with burning for light spots. It is slow and tedious. Over-smoothing with frequency separation is named as the main retouching error. — [Retouching Academy, Micro Transitions](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)

### Inferences
- Math (my derivation). Curves D&B equals per-pixel interpolation: `out = lerp(I, C_dodge(I), m_d)` followed by `lerp(·, C_burn(·), m_b)`, with masks m in [0,1]. Painting at Flow f accumulates `m <- m + f*(1-m)*brush_falloff`, so 1-3% flow gives about 30-100 dabs to saturate. "Luminosity" blend: compute L of the curved result, then recombine with the original's chroma (Photoshop's Luminosity uses a Lum/SetLum model; in code, LAB L* swap or YCbCr Y swap is a close approximation).
- A code implementation of micro D&B, where the agent has no human brush, can be derived from "what is being evened": target luminance `L_target = lowpass(L, sigma_macro)` + preserved pore band. Mask `m = clip((L_target - L_mid)/k)` where L_mid is a mid band (difference of Gaussians around 1-3x blemish size). Positive gives dodge and negative gives burn. Apply at low gain (equivalent to building up slowly) and cap the per-pixel change. This is effectively the "mid-frequency flattening" that micro D&B does by hand.
- Soft Light 50% gray is equivalent to a curve whose strength depends on the base value. Use the Photoshop/W3C soft-light formula, see [Wikipedia: Blend modes](https://en.wikipedia.org/wiki/Blend_modes). A neutral 0.5 layer equals identity.
- Saturation compensation: darkening in RGB raises apparent saturation, and lightening lowers it. A clipped Hue/Sat layer with a small desaturation on burn areas (and a small saturation increase on dodge areas) offsets this. In code, operate on L only (LAB) and leave a/b untouched, or apply a small chroma scale proportional to the mask.

### Gaps
- No pro source gave exact curve point numbers (e.g., input/output) for the dodge/burn curves; McKim says "slightly". Commonly seen values such as midpoint moved ±10-25 levels are not sourced here.
- Could not verify the exact Woloszynowicz saturation-compensation settings outside of a search snippet (page partially inaccessible).
- Brush size in absolute pixels relative to pore size (e.g., at 24MP or 50MP) was not found in any source; sources only say "slightly smaller than the blemish/patch".

## Check / helper layers: construction and use

### Takeaway
Standard helper stack, kept in a group and toggled: (1) desaturation via a 50% gray fill (Saturation 0, Brightness 50) in Color mode, which pros prefer over B&W adjustment because it represents luminosity more accurately; (2) a contrast-boosting Curves layer (darken plus steepen) on top; (3) a solarize curve (4-point zigzag) to exaggerate micro transitions and reveal cloning/healing texture changes; (4) a "midrange peak" curve for smoother texture inspection; (5) a negative (inverted) curve to spot harsh transitions.

### Cited Findings
- Solarize curve: Curves layer. Click about 1/4 up the line and drag up, click another 1/4 to the right and drag down, repeat for 4 points total (a zigzag). It exaggerates small changes, shows blemishes, reveals texture-direction changes from healing/cloning and over-smoothing, and shows D&B effects. — [KelbyOne, Scott Valentine](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)
- Midrange peak curve: drag the curve's middle to the top, drag the highlight endpoint (top-right) straight down, move the white slider slightly left and the black slider slightly right. This gives a smooth center bump and smoother gradients than solarize, which is better for judging skin texture and small blemishes. It pairs with Spot Healing on supporting layers in Darken (for dark blemishes) and Lighten (for light/red blemishes). — [KelbyOne, Scott Valentine](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)
- Luminosity check: Solid Color fill, HSB Saturation 0%, Brightness 50%, blend mode Color. It removes color for D&B work. — [KelbyOne](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/); same 50% grey in Color mode in [Retouching Academy](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
- McKim (crediting Lulie Talmor) prefers the 50% gray Color-mode layer to Black & White adjustment or Channel Mixer Monochrome. Her reason is that B&W conversions distort perceived values. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281); see also [Retouching Academy, B&W conversions in relation to D&B](https://retouchingacademy.com/color-correction-lesson-preview-black-and-white-conversions-in-relation-to-dodging-and-burning/)
- Retouching Academy visual aid = Curves layer that darkens and adds contrast plus 50% grey in Color mode. — [Retouching Academy](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
- Negative check: Curves with the left endpoint dragged to top and right endpoint to bottom (inversion), placed above the luminosity layer. Nudge the middle up or down for contrast and toggle it periodically to find over-corrections and harsh transitions. — [KelbyOne](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)
- Helper layers are temporary and are deleted or hidden before output. Group them and toggle them together. — [KelbyOne](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)

### Inferences
- Code equivalents (my derivation):
  - Luminosity view: `Y = Lum(img)` (Rec.709/601 weights, or LAB L*). Photoshop's Color mode with 50% gray gives SetLum(gray, Lum(base)), which is about the base luminance as gray.
  - Contrast check: `clip((Y - 0.5)*g + 0.5 - d)` with g of about 2-3 and a small darken d.
  - Solarize (4-point zigzag): a piecewise-linear LUT through (0,0),(0.25,1),(0.5,0),(0.75,1),(1,0) or similar. Equivalently `abs(sin(k*pi*Y))` with k of about 2. Each luminance step is magnified about 4x.
  - Midrange peak: a bell LUT `exp(-((Y-0.5)/w)^2)`.
  - Negative: `1-Y`.
  - Color check (not in sources, see Gaps): Hue/Sat with Saturation about +50 to +100 to exaggerate blotchiness.
- For an automated agent these views double as QA metrics. Compute local variance of the solarized luminance in the mid band before and after editing. A drop in the fine band means texture loss, and residual mid-band energy means unevenness that remains.

### Gaps
- No primary source found for the "high-saturation color check layer" exact settings (e.g., Hue/Sat +50 to +100 or Vibrance +100). It is a widely repeated practice, but I did not obtain a citation in this session.

## Frequency separation: construction (8/16-bit), radius, blur type, 3-band, when not to use

### Takeaway
FS: low = Gaussian(I, r); high = I - low + 0.5, recombined via Linear Light. 8-bit: Apply Image Subtract, Scale 2, Offset 128. 16-bit: Apply Image Add, Invert checked, Scale 2, Offset 0. Choose r by increasing it from 0 until volumes and tonal transitions start appearing in the high layer, then stop (about 3-8 px for typical portraits depending on resolution). Use multiple rounds or bands (wavelet) rather than one aggressive split. Do luminance changes with D&B, not FS.

### Cited Findings
- 8 bpc: Apply Image, Blending Subtract, Scale 2, Offset 128. 16 bpc: Apply Image, Blending Add, Invert checked, Scale 2, Offset 0. "No need for 32 BPC mode." — [Adobe Community thread](https://community.adobe.com/t5/photoshop-ecosystem-discussions/how-to-do-math-correct-frequency-separation-of-16-bit-rgb/m-p/15396864); same values in [ExpertPhotography](https://expertphotography.com/frequency-separation-photoshop)
- Construction (McKim): duplicate the base twice. Gaussian-blur the lower copy (low frequency). On the upper copy, run Apply Image from the low layer with the bit-depth settings, then set the high layer to Linear Light. High Pass alternative: run High Pass (same radius) on the top copy, set it to Linear Light at 50% opacity, and Gaussian-blur the low layer at the same radius. McKim calls Apply Image "more accurate". — [Fstoppers, Ultimate Guide to FS](https://fstoppers.com/post-production/ultimate-guide-frequency-separation-technique-8699)
- Radius selection (Aleksey Dovgulya's method): move the radius up from zero, and "as soon as we start seeing excessive tonal transitions, bulky textures and volumes we should stop". In the example, 3.5 px kept fine detail without volume and 7.8 px showed too many transitions. — [Fstoppers FS guide](https://fstoppers.com/post-production/ultimate-guide-frequency-separation-technique-8699)
- Typical numbers: 3-5 px for headshots so the high band holds texture without individual pores leaking into low (search summary); 4-8 px for portraits with no pores visible on the low layer. — [ExpertPhotography](https://expertphotography.com/frequency-separation-photoshop); [tryretouchlab](https://tryretouchlab.com/blog/how-to-do-frequency-separation-photoshop) (lower-confidence)
- Surface Blur as an extra step for blotchy skin: set the radius with threshold at minimum, push threshold to maximum, then lower it slowly until colors stop smearing (watch face and hair outlines). Mask it black and paint white softly at low opacity over problem areas. — [Fstoppers FS guide](https://fstoppers.com/post-production/ultimate-guide-frequency-separation-technique-8699)
- Low layer tools: very soft Healing Brush (sampling current layer), soft low-opacity Clone Stamp, or a low-opacity brush to even color and tone. Work on an empty layer between high and low. High layer tools: Clone Stamp with high hardness and high opacity, or a hard Healing Brush, for blemishes while preserving texture. Avoid smudging. — [Fstoppers FS guide](https://fstoppers.com/post-production/ultimate-guide-frequency-separation-technique-8699)
- Mistakes: a single FS pass is often insufficient, so use 2-3 rounds with different radii for different face areas. Don't make drastic luminance changes in FS. Woloszynowicz: "If you try to make drastic luminance changes with FS... it can reduce texture as your new tones will blend with the light or dark tone of the High Frequency layer." Use D&B for luminance. — [Fstoppers FS guide](https://fstoppers.com/post-production/ultimate-guide-frequency-separation-technique-8699)
- Multi-band (wavelet) equivalent: GIMP Wavelet Decompose outputs N detail "scales" (default example 5) plus a residual. Finest details are in scale 1 and coarser ones in later scales. Scales use Grain Merge so the composite reconstructs exactly. Pores, light wrinkles and crow's-feet sit in the high scales, and larger tone in the residual. Scales are smoothed with G'MIC bilateral: scale 5 at spatial variance 15, value variance 12, 2 iterations; scale 4 at spatial 5-7, value 2-4, 1-2 iterations (defaults 10/7/2). Work from the coarsest scale to finer ones with smaller parameters. Heal the residual for color evening. — [PIXLS.US, Pat David](https://pixls.us/articles/skin-retouching-with-wavelet-decompose/); [GIMP docs](https://docs.gimp.org/2.10/en/plug-in-wavelet-decompose.html)
- Bilateral filter (= Photoshop Surface Blur / GIMP Selective Blur) is edge-preserving: it weights a neighborhood by both spatial distance and value similarity. — [Medium: AR beauty mode implementation](https://medium.com/swlh/how-i-implemented-my-own-augmented-reality-beauty-mode-3bf3b74e5507) (search summary)

### Inferences
- Exact math (my derivation, consistent with the cited settings). Apply Image computes `(Target - Source)/Scale + Offset` for Subtract. In 8-bit: `H = (I - L)/2 + 128`. Linear Light recombination is `B + 2*Blend - 1` (normalized), see [Wikipedia: Blend modes](https://en.wikipedia.org/wiki/Blend_modes). So `L + 2*((I-L)/2 + 0.5) - 1 = I`, which is exact except for 8-bit rounding of the /2 step (the loss is 1 bit). The 16-bit Add+Invert variant computes `(L_inv + I)/2 + 0` = `(1 - L + I)/2`, the same thing without Photoshop's 16-bit offset quirk (Photoshop 16-bit is 0..32768, so offset 128 is not mid-gray).
- In code, skip the 0.5 offset entirely. Work in float32: `low = GaussianBlur(I, sigma)`, `high = I - low`, edits, then `out = low' + high'`. OpenCV: `cv2.GaussianBlur(img32, (0,0), sigmaX=r)`. Photoshop's "radius" is approximately sigma (commonly treated as sigma; exact correspondence not verified).
- Scale radius with resolution. If 3.5-5 px suits a typical headshot crop, a rule like `r ≈ pore_diameter_px × 1-1.5` or `r ≈ face_width_px / 150-250` is plausible but unsourced. Better is to replicate Dovgulya's criterion automatically: increase sigma until the high band's energy starts to include low-frequency structure (e.g., a knee in high-band variance vs sigma, or correlation between the high band and blurred luminance).
- 3-band (recommended for code): `fine = I - G(σ1)`, `mid = G(σ1) - G(σ2)`, `low = G(σ2)`, with σ1 at pore scale (about 1-3 px) and σ2 at blemish/blotch scale (about 3-5× σ1). Edit "mid" (blotchiness, micro transitions) by attenuating it or clipping its outliers. Leave "fine" intact or only heal spots. Even "low" color with a bilateral or guided filter. Use a Laplacian pyramid or à trous wavelet (`cv2.pyrDown/pyrUp` or B3-spline à trous as in GIMP) for exact reconstruction.
- An edge-preserving low pass (bilateral/guided) avoids halos at jaw, hairline and lips where Gaussian FS bleeds color across edges. Alternatively restrict edits with a skin mask eroded away from features.

### Gaps
- No authoritative formula maps pore size in µm or face size to blur radius. Sources give only empirical px ranges or the "stop when volumes appear" criterion.
- Did not confirm the exact Photoshop Gaussian "radius" to sigma relationship from an Adobe source.
- No primary source for a "3-band FS in Photoshop" recipe beyond multi-round FS and wavelet decompose.

## Skin texture preservation: judging retention, texture matching, grain, regraft

### Takeaway
Pros judge texture with check layers (solarize/midrange peak), at 100% zoom, and by never letting the high band be blurred. Heal or clone from texture of matching scale, orientation and luminance, at low Diffusion. Inverted High Pass (HP r, then Gaussian r/3, then invert, then Linear Light/Overlay, masked) smooths a band while keeping finer texture. Texture regraft and grain-matching specifics were not found in authoritative form.

### Cited Findings
- The solarize check reveals "texture direction changes" and over-smoothing from heal/clone. — [KelbyOne](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)
- Inverted High Pass (IHP) steps: stamp visible (Shift+Ctrl/Cmd+Alt+E), High Pass at radius R, Gaussian Blur at R/3, Invert (Ctrl/Cmd+I), blend Linear Light (or Overlay), black mask, paint white where needed. Pairs given: 30/10 (demo), 21/7 (stronger skin smoothing), 15/5 (sharper areas like mouth corners), 9/3 (close-up texture). Keep it subtle; applying it to all skin looks blurry and the texture looks disconnected. — [DMD Digital Retouching, IHP tutorial](https://www.dmd-digital-retouching.com/blog/inverted-high-pass-ihp-retouching-tutorial/)
- IHP radius about 20-25 (about 24) for a typical portrait, and Vivid Light is sometimes used instead of Linear Light. — [search summaries: Creative Market / ExpertPhotography](https://creativemarket.com/blog/smooth-retouch-skin-photoshop) (lower-confidence)
- Micro D&B is the alternative to FS smoothing because it keeps original texture. Excessive FS smoothing is the main error. — [Retouching Academy](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
- Healing Diffusion 1 for skin keeps pore structure and avoids color contamination. High diffusion with soft brushes can create off-hue fringes (e.g., blue between red and yellow). — [KelbyOne, Kristina Sherk](https://insider.kelbyone.com/de-mystifying-the-diffusion-slider/)

### Inferences
- IHP math (my derivation). HighPass_R(I) = I - G_R(I) + 0.5. Blurring by R/3 gives approximately G_{R/3}(I) - G_R(I) + 0.5, a band-pass between R/3 and R. Inverting and applying Linear Light subtracts 2× that band, so `out ≈ I - 2·(G_{R/3} - G_R)`. Because Linear Light doubles, it slightly over-subtracts. At 50% opacity it removes exactly the R/3..R band, so features finer than R/3 (pores) survive. In code: `out = I - α·(G(σ_fine) - G(σ_coarse))·mask` with σ_fine = R/3, α between 0.5 and 1.
- Texture-retention metric for an agent: compare high-band energy (e.g., std of `I - G(1-2px)`) inside the skin mask before and after. A target ratio near 1.0 (e.g., ≥0.9) means texture is kept, while mid-band energy should drop. This is unsourced but follows directly from the check-layer logic.
- Grain/texture matching after any smoothing or healing: measure the residual noise std per channel in a clean skin patch, then add Gaussian or sampled noise of matching std and spectrum (blur the noise to match grain size). For "regraft", copy the high band from a donor skin patch (same face region, similar pore density and orientation) into the target's high band, leaving its low band intact. This is the code analog of cloning on the FS high layer.

### Gaps
- No authoritative source found in this session for "skin regraft" procedures (e.g., Pratik Naik / Natalia Taffarel texture-transplant settings) or for numeric grain/noise matching (Add Noise %, Gaussian/monochromatic). Natalia Taffarel's specific FS/texture methods were not retrievable.

## Healing / cloning best practices

### Takeaway
Work on blank layers with "Current & Below" (or All Layers with "Ignore Adjustment Layers"). Spot Healing (Content-Aware) handles isolated blemishes in uniform skin. Healing Brush with Diffusion about 1 to 5 handles blemishes and under-eye lines. Clone Stamp (often Lighten/Darken mode, hard brush) is for edges, transitions, hair and anywhere healing smears. Patch is for larger areas. To avoid repeating patterns: keep Aligned on, use multiple sources, and rotate or flip the source.

### Cited Findings
- Clone Stamp is "non-interpretive" (copies pixels). Use it for flyaways (with Lighten/Darken mode) and for transitions or varied texture where healing fails. Healing Brush is "interpretive" (separates texture, luminosity and color) and suits facial blemishes and lines under the eyes. Spot Healing guesses from surroundings without a sample and suits minor blemishes in uniform areas (cheeks, chin, forehead). Retouch on a blank layer above. — [Retouching Academy, Essential tools for face & hair](https://retouchingacademy.com/essential-retouching-tools-for-face-and-hair/)
- Sample "All Layers" onto a new blank layer, or "Current & Below" in complex stacks. Toggle "Ignore Adjustment Layers" so curves and check layers aren't baked into samples. Aligned helps decrease "the probability of repeating patterns". There are up to 5 source points in the Clone Source panel, with rotation, scale and flip of the source plus overlay and invert overlay. Healing Brush "Replace" mode behaves like cloning without soft edges on high-frequency detail. Lower Diffusion reduces artifacts in grainy or detailed images, and higher suits smooth areas. "Use Legacy" option exists. — [Julieanne Kost (Adobe)](https://jkost.com/blog/2021/12/10-tips-for-the-clone-stamp-and-healing-brush-tools-in-photoshop.html)
- Diffusion demonstrated range 1-7. Value 1 is for skin (keeps pores, avoids color bleed) and 7 is for smooth areas such as sky or walls. — [KelbyOne, Kristina Sherk](https://insider.kelbyone.com/de-mystifying-the-diffusion-slider/)
- An alternative recommendation is Diffusion 5 with a softer edge for blemishes and flakes, and a harder edge with Diffusion 1 for hair. — [search summary of Behind the Shutter / KelbyOne](https://www.behindtheshutter.com/5-steps-to-brush-up-on-retouching-in-photoshop/) (conflicts slightly with Sherk's "1 for skin"; both agree low Diffusion means more texture fidelity)
- Spot Healing modes: Proximity Match (uses pixels around the edge), Create Texture (synthesizes texture from surroundings), and Content-Aware (analyzes nearby content and preserves highlights, shadows and edges). Healing principle: the sampled texture is blended with the color and luminosity of the destination surroundings. — [Breathing Color](https://www.breathingcolor.com/blogs/news/photoshop-spot-healing-brush); [Adobe Spot Heal page](https://www.adobe.com/products/photoshop/spot-heal.html) (search summaries)
- Midrange-peak check plus Spot Healing on separate layers in Darken (dark blemishes) or Lighten (light/red blemishes) modes, so the heal can only move pixels one direction. — [KelbyOne, Scott Valentine](https://insider.kelbyone.com/using-helper-layers-when-retouching-your-photos-by-scott-valentine/)

### Inferences
- Healing Brush ≈ Poisson/gradient-domain cloning (my inference, widely understood). Keep the source's gradients (texture) and solve for boundary color and luminance from the destination. In OpenCV: `cv2.seamlessClone(src, dst, mask, center, cv2.NORMAL_CLONE)`. Use MIXED_CLONE to keep the stronger gradient. A lighter heal alternative: `out = high_src + low_dst`, meaning transplant the FS high band of the source onto the low band of the destination, which is exactly "texture from source, color/luminance from destination". Diffusion maps roughly to how large the boundary blending region or low-pass sigma is (low means tight, which preserves texture).
- Spot Healing (Content-Aware) ≈ PatchMatch-style exemplar inpainting. Non-generative options are `cv2.inpaint` (Telea/NS) for tiny spots, which smooths and loses texture, so add the high band back. For larger spots, use exemplar search restricted to skin-masked donor regions of similar luminance and pore density, and exclude the immediate neighborhood (≥1-2 spot diameters away) to avoid visible repeats.
- Darken/Lighten-constrained healing: `out = min(I, healed)` for removing bright spots and `max(I, healed)` for removing dark spots. This prevents halos and protects untouched texture.
- Near edges and high contrast (lips, eyelids, hairline, jaw): prefer clone, not heal, because healing pulls the opposite-side color across the boundary. Use a harder brush, Replace or Normal mode, or mask the heal domain so it never crosses an edge (segment, then heal within the segment).

### Gaps
- Adobe's own help page for Healing Brush and Patch returned 403. I could not cite exact Patch tool options (Normal vs Content-Aware, Structure 1-7, Color 0-10) from Adobe in this session; those ranges are from memory and are unverified here.

## Other pro skin tools: color evening, redness, under-eye/wrinkles at reduced opacity

### Takeaway
Color evening uses Hue/Saturation or Selective Color targeted at Reds/Magentas: temporarily exaggerate to find the range, narrow it, then shift hue toward yellow and/or reduce saturation, masked to the problem areas. Alternatively paint on a low-frequency or Color-mode layer. Lines and under-eye are healed or cloned on a separate layer, then opacity is lowered so some of the original remains.

### Cited Findings
- Redness: Hue/Sat on Reds, crank saturation or push hue (reds turn bright cyan) to see the selection, narrow the range sliders until only nose, cheeks and under-eye light up, then set the correction. — [PHLEARN, remove redness](https://phlearn.com/tutorial/how-to-remove-redness-from-skin-in-photoshop/); [PHLEARN, correct red skin](https://phlearn.com/tutorial/correct-red-skin-color-photoshop-quickly/) (search summaries)
- Selective Color on Reds/Neutrals adjusting the Cyan/Magenta/Yellow/Black sliders to refine warmth and remove casts. — [Retouch4me blog](https://retouch4.me/blog/how-to-correct-skin-tone-lightroom-photoshop-retouch4me) (vendor source; lower-confidence)
- Clipping Hue/Sat, Selective Color or Color-mode layers to D&B layers to fix the hue shifts that D&B causes. — [Fstoppers Part 3](https://fstoppers.com/photoshop/ultimate-guide-dodge-burn-technique-part-3-curves-setup-more-9281)

### Inferences
- Code color evening (my derivation): in LAB, compute the low-pass a*, b* (σ about the blotch scale). Redness = a* exceeding the skin median a* by k·MAD. Pull a* toward the local median, `a' = a - λ·max(0, a_low - a_med)`, with λ about 0.5-0.8 and feathered by the skin mask. Leave L and the high bands untouched. This mirrors "narrow Reds range, desaturate or shift hue".
- Under-eye and wrinkles at reduced opacity: the well-known practice is to heal fully on a new layer and then drop the layer to about 30-70% so the feature softens rather than vanishes. In code, `out = lerp(I, healed, 0.3-0.7)`. This specific percentage was not sourced in this session.

### Gaps
- No cited numeric opacity for wrinkle or under-eye softening, and no cited Selective Color slider values for redness. Practices are documented qualitatively only.

## Eyes, lips, teeth, hair (flyaways, gaps), makeup cleanup

### Takeaway
Flyaways: Clone Stamp on a blank layer, in Darken mode for light hair over a dark background and Lighten mode for dark hair over a light background. Heal on gradients away from the head and clone near the head. Teeth: Hue/Sat on Yellows with saturation down (about -50 to -80 as a starting point) and lightness slightly up, masked. Eye, lip and makeup cleanup specifics with numbers were sparsely sourced.

### Cited Findings
- Clone Stamp is the tool for stray hair, used with Lighten or Darken. Lighten removes dark hair on a light background and Darken removes light hair on a dark background. Use Healing or Spot Healing on gradient backgrounds and switch to Clone Stamp closer to the head. — [Retouching Academy](https://retouchingacademy.com/essential-retouching-tools-for-face-and-hair/); [Envato Tuts+](https://photography.tutsplus.com/tutorials/3-ways-to-retouch-fly-away-hair--cms-20373) (search summary)
- Diffusion 1 and a harder edge for fine hair work. — [Behind the Shutter summary](https://www.behindtheshutter.com/5-steps-to-brush-up-on-retouching-in-photoshop/)
- Teeth: Hue/Saturation adjustment, Edit = Yellows, Saturation about -50 to -80 starting point, Lightness slightly up, masked to the teeth. A variant drops master saturation about -5 while doing most of the work in Yellows. — [Photoshop Essentials](https://www.photoshopessentials.com/photo-editing/whiten-teeth/); [SLR Lounge](https://www.slrlounge.com/fix-whiten-teeth-photoshop-right-way/) (search summaries)

### Inferences
- Code for flyaways: detect thin, high-contrast curvilinear strands outside the main hair mass (ridge/Frangi filter on luminance, outside a dilated hair segmentation). Then remove them with directional or exemplar fill from the background, constrained by `min(I, fill)` for light strands on dark and `max(I, fill)` for dark strands on light. That is the Darken/Lighten clone trick, and it prevents halos.
- Hair gap filling (clone hair texture into sparse areas) should copy strands along their flow direction (rotate the source to match orientation, as with the Clone Source panel rotation). Unsourced as a numeric method.
- Eyes and lips: apply the same principles (clone near edges, D&B for shape). Typical moves such as eye-white desaturation or brightening and iris dodge are not numerically sourced here.

### Gaps
- No numeric, primary-source procedures obtained for eye-white cleanup, iris enhancement, lip-line cleanup, or makeup cleanup (foundation creasing, mascara clumps), nor for hair-gap filling. These need further research (e.g., Retouching Academy or Pratik Naik course material, which is mostly paywalled or video).
- Pratik Naik, Natalia Taffarel and PHLEARN full-procedure pages were not fully retrieved. Their 2025-2026 updates (e.g., use of AI tools such as Retouch4me or Evoto in pro pipelines) were not assessed.
