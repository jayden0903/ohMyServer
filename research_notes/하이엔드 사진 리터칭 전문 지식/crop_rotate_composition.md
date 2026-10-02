# Cropping, Rotation/Straightening, Perspective/Lens Correction and Composition — Expert Rules for an AI Editing Agent (as of Oct 2026)

Scope note: this file covers geometric edits only (crop, rotate, straighten, perspective/keystone, lens-profile and wide-angle correction, canvas extension without generative AI) plus the composition principles that drive crop decisions. Numbers marked "(derived)" are my own geometry/arithmetic, not taken from a source; everything else carries an inline source. Research budget limits: several primary PDFs (Adobe helpx, Lee et al. CVPR 2012, Gallagher 2005) returned 403/503 and could not be read directly — see Gaps.

---

## 1. Cropping rules for people (joints, framings, headroom, chin/forehead, eye line, looking room)

### Takeaway
Never let a frame edge land exactly on a joint ("if it can bend, don't crop it"). Crop mid-segment where the limb tapers (mid-thigh, shin, mid-upper-arm, forearm), and keep the eyes near the upper-third line (ICAO ID photos are the one strict numeric standard: head 70–80% of frame height, eyes 50–60% up from the bottom). In tight beauty/headshot crops, cutting the top of the head/hair is fine; cutting the chin is not.

### Cited Findings
**Joints / where not to cut**
- Rule: "If it can bend, don't crop it" — fingers, toes, elbows, knees, wrists and ankles; cropping at joints gives a "stumpy", unintentional look — [Digital Photography School](https://digital-photography-school.com/good-crop-bad-crop-how-to-crop-portraits/)
- Avoid ankles, knees, hips, elbows, shoulders, neck and wrists; cropping there makes subjects look like they have "missing feet/limbs" — [SLR Lounge](https://www.slrlounge.com/portrait-cropping-guide-bad-portrait-crops-how-to-fix-them/)
- The classic mistake is slicing exactly at a wrist, elbow, shoulder seam or base of the neck; crop through the middle of a segment or include the joint fully. A crop that ends mid-thigh reads as a natural 3/4 portrait; one exactly at the knee looks like a mistake. A hand sliced at the wrist is more distracting than one kept whole or excluded cleanly — [Imagen AI / search summary](https://imagen-ai.com/valuable-tips/image-cropping-tips-for-portrait-photographers/)
- Safe crop lines: below the knee, mid-thigh, waist, across the forearm, through the top of the head — [Digital Photography School](https://digital-photography-school.com/good-crop-bad-crop-how-to-crop-portraits/)
- Crop where the body "tapers" as it exits the frame: shin, mid-thigh, upper torso/mid-chest, bridge of nose (ultra-tight for jewelry/accessories), mid-hair (show hair without cropping the hairline/forehead). Exception noted: for male subjects broad shoulders running out of frame can add presence — [SLR Lounge](https://www.slrlounge.com/portrait-cropping-guide-bad-portrait-crops-how-to-fix-them/)

**Chin / forehead / top of head**
- Never crop into the chin: it makes faces look square and unintentional; always keep the chin in frame — [Digital Photography School](https://digital-photography-school.com/good-crop-bad-crop-how-to-crop-portraits/); same rule in [Imagen AI](https://imagen-ai.com/valuable-tips/image-cropping-tips-for-portrait-photographers/)
- Cropping through the top of the head is an accepted crop point — [Digital Photography School](https://digital-photography-school.com/good-crop-bad-crop-how-to-crop-portraits/). Extreme close-ups place the top of the head outside the frame entirely, while the thirds rule still governs eye placement — [Wikipedia: Headroom](https://en.wikipedia.org/wiki/Headroom_(photographic_framing))
- Cinema definition: Extreme Close-Up "stops at the subject's chin and forehead" — [Wikipedia: Shot (filmmaking)](https://en.wikipedia.org/wiki/Shot_(filmmaking))

**Standard framings (where the bottom edge falls)**
- Extreme close-up: chin to forehead. Close-up: shoulder line visible. Medium close-up: more shoulder (conventionally chest). Medium shot: just above or below the waist. American/cowboy (3/4) shot: about mid-thigh upward (originally to show holstered guns). Medium-long shot: frame ends near the knees. Full shot: whole subject just visible. Long shot: subject plus environment. "Italian shot": eyes only — [Wikipedia: Shot (filmmaking)](https://en.wikipedia.org/wiki/Shot_(filmmaking))
- Note the conflict: film grammar names a "medium-long shot ending near the knees", but photo-retouching sources say never end *at* the knee. Resolve by going slightly above (mid-thigh) or below (mid-shin) — [Wikipedia](https://en.wikipedia.org/wiki/Shot_(filmmaking)) vs [SLR Lounge](https://www.slrlounge.com/portrait-cropping-guide-bad-portrait-crops-how-to-fix-them/)

**Headroom and eye line**
- Eyes "ideally positioned one-third of the way down from the top of the frame"; closer shots need less headroom; too much headroom is "dead space", a partly cut head can feel claustrophobic (source: Thompson, *Grammar of the Shot*, 1998, p. 64). Broadcast framing allows ~5% overscan cut-off — [Wikipedia: Headroom](https://en.wikipedia.org/wiki/Headroom_(photographic_framing))
- Put the eyes on the upper-third line or slightly above; eyes near the lower-third line give static, lifeless images — [Digital Photography School](https://digital-photography-school.com/good-crop-bad-crop-how-to-crop-portraits/)
- Video practice: put the eyes on one of the upper thirds intersections in both wide and close shots — [Videomaker / search summary](https://www.videomaker.com/article/f5/9231-framing-good-shots/)
- Too much headroom leaves the face stranded in the lower half and the subject looking small; too little feels cramped — [Imagen AI](https://imagen-ai.com/valuable-tips/image-cropping-tips-for-portrait-photographers/)

**ID/passport photos (strict numeric case)**
- ICAO 9303-style rules: chin to crown is 70–80% of photo height; eyes 50–60% up from the bottom (some guides say 55–65%); face horizontally centred within ±5%; head tilt ≤5° on any axis — [PhotoGov ICAO guide](https://photogov.net/knowledge/standards/icao-9303-biometric-standards/); [compliantphoto](https://compliantphoto.com/icao-9303-photo-requirements). (These are aggregator summaries of ICAO Doc 9303. National specs differ: US head 25–35 mm on a 2×2 in photo — [photopass.ai](https://www.photopass.ai/blog/us-passport-photo-head-size-guide).)

**Lead room / nose room / looking space**
- Nose/look room is the horizontal space in front of the face in the gaze direction. Lead room is the same idea for a moving subject: leave more space in front of the motion than behind — [Videomaker/EditMentor via search](https://help.editmentor.com/en/articles/6050471-headroom-and-lead-room); [Wikipedia: Headroom](https://en.wikipedia.org/wiki/Headroom_(photographic_framing))

### Inferences
- Operational rule set for an agent (synthesis): (1) detect pose keypoints; (2) define "forbidden bands" around each joint (neck base, shoulder, elbow, wrist, hip, knee, ankle, finger/toe joints); a sensible band is about ±3–5% of body height (my heuristic, not from a source); (3) snap crop edges to mid-segment "taper" zones; (4) for head-and-shoulders and tighter, put the eye line at about 0.30–0.38 of frame height from the top (thirds = 0.333, phi = 0.382, derived); (5) allow a head-top crop only when face height is >~50% of frame height (heuristic); (6) never let the bottom edge cross between lower lip and chin bottom.
- Looking room: put the face centre about 1/3 of frame width from the edge it faces away from, so roughly 2/3 of the width is in front of the gaze (derived from the thirds rule; no source gave a numeric ratio).
- Fingers/toes are the most common automated-crop failure, because keypoint models give wrists/ankles but not every phalanx; check the hand segmentation mask against the edge.

### Gaps
- I found no authoritative numeric headroom percentages by shot size (e.g., "x% of frame height above the head for a MCU"). Sources are qualitative apart from the eye-at-1/3 rule and ICAO.
- No source quantified the "safe distance" from a joint at which a crop stops reading as an amputation.

---

## 2. Aspect ratios by use; cover/print bleed & safe areas

### Takeaway
Deliver to the target container's ratio and design inside its safe zone. Instagram (2026): upload 4:5 (1080×1350) or native 3:4 (1080×1440). The profile grid crops to 3:4, so keep key content inside a centred ~1012 px-wide zone of a 4:5 post. 9:16 (1080×1920) for Stories/Reels with UI-free top/bottom margins. Print: 0.125 in (3 mm) bleed, live area about 0.375–0.5 in inside trim, and always the publication's own media-kit spec.

### Cited Findings
- Instagram replaced the 1:1 profile grid with a 3:4 grid preview in Jan 2025 (Mosseri) and has accepted native 3:4 feed photos since May 2025 — [Neal Schaffer](https://nealschaffer.com/instagram-post-size/); [Fstoppers](https://fstoppers.com/news/instagram-kills-square-grid-how-adapt-new-45-layout-and-keep-your-feed-looking-690705)
- Feed: 4:5 1080×1350 (recommended for designed graphics), 3:4 1080×1440 (zero grid crop), 1:1 1080×1080, 1.91:1 1080×566; Stories/Reels 9:16 1080×1920; profile picture 320×320 shown as a circle; served width capped at 1080 px — [Neal Schaffer](https://nealschaffer.com/instagram-post-size/)
- Safe zone for 4:5 posts: keep critical elements in a centred 1012×1350 px area (survives the 3:4 grid crop). For 9:16, keep text away from the top/bottom UI areas (no pixel figure given) — [Neal Schaffer](https://nealschaffer.com/instagram-post-size/); [Search summary of multiple guides](https://www.oktopost.com/blog/instagram-grid-size-guide/)
- Twitter/X historically auto-cropped previews to 16:9 by saliency; in 2021 it removed the algorithm and shows standard aspect ratios uncropped — [Yee et al. arXiv 2105.08667](https://arxiv.org/pdf/2105.08667); [PetaPixel](https://petapixel.com/2021/05/22/twitter-axing-ai-photo-cropping-after-tests-reveal-race-gender-bias/)
- Print: standard bleed is 0.125 in (3 mm) beyond trim on all sides. Typical US magazine full-page trim is about 8.375×10.875 in (213×276 mm), some titles 8.5×11 in. Safe/live area is about 0.375–0.5 in inside trim. Every magazine publishes its own trim/bleed/live specs in its media kit, and those govern — [Search summary: fcapgroup / kapa99 / greenerprinter](https://www.fcapgroup.com/bleed-trim-and-safe-area-in-print-ads/); [kapa99](https://kapa99.com/blog/magazine-and-print-ad-sizes/)
- Broadcast overscan: about 5% of the frame can be lost on consumer displays (relevant to video stills/legacy TV-safe framing) — [Wikipedia: Headroom](https://en.wikipedia.org/wiki/Headroom_(photographic_framing))
- Native ratios: 3:2 (35 mm/most ILCs) = 1.5 rectangle, which Cartier-Bresson-style dynamic-symmetry analysis uses — [DPReview video summary](https://www.dpreview.com/videos/4002734538/dynamic-symmetry-the-genius-of-henri-cartier-bresson-s-composition); [Great Big Photography World / search](https://greatbigphotographyworld.com/dynamic-symmetry/)

### Inferences
- Cover workflow: (1) take trim from the spec, add 3 mm bleed per side and work at 300 ppi; (2) keep faces/eyes inside the live area; (3) on covers the masthead usually sits in the top ~15–20%, so plan headroom for a masthead overlap (common practice in my synthesis, not sourced numerically).
- Multi-output crops: crop to the most restrictive container first (3:4 grid / 9:16 safe zone), then check the subject still satisfies the joint and eye-line rules in each derived ratio.
- 4:5 (0.8) vs 3:4 (0.75): going from 4:5 to 3:4 at fixed height removes 6.25% of width (1080→1012.5 px), which matches the 1012 px safe zone (derived).

### Gaps
- No primary Meta documentation was fetched; Instagram figures come from reputable 2026 aggregators that agree with each other.
- No sourced pixel safe margins for 9:16 Reels UI (commonly quoted ~250 px top/bottom are unverified here).
- I found no authoritative per-magazine cover template (e.g., Vogue). Cover safe-area/masthead conventions are publication-specific.

---

## 3. Composition principles applied to crop decisions

### Takeaway
Thirds (1/3, 2/3), phi grid (0.382/0.618), golden spiral, diagonals and dynamic-symmetry armatures (diagonals plus reciprocals) are candidate snapping guides, not laws. Empirical studies show the rule of thirds has a weak or no relationship with aesthetic ratings, and centred subjects are often preferred. Use the grids to generate candidates and judge them by subject integrity, balance and clean edges.

### Cited Findings
- Lightroom crop overlays: Grid, Thirds, Diagonal, Triangle, Golden Ratio, Golden Spiral, Aspect Ratios. Press O to cycle, Shift+O to rotate asymmetric overlays (spiral/triangle). The cycled set and the aspect-ratio overlays are configurable under Tools > Crop Guide Overlay — [Fstoppers / search summary](https://fstoppers.com/originals/dont-get-stuck-rule-thirds-lightroom-has-lot-more-offer-135275); [presetpro](https://www.presetpro.com/how-to-change-the-crop-overlay-in-lightroom-classic/)
- Harmonic armature ("armature of the rectangle", 14 lines): 4 sides, 2 main diagonals, 4 reciprocals (perpendiculars from corners to the opposite diagonal), 4 secondary diagonals (corner to midpoint of opposite side). Crossings mark "harmonic positions". Rabatment: fold each short side into the long side to make implied squares, giving strong vertical dividers. The "baroque" diagonal runs lower-left→upper-right (ascending); the "sinister" diagonal runs upper-left→lower-right (tension) — [GridMakerPro](https://gridmakerpro.com/grids/advanced-composition/); [Great Big Photography World / search](https://greatbigphotographyworld.com/dynamic-symmetry/)
- Dynamic symmetry (Jay Hambidge, *The Elements of Dynamic Symmetry*) uses root rectangles (√2, √3, √5, golden). The 1.5 rectangle is used for 35 mm frames. Adam Marelli popularised it in photography via Cartier-Bresson analysis — [Wikipedia: Jay Hambidge](https://en.wikipedia.org/wiki/Jay_Hambidge); [DPReview](https://www.dpreview.com/videos/4002734538/dynamic-symmetry-the-genius-of-henri-cartier-bresson-s-composition); [Eric Kim](https://erickimphotography.com/blog/2013/10/10/street-photography-composition-lesson-3-diagonals/)
- Expert disagreement: Cartier-Bresson held that cropping a good photograph means "death to the geometrically correct interplay of proportions" and that a weakly composed photo can rarely be saved under the enlarger. That is anti-crop purism, against the retoucher's view of cropping as a primary tool — [Fstoppers](https://fstoppers.com/education/henri-cartier-bresson-and-myron-barnstone-golden-section-and-dynamic-symmetry-183407) (search summary)
- Empirical evidence: Amirshahi et al. (2014, *Art & Perception*, 30 participants) found aesthetic ratings correlated only weakly with subjective rule-of-thirds scores and **not at all** with calculated ROT values. Highly rated photos and paintings had ROT values as low as non-ROT photos, so ROT "seems to play only a minor, if any, role" — [Amirshahi et al. 2014 PDF](https://www.uniklinikum-jena.de/anatomie1_media/Inhalte/AmirshahiARTP2014.pdf); [ResearchGate](https://www.researchgate.net/publication/259620557_Evaluating_the_Rule_of_Thirds_in_Photographs_and_Paintings)
- A study found participants overwhelmingly preferred a centred object over a thirds placement — [Hoh & Zhang, Semantic Scholar](https://www.semanticscholar.org/paper/Rule-of-Thirds-or-Centered-A-study-in-preference-in-Hoh-Zhang/d6bdbdcf5d91ed6c7c98abe425a346b0931d0103) (search summary). In contrast, a landscape-photo study found Golden Section/thirds composition and horizon position significantly affected perceived beauty — [ScienceDirect (J. Environ. Psychol. 2014)](https://www.sciencedirect.com/science/article/abs/pii/S0272494414000085) (search summary). Golden-ratio preference is slight overall (~53%) — [PMC9787369](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9787369/) (search summary)
- Crops should look deliberate, not accidental, even when they break rules — [Digital Photography School](https://digital-photography-school.com/good-crop-bad-crop-how-to-crop-portraits/)

### Inferences
- Exact guide coordinates (derived, normalized 0–1): thirds lines at 0.333/0.667; phi grid at 0.382/0.618 (1/φ² and 1/φ); rabatment line at x = H/W from each side (for 3:2 landscape, x = 0.667 and 0.333, so in 3:2 rabatment coincides with the thirds lines); for 4:5 portrait the rabatment is at y = 0.8 from top/bottom.
- Reciprocal construction (derived): in a W×H rectangle the reciprocal from a corner meets the main diagonal at its foot. For 3:2, the "eyes" (diagonal × reciprocal intersections) fall at about x = 0.31/0.69 and y = 0.31/0.69 of the frame, i.e. near the thirds intersections.
- Visual weight, negative space, figure-ground and "border patrol" (scan all four edges for bright spots, cut-off objects, tangents and stray limbs before committing) are standard teaching. I did not fetch a primary source with measurable criteria, so I treat them as agent heuristics: (a) no high-luminance or high-saturation blob touching an edge unless it is the subject; (b) no object cut by less than ~5–10% of its size, either include it or exclude it cleanly (heuristic); (c) avoid tangents where an object edge just kisses the frame edge.
- Recommended agent policy: generate candidates snapped to thirds/phi/centre/armature, score them with an aesthetic-crop model (Section 7), then reject any candidate that violates the hard people rules (Section 1) or the edge-cleanliness checks.

### Gaps
- I could not find any teaching by Jake Garn on dynamic symmetry. Jake Garn is a Utah beauty/fashion photographer ([Behance](https://www.behance.net/jakegarn?locale=en_US)), and the prompt may have meant Adam Marelli, the best-known dynamic-symmetry photo educator.
- Golden-spiral placement has no empirical support beyond the slight golden-ratio preference noted above. No study on crop choices specifically was found.

---

## 4. Straightening: horizon, verticals, Dutch angle, tilt perception, auto detection

### Takeaway
Level the true horizon or dominant verticals to about 0° (sub-degree precision). Small residual tilts (≈2–5°) read as mistakes, while intentional Dutch tilts should be ≥10–15° (sweet spot about 15–25°). Rotation always costs crop area: about 5% of area per 1° for 3:2. Auto methods (Hough/edgelet line detection, vanishing points, RANSAC) work only on a minority of casual photos. Bail out when faces would distort or the horizon would get worse.

### Cited Findings
- The human eye is much more sensitive to right angles with one horizontal and one vertical leg than to oblique ones, so even a very small tilt of a line that should parallel the border is noticed — [US Patent 9,466,092 Content-aware image rotation (search summary)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9466092)
- The body-tilt perception threshold is about 2° (range 1.9–5.6°), earlier measured at 4.4°. This is a **vestibular** (body) threshold, not a visual image-tilt threshold, and should not be used directly as an image tolerance — [ResearchGate: Perception Threshold for Tilt](https://www.researchgate.net/publication/51207398_Perception_Threshold_for_Tilt)
- Dutch angle: a 2–5° tilt looks like a mistake; 15–30° looks intentional. Small 5–15° gives mild unease, 20–35° clear instability, 40°+ disorientation. Another guide: under 10° reads as a mistake, over 35° looks amateur unless heavily stylised, sweet spot 15–25°. Sources disagree on the upper bound (30° vs 45°) — [Glass / ExpertPhotography / multiple guides via search](https://expertphotography.com/dutch-angle); [yana-sk-photo](https://yana-sk-photo.uk/blog/dutch-angle-photography-guide)
- ICAO ID photos: head tilt ≤5° on any axis — [PhotoGov](https://photogov.net/knowledge/standards/icao-9303-biometric-standards/)
- Classic auto-straighten: Gallagher (Kodak, 2005) estimated unintended camera roll from vanishing points and removed it — [Gallagher 2005 PDF](http://chenlab.ece.cornell.edu/people/Andy/publications/Andy_files/rotation_crv2005.pdf) (not readable, 503); [US Patent 6,968,094](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6968094)
- Google auto-rectification (Chaudhury et al., "Auto-rectification of user photos"): vanishing-point detection from edgelets (Hough/Gaussian-sphere history, RANSAC), homography T = R·H (affine rectification × vertical alignment), then cropped and scaled back to the original size. Edgelet votes are clipped to zero when the angle exceeds 5°. Feasibility checks bail out if the face bounding-box aspect changes beyond a threshold or if the detected horizon (RANSAC over near-horizontal edgelets) gets *more* tilted after warping. On 2,199 random Google+ photos: 218 had too few vanishing points, 1,233 a bad angle between vanishing points, 173 too much size change, 116 too much rotation, 109 too much face distortion, 4 too much horizon distortion. **Only 346 (15.7%) were rectified** — [Google Research PDF](https://research.google.com/pubs/archive/42532.pdf)
- Classical Hough line detection cannot tell a tilted horizon from a roofline receding to a vanishing point — [tinycomputers.io (practitioner note)](https://tinycomputers.io/posts/processing-51000-photos-with-ai-on-amd-strix-halo.html) (search summary)
- Lee, Shechtman, Wang, Lee, "Automatic Upright Adjustment of Photographs" (CVPR 2012, the basis of Adobe Upright) proposes perception-study-based criteria and optimises a homography — [mlanthology](https://mlanthology.org/cvpr/2012/lee2012cvpr-automatic/)
- Practical reference: Photography Life argues that leveling is not trivial (lens distortion, uneven shorelines, waves) — [Photography Life](https://photographylife.com/why-leveling-the-horizon-isnt-easy) (page paywalled, 402; title only)

### Inferences
- Crop cost of rotation (derived geometry). The largest centred same-aspect crop after rotating by θ has linear scale s = 1/(cos θ + r·sin θ), with r = long/short side. Area kept = s²:
  - 3:2 → 0.5°: 97.4%, 1°: 95.0%, 2°: 90.4%, 3°: 86.2%, 5°: 78.7%
  - 4:3 → 1°: 95.5%, 2°: 91.4%, 5°: 80.8%
  - 1:1 → 1°: 96.6%, 2°: 93.5%, 5°: 85.2%
  - 16:9 → 1°: 94.1%, 2°: 88.8%, 5°: 75.5%
- Agent policy: (a) if |measured tilt| < ~0.2°, do nothing (below likely measurement error); (b) 0.2–10°, correct fully to 0° when a reliable reference exists (sea or lake horizon, plumb architectural verticals, door frames); (c) 10–35° with a clear subject, treat as possibly intentional Dutch and ask or keep; (d) prefer verticals over the visible horizon when they conflict at the centre of the frame (horizons can genuinely slope on shores and hills); (e) for water horizons, measure the far horizon line, not the shoreline. After lens-distortion correction, re-measure, because barrel distortion bows off-centre horizons.
- Verification metric: after correction, the median angle of the dominant near-horizontal Hough lines (or of near-vertical lines, for verticals) should be within ±0.1–0.2° of 0, and the horizon-detector angle must not increase (the Google bail-out criterion).

### Gaps
- I found no peer-reviewed psychophysics on the *visual* JND for photo horizon tilt (e.g., "0.5° is noticeable"). The patent asserts high sensitivity without a number. The vestibular ~2° threshold is a different modality.
- Lee et al. 2012 criteria and user-study figures could not be read (PDF 503).

---

## 5. Perspective & lens correction (keystone, profiles, wide-angle faces, Adaptive Wide Angle, aspect after transform)

### Takeaway
Order of operations: lens profile (distortion + vignetting) and lateral CA removal **first**, then Upright/keystone, then the aspect fix (counter the "squat" look), then crop/scale. Faces at the edges of wide frames need local stereographic-style correction (Shih et al. 2019), not global rectilinear correction. Camera distance matters: at 12 in a nose appears about 30% larger than at infinity, and at 5 ft there is no significant distortion.

### Cited Findings
- Adobe: enable Lens Profile Corrections and Remove Chromatic Aberration **before** Upright. If you change lens corrections later, click "Update" so Upright re-analyses — [Julieanne Kost (Adobe) 2024](https://jkost.com/blog/2024/07/removing-lens-distortions-and-correcting-perspective-in-lightroom-classic.html); [search summary of Adobe docs](https://helpx.adobe.com/lightroom-classic/help/guided-upright-perspective-correction.html)
- Profile corrections fix vignetting and barrel/pincushion distortion. "Remove Chromatic Aberration" fixes lateral CA (blue-yellow, red-green edge fringes) — [teachucomp / Photography Life via search](https://photographylife.com/lightroom-lens-corrections)
- Upright modes: Auto (balanced level, aspect and perspective), Level (weighted to horizontal details), Vertical (weighted to vertical details plus level), Full (full Level + Vertical + Auto perspective), Guided (draw 2–4 guides along edges that should be vertical or horizontal; Ctrl+Tab cycles modes; Shift+T guided tool) — [Adobe helpx via search](https://learn.adobe.com/uk/lightroom-classic/help/upright-automatic-perspective-correction.html); [Julieanne Kost](https://jkost.com/blog/2024/07/removing-lens-distortions-and-correcting-perspective-in-lightroom-classic.html)
- Manual Transform sliders: Vertical, Horizontal, Rotate, Aspect, Scale, Offset X/Y. The Aspect slider fixes compressed/stretched areas and is "especially helpful when there are people/animals in the photo" — [Julieanne Kost](https://jkost.com/blog/2024/07/removing-lens-distortions-and-correcting-perspective-in-lightroom-classic.html)
- Keystone correction makes objects look squat (vertically compressed, horizontally extended) unless the vertical dimension is also stretched. This is minor at small angles and fixed by hand or automatically in dedicated tools. Perspective tools need the angle of view or 35 mm-equivalent focal length, often from EXIF. Optical alternative: shift/tilt-shift (PC) lenses — [Wikipedia: Perspective control](https://en.wikipedia.org/wiki/Perspective_control)
- Lenscraft: even at maximum Vertical/Aspect values some residual convergence can remain, so partial correction is sometimes the ceiling — [Lenscraft via search](https://lenscraft.co.uk/photo-editing-tutorials/lightroom-perspective-correction/)
- Photoshop Adaptive Wide Angle: reads EXIF lens data and profile. Modes: Fisheye, Perspective, Auto, Photomerge panoramas/360. The user draws line or polygon **constraints** on edges that should be straight (Shift = force horizontal/vertical) — [Adobe helpx via search](https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html)
- Shih, Lai, Liang, "Distortion-free wide-angle portraits on camera phones" (ACM TOG 38(4), SIGGRAPH 2019): a content-aware warping mesh is locally stereographic on faces and blends smoothly to perspective projection in the background. Fully automatic, interactive on phones, tested for FOV 70°–120° — [ACM DL](https://dl.acm.org/doi/10.1145/3306346.3322948); [DPReview](https://www.dpreview.com/news/0513233803/researchers-develop-new-anti-face-distortion-method-for-wide-angle-lenses/). Later work combines generative and geometric priors — [arXiv 2410.09911](https://arxiv.org/html/2410.09911v1)
- Ward et al. (JAMA Facial Plastic Surgery, 2018): at 12 in, nose size rises about 30% (men) / 29% (women) versus infinite distance. At 5 ft there is no significant nasal distortion — [ResearchGate](https://www.researchgate.net/publication/323497618_Nasal_Distortion_in_Short-Distance_Photographs_The_Selfie_Effect); [News-Medical](https://www.news-medical.net/news/20180302/Selfie-nose-does-look-bigger-finds-study.aspx)
- Auto-rectification should bail out when a face's bounding-box aspect ratio changes beyond a threshold under the homography — [Google Research](https://research.google.com/pubs/archive/42532.pdf)

### Inferences
- Pipeline: (1) lens profile on (distortion 100%, vignetting 100%, or ~50–80% for portraits if natural fall-off is wanted, a stylistic judgement); (2) CA removal; (3) Upright Vertical/Guided for architecture, Level for landscapes, Auto as a fallback; (4) if the result looks squat, raise Aspect (stretch vertically) until known proportions are restored (doors, windows, a person's head-to-body ratio about 1:7–1:8 for adults is a common figure-drawing canon, unsourced here); (5) crop to remove the transparent/undefined corners, or enable Constrain Crop (Adobe term; the doc was not fetched).
- Partial vs full keystone: full parallel verticals are the norm in architectural/real-estate work. For tall buildings shot steeply upward, many editors leave slight convergence because full correction makes tops look top-heavy. I could not source a percentage (folk advice often says ~70–80% correction), so treat it as a judgement call (see Gaps).
- People in architecture frames: when Upright stretches people near the edges, either mask them back from an uncorrected layer or limit correction. Use the face-aspect bail-out (for example, reject if face width/height changes by more than ~5%; my threshold, the source does not state a number).
- Wide-angle group photos: apply local face correction (Shih-style) rather than global rectilinear correction. Stretching at the edges grows with distance from centre under rectilinear projection.

### Gaps
- Adobe helpx pages returned 403. Constrain Crop behaviour and the exact slider ranges (±100) were not verified from primary docs.
- Capture One Keystone tool documentation was not fetched.
- No sourced number for the "natural-looking residual convergence" percentage.
- Lee et al. 2012 perception criteria (the Upright basis) could not be read.

---

## 6. Canvas extension without generative AI vs. cropping tighter

### Takeaway
Classic Content-Aware Fill / Crop-with-Content-Aware and cloning work for small extensions of low-structure texture (sky, grass, plain walls, studio paper). They fail with repetition, smearing and broken structure on complex or unique content. Extend in small overlapping passes, fix with Clone/Healing, and when the extension would cross structured content (people, architecture, text), crop tighter or change the aspect instead.

### Cited Findings
- Photoshop's Crop tool with "Content-Aware" checked fills the expanded canvas. Alternatively use Image > Canvas Size, then content-aware fill or clone each side separately — [search summary: clippingexpertasia / Adobe community](https://clippingexpertasia.com/blog/how-to-use-content-aware-fill-in-photoshop/)
- Failure modes: repeated patterns when the algorithm reuses the same source area (fix by subtracting that region from the Sampling Brush); smudges on complex non-repeating textures; smeared or blurry patches, which Clone Stamp/Healing can fix if small — [aiarty](https://www.aiarty.com/edit-photo/content-aware-fill-photoshop.htm); [KelbyOne](https://insider.kelbyone.com/create-texture-content-aware-fill/) (search summaries)
- Technique: fill a smaller section, then make a new selection that slightly overlaps the previous result and run again. The changing source gives different results; repeat until the target size — [KelbyOne via search](https://insider.kelbyone.com/create-texture-content-aware-fill/)

### Inferences
- Decision rule for an agent: extend (non-generative) only if (a) the added strip is ≤ ~10–15% of the dimension per side (heuristic), (b) the strip region in the source has low structure (low edge density, no faces or text), and (c) no straight lines cross into it, or lines can be continued with constraints. Otherwise prefer a tighter crop or a different aspect.
- Verification: look for duplicated patches (template-match the filled region against the source; high NCC matches mean repetition), seam gradients at the original border, and broken line continuity.
- After rotation/Upright, filling the transparent corners is a common use. Small corner wedges of sky/ground work well; wedges cutting through architecture usually do not.

### Gaps
- No quantitative studies on how large a classic (PatchMatch-based) content-aware extension can be before failure. Numbers above are heuristics.

---

## 7. Computational auto-cropping & horizon detection vs. expert decisions

### Takeaway
State of the art: GAIC/GAICD (CVPR 2019; TPAMI) formalised crop ranking with about 90 grid-anchor candidates per image, rated by 7 photographers/art students each. Supervised models reach Acc1/5 of about 68–70% and SRCC about 0.85–0.87. The VLM-based Cropper (CVPR 2025, Gemini 1.5 Pro + in-context learning) reaches Acc1/5 88.9% and SRCC 0.904. Pure saliency cropping (Twitter) was abandoned in 2021 over bias and "male gaze" failures. Auto perspective rectification succeeds on only ~16% of casual photos (Google). Experts still disagree about crops, so "top-N" rather than "the one" is the realistic target.

### Cited Findings
- GAIC: grid anchors with M×N = 12×12 bins; corners restricted to m×n = 4×4 regions (content preservation); aspect ratio limited to 0.5–2.0. This reduces millions of crops to about 90 candidates per image — [arXiv 1909.08989](https://arxiv.org/html/1909.08989)
- GAICD: 1,236 source images (1,000 needing recomposition + 236 well-composed), 106,860 annotated crops; 19 annotators (experienced photographers or art students); each crop rated 1–5 by 7 people (MOS); only 5.75% of crops had rating SD > 1.0. The extended version uses 3,336 images (2,636 train / 200 val / 500 test) — [arXiv 1909.08989](https://arxiv.org/html/1909.08989); [search summary](https://arxiv.org/pdf/1909.08989)
- Metrics: SRCC/PCC ranking correlation; "Return K of top-N" accuracy (Acc K/N); rank-weighted variants. These replace IoU/BDE on single-ground-truth datasets (FCDB, FLMS, CUHK-ICD), which are unreliable because many crops are acceptable — [arXiv 1909.08989](https://arxiv.org/html/1909.08989)
- GAIC (MobileNetV2): Acc1/5 62.5%, SRCC 0.783, 200 FPS on GPU / 6 FPS on CPU, <2.5M parameters (journal version figures); CVPR 2019 version: SRCC 0.735, Acc5 46.6%, Acc10 65.5% — [arXiv 1909.08989](https://arxiv.org/html/1909.08989); [CVPR 2019](https://openaccess.thecvf.com/content_CVPR_2019/papers/Zeng_Reliable_and_Efficient_Image_Cropping_A_Grid_Anchor_Based_Approach_CVPR_2019_paper.pdf)
- Cropper (Lee et al., CVPR 2025) on GAICD: Acc1/5 88.9, Acc4/5 79.4, Acc1/10 98.2, SRCC 0.904, PCC 0.860, versus GAIC 68.2/58.5/84.4/0.849/0.874, TransView 69.0/57.8/85.4/0.857/0.880, Chao et al. 70.0/59.8/86.8/0.872/0.893. Subject-aware (SACD): IoU 0.769 vs SAC-Net 0.767. Aspect-ratio-aware (FCDB): IoU 0.756 vs Mars 0.735. User study on 200 images, preference vs A2RL 60.8%, GAIC 62.2%, CGS 63.4%. Settings: 30 retrieved in-context examples, 6 candidates, 2 refinement iterations, temperature 0.05; Gemini 1.5 Pro primary, GPT-4o also tested. Training-free — [arXiv 2408.07790v2](https://arxiv.org/html/2408.07790v2); [CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Lee_Cropper_Vision-Language_Model_for_Image_Cropping_through_In-Context_Learning_CVPR_2025_paper.pdf)
- Twitter saliency cropping: crops were centred on the argmax saliency point, cropping only one dimension to reach the target aspect ratio. Disparities: 8% from parity favouring women, 4% favouring white over Black individuals, 7% favouring white over Black women; "argmax bias" amplifies disparity. Male-gaze cases (chest/legs chosen) were reported. Conclusion: "not everything is best done by algorithm"; Twitter removed the cropper in May 2021 — [Yee, Tantipongpipat, Mishra, arXiv 2105.08667](https://arxiv.org/pdf/2105.08667); [PetaPixel](https://petapixel.com/2021/05/22/twitter-axing-ai-photo-cropping-after-tests-reveal-race-gender-bias/)
- DEF CON 2021 bias bounty: Twitter's saliency favoured younger, slimmer, lighter, smoother-skinned faces and was more likely to crop out people in wheelchairs — [The Register](https://www.theregister.com/2021/08/11/defcon_twitter_ai/)
- Horizon/rectification: the Google edgelet + RANSAC vanishing-point pipeline delivered rectification on 15.7% of 2,199 photos and rejected the rest via safety checks — [Google Research](https://research.google.com/pubs/archive/42532.pdf). Deep single-image calibration with a perceptual measure (Hold-Geoffroy et al.) — [arXiv 1712.01259](https://arxiv.org/pdf/1712.01259). Adobe holds patents on automatic rotation correction and "enhanced automatic perspective and horizon correction" — [US 11,393,072](https://uspto.report/patent/grant/11,393,072); [US 10,652,472](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10652472)

### Inferences
- Agreement ceiling: since GAICD crops have MOS from 7 raters with notable spread, the "correct" crop is a set. An agent should output top-3 to 5 candidates and judge success as "≥1 in the human top-5" (Acc1/5-style), not IoU to a single crop.
- Hybrid agent recipe: VLM (Cropper-style) proposes candidates → hard-constraint filter (joints, chin, eye line, safe zones, minimum resolution) → aesthetic scorer (GAIC-type) re-ranks → border-patrol check. Never use pure argmax saliency for people. Use face/person boxes so no person is cut and the face is not lost to a body region.
- For horizon/perspective: detect line families; if confidence is low or faces would distort, do nothing. The Google results show abstaining is the correct default for most casual photos.

### Gaps
- No direct study comparing auto-crop outputs with named professional photo editors (e.g., magazine photo desks). GAICD annotators are "experienced photographers or art students".
- Precise SOTA horizon-detection accuracy numbers (e.g., HLW dataset AUC) were not gathered.

---

## 8. Resolution after crop (print & web)

### Takeaway
Print: 300 ppi for small prints viewed at arm's length; 240 ppi is indistinguishable for framed wall prints; 180–200 ppi for very large prints viewed from far away. Rule of thumb: viewing distance (in) ≈ 3500 / ppi. Web/social: Instagram serves 1080 px wide, so any crop leaving ≥1080 px on the short side of the post's width is enough. Check the remaining pixels before committing to aggressive crops or heavy rotation/keystone (which also costs pixels).

### Cited Findings
- 300 ppi for small prints; 240 ppi for most wall prints; 180–200 ppi for very large displays. 4×6–8×10 at 1–2 ft: 300 ppi; 11×14–16×20 at 2–3 ft: 240–300 ppi; 20×30–30×40 at 4–6 ft: 180–240 ppi. Required resolution scales inversely with viewing distance (3× farther, 3× less). Optimal viewing distance (in) = 3500 / ppi (240 ppi → ~15 in). Max print size = long-side pixels / 240 (6000 px → 25 in) — [search summary: photoworkout / photoseek / alanranger](https://photoseek.com/2011/print-sharp-maximum-size-quality-resolution-viewing-distance/); [photoworkout](https://www.photoworkout.com/print-resolution/)
- Instagram caps served images at 1080 px wide. Larger uploads only help compression quality — [Neal Schaffer](https://nealschaffer.com/instagram-post-size/)
- Print bleed must be included in pixel dimensions (+0.125 in per side) — [fcapgroup](https://www.fcapgroup.com/bleed-trim-and-safe-area-in-print-ads/)

### Inferences
- Pixel budget checks (derived): magazine full page 8.375×10.875 in + 0.25 in bleed total = 8.625×11.125 in at 300 ppi → **2588×3338 px minimum**. A double-page spread roughly doubles the width (~5100 px). An A4 + 3 mm bleed (216×303 mm) at 300 ppi → ~2551×3579 px.
- Combine rotation and crop losses: e.g., a 24 MP 3:2 file (6000×4000) straightened 2° keeps 95.1% linear (~5705×3803). A further crop to 4:5 portrait from the landscape frame gives ~3042×3803 px, which is enough for a full magazine page at 300 ppi (needs 2588×3338).
- Agent rule: refuse or warn when the post-crop effective ppi at the target output size is < 240 (print, normal viewing) or when the short side is < 1080 px (social). Upsampling (non-generative) beyond about 1.5× usually shows softness (heuristic, unsourced).

### Gaps
- No primary standard (e.g., ISO/FOGRA or a specific magazine spec) was fetched for minimum ppi. 300 ppi is industry convention via secondary sources.
