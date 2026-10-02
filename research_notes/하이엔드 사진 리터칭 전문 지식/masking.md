# Advanced Professional Masking & Selection Techniques (and Algorithms to Reproduce Them in Code)

Scope: high-end retouching / landscape / commercial masking (channel masks, luminosity masks, Blend If, Select & Mask, pen paths, mask refinement, AI segmentation/matting, local-adjustment masks). Non-generative only. Research date: Oct 2026.

Conventions used below: image values normalized to x in [0,1]; "mask" = alpha in [0,1] (white = 1 = selected/revealed). In Photoshop selection arithmetic, "Intersect" behaves as multiplication and "Subtract B from A" behaves as A·(1−B) (see Section 2 inferences for the evidence that this matches measured values).

---

## 1. Channel masking (channel choice, Calculations/Apply Image, Levels/Curves crushing, overlay-mode dodge/burn on channel, hair & foliage extraction)

### Takeaway
Channel masking = pick the R/G/B channel with maximum subject/background separation, duplicate it, increase contrast (Levels/Curves, Calculations/Apply Image to combine channels), then clean it with Overlay-mode brushes (which push near-black darker and near-white lighter while leaving the semi-transparent grey hair strands mostly intact). In code it is literally per-channel arithmetic + a tone curve + local clean-up, and is still the best non-AI method for hair/foliage against a smooth sky or seamless backdrop.

### Cited Findings
- Each RGB image contains three grayscale channels; because subjects contain different amounts of each colour, one channel is usually much closer to a finished mask than the others — [Graphic-design-employment: cutting out hair](https://www.graphic-design-employment.com/cutting-out-hair-in-photoshop.html)
- Channel choice heuristic for people: faces are bright in Red and dark in Blue because skin contains much red and little blue; choose the channel with maximum subject/background separation — [PHLEARN, Advanced Hair Masking with Channels](https://phlearn.com/tutorial/selections-with-channels-photoshop/)
- Always duplicate the channel ("Always work on the copy — editing a live channel changes the image itself") — [PHLEARN](https://phlearn.com/tutorial/selections-with-channels-photoshop/)
- Levels on the channel copy: drag black input slider right to deepen darks, white input slider left to brighten background; but "individual hair strands are semi-transparent — they should stay gray" (don't crush everything to pure B/W) — [PHLEARN](https://phlearn.com/tutorial/selections-with-channels-photoshop/)
- Ctrl/Cmd-click the channel thumbnail to load it; "a channel selection always selects the light areas" — invert if the subject is dark — [PHLEARN](https://phlearn.com/tutorial/selections-with-channels-photoshop/)
- Image > Calculations example for hair: Source 1 = Red, Source 2 = Blue (blue inverted) to define hair against backdrop — [PSDESIRE, Advanced hair masking using Calculations](https://photoshopdesire.com/advanced-hair-masking-using-image-calculations-photoshop/)
- Overlay-mode brush on a channel/mask: painting black deepens what is already dark and leaves light pixels untouched; painting white brightens light areas and protects black; pure black and pure white are unaffected in Overlay mode — so grey hair strands survive. Use lower brush opacity (40–50%) inside hair to preserve flyaways — [PHLEARN, Amazing trick for refining masks](https://phlearn.com/tutorial/amazing-trick-for-refining-masks-in-photoshop/); [LinkedIn Learning, Painting with the Overlay mode](https://www.linkedin.com/learning/photoshop-channels-and-masks/painting-with-the-overlay-mode)
- Dodge and Burn tools are also used directly on the channel/mask: dodge (lighten) what you keep, burn (darken) what you drop — [Graphic-design-employment](https://www.graphic-design-employment.com/cutting-out-hair-in-photoshop.html)
- TK9 exposes R, G, B and simulated C, M, Y channel sources for luminosity-style masks, and a "Adjust with Color" Black & White adjustment to lighten/darken specific hues in the mask (works best on a Lights-1 mask) — i.e. channel-mixer-weighted masks are a pro-standard extension of channel masking — [TK9 Instructions Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf)

### Inferences
- Procedure (pro-standard, synthesized from the above):
  1. Inspect R/G/B (and optionally C=1−R type "fictitious" channels, Lab b*, or B−R difference) and choose max separation. Sky vs foliage: Blue channel usually (sky bright, leaves dark). Dark hair vs light backdrop: Blue or the channel where backdrop is brightest.
  2. Duplicate channel; optionally Calculations (e.g., Blue Multiply Blue, or Red Subtract/Difference Blue) to increase separation. Apply Image does the same into an existing channel.
  3. Levels/Curves in stages, watching hair stay grey; avoid one aggressive step (creates halos / clipped wisps).
  4. Brush in Overlay at 30–50% to push background to white/black without killing edge greys; Dodge (Highlights range) / Burn (Shadows range) for the same purpose.
  5. Paint interior solid (Normal mode) where subject is opaque; load as selection/mask; invert if needed; then decontaminate edge colour (Section 4).
- Programmatic equivalent (numpy/OpenCV):
  ```python
  img = img.astype(np.float32)/255  # or 16-bit /65535
  R,G,B = img[...,2],img[...,1],img[...,0]          # OpenCV BGR
  # separation score per candidate channel using a coarse subject mask (e.g., from BiRefNet/SAM)
  cands = {'R':R,'G':G,'B':B,'1-B':1-B,'B-R':np.clip(B-R+0.5,0,1),'labb':lab_b}
  score = lambda c: abs(c[fg].mean()-c[bg].mean())/(c[fg].std()+c[bg].std()+1e-6)  # Fisher ratio
  # "Calculations": multiply/screen/subtract, e.g. calc = B*B (Multiply) ; calc = 1-(1-B)**2 (Screen)
  # Levels: m = clip((c - black)/(white - black), 0, 1) ** (1/gamma)
  # Overlay brush on mask m with paint value p (0 or 1) at opacity o:
  ov = np.where(m<0.5, 2*m*p, 1-2*(1-m)*(1-p)); m = m + o*(ov-m)   # pure 0/1 unchanged
  ```
  Per the standard Overlay formula, the protection is for the *opposite* extreme: painting black (p=0) leaves m=1 untouched and darkens greys in proportion to their darkness, painting white (p=1) leaves m=0 untouched; mid-greys still move, which is why pros paint at 30–50% opacity in multiple passes rather than 100%. An agent can apply "Overlay-burn" only in the background region of a trimap and "Overlay-dodge" only in the foreground region, automatically.
- Automatic Levels endpoints: choose black = percentile (e.g., 98–99th) of channel values inside a known-background sample, white = 1–2nd percentile inside known foreground (after inversion), so that background → 0 and solid subject → 1 while edge transition stays intermediate.
- Foliage against sky: channel mask of the Blue channel (or B−R) then a Levels crush gives near-perfect leaf/branch masks that SAM-style models typically miss (they give blobby tree crowns).

### Gaps
- No primary source found giving canonical numeric Levels values for channel masks; values are image-dependent. PHLEARN fetched text was a summary and did not list exact Dodge/Burn exposure/range settings.
- Exact Photoshop Calculations blend-mode list behaviour (e.g., Add/Subtract with Scale/Offset) not fetched from Adobe docs (Adobe helpx returned 403).

---

## 2. Luminosity masks: exact definitions (Lights/Darks/Midtones, zone, saturation, colour masks), TK Actions vs Lumenzia, formulas

### Takeaway
Lights-1 = luminance (L1 = x); each higher level is an intersection (multiplication) giving Ln = x^n; Darks Dn = (1−x)^n; Midtones are "everything minus Lights minus Darks" in selection arithmetic (≈ x·(1−x) for M1, peaking at ~25% selection at mid-grey). Zone masks are bell-shaped masks centred on a chosen tone; saturation/vibrance masks use per-pixel saturation (vibrance = inverted saturation). All are trivial to compute in numpy at 16/32-bit float precision.

### Cited Findings
- Kuyper (originator, 2006): Lights = base mask loaded from the composite channel; Light Lights (Lights-2) = Lights intersected with itself; Bright Lights (Lights-3), Super Lights (Lights-4), Ultra Lights (newest) = progressively further intersections; Darks = inverse of Lights; Dark Darks/Shadow Darks/Super Darks/Ultra Darks progressive intersections — [goodlight.us, Different Masks for Different Tones](https://goodlight.us/writing/luminositymasks/luminositymasks-5.html)
- Kuyper Midtones: Basic Mid-tones = All minus Lights and Darks; Expanded = minus Light Lights & Dark Darks; Wide = minus Bright Lights & Shadow Darks; Super = minus Super Lights & Super Darks (i.e., higher midtone level = WIDER) — [goodlight.us](https://goodlight.us/writing/luminositymasks/luminositymasks-5.html)
- Masks can select <50% of any pixel and still work (adjustments feather) — [goodlight.us](https://goodlight.us/writing/luminositymasks/luminositymasks-5.html)
- Formulas: Ln: y = x^n (L1=x … L6=x^6); Dn: y=(1−x)^n; TK9 Midtones base formula max(0, All − Lights − Darks). L1 at Zone V (50%) = 50% selected; L3 at 50% = 12.5%; L6 at 50% ≈ 1.5%; D3 at 60% = 6.4%; D3 at 70% = 2.7%. Measured TK9 midtones at Zone V: M1 ≈ 24%, M2 ≈ 50%, M3 ≈ 84%. Other tools that build midtones by Multiply (Lights × Darks) get the opposite progression (narrower at higher levels, Zone V starting at 25%). Photoshop draws marching ants only where selection > 50% (so marching ants misrepresent luminosity selections) — [Todd Marsh, Luminosity masks: more pixels are selected than you think](https://toddmarsh.com/luminosity-masks-photoshop-tonal-selection/)
- Lumenzia (Greg Benz) uses the same level naming L1–L6 / D1–D6 (the Todd Marsh article ties the x^n formula to Lumenzia's L1/L2…); Lumenzia previews masks with temporary orange overlay layers, has a "zone picker" (click image → zone mask), interactive zone maps, saturation/vibrance masks, and auto-refining levels on previews — [Greg Benz, Lumenzia v5](https://gregbenzphotography.com/luminosity-masking/lumenzia-v5/); [Greg Benz luminosity masking hub](https://gregbenzphotography.com/luminosity-masking/)
- GIMP construction (Pat David): D = All − L; DD = D − L; LL = L − D; Midtones M = L ∩ D — i.e., subtract/intersect operations — [Pat David, Luminosity Masks in GIMP](https://patdavid.net/2013/11/getting-around-in-gimp-luminosity-masks/)
- TK9 Zone masks: built around a picked tone that becomes lightest in the mask; parameters Zone center, Zone brightness (peak value; Kuyper: zone masks "generally work better when there is no pure white in the mask"), Zone width (narrow zones can lack pixels for smooth blending); 9 preset zones (Zone 1–9); Zone 0 ≈ Darks-5/6; on-screen banding on narrow zones is a display compression artefact, not in the mask — [TK9 Instructions Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf)
- TK9 Blend-If zone groups (8-bit scale): Zone 1 centred at 0 tapering to 64; Zone 2 centred 64 tapering to 0 and 128; Zone 3 centred 128 tapering to 64 and 192; Zone 4 centred 192 tapering to 128 and 255; Zone 5 centred 255 tapering to 192 — [TK9 Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf)
- Luminance vs luminosity: TK9 Lights/Darks/Midtones/Zone masks use pixel *luminance* of the composite RGB; Blend If masks use pixel *luminosity*, so they look slightly different and have higher contrast (almost always contain pure black and white) — [TK9 Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf)
- Saturation masks: brighter where colour saturation is higher; Vibrance masks = inverse (brightest in low-saturation pixels); Vibrance-3/-4/-5 are more restrictive; saturation masks tend to be dark because real photos rarely approach max saturation (use MODIFY to brighten); saturation-mask method credited to Chris Tarantino — [TK9 Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf); [Kuyper saturation masks overview via search](https://goodlight.us/writing/saturationmasks/intensifying-saturation.html)
- TK9 Edge mask = local pixel contrast (light where adjacent pixels differ), refined with Maximum/Minimum/Blur; Half-Edge mask selects the light or dark side of an edge (useful for halos along darker objects) — [TK9 Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf)
- Kuyper moved from 8-bit to 16-bit mask calculations; TK9 ensures 16-bit masks throughout; 32-bit support from v3.0.0 but some masks (e.g., Saturation/Vibrance) unavailable in 32-bit — [TK9 Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf); [Kuyper, How to make 16-bit luminosity masks](https://tonykuyper.wordpress.com/2015/02/28/how-to-make-16-bit-luminosity-masks/)
- Conflict note: goodlight.us wording says Bright Lights = "Light Lights intersected with itself" (would be x^4), while Todd Marsh's measurements give L3 = x^3 (Light Lights ∩ Lights). Measured value L3@50% = 12.5% = 0.5^3 supports x^3 for TK9 — [goodlight.us](https://goodlight.us/writing/luminositymasks/luminositymasks-5.html) vs [Todd Marsh](https://toddmarsh.com/luminosity-masks-photoshop-tonal-selection/)

### Inferences
- Selection arithmetic that reproduces the measured numbers: Photoshop "Subtract" is A·(1−B). Then:
  - M1 = 1·(1−L1)·(1−D1) = (1−x)·x → 0.25 at x=0.5 (measured 24% ✔).
  - M2 = (1−x²)(1−(1−x)²) → 0.5625 at 0.5 (measured ~50%; close but not exact — TK9 may normalize or use different internal steps; treat as approximate).
  - Pat David's "LL = L − D" = x·(1−(1−x)) = x² ✔ consistent with Ln = x^n.
  - Multiply-style midtones (other panels): Mn = x^n·(1−x)^n, narrowing with n; often renormalized by 4^n so peak = 1.
- Reference implementation (float32, linear or gamma? — pros compute on the *gamma-encoded* document values, so do the same to match Photoshop):
  ```python
  def lum(img):  # img float RGB 0..1, gamma-encoded document values
      return 0.299*img[...,0]+0.587*img[...,1]+0.114*img[...,2]   # approx PS "RGB composite" luminosity
  x = lum(img)
  L = {n: x**n for n in range(1,7)}; D = {n:(1-x)**n for n in range(1,7)}
  M_tk = {n: (1-L[n])*(1-D[n]) for n in range(1,5)}               # TK subtraction style (widens)
  M_mul = {n: (L[n]*D[n])*4**n for n in range(1,5)}                # multiply style, normalized peak 1
  def zone(x, c, w, peak=0.9):  # bell around tone c, width w (sigma in 0..1 units)
      return peak*np.exp(-0.5*((x-c)/w)**2)
  def zone_tri(x,c,half):  # TK Blend-If-like triangular zone: c=0.5,half=0.25 => Zone 3 (128 ±64)
      return np.clip(1-np.abs(x-c)/half,0,1)
  # Saturation (HSV-style) and vibrance:
  mx, mn = img.max(-1), img.min(-1); S = (mx-mn)/(mx+1e-6); V_mask = 1-S
  Sn = S**n ; Vn = (1-S)**n   # Vibrance-3..5 = more restrictive
  # Hue (colour-range) mask with circular distance and soft falloff:
  dh = np.abs(((H - h0 + 0.5) % 1.0) - 0.5); hue_mask = np.clip(1 - (dh - tol)/fall, 0, 1) * smoothstep(S, s_lo, s_hi)
  ```
  Multiply hue mask by a saturation ramp so near-grey pixels (unstable hue) are excluded — this mirrors how Color Range/HSL tools behave.
- Mask "modify" operations used by TK/Lumenzia (Levels/Curves on the mask, paint-through, "dodge/burn the mask") are just tone curves applied to the mask array; e.g., Lumenzia's auto-levels on preview ≈ percentile stretch of mask values inside a user-indicated region.
- When to use: Lights for sky/highlight recovery; Darks for shadow lift without grey-ing; Midtones for contrast/clarity/saturation without blowing ends; Zone masks to target a picked tone (e.g., a specific grey of fog); Vibrance masks to boost only dull colours (avoids oversaturating already saturated areas); Saturation masks to tame hot colours.
- Pitfalls: (1) marching ants hide <50% selections — always preview the mask; (2) 8-bit masks band in smooth skies — compute in 16/32-bit float; (3) narrow zone masks lack transition pixels → posterized edges; (4) luminosity masks select everything partially, so strong curves through L1 still move shadows.

### Gaps
- Exact luminance weights Photoshop uses for the composite-RGB luminosity channel (Ctrl+Alt+2) were not found in a primary source; commonly cited as Rec.601-like (0.30/0.59/0.11) but unverified here.
- Exact TK9 Midtones-2/3 formula (why M2/M3 measured 50%/84% vs selection-arithmetic predictions 56%/77%) not resolved.
- Lumenzia's internal zone-mask curve shape and its midtone definition were not documented in fetched pages (Lumenzia v11.7 page returned empty content).
- Kuyper's saturation-mask source page (satmask-1) returned 404; exact Photoshop recipe not retrieved.

---

## 3. Blend If: underlying math, split sliders, use for D&B and sky blending

### Takeaway
Blend If computes a per-pixel opacity from the value (Gray composite, or a single R/G/B channel) of This Layer and/or of the composite of all Underlying layers; unsplit sliders give hard thresholds, split sliders give a linear ramp between the two halves, and the This Layer and Underlying Layer results combine (multiply). It is a live, non-pixel mask—ideal for D&B layers (protect clipped highlights/shadows) and for blending skies/exposures by tone.

### Cited Findings
- Black slider: makes layer transparent where value is darker than the slider; white slider: transparent where lighter — [Damien Symonds](https://www.damiensymonds.net/the-blend-if-sliders-in-photoshop/)
- "Underlying Layer" refers to ALL layers beneath (composite), not just the one directly below — [Damien Symonds](https://www.damiensymonds.net/the-blend-if-sliders-in-photoshop/)
- Alt/Option-drag splits a slider; between the two halves values transition from transparent to opaque; wider gap → smoother transition; too wide includes/excludes unwanted detail — [Photoshop Training Channel](https://photoshoptrainingchannel.com/how-to-use-blend-if-photoshop/); [Damien Symonds](https://www.damiensymonds.net/the-blend-if-sliders-in-photoshop/); [Julieanne Kost (Adobe)](https://blogs.adobe.com/jkost/2013/02/blend-if-sliders-in-photoshop.html)
- Blend If "Gray" works on luminance; scaling is linear between the left and right split points — [Stephen Bay, Blend If vs Luminosity Masks](https://stephenbayphotography.com/blog/blend-if-vs-luminosity-masks/)
- Blend If can be set to an individual channel (e.g., Blue for skies) — [Damien Symonds](https://www.damiensymonds.net/the-blend-if-sliders-in-photoshop/)
- TK9: Blend If masks use luminosity data, are higher contrast than luminosity masks, and TK9 offers Pick-a-tone Blend If masks and Zone 1–5 Blend If groups (centres 0/64/128/192/255, tapering ±64) — [TK9 Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf)

### Inferences
- Math (consistent with the cited linear-ramp behaviour; 8-bit slider units → /255):
  ```python
  def ramp_up(v,a,b):   # black slider split (a=left half, b=right half); a==b -> hard step
      return np.clip((v-a)/max(b-a,1e-6),0,1) if b>a else (v>=a).astype(float)
  def ramp_down(v,c,d): # white slider split (c=left half, d=right half)
      return np.clip((d-v)/max(d-c,1e-6),0,1) if d>c else (v<=d).astype(float)
  a_this  = ramp_up(v_this,b0,b1)*ramp_down(v_this,w0,w1)
  a_under = ramp_up(v_under,ub0,ub1)*ramp_down(v_under,uw0,uw1)
  alpha_eff = layer_opacity * layer_mask * a_this * a_under
  out = blend(under, layer)*alpha_eff + under*(1-alpha_eff)
  ```
  where v_under is the composite of everything below (must be re-evaluated if lower layers change — Blend If is "live").
- Uses:
  - D&B (50% grey Overlay/Soft-light layer or curves pair): set Underlying black split ~0/30 and white split ~225/255 so dodging can't push already-bright highlights into clipping and burning can't block up shadows.
  - Sky replacement / exposure blending: on the sky layer, Underlying Gray (or Blue) black slider split so the new sky only shows where the base is bright (e.g., 150/200), keeping dark trees/buildings on top; then refine with a layer mask (Blend If and layer mask multiply).
  - Removing white background from logos/textures: This Layer white slider split (e.g., 230/250).
- Pitfall: Blend If transitions are linear in tone and therefore hard-edged in tone space; mid-tone gaps of <20 levels create posterized fringes; in 16-bit docs the slider is still 0–255 scaled.

### Gaps
- No Adobe primary document found specifying the exact formula for the "Gray" Blend If value (luminosity weights) or confirming multiplicative combination of This/Underlying; the multiply combination is inferred from observed behaviour, not verified.

---

## 4. Select and Mask / Refine Edge, decontaminate colours, defringing, halo avoidance; feathering vs blurring vs density

### Takeaway
Select and Mask is an edge-band matting tool: Edge Detection Radius / Smart Radius define the unknown band in which it estimates partial alpha; Global Refinements (Smooth, Feather, Contrast, Shift Edge) post-process the mask; Decontaminate Colors replaces edge pixel colours with nearby foreground colours. Halos come from residual background colour in partially transparent pixels and are fixed by colour decontamination (foreground estimation), a slight negative Shift Edge, or edge-band re-colouring — not by blurring.

### Cited Findings
- Radius expands the refinement area along the edge; Smart Radius lets the radius contract/expand along the edge depending on content. Higher radius captures more detail but can include background; lower is conservative — [Creative Bloq, Refine Edge explained](https://www.creativebloq.com/advice/photoshop-anatomy-the-refine-edge-box-tool-explained); [Markus Hagner, Select and Mask guide (2026)](https://markus-hagner-photography.com/how-to-use-the-select-and-mask-workspace-in-photoshop-for-complex-cutouts/)
- Contrast creates a harder edge; Shift Edge pushes the edge in/out; shifting inward helps remove halos, sometimes medium values ~−20% — [Creative Bloq](https://www.creativebloq.com/advice/photoshop-anatomy-the-refine-edge-box-tool-explained); [TrickyPhotoshop](https://tricky-photoshop.com/refine_edge_tool/)
- Decontaminate Colors replaces colours of selected edge pixels with colours from nearby pixels; Amount controls how many edge pixels are changed — [Creative Bloq](https://www.creativebloq.com/advice/photoshop-anatomy-the-refine-edge-box-tool-explained)
- Halos appear because the mask carries traces of the old background colour around each hair strand, worst when new background contrasts strongly; Decontaminate Colors fixes halos without AI credits but looks flatter/less detailed than Photoshop's newer (AI) "Enhance Edge" — [ColorExpertsBD, Hair masking in Photoshop v27 beta](https://www.colorexpertsbd.com/blog/hair-masking-in-photoshop/)
- Guided-filter "guided feathering" was benchmarked against Photoshop Refine Edge and closed-form matting (parameters r=60, ε=1e-6) in He et al. — [Guided Image Filtering (He, Sun, Tang)](https://www.sensetime.com/xo/profile/upload/2024/05/23/2012%20Guided%20Image%20Filtering_20240523184437A013.pdf); [Wikipedia: Guided filter](https://en.wikipedia.org/wiki/Guided_filter)

### Inferences
- Pro procedure for hair on a new background: rough selection (Select Subject/Object, or channel mask) → Select and Mask → Refine Hair / Refine Edge Brush over the hair band → Edge Detection radius small for hard edges (1–3 px) and larger or Smart Radius for hair (10–30 px+) → Shift Edge slightly negative (−5 to −20%) for halos → output to New Layer with Layer Mask; Decontaminate only when needed (it bakes pixels and flattens texture) → in many high-end workflows a manual alternative is preferred: a clipped layer above the cutout, set to Color (or Normal) blend, painting/sampling hair colour along the edge, or using "Defringe/Remove Color Matte" style ops.
- Feather vs blur vs density:
  - Feather (selection/mask property) = Gaussian blur of the mask edge, non-destructive in Properties panel; symmetric — it spreads the edge both into and out of the object, so it can let background leak (halo) unless the path is inside the edge.
  - Blurring the mask pixels = same math, destructive.
  - Density (Properties panel) = scales mask so black becomes (1−density) grey: m' = 1 − density·(1 − m); used to fade an adjustment's exclusion zone rather than its edge.
  - Lightroom/LrC brush "Feather" & "Flow/Density" analogues behave similarly.
- Programmatic equivalent of Select & Mask:
  1. coarse mask m0 (segmentation) → 2. trimap: fg = erode(m0>0.5, r_in), bg = erode(m0<0.5, r_out), unknown = rest (Edge Detection Radius ≈ unknown band width; "Smart Radius" ≈ make the band width proportional to local edge uncertainty, e.g., wider where hair-class probability or local gradient variance is high) → 3. alpha matting in unknown band (ViTMatte / closed-form via pymatting / guided filter) → 4. Global refinements: Smooth = small median/morphological open-close on alpha; Feather = Gaussian σ; Contrast = sigmoid/levels on alpha around 0.5: a' = clip((a−0.5)·k+0.5); Shift Edge = levels offset or erode/dilate by fractional px (a' = clip(a + s)) → 5. Decontaminate = foreground colour estimation F such that I = αF + (1−α)B, e.g., `pymatting.estimate_foreground_ml(img, alpha)`; composite F over the new background, not the original pixels.
  ```python
  from pymatting import estimate_alpha_cf, estimate_foreground_ml
  alpha = estimate_alpha_cf(img, trimap)              # closed-form matting (Levin et al.)
  F = estimate_foreground_ml(img, alpha)              # decontaminated colours (fixes halos)
  out = alpha[...,None]*F + (1-alpha[...,None])*new_bg
  ```
- Halo checklist: (a) composite onto pure black and pure white plus the final background to inspect; (b) halos of light around dark subjects = background colour in F → decontaminate; (c) dark/light line = mask edge offset → Shift Edge / erode 0.5–1 px; (d) "glow" from feathering → reduce feather and choke instead.

### Gaps
- Adobe's own Select and Mask documentation (helpx) returned 403; exact slider ranges (Smooth 0–100, Feather 0–1000 px, Contrast 0–100%, Shift Edge −100…+100%) are from memory and should be verified.
- Adobe's algorithm for Select & Mask / Refine Hair / "Enhance Edge" (2025–26 AI edge) is not publicly documented.
- Closed-form matting (Levin, Lischinski, Weiss, CVPR 2006 / PAMI 2008) primary paper not fetched here; pymatting function names are from library knowledge, not verified in this session.

---

## 5. Pen tool / path clipping standards for product work

### Takeaway
For hard-edged products the industry standard is still a hand-drawn Pen-tool vector path, placed slightly inside the true edge, converted to a selection/vector mask with 0–1 px feather (0.5 px common), with retouching layers clipped to the cutout. AI segmentation is used to speed up but final e-commerce deliverables are typically path-based.

### Cited Findings
- A clipping path is a vector outline drawn with the Pen Tool, producing clean cutouts; it remains the industry standard for e-commerce photography, catalog printing and marketplace listings; typical product needs 20–40 anchor points — [LayerEdits, How to create a clipping path](https://layeredits.com/blog/how-to-create-clipping-path-photoshop); [PathEdits, What is a clipping path](https://pathedits.com/blogs/tips/what-is-a-clipping-path)
- Hard-edged products are best selected with a clipping path — [ColorExpertsBD, Clipping path for e-commerce](https://www.colorexpertsbd.com/blog/clipping-path-for-e-commerce-product-photography/)
- Stay slightly inside the actual edge so background isn't included; Make Selection with a small feather such as 0.5 px for a soft edge, or 0 px for a hard edge; clip retouching layers (Alt+Ctrl+G / Opt+Cmd+G) so painting past the edge disappears — [ClippingPathStudio, Pen tool in-depth](https://clippingpathstudio.com/pen-tool-in-photoshop/); [PHLEARN, How to use the Pen Tool](https://phlearn.com/tutorial/use-pen-tool-photoshop/)
- Users report paths becoming "feathered" because Make Selection's anti-aliasing/feather defaults — check the dialog — [Adobe Community thread](https://community.adobe.com/t5/photoshop/making-path-into-selection-why-always-feathered/m-p/8759881)

### Inferences
- Pro spec synthesized: path 0.5–1 px (at 100% zoom on full-res) inside the edge to avoid background fringe; anchor points only at extrema/inflection points with handles ~1/3 of segment length (smooth curves, fewer points); anti-aliased conversion, feather 0–0.5 px for sharp-focus products (up to ~1 px for slightly soft lens edges; more only to match depth-of-field blur); separate subpaths for holes (handles, straps) set to Exclude; save paths in the file (clients' DAM/print workflows read named paths).
- Programmatic path equivalent: (1) get a high-res mask (BiRefNet_HR/ SAM + matting); (2) extract contour (`cv2.findContours`, CHAIN_APPROX_NONE) at subpixel accuracy (marching squares on alpha=0.5 via `skimage.measure.find_contours`); (3) offset inward 0.5 px (`shapely` buffer(−0.5) or distance transform); (4) fit cubic Béziers (Schneider's curve-fitting algorithm, e.g., `potrace`-style or `fitCurves`) with an error tolerance ~0.25–0.5 px and corner detection by angle threshold; (5) rasterize with anti-aliasing at supersampling 4×–8× and optional Gaussian σ≈0.3–0.5 px; (6) export as Photoshop path via SVG/PSD writer if a deliverable path is needed.
- Hybrid: use vector paths for rigid geometry (bottles, electronics) and matting for soft parts (fur, fabric fringe, hair on models) — combine masks with max/min.

### Gaps
- No authoritative published "standard" (e.g., from Amazon/major retouching studios) specifying exact px offset or feather; numbers above come from tutorials and vendor blogs, not formal specs.

---

## 6. Mask refinement operations (levels on mask, gaussian blur, min/max, guided filter / edge-aware refinement)

### Takeaway
Pros refine masks with a small toolkit: Levels/Curves (contrast/choke via tone), Gaussian Blur (feather), Minimum/Maximum (choke/spread), painting in Overlay mode, and edge-aware tools (Refine Edge). In code these map to `np.clip` tone curves, `cv2.GaussianBlur`, `cv2.erode/dilate` (or grey-scale morphology), and the guided filter / fast guided filter, which is the closest open-source analogue to an "edge-aware Refine Edge".

### Cited Findings
- TK9 MODIFY tools for Edge masks include Maximum (expand selected areas), Minimum (contract), Invert, Gaussian Blur — the standard pro mask-refinement primitives — [TK9 Manual](https://goodlight.us/writing/tk9/TK9-Instructions-Manual.pdf)
- Guided filter (He, Sun, Tang, ECCV 2010 / TPAMI 2013): local linear model q = a_k·I + b_k in each window; radius r sets neighbourhood size, ε sets smoothing vs edge preservation; has a theoretical connection to the matting Laplacian; "guided feathering" refines a binary mask into an alpha matte near object boundaries — [Wikipedia: Guided filter](https://en.wikipedia.org/wiki/Guided_filter); [He et al. paper](https://www.sensetime.com/xo/profile/upload/2024/05/23/2012%20Guided%20Image%20Filtering_20240523184437A013.pdf); [MathWorks: What is guided image filtering](https://www.mathworks.com/help/images/what-is-guided-image-filtering.html)
- Automatic trimap generation via independent Erode and Dilate radii (0–200) — erode shrinks definite foreground, dilate expands unknown region — [Matte Anything / Supervisely matting docs (search summary)](https://developer.supervisely.com/app-development/neural-network-integration/inference/image-matting)

### Inferences
- Code mapping:
  ```python
  levels = lambda m,lo,hi,g=1.0: np.clip((m-lo)/(hi-lo),0,1)**(1/g)   # "choke via levels": raise lo
  feather = lambda m,s: cv2.GaussianBlur(m,(0,0),s)
  choke   = lambda m,r: cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r+1,2*r+1)))  # = PS Minimum
  spread  = lambda m,r: cv2.dilate(m, ...)                                                       # = PS Maximum
  # sub-pixel choke: blur then levels: feather(m,1.0) -> levels(m,0.6,1.0)  (edge moves inward ~<1px)
  gf = cv2.ximgproc.guidedFilter(guide=img_u8, src=mask_f32, radius=8, eps=1e-3)  # opencv-contrib
  ```
  Typical guided-filter settings for mask refinement: guide = RGB (or luminance) image, r = 4–16 px at full res for product/skin edges, r = 30–60 px for hair-scale fuzz, ε = 1e-4…1e-2 (on 0–1 data; smaller ε = follows image edges more tightly). Fast guided filter (subsampling factor s=4) for 50+MP images.
- Edge-aware alternatives: joint bilateral filter, domain transform, "Deep Guided Filter"; matting Laplacian solve for the band only.
- Order of ops pros use: fix interior holes (paint/close) → choke/spread to position edge → Levels for edge hardness → small feather (0.3–1 px) to match lens softness → inspect on black/white/red overlay. Avoid blurring then hardening repeatedly (rounds corners, loses fine detail).
- "Mask from mask" combos: intersect (multiply) a luminosity mask with an AI subject mask to restrict tonal adjustments to the subject; subtract (A·(1−B)) to exclude.

### Gaps
- Photoshop's Minimum/Maximum "Roundness" vs "Squareness" option behaviour and exact kernel not documented in fetched sources.

---

## 7. Programmatic equivalents: alpha matting & segmentation models (closed-form, guided filter, ViTMatte, MODNet, BiRefNet, SAM/SAM 2/SAM 3, face parsing) and how they compare to pros' expectations

### Takeaway
State of the art (2026) for an agent: segmentation for "what" (SAM 2/SAM 3, BiRefNet, face parsers) + matting for "how much" at edges (ViTMatte with an auto trimap, BiRefNet-matting/HR-matting trimap-free, pymatting closed-form as CPU fallback) + foreground colour estimation to kill halos. Models deliver good subject masks but pros still expect sub-pixel accurate, halo-free, temporally/print-ready edges, especially on hair, fine foliage, transparent/reflective products — which usually requires the matting + decontamination + manual-style refinement stack.

### Cited Findings
- BiRefNet (MIT): base 1024×1024 (Swin-L); BiRefNet_HR trained at 2048×2048 (Feb 2025); BiRefNet_dynamic trained on 256–2304 px dynamic resolutions (Mar 31, 2025) "robust on any resolution"; BiRefNet-matting (Oct 2024) and BiRefNet_HR-matting (Feb 2025) for trimap-free matting; BiRefNet_lite-2K (Swin-T, 2560×1440); portrait variant — [BiRefNet GitHub](https://github.com/ZhengPeng7/BiRefNet); [HF BiRefNet-matting](https://huggingface.co/ZhengPeng7/BiRefNet-matting)
- BiRefNet-matting reports S-measure 0.979 on TE-P3M-500-NP — [PromptLayer model card](https://www.promptlayer.com/models/birefnet-matting/)
- ViTMatte: first matting system on plain pre-trained ViTs; SOTA on Composition-1k and Distinctions-646 at publication; Composition-1k SAD ≈ 21.5, MSE ≈ 3.3 vs MODNet SAD ≈ 47.1 (aggregated comparison) — [ViTMatte, Information Fusion vol.103](https://dl.acm.org/doi/10.1016/j.inffus.2023.102091); [search-result summary of comparative tables; the originating table (possibly the BEN paper) was not verified](https://arxiv.org/html/2501.06230v1). Note: MODNet is a trimap-free portrait model, so this is not an apples-to-apples comparison with trimap-based ViTMatte.
- ViTMatte is "significantly more accurate on hair, fur and translucent edges" when given a trimap, but needs one; recommended cascade: BiRefNet coarse mask → trimap (erode/dilate) → ViTMatte or pymatting → FBA foreground estimation; pymatting (MIT) often 10–100× faster than deep models when a trimap is available and runs on CPU; MatAnyone (CVPR 2025) for temporally stable video matting — [Background removal library landscape (Apr 2026)](https://ice-ice-bear.github.io/posts/2026-04-13-matting-libraries/)
- Matte Anything: SAM for contour + open-vocabulary detector for transparency → pseudo-trimap via erosion/dilation → pretrained matting model (ViTMatte) for alpha — [Matte Anything (ResearchGate)](https://www.researchgate.net/publication/371375587_Matte_Anything_Interactive_Natural_Image_Matting_with_Segment_Anything_Models)
- SAM 3 (Meta, released Nov 19, 2025): Promptable Concept Segmentation — text noun-phrase or exemplar prompts return masks + IDs for every matching instance (SAM 1/2 were one object per prompt); detects/segments/tracks in images and video; SA-Co benchmark (120K images, 1.7K videos, 200K+ concepts); SAM License, checkpoints + code released — [Roboflow: SAM 3](https://blog.roboflow.com/what-is-sam3/); [MarkTechPost](https://www.marktechpost.com/2025/11/20/meta-ai-releases-segment-anything-model-3-sam-3-for-promptable-concept-segmentation-in-images-and-videos/); [Ultralytics docs](https://docs.ultralytics.com/models/sam-3)
- Community pipelines already pair SAM3 + ViTMatte (e.g., Nuke gizmo) and SAM3 + luma-derived matte blending for soft details (eye, highlight, reflection) — [Nuke-Sam3-Gizmo](https://github.com/Likhith-24/Nuke-Sam3-Gizmo); [sam3-soft-matte](https://github.com/tenpel/sam3-soft-matte)
- Recent research (2026) on unified segment+matte models (e.g., "Segment and Matte Anything in a Unified Model", SAM2Matting) indicates convergence of SAM-style prompting with alpha output — [arXiv 2601.12147](https://arxiv.org/html/2601.12147v1); [SAM2Matting arXiv 2606.27339](https://arxiv.org/pdf/2606.27339)
- Face parsing: CelebAMask-HQ has 512×512 masks, 19 classes: background, skin, l_brow, r_brow, l_eye, r_eye, eyeglass, l_ear, r_ear, earring, nose, mouth, u_lip, l_lip, neck, necklace, cloth, hair, hat — [CelebAMask-HQ GitHub](https://github.com/switchablenorms/CelebAMask-HQ); BiSeNet implementations with pretrained weights + ONNX export (yakhyo/face-parsing), LiteRT port on HF; SegNeXt face parser reportedly much better than BiSeNetV2 — [yakhyo/face-parsing](https://github.com/yakhyo/face-parsing); [FaceParsing-SegNeXt](https://github.com/AiArt-Gao/FaceParsing-SegNeXt); [HF BiSeNet LiteRT](https://huggingface.co/litert-community/BiSeNet-Face-Parsing-LiteRT)
- Diffusion-based matting exists (e.g., SDMatte 2025, layer-diffusion portrait mattes) — excluded by the no-generative constraint but note they are in the SOTA landscape — [SDMatte arXiv](https://arxiv.org/pdf/2508.00443); [arXiv 2501.16147](https://arxiv.org/pdf/2501.16147)

### Inferences
- Recommended agent stack (non-generative):
  1. Subject/object: BiRefNet_HR or _dynamic (MIT, commercial-friendly) for "main subject"; SAM 2/SAM 3 for prompted objects/parts (check SAM License terms for SAM 3).
  2. Parts: BiSeNet/SegNeXt face parsing at 512 px on an aligned face crop → upsample label probabilities, then guided-filter with the full-res crop to snap to edges; combine skin = skin+nose+neck (minus eyes/brows/lips/hair) for skin retouch masks; lips = u_lip+l_lip; eyes = l_eye+r_eye (iris/sclera need a further colour/brightness split).
  3. Edges: trimap from coarse mask (erode ~3–10 px fg, dilate ~10–40 px for hair, scaled with image resolution) → ViTMatte (HF `VitMatteForImageMatting`) or pymatting closed-form for CPU → `estimate_foreground_ml` for colour decontamination.
  4. Tone/colour restriction: multiply AI mask with luminosity/hue/saturation masks (Section 2) for pro-style "selective" adjustments.
- Gap between model output and pro expectation:
  - Segmentation models output near-binary, low-res-upsampled masks (SAM decoder 256×256 logits upsampled) → stair-stepping/blobby edges; pros expect edges matching lens sharpness within ~0.5 px.
  - Hair: models give a helmet or clump; pros expect individual strands and flyaways with correct partial alpha and no colour spill — needs matting + decontamination.
  - Foliage/sky: channel masks routinely beat AI for fine branches; AI sky masks tend to be smooth and miss sky holes in leaves → combine AI sky mask with a Blue-channel luminosity mask (intersect/union).
  - Transparent/reflective products (glass, plastic): neither segmentation nor matting reliably separates refraction/reflection; pros use paths + separate reflection/shadow layers.
  - Print/large-format: models trained ≤2K need tiling or HR variants; run at native res with BiRefNet_HR/dynamic, or run coarse then refine in edge band at full res.
- Quality check metrics an agent can compute: compare against a manually defined trimap band — gradient error and connectivity error (standard matting metrics), plus visual composite on black/white/50% grey.

### Gaps
- No benchmark found directly comparing these models to professional retoucher masks.
- Exact current licenses for SAM 2 (Apache-2.0 per memory) and ViTMatte weights were not verified in this session.
- No first-hand numbers fetched for MODNet beyond the SAD comparison.

---

## 8. Masking strategies for local adjustments (radial/gradient masks; Lightroom/Capture One AI masks: subject, sky, skin, people parts)

### Takeaway
Raw editors now provide AI semantic masks (subject, sky, background, objects, people parts, landscape classes) combined with parametric masks (linear/radial gradients, brush, luminance/colour/depth range) via add/subtract/intersect. The pro strategy is "semantic mask ∩ parametric/tonal mask, feathered," reproducible in code by multiplying a segmentation mask with gradient and range masks.

### Cited Findings
- Lightroom Classic masking panel: Subject, Sky, Background; Objects; Brush, Linear Gradient, Radial Gradient, Range; People — [The Lens Lounge, Masking in LrC](https://thelenslounge.com/how-to-mask-in-lightroom-classic/)
- People masks: entire person, face skin, body skin, eyebrows, eye sclera, iris & pupil, lips, teeth, hair; each person detected individually — [The Lens Lounge](https://thelenslounge.com/how-to-mask-in-lightroom-classic/); [Adobe Community quick tips](https://community.adobe.com/t5/lightroom-classic-discussions/use-people-masking-for-specific-edits-in-lightroom-classic-quick-tips/td-p/13683492)
- Landscape masks: sky, architecture, vegetation, water, mountains, natural/artificial ground in one click — [Lightroom-tools.com](https://lightroom-tools.com/blog/lightroom-classic-masking-tools); [Photofocus](https://photofocus.com/software/lightroom-lightroom-classic-get-more-ai-masking-content-aware-remove/)
- Adobe help: masking with AI controls in Lightroom (web) — [Adobe Help](https://helpx.adobe.com/lightroom/web/edit-photos/apply-masks/mask-with-ai.html)
- Capture One: Magic Brush fills areas of similar colour to the stroke (since C1 21 14.3); AI brush builds an object map then shows object mask previews on hover — [Capture One Support: Magic Brush](https://support.captureone.com/hc/en-us/articles/4403193308049-Magic-Brush); [Michal Krause on C1 AI masks](https://www.michalkrause.com/en/new-version-of-capture-one-adds-ai-masks-and-retether-feature/)

### Inferences
- Code equivalents:
  ```python
  # Linear gradient (LR-style): full effect before p0, zero after p1 along direction
  t = ((X-x0)*dx + (Y-y0)*dy)/((x1-x0)*dx+(y1-y0)*dy); lin = 1 - smoothstep(0,1,t)
  # Radial (elliptical) with feather f in [0,1]: r = normalized ellipse radius
  r = np.sqrt(((Xr)/a)**2 + ((Yr)/b)**2); rad = 1 - smoothstep(1-f, 1, r)   # invert for vignette
  # Range masks: luminance range with smooth falloff, colour range in Lab ΔE, depth range from depth model
  mask = subject * (1 - sky) * lin * lum_range(x, lo, hi, soft)
  ```
  smoothstep matches LR's soft falloff better than linear ramps.
- Strategies used by pros: graduated filter for sky then subtract Subject (keeps foreground buildings/trees unaffected); radial "light painting" intersected with luminance range to brighten only already-lit areas; people-part masks for skin (exposure/texture), iris (+exposure/+saturation small), teeth (−saturation yellow), lips; landscape class masks for vegetation hue shifts; always check mask overlay at 100% for edge errors, then refine with brush subtract at low flow.
- Capture One's Magic Brush ≈ flood-fill/colour-similarity region growing; programmatic analogue: `cv2.floodFill` with tolerance in Lab or graph-based region growing seeded by strokes, then guided-filter smoothing.

### Gaps
- Capture One's 2025–2026 people-part masking specifics (whether it offers skin/eyes/lips parts like LrC) not confirmed in fetched sources.
- Lightroom's internal feather curve shape for gradients and exact AI model resolution not documented.
