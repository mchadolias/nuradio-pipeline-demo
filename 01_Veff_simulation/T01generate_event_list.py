from __future__ import absolute_import, division, print_function
from NuRadioReco.utilities import units
from NuRadioMC.EvtGen.generator import generate_eventlist_cylinder
import argparse
from pathlib import Path
import json


def main():
    parser = argparse.ArgumentParser(
        description="Generate event list for neutrino simulation"
    )

    parser.add_argument(
        "n_events", type=float, help="Number of neutrino events to generate"
    )
    parser.add_argument(
        "energy",
        type=float,
        help="Neutrino energy in eV",
    )
    args = parser.parse_args()

    # Ensure output folder exists
    outputfolder = Path("data/simulated_events")
    outputfolder.mkdir(parents=True, exist_ok=True)

    # Format filename consistently in scientific notation without '+'
    filename = f"{args.energy:.0e}_n{int(args.n_events)}.hdf5".replace("+", "")
    outputfile = outputfolder / filename

    # Load simulation volume
    with open("01_Veff_simulation/simulation_volume.json", "r") as f:
        volume_data = json.load(f)

    # Apply units
    volume = {key: value * units.km for key, value in volume_data.items()}

    # Generate events
    generate_eventlist_cylinder(
        outputfile,
        args.n_events,
        args.energy * units.eV,
        args.energy * units.eV,
        volume,
    )


if __name__ == "__main__":
    main()
