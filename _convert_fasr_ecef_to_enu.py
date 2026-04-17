#!/usr/bin/env python3
"""Convert FASR .cfg ECEF coordinates to ENU and output as JS arrays."""
import numpy as np

def geodetic_to_ecef(lon_deg, lat_deg, h=0):
    """WGS84 geodetic to ECEF."""
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = 2 * f - f * f
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
    x = (N + h) * np.cos(lat) * np.cos(lon)
    y = (N + h) * np.cos(lat) * np.sin(lon)
    z = (N * (1 - e2) + h) * np.sin(lat)
    return np.array([x, y, z])

def ecef_to_enu(ecef, center, lat_deg, lon_deg):
    """ECEF to ENU relative to center."""
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    dx = ecef[0] - center[0]
    dy = ecef[1] - center[1]
    dz = ecef[2] - center[2]
    e = -np.sin(lon) * dx + np.cos(lon) * dy
    n = -np.sin(lat) * np.cos(lon) * dx - np.sin(lat) * np.sin(lon) * dy + np.cos(lat) * dz
    u = np.cos(lat) * np.cos(lon) * dx + np.cos(lat) * np.sin(lon) * dy + np.sin(lat) * dz
    return [e, n, u]

def parse_cfg(filepath):
    """Parse CASA antenna list .cfg file."""
    positions = []
    diams = []
    names = []
    cofa_lon, cofa_lat = None, None
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#COFA='):
                parts = line.replace('#COFA=', '').split(',')
                cofa_lon, cofa_lat = float(parts[0]), float(parts[1])
            elif line.startswith('#'):
                continue
            elif line:
                parts = line.split()
                positions.append([float(parts[0]), float(parts[1]), float(parts[2])])
                diams.append(float(parts[3]))
                names.append(parts[4])
    return np.array(positions), diams, names, cofa_lon, cofa_lat

def format_js_array(enu_list, var_name, pad_names, dish_diam):
    """Format as JS const."""
    lines = [f"// {len(enu_list)} antennas, dish diameter = {dish_diam}m"]
    lines.append(f"const {var_name}_ENU = [")
    for i, (enu, name) in enumerate(zip(enu_list, pad_names)):
        comma = "," if i < len(enu_list) - 1 else ""
        lines.append(f"  [{enu[0]:12.4f}, {enu[1]:12.4f}, {enu[2]:9.4f}]{comma} // {name}")
    lines.append("];")
    lines.append(f"const {var_name}_PADS = {pad_names};")
    return "\n".join(lines)

cfg_dir = "/Users/fisher/Library/Mobile Documents/com~apple~CloudDocs/work/research_project/ipynb_scripts_local/fasr-array-config-simul"

for label, filename in [("FASR_A", "fasr-a_random_spiral_hybrid_120.cfg"),
                         ("FASR_B", "fasr-b_spiral_72.cfg")]:
    path = f"{cfg_dir}/{filename}"
    ecef_all, diams, names, cofa_lon, cofa_lat = parse_cfg(path)
    # Use centroid of antenna ECEF positions as center (avoids altitude offset)
    center = np.mean(ecef_all, axis=0)
    enu_all = [ecef_to_enu(pos, center, cofa_lat, cofa_lon) for pos in ecef_all]
    print(format_js_array(enu_all, label, names, diams[0]))
    print()
