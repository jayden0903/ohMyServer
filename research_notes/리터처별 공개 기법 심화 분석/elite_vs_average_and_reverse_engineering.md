# Elite vs. Average Retouching, and Reverse-Engineering Professional Edits from Before/After Pairs

Research date: 2026-10-02. Scope: concrete, visible, describable qualities that separate elite retouching from average; a defect taxonomy; QC/rubric practices; and non-generative methods to extract "what was changed" from before/after pairs so an agent can learn a retoucher's taste and score its own output.

Access notes: Reddit (r/retouching) returned HTTP 403 to both search and direct JSON fetch; PNAS (Kee & Farid full text), DPReview forum thread, and Shutterstock blog returned 403; ModelMayhem not reached. Findings from those are limited to search-result snippets and are flagged as such.

---

## Q1. What concrete, visible qualities distinguish elite retouching from average retouching?

### Takeaway
Pros consistently define elite work by what is *preserved* and how *invisible* the work is: texture retained (only perfected, not removed), smooth macro tonal transitions that read as 3D form consistent with the existing light, micro-transitions cleaned without smoothing, color variation kept but blotchiness removed, consistency across body parts and across a set, and restraint (smallest effective change). Average work shows the opposite: more change = "better" assumption, blur-based skin, dodge-only flattening, patchy/desaturated D&B, halos and crunchiness.

### Cited Findings
- Restraint is an explicit judging criterion: "some beginner retouchers mistakingly assume that the greater the difference between the original photo and the retouched version, the better the retouch" — professional work requires restraint, especially when the original was professionally shot — [Retouching Academy, Challenge #2 Results (Julia Kuzmenko McKim)](https://retouchingacademy.com/challenge-2-results-overview/)
- Texture is to be perfected, not removed: "Humans have skin texture! Your job is to make that skin texture look perfect, not to remove it"; blur-based retouching discouraged — [Fstoppers, Ryan Cooper, 6 Loathsome Retouching Mistakes](https://fstoppers.com/originals/6-loathsome-retouching-mistakes-drive-editors-insane-103122)
- Two scales of tonal transition: *macro* transitions = global tone shifts caused by 3D form (forehead shape, nose shadow), visible zoomed out; *micro* transitions = tiny value shifts from bumps/hollows visible only zoomed in. "Over smoothing" is named as a primary flaw; elite approach is addressing micro transitions with dodge & burn rather than heavy frequency separation — [Retouching Academy, Dodge & Burn: Working with Micro Transitions (Julia Kuzmenko McKim)](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
- Elite practitioner (Pratik Naik) intentionally keeps color variation: "I like leaving a lot of color variations in the skin intentionally to illustrate a more human element"; process is healing/cloning first, then "dodging and burning till any transitions are evened out"; quality bar is internal: "the job isn't over when the client is happy, it keeps going till I am happy" — [The Retouchist, Interview with Pratik Naik](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- Naik: "A great retouched image is more about the mindset and game plan than it is about the techniques" (search-result snippet, CreativeLive course page) — [CreativeLive, The Art & Business of High-End Retouching](https://www.creativelive.com/classes/art-business-high-end-retouching-pratik-naik)
- Volume/form must follow the existing light: muddy D&B "typically stems from not properly reading the light source first"; dodge strokes go on planes facing the key light, burn on receding areas (under cheekbone, sides of nose) (search snippet) — [photoshoptutorial.com, Why Your Retouching Looks Flat](https://photoshoptutorial.com/posts/why-your-retouching-looks-flat-and-how-dodge-and-burn-fixes-it/)
- Dodge-only work leaves skin "inaccurately light, as well as lacking any depth or contrast"; dodging too many dark areas yields "unrealistic luminosity" and flat texture; over-dodging highlights makes skin "appear oily rather than fresh" — [Retouching Academy, 5 Mistakes to Avoid While Dodging and Burning (Kendra Paige)](https://retouchingacademy.com/5-mistakes-to-avoid-while-dodging-and-burning/)
- Working too zoomed-in (≥100%) leads to "minimal impact or ... removed texture to the point of making skin appear waxy"; take breaks to avoid over-retouching — [Retouching Academy, 5 Mistakes](https://retouchingacademy.com/5-mistakes-to-avoid-while-dodging-and-burning/)
- Cross-region color consistency: "most participants did not address the difference of the skin tones between the face and the hand" — matching hand tone to face elevates the image — [Retouching Academy, Challenge #2](https://retouchingacademy.com/challenge-2-results-overview/)
- Attention to detail/distractions distinguishes winners: misaligned stick-on nails, overdrawn upper lip (revealed by strobing highlights), hairline handled at a "middle ground" (neither over-corrected nor ignored) — [Retouching Academy, Challenge #2](https://retouchingacademy.com/challenge-2-results-overview/)
- Eyes: "eye whites shouldn't ever be white"; reduce eye-brightening layer opacity ≥50% ("demon eyes") — [Fstoppers, Ryan Cooper](https://fstoppers.com/originals/6-loathsome-retouching-mistakes-drive-editors-insane-103122)
- Tonal range: "highlights shouldn't be pure white, clouds shouldn't be black"; over-processed local contrast produces glowing edges ("crunchy") — [Fstoppers, Ryan Cooper](https://fstoppers.com/originals/6-loathsome-retouching-mistakes-drive-editors-insane-103122)
- Effects must be physically motivated: flare without a corresponding light source looks fake — [Fstoppers, Ryan Cooper](https://fstoppers.com/originals/6-loathsome-retouching-mistakes-drive-editors-insane-103122)
- Group-level consistency is a formal professional requirement: in PPR10K, expert retouchers (>5 yrs industry) were told to meet "output standards of professional portrait photography studios" with two requirements: visually pleasing especially in human regions, and a group of photos "adjusted to have a consistent tone"; each expert also had to be self-consistent across similar scenes — [PPR10K, CVPR 2021 paper PDF](https://www4.comp.polyu.edu.hk/~cslzhang/paper/PPR10K-cvpr21-paper.pdf)
- Retouching style is legitimately plural: five FiveK retouchers produced outputs "from a sunset mood ... to a day light look"; "There is no single good answer and the retoucher's interpretation plays a significant role" — [Bychkovsky et al., CVPR 2011](https://people.csail.mit.edu/vladb/photoadjust/db_imageadjust.pdf)

### Inferences
- Operational "elite" signature, expressed as measurable properties of the (after − before) pair:
  1. Small total change magnitude relative to the defect load (restraint) — low mean |ΔL| outside defect regions.
  2. High-frequency band energy in skin roughly preserved (texture not removed); changes concentrated in mid/low frequency bands (tone, transitions).
  3. Low-frequency luminance changes are smooth and correlated with surface orientation relative to the key light (D&B follows form), not random blobs.
  4. Chroma (a*, b*) of skin regions has reduced *local blotchiness* but retained *large-scale variation* (Naik's "color variation").
  5. Consistency: per-region mean Lab across skin regions of the same person (face vs hands vs neck) and across a set converges.
  6. No new artifacts: no halos at edges, no banding, no clipped whites/blacks, no clone repetition.
- "Taste" is per-retoucher (FiveK diversity), so learning should be per-person from that person's pairs rather than a single universal target.

### Gaps
- No studio (Gloss, Loupe, Happy Finish, Box, Saddington Baynes, Stanton Hunter, Electric Art, Pixelstorm) was found publishing explicit, itemized quality criteria for skin/tone; their public sites are portfolio/marketing. The descriptors above come from educators/practitioners and contests rather than studio documents.

---

## Q2. How do top studios describe quality standards, QC, revision rounds, and what art directors check? Are there published QC checklists?

### Takeaway
Top studios do not publish QC checklists; what is public is (a) producer/AD-side process guides (rounds, consolidated feedback, batching), (b) competition jury criteria (brief adherence, visual quality, technical precision, layer hygiene), and (c) vendor-published QA checklists (mostly e-commerce oriented but concrete). Together they give a usable QC protocol: brief compliance → batch scan → 100% zoom on high-risk zones → set-level consistency.

### Cited Findings
- Revision structure: "Round 1 delivery will take the longest, and subsequent revision rounds can be progressively shorter"; with agency + brand, first 1–2 rounds are internal then the process "resets" with the brand; consolidated feedback per round is "the most efficient"; new stakeholders mid-process cause "New-Notes" — [verybusy.io, Producer's Guide to Working with Retouchers Pt 2](https://verybusy.io/blog/the-producer-s-guide-to-working-with-retouchers-part-2)
- Retouchers work non-linearly in task batches across all files (clipping/masking, then color, then cleanup); example schedules show AD review at R1, R2 with 2–3 business-day feedback windows — [verybusy.io Pt 2](https://verybusy.io/blog/the-producer-s-guide-to-working-with-retouchers-part-2)
- Rates typically include 1–2 rounds of feedback (search snippet) — [verybusy.io Pt 2](https://verybusy.io/blog/the-producer-s-guide-to-working-with-retouchers-part-2)
- AD-facing glossary of defects ADs look for: chromatic aberration (color fringing at high-contrast edges), clipping (pure white/black with no detail), color contamination (reflected color tinting skin, e.g. green shirt), banding ("abrupt color steps instead of smooth transitions"), moiré, sharpening halos, color matching across an image and between images — [verybusy.io, Glossary of Retouching Terms for Art Directors](https://verybusy.io/blog/a-glossary-of-retouching-terms-for-art-directors)
- Retoucher of the Year jury criteria: "adherence to the brief, visual quality, and technical precision"; anonymous, three rounds by regional juries; juries include "senior retouchers, photographers, creative directors, cinematographers, and quality controllers from top studios"; technical assessment examines layered PSDs for "clear layer structure and naming" — [Retoucher of the Year, About](https://retoucheroftheyear.com/about-the-competition)
- AOP Martin Evening Excellence in Digital Retouching Award: judges look for "a high degree of proficiency in post-production techniques, producing images with the utmost visual impact within a contemporary creative framework"; entries require before/after examples — [AOP Awards](https://www.aopawards.com/martin-evening-excellence-in-digital-retouching-award/)
- London agency The Retouchers (founder in Lürzer's 200 Best Digital Artists) frames QC as upstream: attending pre-production meetings "to ensure that the right shots are captured in the right way"; "advice is as valuable as our technical skills" — [The Retouchers, About](https://www.the-retouchers.com/about)
- PPR10K dataset QC: "hired another expert to double-check the retouched results and conducted several rounds of feedback-and-repair" — [PPR10K paper](https://www4.comp.polyu.edu.hk/~cslzhang/paper/PPR10K-cvpr21-paper.pdf)
- Published vendor QA checklist (Color Experts BD) — concrete items: no halos/jagged edges/chatter/color spill around cutouts; edges natural at 100% (hair/fur/mesh); shadows consistent in direction and softness; pure-white backgrounds sample RGB 255,255,255 if required; no gradient banding; WB consistent across set; product color matches swatch/Pantone; no clipped highlights unless intended; blacks not crushed; skin tones natural (no orange/gray casts); texture preserved (no plastic skin, waxy fabric, smeared grain); symmetry corrections subtle; at 100% check hairlines, jewelry prongs, glass, lace/mesh, straps for fringing, matte chatter, alpha holes, over-feathered edges, sharpening halos; smooth surfaces checked for patchy healing or repeating clone patterns. Method: Pass 1 batch scan 10–20 s/image; Pass 2 100% zoom on high-risk areas; Pass 3 set-based consistency (color temperature, shadow direction, scale, skin/product hue) — [Color Experts BD, Photo Editing QA Checklist](https://www.colorexpertsbd.com/blog/photo-editing-qa-checklist/)
- Pros' self-QC "check/helper layers": solar curve (6-point wave curves layer) exaggerates small tonal changes to reveal clone oversights, dust, inconsistent D&B, uneven transitions, banding, and flaws visible on phones but not standard monitors; B&W layer isolates tonal inconsistencies — [Fstoppers, Quentin Decaillet, How to Make Sure Your Pictures Are As Clean As Possible](https://fstoppers.com/photoshop/how-make-sure-your-pictures-are-clean-possible-60014)
- Retouching Academy "Visual Aid" setup: Curves to darken/add contrast + 50% gray layer in Color mode to remove color → reveals micro transitions — [Retouching Academy, Micro Transitions](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
- Viewing the D&B layer alone (Alt-click eye): "If it looks patchy or uneven, it will look patchy in your final image too" (search snippet) — [photoshoptutorial.com, Dodge and Burn manual shading](https://photoshoptutorial.com/posts/dodge-and-burn-in-photoshop-the-manual-shading-technique-that-makes-retouching-l/)

### Inferences
- An agent can replicate the human QC protocol as automated passes: (1) global stats (clipping %, histogram), (2) "solar curve" and desaturated-contrast renders fed to a defect detector, (3) zoomed tile inspection of high-risk masks (hairline, eyes, lips, edges), (4) set-level Lab statistics (PPR10K-style variance of means).
- The solar curve is essentially a high-gain periodic tone mapping; computationally equivalent to examining the luminance gradient / Laplacian of the low-frequency band for discontinuities.

### Gaps
- No public QC checklist from the named elite studios (Gloss, Loupe, Happy Finish, Box, Saddington Baynes, Stanton Hunter, Electric Art, Pixelstorm, Retouch Up) was found. Searches for Gloss/Loupe returned only company profiles (e.g., Loupe Digital is a fine-art print studio per [loupedigital.com](https://www.loupedigital.com/)).
- No public data on average number of revision rounds at high-end studios beyond the "1–2 rounds included" norm.

---

## Q3. Recurring critique terms on forums and in pro writing → defect taxonomy

### Takeaway
The recurring critique vocabulary maps cleanly onto measurable defect classes: texture loss (plastic/waxy), tone transition defects (patchy/muddy/blotchy/flat), color defects in D&B (desaturated patches, color blotches, contamination), edge defects (halo, fringing, chatter), gradient defects (banding/posterization), over-processing (crunchy, demon eyes, oily highlights), consistency defects (face vs hands, set mismatch), and detail/distraction misses.

### Cited Findings
- "Plastic skin" from excessive blur — [Fstoppers, Ryan Cooper](https://fstoppers.com/originals/6-loathsome-retouching-mistakes-drive-editors-insane-103122)
- "Waxy" skin from removing texture while zoomed in — [Retouching Academy, 5 Mistakes](https://retouchingacademy.com/5-mistakes-to-avoid-while-dodging-and-burning/)
- "Crunchy": over-processed tonal contrast creating glowing edges — [Fstoppers, Ryan Cooper](https://fstoppers.com/originals/6-loathsome-retouching-mistakes-drive-editors-insane-103122)
- "Patchy desaturated skin" caused by dodging on a gray D&B layer (lightening reduces saturation); fixed with a clipped Selective Color layer adding red/yellow back in Whites — [Jake Hicks, Fixing Discolouration During the Dodge & Burn Retouch](https://jakehicksphotography.com/latest-techniques/2018/6/15/fixing-discolouration-during-the-dodge-burn-retouch)
- "Muddy" D&B: harsh, muddy shadows from too much burn; hard-edged brushes leave visible patches (search snippets) — [photoshoptutorial.com, Why Your Retouching Looks Flat](https://photoshoptutorial.com/posts/why-your-retouching-looks-flat-and-how-dodge-and-burn-fixes-it/)
- "Flat": dodge-only or dodging dark areas → no depth/contrast, flat texture — [Retouching Academy, 5 Mistakes](https://retouchingacademy.com/5-mistakes-to-avoid-while-dodging-and-burning/)
- "Oily": over-dodged highlights — [Retouching Academy, 5 Mistakes](https://retouchingacademy.com/5-mistakes-to-avoid-while-dodging-and-burning/)
- Low-frequency (FS) misuse: small hard brush on low-frequency layer "create[s] visible blotches"; over-blurring causes "tonal flattening" / "watercolor" faces (search snippets) — [photoshoptutorial.com, Frequency Separation](https://photoshoptutorial.com/posts/frequency-separation-in-photoshop-retouch-skin-without-destroying-texture/); [PetaPixel, FS Primer](https://petapixel.com/2015/07/08/primer-using-frequency-separation-in-photoshop-for-skin-retouching/)
- Healing/cloning without separation smears texture "into a blurry mess" (search snippet) — [photoshoptutorial.com, Frequency Separation](https://photoshoptutorial.com/posts/frequency-separation-in-photoshop-retouch-skin-without-destroying-texture/)
- Edge/gradient defects for ADs: halos, banding, chromatic aberration, color contamination, clipping, moiré — [verybusy.io Glossary](https://verybusy.io/blog/a-glossary-of-retouching-terms-for-art-directors)
- Vendor QA defect terms: fringing, matte chatter, alpha holes, over-feathered edges, sharpening halos, patchy healing, repeating clone patterns, orange/gray skin casts — [Color Experts BD QA Checklist](https://www.colorexpertsbd.com/blog/photo-editing-qa-checklist/)
- Stock-agency rejection terms (search snippets): excessive noise/grain, compression artifacts, posterization; over-noise-reduction → soft image → "focus" rejection; over-sharpening → "halo artifacts" and "crispy", over-processed look — [Shutterstock Blog, Why Images Get Rejected For Noise](https://www.shutterstock.com/blog/why-images-get-rejected-for-noise); [Xpiks, Top photo rejection reasons](https://xpiksapp.com/blog/top-photo-rejection-reasons/)
- "Demon eyes" (over-white sclera, over-lit irises); "flare from nowhere"; uncleaned highlight clutter — [Fstoppers, Ryan Cooper](https://fstoppers.com/originals/6-loathsome-retouching-mistakes-drive-editors-insane-103122)
- Consistency/detail misses: face–hand skin-tone mismatch, nails, overdrawn lips, hairline — [Retouching Academy, Challenge #2](https://retouchingacademy.com/challenge-2-results-overview/)

### Inferences — proposed defect taxonomy with computable proxies (proposals, not from a single source)
| Defect (pro term) | Visible symptom | Candidate measurement on after vs before |
|---|---|---|
| Plastic / waxy | pores/fine texture gone | ratio of high-frequency (e.g., Laplacian-pyramid level 0–1) energy in skin mask, after/before; ≪1 = texture loss |
| Texture mismatch | healed patch has different grain than surroundings | local variance of HF band inside edited regions vs ring around them |
| Patchy / blotchy (tone) | uneven low-freq luminance islands | gradient magnitude / Laplacian of low-pass L in skin; solar-curve render contour density |
| Muddy | gray, low-chroma darkened areas | burned regions (ΔL<0) with simultaneous chroma drop or hue shift toward gray |
| Desaturated dodge patches | pale colorless spots | dodged regions (ΔL>0) with ΔC*<0 (Jake Hicks mechanism) |
| Color blotches | red/yellow islands in skin | spatial variance of a*, b* in low band within skin mask |
| Flat | lost 3D form | reduced low-frequency luminance range / contrast across face planes |
| Oily | hot specular areas | % of skin pixels near clip, size of highlight blobs |
| Crunchy / halo | glow along edges | overshoot in luminance profile perpendicular to strong edges; HF energy increase at edges |
| Banding / posterization | stepped gradients | histogram gaps/comb; quantized steps in smooth regions |
| Clipping | no detail in whites/blacks | % pixels at 0/255 per channel vs before |
| Clone repetition | repeated patterns | patch self-similarity / autocorrelation peaks in edited areas |
| Demon eyes | over-white sclera | sclera L* and chroma vs reference ranges; ΔL in eye masks |
| Inconsistency | face vs hands, set drift | ΔE between region means; PPR10K-style variance of a/b means across set |

### Gaps
- Could not access Reddit r/retouching, ModelMayhem retouching forum, or DPReview Retouching forum content directly (403/blocked); Facebook groups are not publicly accessible. The taxonomy is therefore built from educator/pro articles and vendor/agency sources rather than a forum corpus. A forum-frequency analysis of these terms remains undone.

---

## Q4. Methods to reverse-engineer edits from before/after pairs (non-generative)

### Takeaway
There is a solid non-generative toolkit: (1) aligned difference images in Lab (ΔL → dodge/burn map, Δa/Δb → color work), (2) multi-scale/frequency-band differences to separate texture edits from tone edits, (3) dense optical flow to recover liquify/warp fields, (4) least-squares fitting of global tone curves (FiveK practice: 51-point spline on L) and 3D LUTs (least-squares over binned RGB pairs), (5) region-wise color statistics (Reinhard mean/std, PPR10K mean-color variance), (6) interpretable "white-box" filter models (Exposure, RSFNet, HDRNet's local affine grid) whose parameters are human-readable. Kee & Farid (PNAS 2011) is the canonical before/after-pair metric that explicitly decomposes geometric vs photometric change and correlates with human perception of "how retouched".

### Cited Findings
- Practical starting point (pro forum practice): put original and edited on layers, set top to Difference to see where changes are; eyedropper-sample original vs modified values; general inversion is "exceptionally hard" once selective/destructive edits exist (DPReview Retouching Forum thread; search snippet, thread itself 403) — [DPReview, Reverse engineering manipulation to a photograph (eg. curve)](https://www.dpreview.com/forums/thread/2972360)
- Difference blend mode definition (subtracts darker from lighter per channel; black = no change) — [Adobe, Blending mode descriptions](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html)
- Kee & Farid, "A perceptual metric for photo retouching" (PNAS 108(50):19907–19912, 2011): rates images by "explicitly modeling and estimating geometric and photometric changes"; correlates well with perceptual judgments — [Dartmouth Digital Commons abstract](https://digitalcommons.dartmouth.edu/facoa/1540/); [PNAS](https://www.pnas.org/doi/10.1073/pnas.1110747108)
- Kee & Farid details (press): metric on 1–5 scale; built from "eight different summary statistics" covering geometric distortion (body reshaped) and photometric distortion (skin smoothed/altered); validated with 350 observers ranking 450 original/retouched pairs — [PCWorld](https://www.pcworld.com/article/478605/digital_photo_retouching_quantified_in_new_metric.html)
- Warp/liquify recovery: Wang, Wang, Owens, Zhang, Efros (ICCV 2019) script Photoshop Face-Aware Liquify to generate training data; a local warp predictor estimates per-pixel flow, can localize edits and in some cases "undo" them; code public; limited to FAL-type warps — [arXiv 1906.05856](https://arxiv.org/abs/1906.05856); [project page](https://peterwang512.github.io/FALdetector/)
- Classical dense optical flow (no learning needed for aligned pairs): OpenCV provides DIS, Farneback (polynomial expansion, 2003), DualTVL1, DeepFlow, RLOF etc.; `calc` outputs a 2-channel float flow field — [OpenCV Optical Flow Algorithms](https://docs.opencv.org/3.4.20/d2/d84/group__optflow.html); [OpenCV FarnebackOpticalFlow](https://docs.opencv.org/3.4/de/d9e/classcv_1_1FarnebackOpticalFlow.html)
- Global tone-curve fitting from pairs (MIT-Adobe FiveK): adjustments "expressed as a remapping curve from input luminance into output luminance, using the CIE-Lab color space"; curve = spline with 51 uniformly sampled control points fit to input/output luminance pairs by least squares; first PCA coefficient of curves approximates the full curve well; error measured as L2 in Lab where 2.3 = 1 JND; not adjusting gives error 16.3; 5 art-school retouchers × 5,000 RAW photos in Lightroom — [Bychkovsky, Paris, Chan, Durand, CVPR 2011](https://people.csail.mit.edu/vladb/photoadjust/db_imageadjust.pdf)
- Learning a specific user's taste from few examples: Bychkovsky et al. learn the *difference* between a new user and a reference photographer from a handful of examples, selecting training photos by "sensor placement" (maximize mutual information); compared with Kang et al.'s 25-sensor method — [Bychkovsky et al.](https://people.csail.mit.edu/vladb/photoadjust/db_imageadjust.pdf)
- Features that predict expert tone choices: log-intensity percentiles every 2% (also on σ=10, 30 blurred versions), scene brightness from EXIF, equalization CDF projected on 5 PCA comps, detail-weighted CDF, highlight clipping thresholds (1–15%), spatial distribution of 10 tone bands, face-region percentiles — [Bychkovsky et al.](https://people.csail.mit.edu/vladb/photoadjust/db_imageadjust.pdf)
- Simple tone curves can approximate complex ones with equally good enhancement by objective metrics and slight preference in user tests (search snippet; 2026) — [Simple tone curves: theory and applications, Visual Computer](https://link.springer.com/article/10.1007/s00371-026-04505-y)
- 3D LUT estimation from a pair: least-squares estimation (P = (WᵀW)⁻¹WᵀZ with trilinear interpolation weights W) when interpolation is linear, or gradient descent otherwise (patent snippet) — [USPTO 9912925, 3D LUT estimation for color gamut scalability](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9912925); open-source `lut-estimator` reverse-engineers a global RGB→RGB transform from before/after and exports `.cube` (search snippet) — [DeepWiki, kinn00kinn/LUT-Estimator](https://deepwiki.com/kinn00kinn/LUT-Estimator)
- Learned image-adaptive 3D LUTs (Zeng et al., TPAMI 2020) — fast, interpretable color/tone transforms; code public — [ResearchGate](https://www.researchgate.net/publication/344392752_Learning_Image-Adaptive_3D_Lookup_Tables_for_High_Performance_Photo_Enhancement_in_Real-Time); [GitHub HuiZeng/Image-Adaptive-3DLUT](https://github.com/HuiZeng/Image-Adaptive-3DLUT)
- HDRNet (Gharbi et al., SIGGRAPH 2017): learns from input/output pairs the coefficients of a *locally affine color transform* in a bilateral grid, sliced edge-aware to full res — i.e., a compact, inspectable model of local (spatially varying) color/tone edits — [arXiv 1707.02880](https://arxiv.org/abs/1707.02880)
- Exposure (Hu et al., TOG 2018): "white-box" framework modeling retouching ops as resolution-independent differentiable filters; reveals the sequence of editing steps; learns from unpaired collection (uses RL + GAN for training, though the output ops are standard filters) — [arXiv 1709.09602](https://arxiv.org/pdf/1709.09602)
- RSFNet (ICCV 2023): parallel region-specific color filters (saturation, contrast, hue, etc.) plus attention masks showing which region each filter affects; mimics colorists' divide-and-conquer workflow; editable white-box output — [arXiv 2303.08682](https://arxiv.org/abs/2303.08682)
- Image Analogies (Hertzmann et al., SIGGRAPH 2001): learn a "filter" from a pair A→A′ and apply to B to get B′ via multiscale autoregression / Gaussian-pyramid best-match search — [NYU MRL PDF](https://mrl.cs.nyu.edu/publications/image-analogies/analogies-72dpi.pdf)
- Parametric meta-filter modeling from a single example pair (Visual Computer 2014) — estimates a parametric filter from one before/after pair (title/venue only; abstract not retrieved) — [Springer](https://link.springer.com/article/10.1007/s00371-014-0973-y)
- Statistical color transfer (Reinhard et al., 2001): match per-channel mean and std in decorrelated lαβ; "straightforward color statistics can capture some important subjective notions of style" (search snippet) — [Semantic Scholar](https://www.semanticscholar.org/paper/Color-Transfer-between-Images-Reinhard-Ashikhmin/f3a11158e9d8bdfdf07dca756335c084fce0123e); [GitHub jrosebr1/color_transfer](https://github.com/jrosebr1/color_transfer)
- PPR10K (CVPR 2021) metrics usable for self-scoring: ΔE_ab = L2 in CIELAB; human-centered ΔE^HC and PSNR^HC weight human regions 1 and background α=0.5; group-level consistency M_GLC = Σ_c Var(mean_c of each image in group), with a+b channels found "most suitable and stable"; 11,161 RAW photos in 1,681 groups (3–18 per group), 3 experts each, retouched in Camera Raw without geometric changes — [PPR10K paper](https://www4.comp.polyu.edu.hk/~cslzhang/paper/PPR10K-cvpr21-paper.pdf); [GitHub csjliang/PPR10K](https://github.com/csjliang/PPR10K)
- PALATE (arXiv 2608.18622, 2026): personalizes portrait retouching by *selecting among* retouched candidates per user rather than generating edits; shared backbone + category residuals + per-user adapters (512 bytes/user); 72.83% pairwise preference accuracy vs PickScore 58.06%; built on PPR10K — [arXiv 2608.18622](https://arxiv.org/abs/2608.18622)

### Inferences — proposed reverse-engineering pipeline (synthesis; each step uses cited building blocks)
1. **Align**: estimate dense flow before→after (DIS/Farneback). Flow magnitude map = liquify/warp map; warp the before image by the flow so subsequent comparisons are pixel-aligned. (Kee & Farid likewise separate geometric from photometric change first.)
2. **Global layer**: fit a 1D L-curve (FiveK 51-point least-squares spline) and/or a 3D LUT (least-squares) on pixels outside skin/edit masks; residual after removing the global transform = local edits.
3. **Local tone (D&B map)**: low-pass residual ΔL (e.g., Gaussian σ at a few scales) → signed dodge/burn map; correlate with face-plane orientation / key-light direction to judge "form-following".
4. **Texture layer**: per-band (Laplacian pyramid) energy ratio after/before inside skin; detect healing spots as small regions where HF band was replaced (texture changed but low-pass nearly constant).
5. **Color layer**: Δa*, Δb* low-pass maps per region (skin, lips, eyes, hair, background); check dodge areas for ΔC*<0 (desaturation side-effect) and whether region means converged (face vs hands).
6. **Summarize as "taste vector"**: curve PCA coefficients, LUT, per-region mean ΔLab, D&B amplitude/scale, HF retention ratio per region, warp magnitude per facial region. Learn per-retoucher distributions from multiple pairs (FiveK shows a handful of examples can personalize global tone).
7. **Self-scoring**: compare agent's output vs elite reference with ΔE (overall and human-weighted), GLC variance across a set, HF retention, halo/banding/clipping detectors, and a Kee–Farid-style "how much was changed" score to enforce restraint.

### Gaps
- Kee & Farid's exact eight statistics and correlation coefficients could not be verified (PNAS full text 403; PMC behind reCAPTCHA). From memory the paper fits local affine-type geometric models and local linear filters + SSIM for photometric changes, but this is unverified and should not be quoted as fact.
- No published method found that specifically decomposes a retouch into Photoshop-layer-equivalent D&B + FS + Liquify layers from a flattened pair; the pipeline above is a synthesis.
- The LUT-Estimator repo/deepwiki details (binning, empty-cell handling) could not be fetched (HTTP 429).

---

## Q5. How are student/contest/agency works graded (rubrics)?

### Takeaway
Formal rubrics are sparse publicly. Contest criteria reduce to brief adherence, visual quality, technical precision (including file/layer hygiene), plus restraint and attention to detail per Retouching Academy feedback. Stock agencies grade negatively via rejection categories (noise/artifacts/posterization, focus/softness from over-NR, halos from over-sharpening).

### Cited Findings
- Retoucher of the Year: "adherence to the brief, visual quality, and technical precision"; layered PSD inspection for "clear layer structure and naming"; categories Rising Star, Supernova, Luminist (color grading in Lightroom/Capture One/Camera Raw), Alchemist (composites), Halo (fashion) — [Retoucher of the Year](https://retoucheroftheyear.com/about-the-competition)
- Retouching Academy Beauty Retouching Contest judged by RA and sponsors (Wacom, Capture One) in skill tiers: Beginner and Experienced Enthusiast (≥2 years) (search snippet) — [Fstoppers, New Retouching Academy Beauty Retouching Contest](https://fstoppers.com/contests/new-retouching-academy-beauty-retouching-contest-247723)
- RA Challenge #2: winner chosen by community vote (74 votes); judge critique emphasized restraint, distractions (nails), hairline middle ground, face–hand tone match, overdrawn lips — [Retouching Academy, Challenge #2](https://retouchingacademy.com/challenge-2-results-overview/)
- AOP Martin Evening Award: proficiency + "utmost visual impact within a contemporary creative framework"; requires before/after; ≥2 years experience; AI-assisted tools allowed but not fully AI-generated work — [AOP Awards](https://www.aopawards.com/martin-evening-excellence-in-digital-retouching-award/)
- Shutterstock rejection categories (search snippets): excessive noise/grain/compression artifacts/posterization; focus rejection from over-noise-reduction softness; over-sharpening halos/"crispy" — [Shutterstock Blog](https://www.shutterstock.com/blog/why-images-get-rejected-for-noise); [Xpiks](https://xpiksapp.com/blog/top-photo-rejection-reasons/)

### Inferences
- A practical rubric for an agent: (a) Brief/intent adherence; (b) Restraint (change magnitude vs need); (c) Texture integrity; (d) Tonal transitions and form; (e) Color uniformity and cross-region/set consistency; (f) Edge and artifact cleanliness; (g) Detail/distraction coverage; (h) Technical delivery (clipping, banding, color space). Each maps to measurements in the Q3 table.

### Gaps
- No published point-based rubric from a retouching school (e.g., RA courses, Fstoppers tutorials) was found. Adobe Stock rejection threads exist ([Adobe Community, Rejection for artifacts](https://community.adobe.com/t5/stock-contributors-discussions/rejection-for-artifacts/td-p/10115022)) but were not read.

---

## Q6. Published before/after case studies with step-by-step breakdowns from top retouchers

### Takeaway
Step-by-step public breakdowns exist mainly from educators (Retouching Academy, Jake Hicks, Fstoppers contributors, Pratik Naik interviews/courses) rather than from studios; they describe an order of operations (cleanup → D&B transitions → color fixes → global) and the check-layer method, which are directly useful as priors for reverse engineering.

### Cited Findings
- Naik's order: healing/cloning cleanup first, then D&B "till any transitions are evened out", retaining skin color variation — [The Retouchist](https://www.retouchist.org/blog/interview-pratik-naik-craftsman-luxury-skin)
- Jake Hicks: step-by-step D&B on 50% gray layer, then diagnosis of resulting desaturated patches and Selective Color (Whites) fix — [Jake Hicks Photography](https://jakehicksphotography.com/latest-techniques/2018/6/15/fixing-discolouration-during-the-dodge-burn-retouch)
- Retouching Academy micro-transition walkthrough with visual-aid layers — [Retouching Academy](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/)
- Retouching Academy challenge results compare multiple entrants' versions of the same raw — effectively a public multi-retoucher before/after set with judge commentary — [Retouching Academy, Challenge #2](https://retouchingacademy.com/challenge-2-results-overview/)
- Pratik Naik's paid series (CreativeLive, The Portrait Masters) contain full breakdowns (not free) — [CreativeLive](https://www.creativelive.com/classes/art-business-high-end-retouching-pratik-naik); [The Portrait Masters](https://theportraitmasters.com/product/the-retouching-series/)
- ConradDigital publishes retouching case studies (not reviewed) — [ConradDigital Case Studies](https://conraddigital.com/retouching-case-studies/)
- Public paired datasets usable as "elite example" training corpora: MIT-Adobe FiveK (5 retouchers × 5,000) — [Bychkovsky et al.](https://people.csail.mit.edu/vladb/photoadjust/db_imageadjust.pdf); PPR10K (3 experts × 11,161 portraits, with masks and group consistency) — [GitHub csjliang/PPR10K](https://github.com/csjliang/PPR10K). Both contain only global/Camera Raw-type edits, not local skin retouching.

### Inferences
- Because the common pro order is cleanup → D&B → color → global grade, a reverse-engineering decomposition should peel in the reverse order: global curve/LUT first, then color regions, then low-frequency D&B, then high-frequency healing.
- Challenge-style multi-entrant sets (same raw, many retouchers, judge ranking) are ideal for learning "elite vs average" contrasts if images can be legally obtained.

### Gaps
- No free, studio-published (Gloss, Happy Finish, Saddington Baynes, etc.) step-by-step case study with layer-level breakdown was found.
- No public paired dataset with high-end *local* beauty retouching (skin D&B, liquify) by named elite retouchers was found; FFHQR-type datasets were not investigated here.
