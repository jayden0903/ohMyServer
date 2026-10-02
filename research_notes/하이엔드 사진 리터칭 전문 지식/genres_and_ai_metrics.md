# Genre-Specific Retouching Practice and Quantitative / AI Evaluation of Parametric (Non-Generative) Retouching

Scope note: research conducted 2026-10-02. Sources are a mix of primary papers (arXiv/CVF/NeurIPS/SIGGRAPH), official competition rules, and secondary industry guides. Secondary-source claims (marketplace image specs, tutorial blogs) are flagged. Items not verified in this session are moved to Gaps, even when they are "well known".

---

## A1. How retouching differs by genre (what is fixed, how heavy, deliverables, time budgets)

### Takeaway
Retouching weight scales roughly as: portrait/headshot (light, keep permanent features) < editorial (moderate, series consistency) < commercial (heavy, remove every distraction, hours per image) < beauty (heaviest skin work, 3 to dozens of hours) < creative/composite. E-commerce product work is governed less by taste than by hard marketplace specs (pure white RGB 255, ~85% fill, >=1000-1600 px long side, sRGB, consistent framing across SKUs).

### Cited Findings
- Portrait retouching: permanent features (scars, freckles, moles) are retained; only non-permanent issues (pimples, redness, bruises) are removed; "the skin is generally left intact apart from removing non-permanent details", with only minimal evening of texture in female portraits. — [Retouching Academy, Retouching Guidelines & Considerations](https://retouchingacademy.com/retouching-guidelines-and-considerations/)
- Editorial retouching: permanent features may be removed/reduced, wrinkles minimized, discoloration addressed; result "cleaned up, but not excessively polished"; consistency across the whole series of images is required. — [Retouching Academy](https://retouchingacademy.com/retouching-guidelines-and-considerations/)
- Commercial retouching: all distracting elements removed; parts of the image may be changed to "beautify" the surroundings; "more time-consuming than the previous two categories", "a number of hours to complete"; visual consistency across the collection is prioritized; subject matter spans cars, clothes, products, jewelry, food, cosmetics, etc. — [Retouching Academy](https://retouchingacademy.com/retouching-guidelines-and-considerations/)
- Beauty retouching: all permanent and temporary imperfections removed; skin can take up to ~90% of the frame in makeup beauty; time "anywhere from 3 up to dozens of hours"; dodge & burn is the core technique. — [Retouching Academy](https://retouchingacademy.com/retouching-guidelines-and-considerations/)
- Creative retouching (multi-image composites, reality manipulation acceptable) is the most time-intensive category. — [Retouching Academy](https://retouchingacademy.com/retouching-guidelines-and-considerations/)
- Amazon main image (secondary source, Amazon's own help page did not render in fetch): pure white background RGB (255,255,255); off-white such as 253,253,253 can trigger automated flagging; product should fill ~85% of the frame; minimum 1,000 px on longest side (zoom activates at >=1,000 px; 1,600 px+ recommended); <10 MB; JPG/PNG/TIFF/GIF; sRGB; no text/watermarks. — [SquareShot 2026 guide](https://www.squareshot.com/post/amazon-product-image-dimensions); [Sellhound](https://www.sellhound.com/learn/amazon-main-image-requirements) (search-result summaries; official page: [Amazon Seller Central G1881](https://sellercentral.amazon.com/help/hub/reference/external/G1881) — content not retrievable)
- Shopify (secondary): recommends 2048x2048 px square; white not mandated but clean backgrounds recommended; consistency rules for catalogs: same aspect ratio, background, lighting/color temperature, same padding/product placement in frame, same editing treatment; JPEG q80-85 at 2048 px typically 150-300 KB. — [SquareShot Shopify guide](https://www.squareshot.com/post/shopify-product-image-requirements); [Pixc](https://pixc.com/blog/shopify-image-sizes-guide/)
- Wedding/portrait sets: PPR10K's expert retouchers adjusted each group of photos of the same subject/scene "to have consistent tones" — group-level consistency is an explicit professional requirement for portrait/event delivery. — [PPR10K, arXiv 2105.09180](https://arxiv.org/abs/2105.09180)

### Inferences
- An agent should pick a "retouch intensity profile" per genre before touching sliders, e.g.:
  - Headshot/portrait/wedding: remove transient blemishes only; keep moles/freckles/scars; texture retention target near 1.0 (see B2 metrics); priority on batch/group tonal consistency (wedding sets of hundreds of images => global parametric edits + sync, minimal local work).
  - Editorial/fashion: moderate cleanup, wrinkles softened not erased; series consistency is a hard constraint.
  - Beauty: heavy D&B, all blemishes; but pore texture must survive at 100% zoom (high-end beauty is judged at pixel level).
  - Commercial/advertising: remove every distraction, environment cleanup, client-brand color accuracy.
  - E-commerce: rule-checkable deliverable (background exact 255, fill ratio, dimensions, sRGB) => implement as hard pass/fail validators, not aesthetic judgment.
- Because e-commerce validators operate on pixel values, a background that "looks white" (e.g., 250-254) is a failure; an automated check should count non-255 pixels in the background mask outside a small shadow region.

### Gaps
- No primary source found with concrete per-image time budgets/pricing for fashion vs. wedding vs. headshot retouching (Retouching Academy gives only qualitative ranges for commercial and beauty). Industry pricing pages exist but were not verified.
- Amazon's official help page could not be fetched; the 85% fill / 1000 px / RGB 255 figures come from secondary 2026 seller guides (consistent across several, but not primary). Amazon category-specific rules (apparel on-model, jewelry) not verified.
- Food and architecture genre-specific retouching norms were not researched in depth (no sources gathered).

---

## A2. Product retouching specifics (dust, reflections, labels, color accuracy, shadows)

### Takeaway
Product retouching is dominated by measurable, deterministic targets: exact background value, consistent framing/padding, color matching to the physical product (sRGB delivery), and clean surfaces. Shadow creation and reflection control are typically done with masks/gradients and duplicated-flipped layers rather than generative tools, but I found no high-quality primary source detailing these steps in this session.

### Cited Findings
- Marketplace main images require exact pure white (255,255,255) and "accurate product representation"; slightly off-white values can be flagged by automated compliance. — [SquareShot](https://www.squareshot.com/post/amazon-product-image-dimensions); [Clipping Path Masterly](https://www.clippingpathmasterly.com/resources/amazon-product-image-requirements/) (secondary)
- Catalog consistency: same aspect ratio, padding/product placement, lighting/color temperature and editing treatment across all products. — [SquareShot Shopify guide](https://www.squareshot.com/post/shopify-product-image-requirements)
- Commercial retouching (incl. products, jewelry, cosmetics, food) requires removing all distracting elements and often takes hours per image. — [Retouching Academy](https://retouchingacademy.com/retouching-guidelines-and-considerations/)

### Inferences
- Implementable product checks for an agent:
  - Background purity: fraction of background-mask pixels exactly (255,255,255) — target >= 99% outside the shadow region.
  - Fill ratio: bounding box of non-white pixels / frame along the long side — target ~0.85 (Amazon) and identical +/- a few px across SKUs.
  - Centering/padding consistency across SKUs: std-dev of bbox margins across the set.
  - Color accuracy to physical product: Delta E 2000 between a reference swatch measurement (spectrophotometer or a shot with color checker) and the corresponding retouched region; common working tolerance ~2-3 Delta E00 (tolerance value is industry convention, not verified here).
  - Label straightening: detect label text baseline/edges (Hough lines) and measure residual angle (target < 0.2-0.5 deg; my estimate).
  - Dust: count of small high-contrast specks in a high-pass image within the product mask at 100% zoom tiles.
- Non-generative shadows: (a) "natural" shadow kept from capture on a white sweep, then lifting background to 255 with a luminosity/curves mask that excludes the shadow; (b) drop shadow = product mask, blurred, offset, multiply at low opacity; (c) reflection = flipped duplicate with gradient mask. These are standard practice but unsourced in this session.

### Gaps
- No primary, authoritative source retrieved on jewelry/cosmetics packshot workflows (reflection control with flags/cards, focus stacking for jewelry, label straightening steps, shadow conventions per marketplace). Recommend a follow-up search (e.g., Fstoppers / Retouching Academy commercial category, jewelry retouching tutorials).
- No sourced numeric tolerances for color accuracy in e-commerce (Delta E thresholds) were found.

---

## A3. Landscape specifics (exposure blending, luminosity masks, sky/foreground balance, competition ethics)

### Takeaway
Landscape retouching is tonal rather than cosmetic: exposure blending of brackets and luminosity-mask-targeted local contrast/dodge-burn; ethics rules (e.g., NLPA) allow stacking/blending/panoramas, dust and small-transient-object removal, and standard global/local adjustments, but forbid adding skies/elements, removing significant features, and AI-generated imagery, with RAW verification for finalists.

### Cited Findings
- NLPA allowed: image stacking/averaging and focus stacking for technical quality; exposure bracketing/blending; panoramas including distortions needed for stitching; removal of "small and transient elements" (leaves, twigs, distant cars); removal of dust spots and flares; white balance, exposure, color, contrast, dodging and burning "as long as the 'golden rule' is met"; B&W conversion. — [Natural Landscape Photography Awards rules](https://www.naturallandscapeawards.com/rules)
- NLPA disallowed: adding skies, foregrounds, birds, mist, sun, moon, rainbows (sky replacement); cloning out significant elements such as trees or electricity pylons; "No AI-generated imagery"; finalists must supply RAW files on request or risk disqualification. — [NLPA rules](https://www.naturallandscapeawards.com/rules)
- Luminosity masks are selections derived from the image's own brightness that restrict adjustments to tonal ranges; typical generated sets have Brights 1-6, Darks 1-6, Midtones 1-6 (18 channels); 16-bit variants create 7 levels each (21 masks). — [CaptureLandscapes](https://www.capturelandscapes.com/introduction-to-luminosity-masks/); [Julia Anna Gospodarou guide](https://www.juliaannagospodarou.com/complete-guide-luminosity-masks/) (tutorial sources)
- Exposure blending workflow: a typical three-shot bracket covers highlights, midtones, shadows; luminosity masks blend them for high-contrast scenes such as sunrises/cityscapes. — [Digital Photography School](https://digital-photography-school.com/exposure-blending-using-luminosity-masks-tutorial/); [Fstoppers](https://fstoppers.com/education/how-use-luminosity-masks-landscape-and-cityscape-image-editing-189377)

### Inferences
- An agent's landscape mode should restrict itself to NLPA-compatible operations by default (global tone/color, luminosity-masked local contrast, dust/flare removal, small transient object removal) and log every clone/heal to support "RAW verification"-style auditability.
- Measurable landscape failure modes to check: halos at sky/horizon boundaries (see B2 halo metric), clipped highlights/shadows (% pixels at 0 or 255 per channel), sky/foreground luminance ratio (mean L* sky region vs. foreground; overly flat ratio = "HDR look").

### Gaps
- The exact wording of NLPA's "golden rule" was not captured verbatim (fetch summarized it). Other competitions' rules (e.g., Wildlife Photographer of the Year, Landscape Photographer of the Year) not compared.
- No quantitative research found linking luminosity-mask settings to perceived quality.

---

## B1. General IQA / aesthetic metrics (NIMA, MUSIQ, CLIP-IQA, LAION, Q-Align, TOPIQ, BRISQUE/NIQE): correlation with experts and failure modes

### Takeaway
Generic no-reference metrics are weak, biased proxies for retouching quality: they score global aesthetics/technical distortion, not skin-texture balance or edit faithfulness; aesthetic scorers show fidelity preference (penalizing any perturbation) and cultural/style biases. Use them only as secondary signals or guardrails, not as the main objective.

### Cited Findings
- On AVA aesthetics, TOPIQ-IAA reaches SRCC ~0.790 while zero-shot CLIP-IQA reaches only ~0.338 (pyiqa benchmark, as summarized by search). — [pyiqa benchmark docs](https://iqa-pytorch.readthedocs.io/en/latest/benchmark.html)
- MUSIQ (Google) is a multi-scale transformer that handles native resolution/aspect ratio; SOTA on technical quality datasets (PaQ-2-PiQ, KonIQ-10k, SPAQ) and comparable on AVA. — [Google Research blog](https://research.google/blog/musiq-assessing-image-aesthetic-and-technical-quality-with-multi-scale-transformers/)
- Q-Align (ICML 2024) scores via discrete text-defined levels with an LMM; ArtiMuse (2025) reports consistently better results than Q-Align on aesthetic benchmarks. — [ArtiMuse arXiv 2507.14533](https://arxiv.org/pdf/2507.14533); [Awesome-IQA list](https://github.com/chaofengc/Awesome-Image-Quality-Assessment)
- For face retouching, NIMA and MUSIQ "lack the fine-grained perceptual sensitivity required" and focus on global aesthetics rather than smoothness-texture balance or blemish removal accuracy; BeautyGRPO built a dedicated 5-dimension preference reward instead. — [BeautyGRPO arXiv 2603.01163](https://arxiv.org/html/2603.01163v1)
- Audit of LAION-Aesthetics, PickScore, ImageReward, HPSv2 under pixel-level CIELAB L* skin-lightness shifts: dominant inverted-U — "unaltered images score highest, and perturbations in either direction are penalized" (fidelity preference); synthetic-face audits gave the wrong bias direction vs. 1,470 real faces. — [arXiv 2608.23593](https://arxiv.org/abs/2608.23593)
- LAION-Aesthetics predictor: biased toward particular styles (rates realistic landscapes/cityscapes/portraits from Western and Japanese artists highest; disproportionately high scores for anime/casual snapshots per one summary); aesthetic models lean on low-level features like saturation and do poorly with stylistic/cultural context. — [Algorithmic Gaze audit, arXiv 2601.09896](https://arxiv.org/html/2601.09896v4); [arXiv 2406.09397](https://arxiv.org/html/2406.09397v1) (the "anime" claim came from a search summary; treat as uncertain)
- Pixel-fidelity metrics vs. human edit judgments: PSNR shows "almost no correlation" with judge factors; SSIM ~0.10-0.15 correlation with global consistency; LPIPS best but < 0.35; CLIP score has limited explanatory power — because they reward similarity to the original, whereas good editing is defined by intentional differences. — [Human-Aligned MLLM Judges, arXiv 2602.13028](https://arxiv.org/html/2602.13028v1)

### Inferences
- Treat NR-IQA (MUSIQ/TOPIQ/NIQE/BRISQUE) as "do-no-harm" guardrails: the score after editing should not drop vs. original beyond a tolerance (catches added noise, banding, over-sharpening artifacts), rather than maximizing it (maximizing invites saturation/contrast hacking).
- Because aesthetic scorers show fidelity preference and saturation sensitivity, they can both under-reward legitimate retouching and be gamed; never use a single aesthetic score as RL reward without fidelity/identity constraints.
- Compute metrics per multi-scale tile (e.g., full image downsampled, 2x2, 4x4 tiles at 100%) because MUSIQ-style global scores average away local defects (halos, blotches) that pros judge at 100% zoom.

### Gaps
- No study found that directly measures correlation of NIMA/MUSIQ/CLIP-IQA/Q-Align/TOPIQ with professional retoucher judgments on retouched (as opposed to distorted/generated) photos. This is a real gap in the literature as far as this search could find.
- BRISQUE/NIQE specific behavior on skin-smoothed images not sourced (BeautyGRPO reports NIQE values only: 10.83 vs 11.15).

---

## B2. Retouching-specific metrics (texture retention, blotchiness, halos, skin hue stats, identity, Delta E, SSIM/LPIPS over-edit penalty)

### Takeaway
Research on face retouching converges on a trio: identity preservation (ArcFace/AdaFace cosine), naturalness/texture (frequency-band analysis; NIQE), and region-weighted color fidelity (PPR10K's human-centered PSNR/Delta E and group consistency). Most specific defect metrics (texture ratio, blotchiness maps, halo detectors) must be engineered; they are not standardized benchmarks.

### Cited Findings
- Fine skin texture lives in high-frequency bands while blemishes dominate low-frequency bands (basis for frequency-separation and for band-energy metrics). — [FabSoften (ResearchGate)](https://www.researchgate.net/publication/343275568_FabSoften_Face_Beautification_via_Dynamic_Skin_Smoothing_Guided_Feathering_and_Texture_Restoration)
- ICCV 2025 face retouching uses frequency selection & restoration (spatial-frequency filtering) plus Laplacian-pyramid multi-resolution fusion to remove large blemishes while preserving local fine detail. — [Xu et al., ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Xu_Face_Retouching_with_Diffusion_Data_Generation_and_Spectral_Restorement_ICCV_2025_paper.pdf)
- Identity: MoFRR evaluates biometric veracity by cosine similarity of ArcFace and AdaFace features (plus PSNR/SSIM). BeautyGRPO reports ArcFace similarity 0.952 (FFHQR) and 0.944 (in-the-wild) for its retouching outputs. — [MoFRR ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Liu_MoFRR_Mixture_of_Diffusion_Models_for_Face_Retouching_Restoration_ICCV_2025_paper.pdf); [BeautyGRPO](https://arxiv.org/html/2603.01163v1)
- Over-smoothing is the characteristic failure of learned retouchers: RetouchFormer shows "inaccurate blemish detection, incomplete blemish removal, and excessive smoothing that erases skin texture"; preferred outputs keep "skin texture, pores, natural gloss". — [BeautyGRPO](https://arxiv.org/html/2603.01163v1)
- PPR10K defines human-region-weighted metrics PSNR^HC and Delta E^HC (emphasizing the person mask) and a group-level consistency metric G_l, alongside PSNR and Delta E. — [PPR10K GitHub](https://github.com/csjliang/PPR10K); [arXiv 2105.09180](https://arxiv.org/abs/2105.09180)
- Fine-grained edit evaluation rubrics include Identity Preservation, Unchanged Regions, Global Consistency, Texture and Detail, Color and Lighting, Seamlessness (12 factors total). — [arXiv 2602.13028](https://arxiv.org/html/2602.13028v1)
- MonetGPT reports SSIM 0.90, LPIPS 0.07, PSNR 23.75, histogram intersection 79.50 vs expert targets on Adobe5K (vs Exposure LPIPS 0.14, PSNR 15.12) — i.e., reference-based fidelity metrics are the norm when an expert target exists. — [MonetGPT arXiv 2505.06176](https://arxiv.org/html/2505.06176v1)

### Inferences (engineering proposals for an agent's self-check; thresholds are my estimates, to be calibrated)
- Texture/pore retention ratio (per skin tile at 100%): R_tex = E_hf(after) / E_hf(before), where E_hf = energy of a band-pass (e.g., Laplacian-pyramid level 1-2 or DoG sigma ~0.5-2 px at native res) inside the skin mask excluding blemish masks. Portrait/headshot: target ~0.85-1.0; beauty: ~0.7-0.95; < 0.6 flags "plastic skin". R_tex > 1.15 flags over-sharpening/grain injection.
- Blotchiness map: local std of L* after low-pass (sigma ~ 1-3% of face width) within skin mask; compare the 95th percentile before/after; D&B should reduce low-frequency variance while R_tex stays ~1.
- Halo detector: along edges detected in the original (Canny on L*), sample L* profiles perpendicular to the edge in the edited image; overshoot beyond both plateaus > ~3-5 L* units across a band wider than ~2-3 px = halo. Run per tile; flag sky/horizon tiles in landscape mode.
- Skin tone statistics: in CIELAB/LCh over the skin mask, track mean hue angle h, chroma C*, and their spread (IQR); excessive spread = blotchy color; a shift of mean Delta E00 > ~3 vs. original without instruction = unintended tone change. Use group-level spread of these stats across a set (PPR10K-style G_l idea) for wedding/series consistency.
- Identity guard: ArcFace cosine(original, edited) — research outputs reach ~0.94-0.95 even with generative retouching; a parametric pipeline should sit higher (proposed alarm < 0.95; unverified threshold).
- Over-edit penalty: LPIPS/SSIM vs. original measured on non-target regions (background, hair, eyes) should stay near identity (e.g., LPIPS < ~0.02-0.05 there); whole-image LPIPS vs original is only a soft budget, since good edits are intentional differences (per arXiv 2602.13028).
- Clipping/banding checks: % pixels at 0/255 per channel before vs after; histogram gaps/comb in 8-bit export (banding), especially in skies and gradients.

### Gaps
- No standardized, published "texture retention ratio" or "blotchiness index" with validated thresholds was found; above formulas are proposals.
- Exact formulas and numeric results for PPR10K's PSNR^HC / Delta E^HC / G_l were not retrieved (CVF PDF returned 403; README lacks the table).
- No sourced halo-detection metric specific to retouching was found.

---

## B3. Parametric / white-box automatic retouching research (what worked, limitations)

### Takeaway
The field moved from (1) differentiable white-box filters + RL (Exposure, 2018) and (2) fast learned color transforms (3D LUTs, CSRNet, RSFNet) trained on FiveK/PPR10K, to (3) 2025-2026 MLLM agents that plan and set Lightroom-like parameters (MonetGPT, PhotoArtAgent, JarvisArt, PerTouch, JarvisEvo). Key lessons: off-the-shelf MLLMs are poor at choosing parameters without operation-aware training; staged ordering (light -> color -> per-hue) helps; closed-loop evaluate-and-revise improves results; static external reward models get hacked.

### Cited Findings
- Exposure (Hu et al., ACM TOG 2018/SIGGRAPH): resolution-independent differentiable filters; deep RL chooses the next operation and its parameters given the current image; trained on unpaired data (a photo collection exhibiting the desired style), via GAN-style objective. — [arXiv 1709.09602](https://arxiv.org/pdf/1709.09602); [GitHub](https://github.com/csjunxu/exposure)
- Image-adaptive 3D LUT (Zeng et al., TPAMI 2020): learns several basis 3D LUTs + a small CNN predicting fusion weights; PSNR 25.21 dB on FiveK; < 600K parameters; < 2 ms for a 4K image on a Titan RTX. — [HuiZeng/Image-Adaptive-3DLUT](https://github.com/HuiZeng/Image-Adaptive-3DLUT); [PAMI paper](https://www4.comp.polyu.edu.hk/~cslzhang/paper/PAMI_LUT.pdf)
- PPR10K: 1,681 groups / 11,161 raw portrait photos, each retouched by three experts; human-region masks; goals: human-region priority (HRP) and group-level consistency (GLC); splits 8,875 train / 2,286 val; 360p training images available. — [arXiv 2105.09180](https://arxiv.org/abs/2105.09180); [GitHub](https://github.com/csjliang/PPR10K)
- PPR10K baselines (as reported in a follow-up paper via search summary): HDRNet ~23.93-24.08 dB, CSRNet ~22.72-23.76, 3D LUT ~24.70-25.64 across expert a/b/c; follow-up pixel-adaptive method 24.82-25.72. — [Wang et al., arXiv 2112.03536](https://arxiv.org/pdf/2112.03536) (numbers from search snippet; verify)
- RSFNet (ICCV 2023): white-box via linear sums of region-specific color filters predicted with region maps (K=10 for FiveK, 16 for PPR10K); beats other white-box methods (e.g., Harmonizer) on PSNR/SSIM with faster inference; strong on "zeroed as-shot" inputs needing large temperature/hue changes. — [RSFNet ICCV 2023](https://openaccess.thecvf.com/content/ICCV2023/papers/Ouyang_RSFNet_A_White-Box_Image_Retouching_Approach_using_Region-Specific_Color_Filters_ICCV_2023_paper.pdf); [GitHub](https://github.com/Vicky0522/RSFNet)
- MonetGPT (SIGGRAPH 2025, TOG): 33 procedural ops in three ordered stages — (1) lighting: blacks, contrast, exposure, highlights, whites, shadows; (2) saturation, temperature, tint; (3) per-color hue/saturation/luminance over 8 ranges; parameters on a perceptually linear [-100,+100] scale. Trained with three "puzzles" (A: identify op+value from a pair; B: rank 4 perturbed variants vs expert edit and estimate correction; C: plan full sequence with <Adjustment, Issue, Solution> reasoning) built from PPR10K (~7K/5K/13K samples). Finding: current MLLMs "perform poorly when queried directly" for procedural ops; direct fine-tuning without puzzles overfit. Limitations: global ops only, artist bias from ~8K images, ~25 s inference. — [arXiv 2505.06176](https://arxiv.org/html/2505.06176v1); [GitHub](https://github.com/niladridutt/monetGPT)
- PhotoArtAgent (2025): VLM does explicit artistic analysis, outputs Lightroom parameters via API, then evaluates the result and proposes new parameters iteratively, explaining rationale; reported to beat prior methods in user studies and be comparable to professional artists. — [arXiv 2505.23130](https://arxiv.org/abs/2505.23130)
- JarvisArt (NeurIPS 2025): MLLM agent orchestrating 200+ Lightroom tools, scene- and region-level edits; CoT SFT then GRPO-R RL; Agent-to-Lightroom (A2L) protocol; MMArt dataset. — [arXiv 2506.17612](https://arxiv.org/pdf/2506.17612); [GitHub](https://github.com/LYL1015/JarvisArt)
- JarvisEvo (arXiv 2511.23002, Qwen3-VL-8B base): SFT on 150K samples, then Synergistic Editor-Evaluator Policy Optimization (SEPO), then reflection fine-tuning (5K); interleaved multimodal CoT; up to 4 editing steps. On ArtEdit-Bench (English subset) vs JarvisArt: L1 7.82 vs 13.21, L2 12.45 vs 38.45, overall 8.77 vs 7.89; vs Nano-Banana (generative) L1 7.82 vs 11.54. Its evaluator: SRCC 0.724 / PLCC 0.712 vs human, above Gemini-2.5-Flash (0.619) and Qwen3-VL (0.571). Human preference win rate 49% vs Nano-Banana 28%. — [arXiv 2511.23002](https://arxiv.org/html/2511.23002v2)
- PerTouch (2025): diffusion-based but parameter-map controlled — 4 attributes (colorfulness, contrast, color temperature, brightness) per semantic region in [-1,1]; VLM agent maps weak ("optimize this") vs strong instructions (with detection + SAM); scene-aware memory of past user parameters for personalization; "feedback-driven rethinking" loop; evaluated on FiveK's 5 expert styles. — [arXiv 2511.12998](https://arxiv.org/html/2511.12998v2) (note: not purely parametric; render stage is generative)

### Inferences
- For a non-destructive agent: copy MonetGPT's ordering (global light -> WB/saturation -> HSL), JarvisEvo/PhotoArtAgent's critic loop, and RSFNet/PerTouch's region-map idea (apply parametric adjustments through semantic masks: skin, sky, background).
- Expected attainable fidelity vs a given expert on FiveK/PPR10K-style data is only ~24-26 dB PSNR even for strong models; style ambiguity across experts is large, so the agent should not chase a single "correct" answer — it should satisfy constraints + a preference/critic signal.

### Gaps
- Not verified this session (background knowledge only, treat as unconfirmed): CSRNet (He et al., ECCV 2020, ~37K params, conditional sequential retouching via 1x1 convs + condition vector); Deep Preset (Ho et al., WACV 2021, learning color style/preset transfer); Distort-and-Recover (Park et al., CVPR 2018, DQN for color enhancement trained by distorting good images); MIT-Adobe FiveK (Bychkovsky et al., CVPR 2011; 5,000 RAW images, 5 experts A-E, expert C commonly used). Numbers should be re-checked before citing.
- JarvisArt's own quantitative results (MMArt-Bench numbers) not extracted.

---

## B4. VLMs as evaluators/critics for image editing: reliability, biases, mitigation

### Takeaway
MLLM judges reach moderate agreement with humans (best SRCC ~0.6-0.72 on photo-editing aesthetics; >80% within +/-1 on a 7-point scale per factor), but are lenient (score inflation), compress scores to the middle, are strongly order-sensitive in pairwise mode (up to 60.9% reversals), swayed by irrelevant visual cues and fabricated "majority" opinions, and are exploitable as static RL rewards. Mitigate with order-swapped pairwise + ties, calibrated pointwise anchors, deterministic defect metrics, zoomed crops, and evaluators trained/co-evolved on human labels.

### Cited Findings
- JarvisEvo: a static Gemini-2.5-Pro reward worked early but was later hacked — "self-predicted scores continue to increase" while editing quality degraded; removing the evaluator loop made self-evaluation scores rise while pairwise preference rewards declined; co-evolving the evaluator with human-annotated calibration and pairwise win-rate rewards fixed it. Biases listed for static judges: bandwagon, beauty effect, self-preference, solution fixation. — [arXiv 2511.23002](https://arxiv.org/html/2511.23002v2)
- EditJudgeBias (arXiv 2610.01670): 5 MLLM judges, 1,196 real editing samples, 13 injected quality-preserving cues; swapping candidate order reverses up to 60.9% of pairwise decisions; fabricated majority opinions raise ratings; irrelevant visual elements shift judgments more than whole-image manipulations; edit-region cues reduce human agreement; robustness needs 3 views (cue invariance, human agreement, pairwise stability) measured against each judge's own noise floor. — [arXiv 2610.01670](https://arxiv.org/abs/2610.01670)
- Human-aligned fine-grained judges (arXiv 2602.13028): 12-factor rubric; judge-human MAE 0.63-1.29 on a 7-point scale, >80% agreement within +/-1 for most factors; but Pearson only ~0.34-0.36 on the best factors; judges more lenient (mean 6.24 vs human 5.65); simple minimal prompt outperformed elaborate factor rubrics and example-guided prompts; GPT-5-mini aligned better than Gemini-2.5-Pro on most factors. — [arXiv 2602.13028](https://arxiv.org/html/2602.13028v1)
- General MLLM-as-judge: GPT-4V approaches human concordance mainly in pairwise comparison when ties are allowed; in scoring, MLLMs over-populate the middle of the scale and fail to penalize poor outputs. — [EmergentMind summary of MLLM-as-a-Judge](https://www.emergentmind.com/topics/mllm-as-a-judge-mechanism) (aggregator; original is Chen et al. 2024 MLLM-as-a-Judge)
- Pairwise protocols are more vulnerable to distractor features (preferences flip in ~35% of cases) whereas absolute scoring is more robust to manipulation (text-LLM study). — [arXiv 2504.14716](https://arxiv.org/abs/2504.14716)
- Off-the-shelf MLLMs perform poorly at directly proposing procedural retouching parameters (motivating MonetGPT's puzzle training — Puzzle B is effectively a critic task: rank perturbed variants and estimate the correction). — [MonetGPT](https://arxiv.org/html/2505.06176v1)

### Inferences (critic-loop design)
- Use a hybrid critic: deterministic metrics (B2) as hard gates -> VLM as rubric judge only on what metrics can't see (intent, taste, naturalness).
- Pairwise with both orders (A/B and B/A), allow "tie", accept only order-consistent verdicts; treat inconsistency as "no significant difference".
- Pointwise scoring anchored with reference exemplars (good/over-edited/under-edited of the same image) to counter middle-of-scale compression.
- Multi-scale tiles: feed the full frame (composition/global tone) plus 100% crops of skin, eyes, edges/horizon, background; ask defect-specific questions per crop ("is pore texture visible?", "any halo along this edge?").
- Helper/check layers to amplify defects for the VLM (common pro practice, unsourced here): high-pass/frequency map for texture, a "solarize"/high-contrast curve or B&W luminosity view for D&B blotches, saturation map for color blotches, difference image vs original for over-editing scope.
- Never give the judge the editor's rationale or claims ("experts preferred this") — fabricated majority cues inflate scores (EditJudgeBias).
- Keep a held-out human-labeled set to monitor judge drift; if critic score rises while metric gates/human spot checks degrade, it's reward hacking (JarvisEvo signal).

### Gaps
- No study found that specifically tests helper/check layers (solarize curves, frequency maps) as VLM inputs; ensembles of judges for photo retouching specifically not found.
- Judge reliability specifically on subtle parametric retouches (small tone differences) vs. generative edits is under-studied; most benchmarks are instruction-based generative editing.

---

## B5. Preference learning / "taste" modeling from before-after pairs

### Takeaway
Style/taste is learned either (a) per-expert supervised mappings (FiveK 5 experts, PPR10K 3 experts — separate models per style), (b) unpaired style collections (Exposure), (c) memory of a user's past parameter choices conditioned on scene (PerTouch), or (d) pairwise-preference reward models trained with VLM-assisted plus human-verified labels (BeautyGRPO's FRPref-10K) and used for GRPO-style RL.

### Cited Findings
- PPR10K: each photo has three independent expert retouches; pretrained models are released per expert (a, b, c); expert-specific PSNRs differ by up to ~1 dB for the same method, indicating distinct styles. — [PPR10K GitHub](https://github.com/csjliang/PPR10K); [arXiv 2112.03536](https://arxiv.org/pdf/2112.03536)
- Exposure learns a retouching style from an unpaired set of photos the user likes. — [arXiv 1709.09602](https://arxiv.org/pdf/1709.09602)
- PerTouch: scene-aware memory stores editing parameters with scene semantics and samples control values from a learned conditional distribution for new images (long-term personalization). — [arXiv 2511.12998](https://arxiv.org/html/2511.12998v2)
- BeautyGRPO: FRPref-10K preference pairs labeled by GPT-4o, Qwen2.5-VL-72B, Gemini 2.5 Pro then audited by trained annotators with senior expert arbitration, across 5 dimensions (skin smoothing, blemish removal, texture quality, clarity, identity preservation); reward model trained in 3 stages (SFT on 2K reasoning samples, self-training with consistency filtering on 8K, GRPO with outcome+process rewards); 63.25% user-study win rate vs. 6.5-12% for competitors. — [arXiv 2603.01163](https://arxiv.org/html/2603.01163v1)
- JarvisEvo uses pairwise win-rate rewards among trajectories to amplify reward variance and resist superficial optimization. — [arXiv 2511.23002](https://arxiv.org/html/2511.23002v2)

### Inferences
- For per-retoucher taste: store (image features/scene tags, parameter vector, accepted/rejected) tuples; fit a lightweight preference model (Bradley-Terry over parameter deltas, or kNN over scene embeddings like PerTouch) and use it to initialize parameters, leaving the critic loop for refinement.
- Encode genre (A1) as a conditioning variable in the taste model — the same retoucher applies different skin-texture targets for headshots vs beauty.

### Gaps
- No published dataset of pairwise preferences over parametric (slider-level) retouch variants by professionals was found (BeautyGRPO is generative face retouching; MonetGPT puzzle B is synthetic perturbation, not human preference).
- How many before/after pairs are needed to capture an individual's style reliably was not found.
