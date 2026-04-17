#!/usr/bin/env python3
"""
generate-uv-synthesis.py
------------------------
Pre-compute UV-synthesis frames for FOUR combinations and write a
self-contained HTML gallery (fourier-synthesis-gallery.html).

Array configs   × Synthesis modes  =  4 image sets
  Random array     Snapshot (h=0)      random_snap
  Spiral array     Earth rotation      random_er
                                        spiral_snap
                                        spiral_er

Antenna ordering: sorted by distance from center so that pressing Play
grows the array outward — inner core first, long baselines last.

Panels (4×1 on wide, 2×2 on medium):
  True Sky | UV Coverage | Dirty Image | PSF (dirty beam)

Usage:
  python generate-uv-synthesis.py

Dependencies: numpy, Pillow
"""

import numpy as np
import base64, io, os, sys, pathlib

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")

# ── Parameters ─────────────────────────────────────────────────────────────
NPIX           = 128
IMG_PX         = 256
UV_RANGE       = 80      # display range in baseline units
BASELINE_SCALE = 0.50    # baseline units → FFT pixel index
N_FRAMES       = 18      # frames per image set
N_PER_ARM      = 15      # antennas per spiral arm  (total 3*N+1 = 46)
N_RANDOM       = 30      # total antennas in random array
DEC_DEG        = 40.0    # source declination for Earth-rotation
H_STEP         = 4.0     # hour-angle step in degrees
OUTFILE = os.path.join(os.path.dirname(__file__), "fourier-synthesis-gallery.html")

# ── Colormap helpers ────────────────────────────────────────────────────────
def _hot_rgb(t):
    r = np.clip(t * 3,       0, 1)
    g = np.clip(t * 3 - 1,   0, 1)
    b = np.clip(t * 3 - 2,   0, 1)
    return (r*255).astype(np.uint8), (g*255).astype(np.uint8), (b*255).astype(np.uint8)

def apply_hot(arr2d, vmin=None, vmax=None):
    a = arr2d.astype(float)
    if vmin is None: vmin = a.min()
    if vmax is None: vmax = a.max()
    t = np.clip((a - vmin) / (vmax - vmin + 1e-30), 0, 1)
    r, g, b = _hot_rgb(t)
    return np.stack([r, g, b], axis=-1)

def render_image(arr2d, vmin=None, vmax=None):
    a = arr2d.astype(float)
    if vmin is None: vmin = a.min()
    if vmax is None: vmax = a.max()
    t = np.clip((a - vmin) / (vmax - vmin + 1e-30), 0, 1)
    c = (t * 255).astype(np.uint8)
    gray = np.stack([c, c, c], axis=-1)
    return Image.fromarray(gray, 'RGB').resize((IMG_PX, IMG_PX), Image.NEAREST)

def render_psf(arr2d):
    """Diverging grayscale: -1 → black (0), 0 → mid-gray (128), +1 → white (255)."""
    a = np.clip(arr2d.astype(float), -1, 1)
    c = ((a + 1) / 2 * 255).astype(np.uint8)
    gray = np.stack([c, c, c], axis=-1)
    return Image.fromarray(gray, 'RGB').resize((IMG_PX, IMG_PX), Image.NEAREST)

def to_b64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format='PNG', optimize=False, compress_level=1)
    return base64.b64encode(buf.getvalue()).decode()

# ── Sky model ───────────────────────────────────────────────────────────────
def make_sky():
    img_path = pathlib.Path(__file__).parent / "figures/cygnusA_radio.jpg"
    if not img_path.exists():
        raise FileNotFoundError(f"Sky model not found: {img_path}")
    img = Image.open(img_path).convert('L').resize((NPIX, NPIX), Image.LANCZOS)
    sky = np.array(img, dtype=float)
    return sky / sky.max()

# ── Dirty image & PSF ───────────────────────────────────────────────────────
def compute_dirty(sky_fft, baselines):
    vis = np.zeros((NPIX, NPIX), dtype=complex)
    for bu, bv in baselines:
        ui = int(round(bu * BASELINE_SCALE)) % NPIX
        vi = int(round(bv * BASELINE_SCALE)) % NPIX
        vis[vi, ui] = sky_fft[vi, ui]
        vis[-vi % NPIX, -ui % NPIX] = np.conj(sky_fft[vi, ui])
    dirty = np.fft.fftshift(np.real(np.fft.ifft2(vis)))
    peak  = dirty.max()
    if peak > 1e-10: dirty /= peak
    return dirty

def compute_psf(baselines):
    mask = np.zeros((NPIX, NPIX), dtype=complex)
    for bu, bv in baselines:
        ui = int(round(bu * BASELINE_SCALE)) % NPIX
        vi = int(round(bv * BASELINE_SCALE)) % NPIX
        mask[vi, ui] = 1.0
        mask[-vi % NPIX, -ui % NPIX] = 1.0
    psf  = np.fft.fftshift(np.real(np.fft.ifft2(mask)))
    peak = psf.max()
    if peak > 1e-10: psf /= peak
    return psf

def gen_frame(sky_fft, baselines):
    dirty = compute_dirty(sky_fft, baselines)
    psf   = compute_psf(baselines)
    uv    = render_uv(baselines, dot_size=1)
    return to_b64(uv), to_b64(render_image(dirty, vmin=-0.15, vmax=1.0)), to_b64(render_psf(psf))

# ── UV coverage image ────────────────────────────────────────────────────────
def render_uv(baselines, dot_size=1):
    img  = Image.new('RGB', (IMG_PX, IMG_PX), (12, 14, 28))
    draw = ImageDraw.Draw(img)
    cx = cy = IMG_PX // 2
    scl = (IMG_PX // 2 - 14) / UV_RANGE
    for g in range(-UV_RANGE, UV_RANGE + 1, 20):
        gx = int(cx + g * scl); gy = int(cy - g * scl)
        draw.line([(gx, 0), (gx, IMG_PX)], fill=(30, 36, 55), width=1)
        draw.line([(0, gy), (IMG_PX, gy)], fill=(30, 36, 55), width=1)
    draw.line([(0, cy), (IMG_PX, cy)], fill=(60, 72, 96), width=1)
    draw.line([(cx, 0), (cx, IMG_PX)], fill=(60, 72, 96), width=1)
    D = dot_size
    for bu, bv in baselines:
        px = int(round(cx + bu * scl)); py = int(round(cy - bv * scl))
        draw.ellipse([px-D, py-D, px+D, py+D], fill=(86, 185, 255))
        qx = int(round(2*cx - px));    qy = int(round(2*cy - py))
        draw.ellipse([qx-D, qy-D, qx+D, qy+D], fill=(86, 185, 255))
    return img

# ── Array configurations ─────────────────────────────────────────────────────
def sort_by_radius(positions):
    """Sort antennas by distance from origin (keep [0] = central first)."""
    central = [positions[0]]
    rest    = sorted(positions[1:], key=lambda p: p[0]**2 + p[1]**2)
    return central + rest

def make_random_array(n=N_RANDOM, seed=42):
    """
    Compact random array: positions drawn log-uniformly in radius with a
    density bias toward the center (realistic for interferometers).
    """
    rng = np.random.default_rng(seed)
    positions = [(0.0, 0.0)]
    while len(positions) < n:
        t     = rng.uniform(0, 1) ** 1.4     # bias: more antennas at small r
        r     = 3.0 * (72.0 / 3.0) ** t
        theta = rng.uniform(0, 2 * np.pi)
        positions.append((r * np.cos(theta), r * np.sin(theta)))
    return sort_by_radius(positions)

def make_spiral_array(n_per_arm=N_PER_ARM, r_min=3.0, r_max=72.0):
    """
    3-arm Y-shape logarithmic spiral + 1 central antenna.

    Each arm follows r = r_min*(r_max/r_min)^t, θ = inner_angle + t*sweep.
      inner_angle: 0°, 120°, 240°  (Y at small r)
      outer tip:   180°, 300°, 60°  (Y rotated 180° at large r)
    sweep_deg=180 gives a half-turn spiral per arm.

    Antennas are sorted by radius so that Play grows all arms simultaneously
    from the center outward.
    """
    sweep_deg = 180.0
    positions = [(0.0, 0.0)]
    for arm in range(3):
        inner_angle = arm * 120.0
        for i in range(1, n_per_arm + 1):
            t     = i / n_per_arm
            r     = r_min * (r_max / r_min) ** t
            theta = (inner_angle + t * sweep_deg) * np.pi / 180.0
            positions.append((r * np.cos(theta), r * np.sin(theta)))
    return sort_by_radius(positions)

# ── Baseline generators ───────────────────────────────────────────────────────
def _dedup_key(bu, bv):
    return (int(round(bu * BASELINE_SCALE)) % NPIX,
            int(round(bv * BASELINE_SCALE)) % NPIX)

def snapshot_baselines_for_n(positions, n):
    """All unique baselines from the first n antennas at h=0."""
    seen = set(); pts = []
    for i in range(n):
        for j in range(i + 1, n):
            bu = positions[i][0] - positions[j][0]
            bv = positions[i][1] - positions[j][1]
            key = _dedup_key(bu, bv)
            if key == (0, 0) or key in seen: continue
            seen.add(key); pts.append((bu, bv))
    return pts

def earth_rotation_baselines_for_n(positions, n):
    """
    All unique UV points from the first n antennas with Earth-rotation synthesis.
    Each physical baseline (Bx, By) sweeps through hour angles h ∈ [−90°, +90°]:
      u(h) = Bx·cos(h) − By·sin(h)
      v(h) = [Bx·sin(h) + By·cos(h)]·sin(δ)
    where δ = DEC_DEG, h step = H_STEP degrees.
    """
    DEC  = DEC_DEG * np.pi / 180.0
    seen = set(); pts = []
    for i in range(n):
        for j in range(i + 1, n):
            Bx = positions[i][0] - positions[j][0]
            By = positions[i][1] - positions[j][1]
            for h_deg in np.arange(-90, 90 + H_STEP / 2, H_STEP):
                h  = h_deg * np.pi / 180.0
                bu = Bx * np.cos(h) - By * np.sin(h)
                bv = (Bx * np.sin(h) + By * np.cos(h)) * np.sin(DEC)
                key = _dedup_key(bu, bv)
                if key == (0, 0) or key in seen: continue
                seen.add(key); pts.append((bu, bv))
    return pts

# ── Frame generation for one image set ───────────────────────────────────────
def generate_set(positions, sky_fft, earth_rotation=False, label_prefix=""):
    """
    Generate N_FRAMES frames for one (array, mode) combination.
    Antennas are added from inside out (sorted by radius).
    Returns dict with keys uv, dirty, psf, labels (lists of base64 strings / labels).
    """
    n_total = len(positions)
    raw     = np.logspace(np.log10(2), np.log10(n_total), N_FRAMES)
    counts  = sorted(set(max(2, int(round(x))) for x in raw))

    out = {'uv': [], 'dirty': [], 'psf': [], 'labels': []}
    bl_fn = earth_rotation_baselines_for_n if earth_rotation else snapshot_baselines_for_n
    mode_str = "UV tracks" if earth_rotation else "baselines"

    for idx, n_ant in enumerate(counts):
        bl    = bl_fn(positions, n_ant)
        n_vis = 2 * len(bl)
        print(f"  {label_prefix} frame {idx+1:2d}/{len(counts)}: "
              f"{n_ant:2d} antennas, {n_vis:5d} {mode_str}...", end='\r')
        u, d, p = gen_frame(sky_fft, bl)
        out['uv'].append(u);  out['dirty'].append(d);  out['psf'].append(p)
        out['labels'].append(f"{n_ant} antennas · {n_vis} {mode_str}")
    print()
    return out

# ── HTML template ────────────────────────────────────────────────────────────
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UV Synthesis Gallery</title>
  <style>
    :root {
      --bg: #eef1f4; --bg-deep: #dde4eb;
      --panel: rgba(255,255,255,0.92);
      --ink: #1f1f1f; --muted: #5e6772;
      --shadow: 0 18px 48px rgba(31,41,55,0.1);
      --radius: 22px; --accent: #2563eb;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: "Avenir Next","Segoe UI",sans-serif;
      background: radial-gradient(circle at top left,rgba(37,99,235,0.06),transparent 28%),
                  linear-gradient(180deg,var(--bg) 0%,var(--bg-deep) 100%);
      padding: 24px; color: var(--ink); min-height: 100vh;
    }
    .shell { max-width: 1300px; margin: 0 auto; display: grid; gap: 18px; }
    .hero, .panel {
      background: var(--panel); border: 1px solid rgba(31,31,31,0.08);
      border-radius: var(--radius); box-shadow: var(--shadow); padding: 26px 30px;
    }
    .hero h1 {
      font-family: Georgia, serif; font-size: clamp(1.6rem,3vw,2.8rem);
      line-height: 1.0; letter-spacing: -0.02em; margin-bottom: 12px;
    }
    p { color: var(--muted); line-height: 1.55; margin-bottom: 8px; }
    .formula {
      font-family: "Courier New",monospace; font-size: 14px;
      background: rgba(37,99,235,0.07); border-left: 3px solid var(--accent);
      padding: 10px 16px; border-radius: 0 8px 8px 0; margin: 10px 0; color: var(--ink);
    }
    h2 { font-size: 1.2rem; font-weight: 700; margin-bottom: 14px; }
    h3 { font-size: 0.92rem; font-weight: 600; color: var(--muted); margin-bottom: 6px; }

    /* Controls bar */
    .controls-bar {
      display: flex; align-items: center; gap: 16px; flex-wrap: wrap; margin-bottom: 18px;
    }
    .cfg-tabs { display: flex; gap: 8px; }
    .cfg-btn {
      padding: 7px 20px; border: 2px solid var(--accent); border-radius: 10px;
      background: transparent; color: var(--accent); cursor: pointer;
      font-size: 14px; font-family: inherit; font-weight: 600;
      transition: background 0.15s, color 0.15s;
    }
    .cfg-btn.active { background: var(--accent); color: #fff; }
    .cfg-btn:hover:not(.active) { background: rgba(37,99,235,0.08); }

    /* Earth-rotation toggle */
    .er-wrap {
      display: flex; align-items: center; gap: 10px;
      border-left: 1px solid rgba(31,31,31,0.12); padding-left: 16px;
    }
    .er-wrap label { font-size: 14px; font-weight: 600; color: var(--muted); cursor: pointer; }
    /* iOS-style toggle switch */
    .switch { position: relative; display: inline-block; width: 44px; height: 24px; }
    .switch input { opacity: 0; width: 0; height: 0; }
    .slider-sw {
      position: absolute; cursor: pointer; inset: 0;
      background: #cbd5e1; border-radius: 24px; transition: background 0.2s;
    }
    .slider-sw:before {
      content: ""; position: absolute; width: 18px; height: 18px;
      left: 3px; top: 3px; background: #fff; border-radius: 50%;
      transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    input:checked + .slider-sw { background: var(--accent); }
    input:checked + .slider-sw:before { transform: translateX(20px); }

    /* Gallery: 4×1 on wide, 2×2 on medium */
    .gallery {
      display: grid; grid-template-columns: repeat(4, 1fr);
      gap: 16px; margin-top: 4px;
    }
    .gallery .col { display: flex; flex-direction: column; align-items: center; gap: 6px; }
    .gallery img {
      width: 100%; aspect-ratio: 1;
      border-radius: 10px; display: block; image-rendering: pixelated;
    }
    @media (max-width: 960px) { .gallery { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 500px) { .gallery { grid-template-columns: 1fr; } }

    /* Slider row */
    .slider-row {
      display: flex; align-items: center; gap: 14px;
      margin-top: 20px; padding-top: 18px;
      border-top: 1px solid rgba(31,31,31,0.07);
    }
    input[type=range] {
      flex: 1; -webkit-appearance: none; height: 6px;
      background: #d1d5db; border-radius: 3px; outline: none;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none; width: 20px; height: 20px;
      background: var(--accent); border-radius: 50%; cursor: pointer;
    }
    .badge {
      font-family: "Courier New",monospace; font-size: 13px; font-weight: 700;
      color: var(--accent); white-space: nowrap; min-width: 260px; text-align: right;
    }
    .play-btn {
      padding: 8px 20px; border: none; border-radius: 10px; cursor: pointer;
      font-size: 14px; font-family: inherit; font-weight: 600;
      background: var(--accent); color: #fff; white-space: nowrap; transition: background 0.15s;
    }
    .play-btn.is-playing { background: #dc2626; }
    .play-btn:hover { filter: brightness(0.9); }
    .caption { font-size: 12px; color: var(--muted); text-align: center; }
  </style>
</head>
<body>
<div class="shell">
  <div class="hero">
    <h1>UV Synthesis &amp;<br>Image Reconstruction</h1>
    <p>Each antenna pair samples one Fourier component of the sky. The slider grows the array from the innermost antennas outward. Toggle <strong>Earth Rotation</strong> to sweep each baseline through ±90° of hour angle, dramatically improving UV coverage.</p>
    <div class="formula">I<sub>dirty</sub> = FT<sup>−1</sup>{V(u,v)·S(u,v)} &nbsp;&nbsp; PSF = FT<sup>−1</sup>{S(u,v)}</div>
    <p>Sky model: <strong>Cygnus A at 5 GHz</strong>. PSF colormap: <span style="color:#3b82f6">blue</span> = negative sidelobes, dark→white = positive.</p>
  </div>

  <div class="panel">
    <h2>UV Coverage → Dirty Image → PSF</h2>
    <div class="controls-bar">
      <div class="cfg-tabs">
        <button class="cfg-btn active" data-array="random">Random Array</button>
        <button class="cfg-btn"        data-array="spiral">Spiral Array</button>
      </div>
      <div class="er-wrap">
        <label class="switch">
          <input type="checkbox" id="erToggle">
          <span class="slider-sw"></span>
        </label>
        <label for="erToggle">Earth Rotation</label>
      </div>
    </div>

    <div class="gallery">
      <div class="col">
        <h3>True Sky</h3>
        <img id="skyImg" src="data:image/png;base64,__SKY__" alt="True sky">
        <div class="caption">Cygnus A at 5 GHz — 128×128 (fixed)</div>
      </div>
      <div class="col">
        <h3>UV Coverage</h3>
        <img id="uvImg" src="" alt="UV coverage">
        <div class="caption" id="uvCaption">—</div>
      </div>
      <div class="col">
        <h3>Dirty Image</h3>
        <img id="dirtyImg" src="" alt="Dirty image">
        <div class="caption" id="dirtyCaption">IFT of sampled visibilities</div>
      </div>
      <div class="col">
        <h3>PSF (Dirty Beam)</h3>
        <img id="psfImg" src="" alt="PSF">
        <div class="caption" id="psfCaption">IFT of sampling mask</div>
      </div>
    </div>

    <div class="slider-row">
      <button class="play-btn" id="playBtn">▶ Play</button>
      <input type="range" id="slider" min="0" max="17" value="0" step="1">
      <div class="badge" id="badge">—</div>
    </div>
  </div>
</div>

<script>
  const SETS = {
    random_snap: { uv:[__UV_RS__], dirty:[__DIRTY_RS__], psf:[__PSF_RS__], labels:[__LBL_RS__] },
    random_er:   { uv:[__UV_RE__], dirty:[__DIRTY_RE__], psf:[__PSF_RE__], labels:[__LBL_RE__] },
    spiral_snap: { uv:[__UV_SS__], dirty:[__DIRTY_SS__], psf:[__PSF_SS__], labels:[__LBL_SS__] },
    spiral_er:   { uv:[__UV_SE__], dirty:[__DIRTY_SE__], psf:[__PSF_SE__], labels:[__LBL_SE__] },
  };

  let currentArray = 'random', earthRot = false, frame = 0, timer = null;
  const getKey = () => `${currentArray}_${earthRot ? 'er' : 'snap'}`;

  const slider   = document.getElementById('slider');
  const uvImg    = document.getElementById('uvImg');
  const dirtyImg = document.getElementById('dirtyImg');
  const psfImg   = document.getElementById('psfImg');
  const badge    = document.getElementById('badge');
  const uvCap    = document.getElementById('uvCaption');
  const playBtn  = document.getElementById('playBtn');
  const erToggle = document.getElementById('erToggle');

  function showFrame(i) {
    const s = SETS[getKey()];
    const n = Math.max(0, Math.min(i, s.uv.length - 1));
    uvImg.src    = 'data:image/png;base64,' + s.uv[n];
    dirtyImg.src = 'data:image/png;base64,' + s.dirty[n];
    psfImg.src   = 'data:image/png;base64,' + s.psf[n];
    badge.textContent  = s.labels[n];
    uvCap.textContent  = s.labels[n];
    slider.value = n;
  }

  function switchSet() {
    stopPlay();
    const s = SETS[getKey()];
    slider.max = s.uv.length - 1;
    frame = Math.min(frame, s.uv.length - 1);
    showFrame(frame);
  }

  function stopPlay() {
    clearInterval(timer); timer = null;
    playBtn.textContent = '▶ Play';
    playBtn.classList.remove('is-playing');
  }

  slider.addEventListener('input', () => { frame = +slider.value; showFrame(frame); });

  playBtn.addEventListener('click', () => {
    if (timer) { stopPlay(); return; }
    const s = SETS[getKey()];
    if (frame >= s.uv.length - 1) frame = 0;
    playBtn.textContent = '⏹ Stop';
    playBtn.classList.add('is-playing');
    timer = setInterval(() => {
      showFrame(frame++);
      if (frame >= s.uv.length) stopPlay();
    }, 700);
  });

  document.querySelectorAll('.cfg-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      currentArray = btn.dataset.array;
      document.querySelectorAll('.cfg-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      switchSet();
    });
  });

  erToggle.addEventListener('change', () => { earthRot = erToggle.checked; switchSet(); });

  switchSet();
</script>
</body>
</html>
"""

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("Building sky model...")
    sky     = make_sky()
    sky_fft = np.fft.fft2(np.fft.ifftshift(sky))
    sky_arr = np.clip(sky * 255, 0, 255).astype(np.uint8)
    sky_b64 = to_b64(Image.fromarray(sky_arr, 'L').resize((IMG_PX, IMG_PX), Image.LANCZOS).convert('RGB'))

    print(f"Building random array ({N_RANDOM} antennas, sorted by radius)...")
    rand_pos = make_random_array()
    print(f"Building spiral array ({3*N_PER_ARM+1} antennas, sorted by radius)...")
    spir_pos = make_spiral_array()

    configs = [
        ('random_snap', rand_pos, False, 'Random/snapshot'),
        ('random_er',   rand_pos, True,  'Random/Earth-rot'),
        ('spiral_snap', spir_pos, False, 'Spiral/snapshot'),
        ('spiral_er',   spir_pos, True,  'Spiral/Earth-rot'),
    ]

    sets = {}
    for key, positions, earth_rotation, prefix in configs:
        print(f"\n── {prefix} ──")
        sets[key] = generate_set(positions, sky_fft, earth_rotation, prefix)

    # ── Build HTML ────────────────────────────────────────────────────────
    print("\nBuilding HTML...")
    def jsa(lst): return ',\n    '.join(f'"{s}"' for s in lst)
    def jsl(lst): return ','.join(f'"{s}"' for s in lst)

    html = HTML_TEMPLATE.replace('__SKY__', sky_b64)
    for (key, _, _, _), tag in zip(configs, ['RS', 'RE', 'SS', 'SE']):
        s = sets[key]
        html = (html
            .replace(f'__UV_{tag}__',    jsa(s['uv']))
            .replace(f'__DIRTY_{tag}__', jsa(s['dirty']))
            .replace(f'__PSF_{tag}__',   jsa(s['psf']))
            .replace(f'__LBL_{tag}__',   jsl(s['labels']))
        )

    with open(OUTFILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Saved: {OUTFILE}  ({os.path.getsize(OUTFILE)/1e6:.1f} MB)")

if __name__ == '__main__':
    main()
