# Bound-preserving compact tracer transport in coastal and ocean models

Code and reproducibility materials for the manuscript:

> **Bound-preserving compact tracer transport in coastal and ocean models: a case
> study in expert-guided large-language-model (Claude Opus 4.8) scientific computing**
> — S. Sankaranarayanan (submitted to the *Journal of Computing in Civil Engineering*, ASCE).

The paper makes two contributions:

1. **A computational contribution** — a bound-preserving high-resolution compact
   (Padé) finite-difference scheme (limiter method from Li, Xie & Zhang 2018) applied
   to scalar/tracer transport in coastal and ocean flows, verified on the LeVeque
   deformational-flow benchmark and demonstrated on a **calibrated mixed-tide San
   Francisco Bay model**.
2. **A methodological contribution** — a documented, reproducible **expert-in-the-loop
   large-language-model workflow** for building and validating the model. The workflow,
   including the physical errors the expert corrected, is recorded in
   [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

This is a transport-scheme demonstration in an observationally-calibrated tidal field,
**not** a hindcast of the 2007 Cosco Busan oil spill (which is wind- and
weathering-driven).

## Requirements
Python 3 with `numpy`, `scipy`, `matplotlib` (and `netcdf4` for the bathymetry fetch).
The scripts were run with [`uv`](https://docs.astral.sh/uv/):

```
uv run --with numpy --with scipy --with matplotlib python3 <script>.py
uv run --with netcdf4 --with numpy python3 fetch_crm.py   # bathymetry fetch
uv run --with sympy python3 sympy_proofs.py               # symbolic verification
```

## Reproduce end to end
From `paper/`:
```
uv run --with netcdf4 --with numpy            python3 fetch_crm.py            # NOAA CRM bathymetry subset
uv run --with numpy --with scipy              python3 build_sfbay_fine.py     # 200 m grid
uv run --with numpy --with scipy              python3 gen_currents_mixed.py   # calibrated mixed-tide field (one run)
uv run --with numpy --with scipy --with matplotlib python3 sfbay_tides_fig.py
uv run --with numpy --with scipy --with matplotlib python3 sfbay_currents_fig.py
uv run --with numpy --with scipy --with matplotlib python3 sfbay_domain.py
uv run --with numpy --with scipy --with matplotlib python3 sfbay_transport.py
uv run --with numpy --with scipy --with matplotlib python3 gen_plots.py       # benchmark figures
tectonic manuscript_asce.tex                                                   # build the manuscript
```
Acceptance: Golden Gate M₂ elevation ≈ 0.58 m and current ≈ 0.96 m/s (within the error
of the validated model of Sankaranarayanan & French McCay 2003); no cell dries; all
figures regenerate; the manuscript compiles. See [`paper/CALIBRATION.md`](paper/CALIBRATION.md).

## Data sources (public)
- Bathymetry: NOAA NCEI **Coastal Relief Model**, Vol. 7 (3 arc-second), via OPeNDAP.
- Tidal harmonic constants: NOAA **Tides & Currents**, station **9414290** (San Francisco).

Generated `.npz` data files (including the ~46 MB current field) are **not** committed;
they regenerate from the pipeline above.

## Repository layout
```
paper/        manuscript source (manuscript_asce.tex, references.bib), CALIBRATION.md,
              figure/model scripts, figures/
_dev/         numerical-scheme modules (advdiff.py, compact_stable.py, bp_compact.py, sharp.py)
REPRODUCIBILITY.md   the expert-guided workflow (prompts, expert constraints, validation targets)
```

## Note on paths
For transparency this initial release keeps the scripts as run; the `DEV`/`OUT` path
constants at the top of each script are absolute and should be edited for your machine
(a portable, relative-path version is planned).

## License
Code released under the MIT License (see `LICENSE`). The input datasets are public NOAA
products. Copyrighted journal articles are **not** included.

## AI-use disclosure
This study was carried out using the large language model **Claude Opus 4.8**
(Anthropic) as an implementation and drafting assistant, under the direction, review,
and full responsibility of the author. The model is a tool, not an author. See the
manuscript's disclosure and the "expert-guided LLM workflow" section.
