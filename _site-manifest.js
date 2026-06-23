window.PHYS681_SITE_MANIFEST = {
  "collection": {
    "title": "NJIT PHYS 681 Spring 2026: Solar Physics and Instruments Teaching Visualizations",
    "version": "v1.0.0",
    "date": "2026-04-28",
    "course": "NJIT PHYS 681 Spring 2026",
    "doi": "10.5281/zenodo.20820901",
    "doi_url": "https://doi.org/10.5281/zenodo.20820901",
    "concept_doi": "10.5281/zenodo.20820901",
    "concept_doi_url": "https://doi.org/10.5281/zenodo.20820901",
    "version_doi": "10.5281/zenodo.20820902",
    "version_doi_url": "https://doi.org/10.5281/zenodo.20820902",
    "zenodo_record": "https://zenodo.org/records/20820902",
    "author": "Sijie Yu; Codex; Claude Code",
    "authors": [
      {
        "name": "Sijie Yu",
        "role": "Assistant Professor",
        "affiliation": "NJIT"
      },
      {
        "name": "Codex"
      },
      {
        "name": "Claude Code"
      }
    ],
    "description": "A subset of the NJIT PHYS 681 Spring 2026 Solar Physics and Instruments teaching materials, containing interactive static HTML visualizations and narrative notes for solar physics, emission, propagation, interferometry, and instrumentation topics."
  },
  "modules": [
    {
      "id": "emission-propagation",
      "title": "Emission and Propagation",
      "description": "Radiometry, transfer, propagation, and radio emission mechanisms."
    },
    {
      "id": "interferometry-instrumentation",
      "title": "Radio Interferometry and Instrumentation",
      "description": "Interferometric measurement, Fourier imaging, polarization, receivers, antennas, and instrument data paths."
    }
  ],
  "pages": [
    {
      "filename": "html/emission-mechanism-explorer-narratives.html",
      "title": "Lecture Narrative: Emission Mechanisms",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Connect radio observables, transfer, propagation, and emission mechanisms into a coherent lecture narrative.",
      "prereqs": "Basic radiative transfer and plasma frequency concepts",
      "expected_minutes": 90,
      "narrative_anchor": "#",
      "dependencies": [
        "emission-mechanism-explorer-narratives_files",
        "emission-mechanism-explorer-narratives.pdf",
        "figures/explorer-screenshots"
      ],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/gyro-ensemble-spectrum-razin.png",
      "group": "Course Guide"
    },
    {
      "filename": "html/specific-intensity-flux-density.html",
      "title": "Radiometry: Specific Intensity and Flux Density",
      "module": "emission-propagation",
      "tier": "B",
      "learning_goal": "Distinguish brightness, solid angle, flux density, Jansky units, and brightness temperature.",
      "prereqs": "Solid angle, inverse-square dilution",
      "expected_minutes": 12,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#specific-intensity-and-flux-density-explorer",
      "dependencies": [],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/specific-intensity-line-of-sight.png",
      "group": "Foundations"
    },
    {
      "filename": "html/radio-transfer-mechanisms.html",
      "title": "Radiative Transfer: Emission, Absorption, and Brightness",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Show how emissivity, opacity, source function, and background radiation produce observed brightness temperature.",
      "prereqs": "Specific intensity, optical depth",
      "expected_minutes": 15,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#radio-transfer-mechanisms-explorer",
      "dependencies": [],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/radio-transfer-brightness-temperature.png",
      "group": "Foundations"
    },
    {
      "filename": "html/magnetoionic-propagation.html",
      "title": "Magnetoionic Propagation: X/O Modes and Cutoffs",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Explain x/o mode propagation, cutoff, stopbands, refractive index, and polarization in a magnetized plasma.",
      "prereqs": "Plasma frequency, cyclotron frequency, wave polarization",
      "expected_minutes": 18,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#magnetoionic-propagation-explorer",
      "dependencies": [],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/magnetoionic-wave-propagation.png",
      "group": "Foundations"
    },
    {
      "filename": "html/bremsstrahlung-explorer.html",
      "title": "Free-Free Emission: Bremsstrahlung",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Connect Coulomb acceleration, thermal free-free emissivity, and thick-thin radio transfer.",
      "prereqs": "Coulomb force, Maxwellian distribution, optical depth",
      "expected_minutes": 20,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#bremsstrahlung-explorer",
      "dependencies": [],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/bremsstrahlung-thermal-emissivity.png",
      "group": "Incoherent Emission"
    },
    {
      "filename": "html/gyro-emission-explorer.html",
      "title": "Gyro Emission: Cyclotron to Gyrosynchrotron",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Relate single-electron gyro motion, beaming, harmonics, ensemble spectra, opacity, and Razin suppression.",
      "prereqs": "Lorentz factor, cyclotron frequency, pitch angle",
      "expected_minutes": 25,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#gyro-emission-explorer",
      "dependencies": [],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/gyro-single-electron-beam.png",
      "group": "Incoherent Emission"
    },
    {
      "filename": "html/plasma-emission-explorer.html",
      "title": "Plasma Emission: Beams, Langmuir Waves, and Dynamic Spectra",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Show beam free energy, Langmuir growth, density drift, and dynamic spectral signatures.",
      "prereqs": "Plasma frequency, beam instability, dispersion relation",
      "expected_minutes": 30,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#plasma-emission-explorer",
      "dependencies": [],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/plasma-panel-a-free-energy.png",
      "group": "Coherent Plasma Emission"
    },
    {
      "filename": "html/plasma-radiation-conversion-map.html",
      "title": "Plasma Conversion Map: Fundamental and Harmonic Paths",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Map nonlinear conversion paths from Langmuir waves to escaping fundamental and harmonic radiation.",
      "prereqs": "Langmuir waves, ion-sound waves, wave-wave coupling",
      "expected_minutes": 15,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#plasma-radiation-conversion-map-and-companion-pages",
      "dependencies": [
        "plasma-conversion-shared.css"
      ],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/plasma-conversion-fundamental-escape.png",
      "group": "Coherent Plasma Emission"
    },
    {
      "filename": "html/plasma-fundamental-conversion.html",
      "title": "Fundamental Plasma Emission: Scattering and Mode Conversion",
      "module": "emission-propagation",
      "tier": "B",
      "learning_goal": "Explain scattering or mode conversion from electrostatic Langmuir waves to transverse escaping radiation.",
      "prereqs": "Langmuir waves, transverse electromagnetic waves",
      "expected_minutes": 12,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#scattering-mode-conversion",
      "dependencies": [
        "plasma-conversion-shared.css"
      ],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/plasma-conversion-mode-conversion.png",
      "group": "Coherent Plasma Emission"
    },
    {
      "filename": "html/plasma-backscattering-decay.html",
      "title": "Langmuir Backscatter and Decay",
      "module": "emission-propagation",
      "tier": "B",
      "learning_goal": "Show how backscattering creates counter-propagating Langmuir waves for harmonic emission.",
      "prereqs": "Wave-vector matching, ion-sound waves",
      "expected_minutes": 12,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#backscattering-decay",
      "dependencies": [
        "plasma-conversion-shared.css"
      ],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/plasma-conversion-branch-matching.png",
      "group": "Coherent Plasma Emission"
    },
    {
      "filename": "html/plasma-harmonic-coalescence.html",
      "title": "Harmonic Plasma Emission: Langmuir Coalescence",
      "module": "emission-propagation",
      "tier": "B",
      "learning_goal": "Show how oppositely directed Langmuir waves coalesce into harmonic electromagnetic radiation.",
      "prereqs": "Langmuir waves, wave-vector matching",
      "expected_minutes": 12,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#langmuir-wave-coalescence",
      "dependencies": [
        "plasma-conversion-shared.css"
      ],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/plasma-conversion-branch-matching.png",
      "group": "Coherent Plasma Emission"
    },
    {
      "filename": "html/ecm-emission-explorer.html",
      "title": "Electron Cyclotron Maser: Resonance and Escape",
      "module": "emission-propagation",
      "tier": "A",
      "learning_goal": "Explain loss-cone free energy, cyclotron resonance, beam geometry, and escape conditions for ECM.",
      "prereqs": "Cyclotron frequency, pitch angle, magnetoionic modes",
      "expected_minutes": 25,
      "narrative_anchor": "html/emission-mechanism-explorer-narratives.html#ecm-emission-explorer",
      "dependencies": [],
      "status": "release",
      "screenshot": "figures/explorer-screenshots/ecm-panel-a-resonance-velocity.png",
      "group": "Coherent Plasma Emission"
    },
    {
      "filename": "html/radio_interferometry_fundamentals.html",
      "title": "Interferometry Basics: Delay, Fringes, and Visibility",
      "module": "interferometry-instrumentation",
      "tier": "A",
      "learning_goal": "Connect geometric delay, fringes, bandwidth, and visibility phase in radio interferometry.",
      "prereqs": "Sinusoidal waves, path difference, Fourier phase",
      "expected_minutes": 25,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "Measurement and Imaging"
    },
    {
      "filename": "html/fourier-interferometry.html",
      "title": "Fourier Imaging: Spatial Frequencies to Images",
      "module": "interferometry-instrumentation",
      "tier": "A",
      "learning_goal": "Show how Fourier components build images and how interferometers sample spatial frequencies.",
      "prereqs": "Fourier series, complex phase",
      "expected_minutes": 20,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "Measurement and Imaging"
    },
    {
      "filename": "html/fourier-synthesis-gallery.html",
      "title": "UV Synthesis Gallery: Coverage, Dirty Beam, and PSF",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Compare uv coverage and synthesized image behavior across sampling patterns.",
      "prereqs": "Visibility sampling, Fourier transform",
      "expected_minutes": 15,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "Measurement and Imaging"
    },
    {
      "filename": "html/radio-interferometric-image-reconstruction.html",
      "title": "Image Reconstruction: Dirty Images, CLEAN, and Deconvolution",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Compare dirty images, deconvolution, and reconstruction choices in radio imaging.",
      "prereqs": "Dirty beam, convolution, uv sampling",
      "expected_minutes": 20,
      "narrative_anchor": "",
      "dependencies": [
        "figures/casatasks.imaging.tclean.webp"
      ],
      "status": "release",
      "screenshot": "",
      "group": "Measurement and Imaging"
    },
    {
      "filename": "html/polarization-ellipse-interactive.html",
      "title": "Polarization Ellipse: Jones Vector and Stokes Geometry",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Relate electric-field components, phase difference, and polarization ellipse geometry.",
      "prereqs": "Vector waves, phase",
      "expected_minutes": 12,
      "narrative_anchor": "",
      "dependencies": [
        "figures/Poincaresp.png"
      ],
      "status": "release",
      "screenshot": "",
      "group": "Polarization and Spectral Diagnostics"
    },
    {
      "filename": "html/zeeman-components-illustration.html",
      "title": "Zeeman Components: Splitting and Polarization",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Illustrate Zeeman splitting components and their polarization signatures.",
      "prereqs": "Spectral lines, magnetic-field splitting",
      "expected_minutes": 10,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "Polarization and Spectral Diagnostics"
    },
    {
      "filename": "html/receiver-noise-interactive.html",
      "title": "Receiver Noise: System Temperature and Sensitivity",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Explain receiver noise, system temperature, and sensitivity tradeoffs.",
      "prereqs": "Thermal noise, bandwidth, integration time",
      "expected_minutes": 12,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "Receivers and Antennas"
    },
    {
      "filename": "html/beam-pattern-feed-illumination.html",
      "title": "Antenna Beam Pattern: Feed Illumination and Taper",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Show how feed taper changes aperture illumination, beam width, sidelobes, and source coupling.",
      "prereqs": "Aperture diffraction, antenna temperature",
      "expected_minutes": 18,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "Receivers and Antennas"
    },
    {
      "filename": "html/aperture-blockage-efficiency.html",
      "title": "Aperture Blockage: Efficiency and Beam Distortion",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Connect aperture blockage geometry to efficiency loss and beam structure.",
      "prereqs": "Aperture illumination, Fourier diffraction",
      "expected_minutes": 15,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "Receivers and Antennas"
    },
    {
      "filename": "html/delay_pattern_interactive.html",
      "title": "EOVSA Delay: Multiband Offset and Inband Slope",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Separate multiband delay offsets from inband phase slopes.",
      "prereqs": "Phase slope, frequency channels, delay",
      "expected_minutes": 18,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "EOVSA and FASR Instrumentation"
    },
    {
      "filename": "html/eovsa-frequency-tuning-explainer.html",
      "title": "EOVSA Frequency Tuning: Three-Stage Downconversion",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Explain EOVSA three-stage frequency tuning and band selection.",
      "prereqs": "Heterodyne mixing, bandpass",
      "expected_minutes": 12,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "EOVSA and FASR Instrumentation"
    },
    {
      "filename": "html/corner_turn_visualization.html",
      "title": "EOVSA Corner Turn: Data Reordering",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Show how EOVSA data are rearranged through the corner-turn processing step.",
      "prereqs": "Channelization, data flow",
      "expected_minutes": 12,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "EOVSA and FASR Instrumentation"
    },
    {
      "filename": "html/eovsa-adc-demux-explainer.html",
      "title": "EOVSA ADC Demux-by-4: Sample Stream Organization",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Explain ADC demultiplexing and sample stream organization.",
      "prereqs": "Sampling, digital signal paths",
      "expected_minutes": 10,
      "narrative_anchor": "",
      "dependencies": [],
      "status": "release",
      "screenshot": "",
      "group": "EOVSA and FASR Instrumentation"
    },
    {
      "filename": "html/fasr_mutual_coupling_diagnostics.html",
      "title": "FASR Diagnostics: Shadowing, Coupling, and UV/PSF",
      "module": "interferometry-instrumentation",
      "tier": "B",
      "learning_goal": "Explore antenna layout, shadowing, and coupling diagnostics for FASR-style arrays.",
      "prereqs": "Array geometry, antenna coupling",
      "expected_minutes": 18,
      "narrative_anchor": "",
      "dependencies": [
        "fasr_calibrators.js",
        "_fasr_enu_data.js"
      ],
      "status": "release",
      "screenshot": "",
      "group": "EOVSA and FASR Instrumentation"
    }
  ]
};
