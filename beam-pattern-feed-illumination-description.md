# Beam Pattern Depends on Feed Illumination

This HTML is a standalone teaching visualization for reflector antennas. It now combines two linked lessons:

- feed taper changes the reflector beam pattern,
- beam dilution controls how much of a realistic radio source becomes antenna temperature.

The page is intentionally styled after the `calwidget_html` frontend: a cool Apple-like toolbar, glass panels, a fixed-width control rail, and a scrollable analysis wall with plot-first cards.

## Teaching point

- Uniform illumination gives the narrowest beam but stronger sidelobes.
- Taper softens the dish edge, lowers sidelobes, and broadens the main beam because the effective diameter shrinks.
- Extended sources do not couple like point sources.
- The Sun remains bright enough to give kilokelvin antenna temperatures on an EOVSA-sized dish even when the beam is not fully filled.
- Weak calibrators remain tiny compared with `Tsys ~ 100 K`, which motivates using a larger dish for calibration.

## Page structure

- Toolbar:
  - source selector
  - 3D feed/system beam mode selector
  - dish preset buttons for `2.1 m`, `10 m`, and `27 m`
- Left control rail:
  - page summary and key equations
  - taper preset buttons
  - sliders + numeric inputs for edge taper, dish diameter, and wavelength
  - live beam metrics
  - current-source explanation and lecture reference note
- Right analysis wall:
  - side-by-side 3D scenes for uniform and tapered illumination
  - beam-cut plot comparing uniform and tapered cases
  - source-coupling plot with beam, source disk, and beam-times-source product

## Source catalog

The source selector uses five pedagogical cases:

- `quiet_sun`
  - fixed `32 arcmin` disk
  - brightness temperature from a lecture-fit microwave curve anchored to the `10^4-10^5 K` range
- `taurus_a`
  - fixed `9 arcmin` equivalent disk
  - Perley-Butler 2017 polynomial flux model
- `virgo_a`
  - fixed `16 arcmin` equivalent disk
  - Perley-Butler 2017 polynomial flux model
- `cygnus_a`
  - fixed `2 arcmin` equivalent disk
  - Perley-Butler 2017 polynomial flux model
- `cal_20jy`
  - unresolved `20 Jy` calibrator tied directly to the lecture text

For the PB17 sources, the polynomial is clipped to the published validity range when the selected wavelength moves outside that source's recommended GHz interval.

## Numerical model

### Beam model

- The aperture illumination is radial over a circular dish.
- Uniform illumination uses constant amplitude.
- Tapered illumination uses a smooth edge falloff set by the edge taper in dB.
- The beam cut comes from a sampled radial transform with a `J0` kernel.
- `Deff` is inferred from illumination efficiency and is used for the lecture-style point-source conversion.

### Source model

- Extended sources are treated as circular uniform disks.
- For the Sun, the page starts from a brightness-temperature model and derives flux density from disk size.
- For Taurus A, Virgo A, and Cygnus A, the page starts from total flux density and derives a uniform equivalent `Tb`.
- The `20 Jy` calibrator is treated as a point source.

### Antenna temperature model

- Point-source reference:
  - the page explicitly preserves the lecture convention
  - `1 Jy` on a `10 m` dish is presented as about `0.05 K`, which preserves the intended classroom-scale comparison quoted in the lecture text
- Extended sources:
  - `Ta` is computed from the tapered radial beam profile through an axisymmetric beam-disk overlap integral
  - the coupled temperature is `Tb` times the fraction of the beam solid angle that falls on the source
- The source-coupling plot shows:
  - tapered beam profile
  - source top-hat disk profile
  - shaded `beam × source` region whose integral drives the coupling result

## What should be reviewed

- Whether the `calwidget_html`-style reskin feels consistent with the rest of the teaching visualizations.
- Whether the source-coupling panel makes the weak-calibrator versus quiet-Sun contrast obvious within a few seconds.
- Whether the `2.1 m`, `10 m`, and `27 m` presets produce the intended classroom comparisons.
- Whether the quiet-Sun case remains in the intended `Ta ~ 10^3 K` regime for EOVSA-like settings.
- Whether any PB17 clipping note or source annotation needs to be made more explicit for students.
