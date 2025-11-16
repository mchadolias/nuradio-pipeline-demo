#!/usr/bin/env python3
import yaml
import numpy as np
import argparse

# -----------------------------
# CLI
# -----------------------------
parser = argparse.ArgumentParser(
    description="Generate job YAML for neutrino simulations"
)
parser.add_argument(
    "--params",
    type=str,
    default="configs/job_params.yaml",
    help="Input YAML file with job parameters",
)
parser.add_argument(
    "--output", type=str, default="snake_config.yaml", help="Output YAML file"
)
parser.add_argument(
    "--mode",
    choices=["custom", "range"],
    default=None,
    help="Job generation mode: custom uses predefined jobs, range generates from energy range",
)
args = parser.parse_args()

# -----------------------------
# Load YAML parameters
# -----------------------------
with open(args.params) as f:
    params = yaml.safe_load(f)

# -----------------------------
# Determine mode
# -----------------------------
mode = args.mode
if mode is None:
    # Infer mode from YAML
    if "jobs" in params and params["jobs"]:
        mode = "custom"
    elif "range" in params:
        mode = "range"
    else:
        raise ValueError("Cannot determine mode: no 'jobs' or 'range' section in YAML")

# -----------------------------
# Custom jobs
# -----------------------------
if mode == "custom":
    if "jobs" not in params or not params["jobs"]:
        raise ValueError("Mode 'custom' requires a non-empty 'jobs' list in YAML")
    jobs = []
    for j in params["jobs"]:
        energy = float(j["energy"])
        n_events = int(j["n_events"])
        jobs.append({"energy": energy, "n_events": n_events})

# -----------------------------
# Range-generated jobs
# -----------------------------
elif mode == "range":
    r = params.get("range", {})
    E_min = float(r.get("E_min", 5e16))
    E_max = float(r.get("E_max", 1e20))
    if E_max <= E_min:
        raise ValueError(f"E_max ({E_max}) must be greater than E_min ({E_min})")

    range_type = r.get("range_type", "log")  # log, linear, geometric
    points_per_decade = r.get("points_per_decade", 5)
    total_points = r.get("total_points", None)

    n_events_max = float(r.get("n_events_max", 50000))
    n_events_min = float(r.get("n_events_min", 5000))
    if n_events_max < n_events_min:
        raise ValueError("n_events_max must be >= n_events_min")

    decline_type = r.get("decline_type", "exponential")  # exponential, linear, none
    decline_factor = float(r.get("decline_factor", 1.0))

    # -----------------------------
    # Determine number of points
    # -----------------------------
    if total_points is not None:
        n_points = int(total_points)
    elif points_per_decade is not None and range_type == "log":
        n_decades = np.log10(E_max) - np.log10(E_min)
        n_points = int(points_per_decade * n_decades) + 1
    else:
        n_points = 14

    # -----------------------------
    # Generate energy array
    # -----------------------------
    if range_type == "log":
        energies = np.logspace(np.log10(E_min), np.log10(E_max), n_points)
    elif range_type == "linear":
        energies = np.linspace(E_min, E_max, n_points)
    elif range_type == "geometric":
        energies = np.geomspace(E_min, E_max, n_points)
    else:
        raise ValueError(f"Unknown range_type: {range_type}")

    # -----------------------------
    # Compute n_events per energy
    # -----------------------------
    jobs = []
    for i, E in enumerate(energies):
        frac = np.log10(E / E_min) / np.log10(E_max / E_min) if E_max != E_min else 0
        frac = np.clip(frac, 0.0, 1.0)

        if decline_type == "exponential":
            if frac == 0.0:
                n_events = n_events_max
            elif frac == 1.0:
                n_events = n_events_min
            else:
                log_ratio = np.log10(n_events_min / n_events_max)
                n_events = n_events_max * 10 ** (log_ratio * (frac**decline_factor))
        elif decline_type == "linear":
            n_events = n_events_max - (n_events_max - n_events_min) * (
                frac**decline_factor
            )
        elif decline_type == "none":
            n_events = n_events_max
        else:
            raise ValueError(f"Unknown decline_type: {decline_type}")

        n_events = max(n_events_min, min(n_events_max, n_events))
        jobs.append({"energy": float(E), "n_events": int(round(n_events))})

# -----------------------------
# Output YAML
# -----------------------------
output_dict = {"conda_env": "envs/nuradio_env.yaml", "jobs": jobs}

with open(args.output, "w") as f:
    yaml.safe_dump(output_dict, f)

print(f"Mode: {mode}")
print(f"Generated {len(jobs)} jobs -> {args.output}")
print("First jobs:")
for job in jobs[:5]:
    print(f"  Energy={job['energy']:.2e} eV, n_events={job['n_events']}")
