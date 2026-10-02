# Professional Color Correction, Skin Tone Numeric Standards, and Color Grading (high-end retouching / colorist practice, as of 2026-10)

Scope note: research for an AI agent that must apply and verify color work with measurable criteria using only non-destructive, non-generative tools (curves, selective color, hue/sat, color balance, gradient maps, LUTs, camera calibration / RAW development). Numbers marked "computed" were derived by the researcher from cited source data (formulas shown), not taken from a source.

---

## 1. Skin tone numeric standards (CMYK ratios, Lab a*/b*, hue angles, vectorscope skin line, RGB ratios)

### Takeaway
No single "correct" skin value exists; every practitioner source frames skin as a set of *relationships*: in CMYK, Y >= M (Y slightly higher, within ~10-20%), C ~= 1/5 to 1/3 of M (rising toward ~1/2 of M for very dark skin); in Lab, a* and b* both positive with b* slightly >= a* and midtone chroma ~15-20 (Margulis-school, "preferred" reproduction); in measured skin (spectrophotometry), CIELAB hue angle h_ab clusters around ~53-62 deg across all ethnic groups with C* ~18-22; on a Rec.709 vectorscope, skin sits on/near the 123 deg "skin-tone line" (+/-10-20 deg). Within-group variation exceeds between-group variation, so ethnicity-specific targets should be treated as soft priors, not rules.

### Cited Findings

**CMYK relationships (print-retouching tradition)**
- For satisfactory Caucasian skin, Yellow should be similar to Magenta (within ~10 points), with Yellow typically a bit stronger than Magenta; Cyan should be one-third to one-fifth of Magenta. A common light-Caucasian combination is C10 M40 Y50 K0. — [Photofocus, Lee Varis "Color Correction for the Best Skin Tone"](https://photofocus.com/photography/color-correction-for-the-best-skin-tone/) (Varis's own PDF at [varis.com](https://varis.com/books/ColorCorrectSkinTone.pdf) is an image-only PDF and could not be text-extracted)
- Alternate formulation: Cyan between 20% and 33% of Magenta; Yellow equal to or slightly higher than Magenta, never less than Magenta and probably not more than ~20% above it. — [DPReview Retouching forum thread "Question About CMYK Values And Skin Tone"](https://www.dpreview.com/forums/thread/2713305) (forum source; consistent with Varis)
- Ethnic variation (as summarized in search results from Varis/retouching-blog material): Black skin is stronger in both C and M, with C often rising to about half of M; Asian skin is a bit stronger in Y and C than the Caucasian example. — [Photofocus/Varis](https://photofocus.com/photography/color-correction-for-the-best-skin-tone/); [Pixelation blog, "Correcting Skin Color: Age, Ethnicity, and Tonal Variations"](https://pixelationblog.wordpress.com/2009/06/10/correcting-skin-color-skin-tones-age-and-ethnicity/) (page not fetched in full; attribution to specific page is from search snippet)
- "There is no single combination of RGB or CMYK values ... that produces the only 'correct' flesh tone. It is the relationship of the three colors to each other" that is the guide. — [Photofocus/Varis](https://photofocus.com/photography/color-correction-for-the-best-skin-tone/)

**Lab (Margulis school / preferred reproduction)**
- Dan Margulis (*Photoshop LAB Color*): for Caucasian skin, B is slightly greater than A (yellower = preferred, "tanned" look vs. redder). — [FM Forums "Skin Tone and LAB color"](https://www.fredmiranda.com/forum/topic/329392/); [Dehancer "Lifelike" book, Ch. 16 "What Color is Your Skin?"](https://blog.dehancer.com/lifelike-book/chapter-16-what-color-is-your-skin/)
- Midtone skin: typical A and B values 15-20; below ~15 reads paler/more neutral; above ~30 looks oversaturated. Highlights and shadows carry different (per the chapter, higher) AB values than midtones. B < A (redder) is natural/acceptable for older people, babies, blondes and red-haired subjects. — [Dehancer Ch. 16](https://blog.dehancer.com/lifelike-book/chapter-16-what-color-is-your-skin/)
- Worked examples: an uncorrected portrait at -5A/19B (greenish-yellow cast, "highly irregular") corrected to 15A/16B; a cold tablet-lit shadow at -3A/-25B vs normal skin at 20A/17B. Asian skin measured "almost the same" Lab as Caucasian but "more yellow (golden)". — [Dehancer Ch. 16](https://blog.dehancer.com/lifelike-book/chapter-16-what-color-is-your-skin/)
- Margulis on preference: viewers dislike overly pale or pink skin and consider suntanned skin more "accurate"; this preference is strongest for light-skinned Caucasians. — [Dehancer Ch. 16 quoting Margulis](https://blog.dehancer.com/lifelike-book/chapter-16-what-color-is-your-skin/)

**Measured skin color (CIELAB, academic)**
- Largest dataset found (2026, ISSA archive, 14,532 measurements, 2,113 subjects, 8 groups, 10 body sites), mean (SD): Caucasian L*61.2(5.4) a*11.0(3.9) b*14.7(2.7) C*18.7; Chinese 59.8/10.1/16.7, C*19.7; Japanese 63.5/9.8/17.0, C*19.8; South Asian 52.7/10.4/17.9, C*20.8; African 39.6/10.2/14.4, C*17.7; Iraqi 57.3/10.2/15.8, C*19.0; Thai 56.4/10.0/19.0, C*21.6; Arabian 60.2/10.9/17.9, C*21.1. 89.4% of samples have a perceptually indistinguishable (dE*ab ~2) counterpart in another ethnicity; median gamut overlap between group pairs 60.5%; "within-group variability ... frequently exceeds between-group differences." — [Lu et al. 2026, Skin Research and Technology (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13097458/); [Wiley version](https://onlinelibrary.wiley.com/doi/full/10.1111/srt.70343)
- Wang, Xiao, Wuerger et al. (CIC 2015): mean hue angles 60 deg (Oriental), 54 deg (Caucasian), 60 deg (South Asian), 53 deg (African) with one instrument; 60/56/59/54 deg with another. Biggest between-group difference is along b* (yellowness): Thai highest, Caucasian lowest. Distributions overlap heavily. — [Wang et al., "Measuring Human Skin Colour", IS&T Reporter](https://www.imaging.org/common/uploaded%20files/pdfs/Reporter/Articles/2016_31/REP31_1_2015CIC_WANG_PG230.pdf)
- Classic reference on skin in CIELAB: Weatherall & Coombs, J Invest Dermatol 1992. — [JID](https://www.jidonline.org/article/0022-202X(92)90347-7/pdf) (not fetched; cited for provenance only)
- Fitzpatrick scale limitations vs CIELAB measurement discussed in — [NHSJS 2024](https://nhsjs.com/2024/shades-of-skin-limitations-of-the-fitzpatrick-scale-with-cielab/) (not fetched)

**Vectorscope skin-tone line**
- Skin-tone reference line default is 123 deg (configurable 0-359). It derives from NTSC I/Q, where I/Q axes are rotated 33 deg from Cb/Cr; the -I direction roughly corresponds to human skin. "Most properly exposed skin falls within ~10-20 deg of that axis regardless of complexion; only hue balance differs." Tolerance bands of +/-10 deg or +/-20 deg are common; treat as a guide, not a hard rule. — [Time in Pixels, Nobe OmniScope docs: Vectorscope](https://docs.timeinpixels.com/nobe-omniscope/scopes/vectorscope)
- Same concept in Premiere Pro (skin-tone line used to correct skin) — [Adobe Premiere Pro "Correct skin tones"](https://helpx.adobe.com/si/premiere-pro/how-to/correct-skin-tones.html); Pinnacle "Selective Vectorscope" — [Pinnacle](https://www.pinnaclesys.com/en/landing/color-grading/selective-vectorscope/)

**RGB / HSV rules (computer-vision skin detection; useful as sanity gates, not aesthetic targets)**
- Kovac et al. rule (uniform daylight): skin if R>95, G>40, B>20, max-min>15, |R-G|>15, R>G, R>B. — [Human Skin Detection Using RGB, HSV and YCbCr (arXiv 1708.02694)](https://arxiv.org/pdf/1708.02694)
- Takayama et al.: skin if Hue 0-40 deg and Value >75% (animation-character paper). — [arXiv 1503.06275](https://arxiv.org/pdf/1503.06275)
- Practitioner heuristic: healthy skin R > G > B; a quoted "common" ratio R 70-80%, G 60-70%, B 50-60%. — [Retouch4me blog](https://retouch4.me/blog/how-to-correct-skin-tone-lightroom-photoshop-retouch4me) (vendor blog; low authority)
- App-vendor reference swatches (low authority, unsourced): Fair Lab 84/10/18 (RGB 245,212,180); Light 77/13/22; Medium-light 64/17/28; Medium 54/20/30; Medium-dark 43/22/28; Dark 29/20/22; Deep 20/16/16; rule "a* positive, b* positive". — [Luttie skin-tone balance tool](https://luttie.app/tools/skin-tone-balance)

### Inferences
- Computed (researcher): converting the Lu et al. 2026 group means (D65 assumed, sRGB) gives: h_ab 53.2 deg (CA), 58.8 (CN), 60.0 (JP), 59.8 (SA), 54.7 (AF), 57.2 (IQ), 62.2 (TH), 58.7 (AB); HSV hue 19.9-25.1 deg; HSV saturation 31-40%; G/R 0.74-0.81 and B/R 0.60-0.69; Rec.709 CbCr vector angle (counter-clockwise from +Cb) 124.7-131.7 deg. This independently reproduces the 123 deg skin line (+~2-9 deg yellower), confirming the scope convention and the "+/-10 deg" band. Formula: h_ab = atan2(b*, a*); vectorscope angle = atan2(Cr, Cb) with BT.709 coefficients.
- Measured skin (C* ~18-22, b*/a* ~1.3-1.9) is *less red-relative-to-yellow* than many retouchers' targets would imply but has a similar chroma; Margulis's 15-20 midtone AB range is consistent with measured chroma. Photographic "preferred" skin is typically slightly more saturated/yellow than colorimetric skin (Margulis preference quote), so an agent should default to h_ab ~50-65 deg, a* > 0, b* >= a* (except for flagged subjects: infants, elderly, redheads), midtone C* ~15-28, and flag C* > ~30-35 as oversaturated.
- Translating CMYK rules into code requires a defined CMYK profile (e.g., US Web Coated SWOP v2 or FOGRA39); results differ by profile, so Lab/hue-angle rules are more portable for automated checking.
- Suggested machine gates (synthesis): (1) median skin h_ab in [48, 66] deg (soft), (2) a*>0 and b*>0, (3) b*/a* in [0.9, 2.0] (red-skewed subjects may be 0.8-1.0), (4) vectorscope angle within +/-10 deg of 123 deg (hard warn at +/-20 deg), (5) R>G>B in sRGB.

### Gaps
- Primary text of Margulis's CMYK skin rules (*Professional Photoshop*, 5th ed.) not retrieved; the CMYK rules here come via Varis and forum summaries. Margulis Lab numbers also secondhand (Dehancer, FM Forums).
- Lee Varis's original PDF is image-only; exact per-ethnicity CMYK numbers from it were not extracted.
- Lu et al. 2026 did not state illuminant/observer in the extracted text; the CIE conditions (likely D65/10 deg) are unconfirmed, which affects the computed hue/RGB numbers by a few degrees.
- No authoritative published "skin hue variance" tolerance (e.g., max std of h_ab across a face) was found.

---

## 2. Neutral / white balance correction and color-checker profiling

### Takeaway
Pros neutralize with a measured gray (gray card, ColorChecker gray patches or known neutrals) so that R=G=B (equivalently Lab a*=b*=0), then build per-lighting custom camera profiles from a ColorChecker shot (DCP for Lightroom/ACR, ICC for Capture One). Verification is per-patch Delta E, with ~1 dE00 regarded as excellent and ~2 dE00 as the visual threshold.

### Cited Findings
- Calibrite ColorChecker Camera Calibration software builds custom profiles from ColorChecker Classic/Passport or Digital SG targets; outputs DNG/DCP profiles for Adobe Camera Raw/Lightroom/Photoshop, and ICC camera profiles for Capture One (with Calibrite PROFILER). Lightroom plug-in: File > Export with Preset > ColorChecker Camera Calibration. — [Calibrite ColorChecker Camera Calibration](https://calibrite.com/photo-target/); [Calibrite: Using Camera Profiles in Adobe Lightroom](https://calibrite.com/learning-centre/using-camera-profiles-in-adobe-lightroom/)
- Workflow: shoot a ColorChecker frame under the same light as the session's key scenes; generate a DCP (Lightroom) or ICC (Capture One) for that lighting condition; apply across the set. — [Calibrite](https://calibrite.com/photo-target/); [Calibvision "How to Use a ColorChecker 24 in Lightroom" (2026)](https://calibvision.com/blog/how-to-use-colorchecker-24-lightroom/); [Brent Bergherm, Calibrating your Camera for Consistent Color](https://brentbergherm.com/how-to/calibrating-your-camera-for-consistent-color/)
- Custom DCPs may fail to appear in Lightroom Classic 12.4 in some installs (known user issue) — [Adobe Community thread](https://community.adobe.com/t5/lightroom-classic-discussions/custom-made-x-rite-colorchecker-dcp-profiles-don-t-show-up-in-lightroom-classic-12-4/td-p/13909245)
- In Lab, a neutral is a*=b*=0; Dehancer's examples show casts as negative a* (green) / negative b* (blue) shifts in skin and shadows (e.g., -3A/-25B in tablet-lit shadow). — [Dehancer Ch. 16](https://blog.dehancer.com/lifelike-book/chapter-16-what-color-is-your-skin/)
- Profile verification is done per patch in CIEDE2000; max error < 1.0 dE00 is cited as ideal. — search-result summary of [Colorium Lab](https://colorium-lab.web.app/) and [Metricgate dE2000 calculator](https://metricgate.com/docs/delta-e-ciede2000/) (tool/vendor pages; medium authority)

### Inferences
- Agent procedure: (1) locate neutral reference (ColorChecker row 4 patches, gray card, known-white surfaces with no specular clipping); (2) sample a 5x5+ pixel average, not a single pixel; (3) apply per-channel curve or WB/tint so the sample's a*,b* -> 0 (|a*|,|b*| < ~1-2); (4) check ColorChecker patches against reference Lab (published by Calibrite for post-2014 charts) using dE00 — target mean < ~2, max < ~4-5 for camera profiles; (5) then evaluate skin with section 1 gates. Note: deliberately warm grades will leave neutrals non-neutral; neutralization should be the *correction* stage before grading.
- Dual-illuminant DCPs (e.g., built from StdA + D65 shots) interpolate between two calibration illuminants; this is how Adobe's own profiles work, but this was not verified in a fetched source in this session.

### Gaps
- Official ColorChecker reference Lab values (Calibrite's published table) and the specific mean/max dE that Calibrite reports as "good" were not retrieved.
- Capture One's ICC-from-ColorChecker procedure details (e.g., need for linear "Linear Response" curve before profiling) not verified.
- Dual-illuminant DCP specifics not verified from a primary source.

---

## 3. Correcting skin color unevenness (redness, yellow/green casts, targeted hue/sat, selective color)

### Takeaway
Pro practice localizes correction: a Hue/Saturation layer targeted to Reds (range narrowed by eyedropper/sliders), shifted slightly toward yellow and/or reduced in saturation, then masked to blotches only; Capture One's Skin Tone tool provides "Uniformity" sliders that compress hue/saturation/lightness spread toward a picked reference. Verification = reduced spread of h_ab / a* across the skin mask.

### Cited Findings
- Redness workflow: add Hue/Saturation adjustment layer, choose "Reds", use the panel eyedropper on the reddest skin, temporarily max the sliders to visualize the range, adjust the range sliders in the color bar, then shift Hue/Saturation/Lightness and paint the effect into blotches via mask. — [PHLEARN "Remove Redness From Skin in Photoshop"](https://phlearn.com/tutorial/how-to-remove-redness-from-skin-in-photoshop/); [SLR Lounge "Correct Red Blotchy Skin"](https://www.slrlounge.com/how-to-easily-correct-red-blotchy-skin-in-photoshop/); [PetaPixel "Remove Red Patches in 1 Minute"](https://petapixel.com/2018/12/26/how-to-remove-red-patches-from-skin-in-photoshop-in-just-1-minute/)
- Capture One Color Editor > Skin Tone tab: "Amount" sliders (Hue: left/right adds green/red; Saturation; Lightness) and "Uniformity" sliders that blend Hue/Saturation/Lightness of colors inside the selection wireframe toward the picked reference; for Caucasian skin pick a neutral (well-colored) skin tone and expand the range to include the unwanted reds and yellows. — [Capture One Support: Adjusting skin tones](https://support.captureone.com/hc/en-us/articles/360002596077-Adjusting-skin-tones); [Capture One blog: How to get uniform skin tones](https://www.captureone.com/blog/get-uniform-skintones); [Capture One blog: Achieving perfect skin tones](https://www.captureone.com/blog/achieving-perfect-skin-tones-using-capture-one)
- Margulis-school diagnosis: a green/yellow cast shows as a* near 0 or negative with b* high (e.g., -5A/19B), corrected to ~15A/16B. — [Dehancer Ch. 16](https://blog.dehancer.com/lifelike-book/chapter-16-what-color-is-your-skin/)

### Inferences
- Quantified approach for an agent: build a skin mask, compute per-pixel h_ab and C*. Redness blotches are pixels with h_ab well below the face median (e.g., > ~8-10 deg toward red/lower angle) and/or higher a*. Correct with a Reds-targeted Hue shift (+ toward yellow) and saturation reduction until blotch median h_ab and a* are within ~dE00 2 of the surrounding skin median (JND ~2 per Lu et al.). Yellow/green casts: pixels with a* low relative to b*; correct with curves in a* (Lab) or Selective Color "Yellows/Reds" by reducing Yellow / adding Magenta in small steps.
- Typical values: corrections should be small (hue shifts of a few degrees, saturation reductions of ~5-20 points in Photoshop units) — this is practitioner convention but no fetched source gave exact numbers.
- Success metric: decrease in skin-mask std(h_ab) and std(a*) without shifting the median outside section 1 gates; ensure transitions show no masking halos (check gradient of a* at mask edges).

### Gaps
- No authoritative published "typical" Selective Color percentages for skin (e.g., Reds: -Cyan x%) were found; retouching-academy sources were not retrieved.
- No published threshold for "acceptable" intra-face hue variance.

---

## 4. Color grading techniques (split toning, curves, gradient maps, LUTs, harmony, skin vs background separation, grading wheels)

### Takeaway
Grading is done by tonal zone (shadows/midtones/highlights) using wheels or split toning; the dominant commercial harmony is complementary orange (skin) vs teal (shadows/background), which maximizes subject-background "color contrast". Skin is protected (kept on the skin line) while background/shadows carry the stylistic hue. Lightroom's Color Grading panel adds Blending and Balance controls; Capture One offers skin-specific tools plus color harmonies.

### Cited Findings
- Lightroom Color Grading: three wheels (Shadows, Midtones, Highlights) plus a Global wheel; distance from center = intensity. Blending (100 = all three ranges spill fully into each other, smoothest) and Balance (left = more of image treated as shadows; right = more as highlights). Replaced old Split Toning panel. — [DIYPhotography "Lightroom Color Grading"](https://www.diyphotography.net/lightroom-color-grading/); [Photzy "From Split Toning to Color Grading"](https://photzy.com/from-split-toning-to-color-grading-lightroom-changes-explored/); [Darkroom Help: Color Grading Wheels](https://darkroom.co/help/edit/color-grading)
- Orange-and-teal: skin naturally falls in orange; teal is opposite on the wheel; pushing shadows/background toward teal creates color contrast that separates subject from background. — [Fstoppers "Cinematic Orange and Teal in Lightroom"](https://fstoppers.com/lightroom/create-cinematic-orange-and-teal-color-grade-lightroom-577820); [Impact Photography cinematic walkthrough](https://www.impact-photography.com/how-to-color-grade-photos-to-look-cinematic-in-lightroom-a-complete-walkthrough/)
- Colorists grade by tonal zones: highlights for emotional feel, midtones for skin/subject, shadows with their own color character. — [Impact Photography](https://www.impact-photography.com/how-to-color-grade-photos-to-look-cinematic-in-lightroom-a-complete-walkthrough/)
- Capture One supports applying color harmonies (complementary, analogous, etc.) in its color tools. — [Capture One blog: Applying color harmonies](https://www.captureone.com/blog/applying-color-harmonies-in-capture-one)
- Vectorscope skin line is used during grading to verify skin hasn't drifted: trace energy outside the band = hue drift. — [Time in Pixels](https://docs.timeinpixels.com/nobe-omniscope/scopes/vectorscope)

### Inferences
- Orange-teal geometry: skin vector ~123-132 deg (computed in section 1); its complement is ~303-312 deg on the vectorscope (teal/cyan-blue). A grade can be checked numerically: background/shadow median vectorscope angle ~ skin angle + 180 deg +/- 20 deg for complementary; within +/-30 deg for analogous.
- "Separating skin from background grade": apply the global look, then use a skin-range qualifier (Hue/Sat range, Capture One Skin Tone, Lightroom HSL Orange) or mask to pull skin back to its pre-grade h_ab (within dE00 ~2-3) while background keeps the shift.
- Gradient maps / LUTs at low opacity: common practitioner habit is low opacity (~5-20%) with Soft Light/Color blend modes; LUTs should be applied after normalization (correct WB/exposure) because LUTs assume a specific input. These are conventions; no fetched source supplied numbers.
- Verification of a grade: measure (a) skin median h_ab shift vs pre-grade (keep < ~5 deg unless stylistic intent), (b) skin C* within gates, (c) out-of-gamut / clipped pixel % after conversion to output space.

### Gaps
- No primary Mixing Light / Lowepost / Retouching Academy content retrieved; typical gradient-map opacities and LUT strengths are unsourced conventions.
- No quantitative definition of "color contrast" from colorist literature was found.

---

## 5. RAW development best practices (profiles, exposure, recovery, color spaces, bit depth, soft proofing, output)

### Takeaway
Standard pro pipeline: custom or appropriate camera profile -> exposure/WB -> highlight/shadow recovery -> edit in 16-bit ProPhoto RGB (or Adobe RGB) -> soft proof for print -> convert to 8-bit sRGB only at final web export (perceptual or relative colorimetric with black-point compensation).

### Cited Findings
- Edit in ProPhoto RGB at 16-bit, convert to sRGB at export for web/delivery. 8-bit ProPhoto bands aggressively because the larger gamut spreads 256 levels farther apart; Photoshop "16-bit" provides 32,768 levels per channel. — [Markus Hagner Photography: sRGB vs Adobe RGB vs ProPhoto (July 2026)](https://markus-hagner-photography.com/srgb-vs-adobe-rgb-vs-prophoto-rgb-which-color-space-to-use-and-when/); [Auric Artisan: RGB working spaces compared (2026)](https://auricartisan.com/library/learn/articles/2026-05-25-rgb-working-spaces-compared)
- Convert to 8-bit sRGB at the very end; standard sRGB profiles use relative colorimetric and clip out-of-gamut detail, so for wide-gamut images a perceptual-capable (v4) sRGB profile can preserve gradation. — [Adobe Community: ideal workflow 16-bit ProPhoto -> 8-bit sRGB](https://community.adobe.com/questions-712/whats-the-ideal-workflow-for-converting-16-bit-prophoto-to-8-bit-srgb-1153651); [DPReview: How to best convert from ProPhoto to sRGB](https://www.dpreview.com/forums/thread/4252548)
- Camera profiles are chosen at the top of Lightroom's Basic panel (Profile Browser); custom DCPs from ColorChecker appear there. — [Calibrite: Using Camera Profiles in Lightroom](https://calibrite.com/learning-centre/using-camera-profiles-in-adobe-lightroom/)
- ICC/soft-proofing workflows for photographers in 2026 described in — [Tov Studio: ICC Profile Color Management Workflow (2026)](https://tovstudiophoto.com/icc-profile-color-management-workflow-photography/); [Tov Studio: Soft Proofing 2026](https://tovstudiophoto.com/wedding-photographer-icc-soft-proofing-2026-guide/) (not fetched in full)

### Inferences
- Machine checks: (1) working file bit depth = 16; (2) working space ProPhoto/Adobe RGB/Display P3; (3) before export, compute % pixels out of sRGB gamut (Lab -> sRGB linear values outside [0,1]); if > ~1-2% in salient areas (skin, products), reduce saturation locally before conversion rather than relying on clipping; (4) after export, embed sRGB ICC; (5) for print, soft proof with the paper's ICC and check gamut warning.
- Disagreement: some practitioners argue Adobe RGB or Display P3 suffices and ProPhoto only matters for highly saturated subjects; skin tones themselves are well within sRGB (computed sRGB values in section 1 are all in-gamut), so gamut issues are mostly in saturated backgrounds/clothing.

### Gaps
- Adobe's own documentation on Lightroom's internal space (linear ProPhoto primaries, "MelissaRGB" for display) not retrieved in this session.
- No primary source retrieved for exposure/highlight-recovery numeric guidance (e.g., histogram headroom targets).

---

## 6. Monitor calibration and viewing conditions

### Takeaway
Two camps: a photo/web editing target of D65 (6500K), 100-120 cd/m², gamma 2.2 (or sRGB tone curve); a prepress/soft-proofing standard (ISO 12646 with ISO 3664 P2) of D50, ~160 cd/m² default for testing, gamma ~2.2. For print matching in dim rooms, many lower luminance to 80-100 cd/m². Sources disagree, so the target should be chosen by output.

### Cited Findings
- Basic recommended targets: Gamma 2.2, White point D65 (6500K), Luminance 100-120 cd/m². 120 cd/m² is a common software default; acceptable range 80-120; 100 cd/m² often recommended for prepress; Eizo recommends 80-100 cd/m² for print proofing. — [American Color Imaging: Monitor Calibration Guide](https://acilab.com/monitor-calibration-guide-for-accurate-prints/); [Digital Photography School: Six aspects of monitor calibration](https://digital-photography-school.com/six-aspects-monitor-calibration-need-know/); [Atelier Mond 2026 guide](https://mondphotos.com/2026/03/31/the-ultimate-guide-to-calibrating-your-monitor-for-accurate-prints/)
- ISO 12646 (displays for colour proofing): default calibration for testing is 160 cd/m², white point D50 (x=0.3457, y=0.3585, 2 deg observer), gamma ~2.2; with ISO 3664 viewing condition P2, 160 cd/m² correlates with 500 lux on a perfect reflecting diffuser. — [Wikipedia: Monitor proofing](https://en.wikipedia.org/wiki/Monitor_proofing); [ISO 12646:2015 sample (iTeh)](https://cdn.standards.iteh.ai/samples/57311/19256ef439e54e00a1724d18f3640e47/ISO-12646-2015.pdf); [IDEAlliance Soft Proofing Certification protocol](https://www.idealliance.org/wp-content/uploads/2016/10/IDEAlliance-Soft-Proofing-Certification-Protocol-v9.pdf)
- Conflicting secondary claims: one summary attributes "80-120 cd/m²" and "D65, 75-100 cd/m²" to ISO 3664 (2000 edition) — these figures appear in older guides and conflict with the ISO 12646/3664:2009 D50/160 cd/m² pairing above. — [DesignYourWay](https://www.designyourway.net/blog/how-to-calibrate-your-monitor-for-print/) vs [Wikipedia: Monitor proofing](https://en.wikipedia.org/wiki/Monitor_proofing)
- Community discussion of luminance choice (DisplayCAL) — [DisplayCAL forum: which monitor brightness](https://hub.displaycal.net/forums/topic/what-monitor-brightness-is-recommended/) (not fetched)

### Inferences
- For an AI agent, monitor calibration is irrelevant to *numeric* verification (it reads pixel values directly), but it matters for any human review loop. The agent should evaluate in a defined, documented space (sRGB/D65 for web; Lab D50 via ICC for print) and report which.
- Note Lab white reference: ICC profile connection space is D50; many Python libraries default to D65 Lab. A mismatch shifts measured skin a*/b* by a few units — agents must fix one convention.

### Gaps
- dpbestflow (ASMP) monitor calibration page returned HTTP 503; its recommendations could not be verified.
- ISO 3664:2009 primary text not retrieved; exact display luminance clause unverified.

---

## 7. Consistency across a series (color matching)

### Takeaway
Consistency is achieved upstream (same custom camera profile per lighting setup, a ColorChecker/gray reference frame per setup, synchronized RAW settings) and verified downstream by comparing a reference image's skin and neutral statistics against each image.

### Cited Findings
- Shoot a ColorChecker under each lighting setup and apply the resulting profile to all frames from that setup — the core consistency mechanism promoted by Calibrite. — [Calibrite](https://calibrite.com/photo-target/); [Brent Bergherm](https://brentbergherm.com/how-to/calibrating-your-camera-for-consistent-color/)
- Capture One Skin Tone uniformity uses a picked reference color and pulls the selected range toward it; the same reference/adjustment can be copied across images. — [Capture One Support](https://support.captureone.com/hc/en-us/articles/360002596077-Adjusting-skin-tones)
- JND for skin: dE*ab ~2 used as the perceptual threshold in skin research. — [Lu et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13097458/)

### Inferences
- Agent procedure: choose a hero image; compute for each image (a) neutral reference Lab, (b) skin-mask median L*, a*, b*, h_ab, C*; match via per-channel curves/WB so neutral dE00 < ~1-2 and skin median dE00 < ~2-3 vs hero (L* may legitimately differ with lighting; compare a*/b* or dC*/dh separately). Photoshop "Match Color" or histogram matching can be a starting point but must be followed by the skin/neutral check.

### Gaps
- No retrieved professional source specifying numeric series-consistency tolerances (e.g., catalog/e-commerce dE spec). E-commerce product color tolerance standards were not researched here.

---

## 8. Measurable metrics usable by code

### Takeaway
Use CIEDE2000 for all color-difference checks: < 1 imperceptible, ~2 just-noticeable (also the skin-research JND), ~3.3-3.5 a practical print tolerance. Combine with skin hue-angle/vectorscope gates, chroma bounds, neutral a*/b* ~ 0, and gamut/clipping percentages.

### Cited Findings
- dE00 < 1.0 "golden pass"; within ~2.0 dE00 humans should not distinguish; < 1.5-2.0 acceptable in some contexts. — [Metricgate dE2000 docs](https://metricgate.com/docs/delta-e-ciede2000/); [ResearchGate: CIEDE2000 vs visual thresholds](https://www.researchgate.net/figure/CIEDE2000-color-differences-DE00-compared-with-literature-data-for-visual-thresholds_fig2_362275999)
- Printing: dE*ab = 5 corresponds to dE00 0.95-6.42 (mean 3.30), so recommended print tolerance dE00 = 3.3 (looser 3.5). — [Scientific.net: Printing color difference tolerance by CIEDE2000](https://www.scientific.net/AMM.262.96)
- Industry grades: Grade A dE00 1.6-3.2 (hardly noticeable / same color); Grade B 3.2-6.5. — search-result summary (Nippon Denshoku scale; primary not fetched)
- Dental ceramics (skin-adjacent biological color) has published CIEDE2000 perceptibility/acceptability thresholds for lightness, chroma and hue separately. — [Journal of Dentistry 2011 (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0300571211002235) (abstract only)
- Reference implementations of CIEDE2000 in 40+ languages. — [GitHub michel-leonard/ciede2000-color-matching](https://github.com/michel-leonard/ciede2000-color-matching)
- Skin JND dE*ab ~2; skin-research individual overlap analysis based on this threshold. — [Lu et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13097458/)
- Vectorscope tolerance band +/-10 deg or +/-20 deg around 123 deg. — [Time in Pixels](https://docs.timeinpixels.com/nobe-omniscope/scopes/vectorscope)

### Inferences (proposed metric set for an agent; thresholds synthesized from the findings above)
| Check | Computation | Target / pass |
|---|---|---|
| Neutral balance | mean Lab of neutral samples | abs(a*), abs(b*) < 1.5 (correction stage) |
| Profile accuracy | dE00 per ColorChecker patch | mean < 2, max < 4-5 |
| Skin hue | median h_ab over skin mask | ~48-66 deg (soft), warn outside |
| Skin vector angle | atan2(Cr,Cb) BT.709 | 123 deg +/-10 (warn +/-20) |
| Skin yellow/red balance | b*/a* | ~0.9-2.0 (redder OK for infants/elderly/redheads) |
| Skin chroma | C* median | ~15-28; flag >30-35 (Margulis: >30 oversaturated) |
| Skin uniformity | std(h_ab), std(a*) in mask | decrease after correction; blotches within dE00 ~2 of median |
| Series consistency | dE00 of skin median & neutrals vs hero | skin < 2-3, neutrals < 1-2 |
| Print tolerance | dE00 proof vs target | <= 3.3-3.5 |
| Gamut/clipping | % pixels outside output gamut; % channels at 0/255 | near 0 in skin; low single-digit % overall |
| Bit depth | file metadata | 16-bit during edit; 8-bit only at export |

- Always state Lab white point (D50 vs D65) and observer; compute dE00 on the same convention.

### Gaps
- No professional retouching source specifying dE tolerances for skin-specific deliverables (e.g., cosmetic advertising) was found.
- No published standard for acceptable skin hue variance or gamut clipping percentages; thresholds above are synthesized.
