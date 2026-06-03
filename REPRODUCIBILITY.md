---
name: coastal-tracer-transport-paper
description: Reproduce the expert-guided study "A bound-preserving high-resolution compact scheme for tracer transport in coastal and ocean models" — build & calibrate a mixed-tide San Francisco Bay hydrodynamic model on real CRM bathymetry, run the bound-preserving compact vs upwind transport comparison, generate all figures, and assemble the Ocean Engineering manuscript. Use when asked to rebuild, extend, or reproduce this paper or its SF Bay tidal-current model.
---

# Coastal tracer-transport paper — reproducible workflow

This skill encodes the **prompt-driven, expert-in-the-loop workflow** that produced the
paper. It is both a reproduction protocol and the documentation of the human–AI method
that is itself a contribution of the paper. Each "PROMPT" line is the kind of
natural-language instruction that drove the step; each "EXPERT CONSTRAINT" is a
non-negotiable physical requirement the domain expert imposed (and that an LLM left
unguided got wrong at least once — see §Expert corrections).

Working dir: `compact-advection-diffusion/paper/`.
Run Python with `uv run --with numpy --with scipy --with matplotlib python3 <script>`
(DEM fetch additionally needs `--with netcdf4`; symbolic checks `--with sympy`).
Numerics dev modules live in `compact-advection-diffusion/_dev/`.

## 0. Scientific framing (fix this first, it governs everything)
- Honest positioning: the **bound-preserving compact method is published** (Li, Xie &
  Zhang 2018, SINUM 56:3308). The contribution is the **coastal/ocean application** +
  the comparison against the 3rd-order upwind of Sankaranarayanan, Shankar & Cheong
  (1998), the deformational benchmark, and a calibrated mixed-tide SF Bay field.
- Second contribution: the **expert-guided LLM workflow** (this file).
- Do NOT claim method novelty; do NOT claim an oil-spill hindcast.

## 1. Numerics (deformational benchmark)
- PROMPT: "implement a 4th-order compact (Padé) 1st/2nd derivative with a STABLE
  no-flux closure, RK4, on the LeVeque deformational flow; make it bound-preserving."
- Compact-4 first derivative: `¼f'_{i-1}+f'_i+¼f'_{i+1} = (3/2)(f_{i+1}-f_{i-1})/2h`.
  EXPERT CONSTRAINT: impose Neumann `f'=0` at walls (NOT Lele one-sided extrapolation,
  which is unstable here).
- Bound-preserving: a-posteriori FCT blend of the compact RK4 update toward a
  first-order upwind update via a per-node DMP θ-limiter (`_dev/bp_compact.py`).
- Compare 1st-order upwind, 3rd-order upwind (OE-1998), plain compact, bp-compact on a
  Zalesak slotted cylinder. Verify with `sympy_proofs.py`. Figures: `gen_plots.py`.

## 2. San Francisco Bay bathymetry (real DEM)
- PROMPT: "use a fine grid on real bathymetry, otherwise the transport is wrong."
- Fetch NOAA Coastal Relief Model Vol.7 (3 arc-sec) over lon −122.70…−121.95,
  lat 37.40…38.25 via OPeNDAP `https://www.ngdc.noaa.gov/thredds/dodsC/crm/crm_vol7.nc`
  (indices x[6360:7261], y[480:1501]).
- `build_sfbay_fine.py`: regrid to a uniform **200 m** mesh; flood-fill keep
  Pacific-connected water; resolves the ~90 m Golden Gate strait.

## 3. Mixed-tide hydrodynamic model (the key physics)
- PROMPT: "SF Bay is a mixed (diurnal + semidiurnal) tide — account for it."
- `gen_currents_mixed.py`: vectorized semi-implicit **Casulli (1990)** θ-method solver
  (one production run records all station currents).
- EXPERT CONSTRAINTS (all required, all were corrections at some point):
  1. **Mixed tide**: force 6 constituents M2,S2,N2,K1,O1,P1 at the Pacific boundary
     with amplitudes/phases from **NOAA Golden Gate station 9414290**
     (mdapi `.../stations/9414290/harcon.json`). NOT M2-only.
  2. **Physical minimum depth HMIN = 2–3 m** (NOT 10 m — unphysical).
  3. **No drying / stability**: depth-dependent **Manning** drag
     `Cd = g n²/H^(1/3)`, n=0.037 (Cd≈0.003 at the Gate matching 2003; ≈0.009 on
     shoals) + a Rayleigh **sponge** (RMAX 6e-3/s south of ~37.76°N) to damp the
     South Bay resonance. Verify `max|η| < HMIN` (no cell dries).
  4. **Keep the full bay** (do NOT trim South Bay — it holds the tidal prism that
     drives the Gate current; trimming drops the Gate current from ~1.0 to ~0.7 m/s).
- Calibration procedure: two short single-constituent runs give per-band gains;
  offshore amp = NOAA_amp / gain × SD_CORR (1.10 restores M2 lost to quadratic-drag
  coupling). See `CALIBRATION.md`.

## 4. Validation targets (must hit before accepting the field)
- Golden Gate M2 surface elevation ≈ 0.58 m (NOAA 0.576); S2 ≈ 0.14; O1 ≈ 0.22.
  Form factor (K1+O1)/(M2+S2) ≈ 0.9 → mixed. (N2/K1/P1 not separable in ~16 d.)
- Golden Gate M2 current ≈ 0.96 m/s (obs 1.1, within the 0.2 m/s error of
  Sankaranarayanan & French McCay 2003); Oakland ≈ 0.5 (obs 0.6).
- Wet/dry: max surface depression < HMIN (e.g. 2.7 m < 3 m → min column 0.3 m > 0).
- Figures: `sfbay_tides_fig.py` (diurnal inequality), `sfbay_currents_fig.py`
  (4-station currents, ONE simulation), `sfbay_domain.py` (flood/ebb bathymetry +
  landmarks), `sfbay_transport.py` (5-scheme transport, computes + renders).

## 5. Honest scope (enforce in the text)
- EXPERT CONSTRAINT: the SF Bay case is a **transport-scheme demonstration in a
  calibrated tidal field, NOT a Cosco Busan oil-spill hindcast**. The real slick was
  wind-driven (windage ~3% + Stokes drift) + weathering; the Nov 2007 winds are not
  included. Cite NOAA OR&R + Incardona et al. (2012, PNAS & PLoS ONE) for spill
  context; GNOME (Beegle-Krause 2001) as the operational trajectory tool.
- Cosco Busan NRDA data (SCAT shoreline oiling) is in NOAA DIVER/ERMA — usable only
  for a qualitative overlay, not quantitative validation.

## 6. Manuscript
- `manuscript.tex` (elsarticle, `authoryear`/`elsarticle-harv`, needs `amsmath,
  amssymb,graphicx,booktabs,algorithm,algpseudocode,xcolor`). Compile with `tectonic`.
- Must include: full formulations (compact family + order conditions, 2nd-deriv,
  explicit upwind eqs, Algorithm 1 limiter box), resolution analysis, convergence,
  deformational benchmark + table, SF Bay application (mixed-tide figs + validation
  tables), a numbered **"An expert-guided LLM workflow"** section, and an **AI-use
  disclosure** (Claude Opus 4.8).

## Expert corrections (the heart of the workflow contribution)
Record/preserve these — they show domain knowledge governed the outcome:
1. single-constituent M2 → six-constituent **mixed** tide;
2. unphysical HMIN=10 m → physical 2–3 m + Manning friction + sponge (no drying);
3. coarse grid over-concentrating the Gate → strait-resolving 200 m grid;
4. trimming South Bay (killed the prism) → keep the full bay;
5. implied oil-spill hindcast → honest tracer-transport demonstration (+ wind caveat);
6. wrong shoreline figure / missing spill citations → corrected against NOAA + literature.

## Reproduce end-to-end
```
uv run --with netcdf4 --with numpy python3 fetch_crm.py        # (one-time DEM fetch)
uv run --with numpy --with scipy python3 build_sfbay_fine.py    # 200 m grid
uv run --with numpy --with scipy python3 gen_currents_mixed.py  # calibrated mixed-tide field (one run)
uv run --with numpy --with scipy --with matplotlib python3 sfbay_tides_fig.py
uv run --with numpy --with scipy --with matplotlib python3 sfbay_currents_fig.py
uv run --with numpy --with scipy --with matplotlib python3 sfbay_domain.py
uv run --with numpy --with scipy --with matplotlib python3 sfbay_transport.py
uv run --with numpy --with scipy --with matplotlib python3 gen_plots.py    # benchmark figs
tectonic manuscript.tex
```
Acceptance: Gate elevation/current within tolerance (§4), no cell dries, all figures
regenerated, manuscript compiles with 0 undefined citations.
