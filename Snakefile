from pathlib import Path

# Load global config
configfile: "snake_config.yaml"

# Ensure output folders exist
for d in [
    "data/simulated_events",
    "data/triggered_events",
    "figures/results",
    "logs"
]:
    Path(d).mkdir(parents=True, exist_ok=True)
    
# Final rule: when finished, produce figures
# (You can switch back to this later)
rule all:
    input:
        "figures/results/Veff.pdf",
        "figures/results/limits.pdf"


# Rule 1st: Generate events
rule event_generation:
    input:
        script="01_Veff_simulation/T01generate_event_list.py"
    output:
        "data/simulated_events/{energy}_n{n_events}.hdf5"
    conda:
        config["conda_env"]
    log:
        "logs/event_generation_{energy}_n{n_events}.log"
    shell:
        """
        python {input.script} \
             {wildcards.n_events} {wildcards.energy} \
              2>&1 | sed 's/\\x1b\\[[0-9;]*m//g' > {log}
        """


# Rule 2nd: Simulate detector response
rule detector_simulation:
    input:
        script="01_Veff_simulation/T02RunSimulation.py",
        hdf5_gen="data/simulated_events/{energy}_n{n_events}.hdf5"
    output:
        hdf5_trig="data/triggered_events/{energy}_n{n_events}.hdf5"
    params:
        station_config="configs/surface_station_1GHz.json",
        sim_config="configs/config.yaml",
    conda:
        config["conda_env"]
    log:
        "logs/detector_simulation_{energy}_n{n_events}.log"
    shell:
        """
        python {input.script} \
            {input.hdf5_gen} \
            {params.station_config} \
            {params.sim_config} \
            {output.hdf5_trig} \
            2>&1 | sed 's/\\x1b\\[[0-9;]*m//g' > {log}
        """


# Rule 3rd: Visualize Veff
rule plot_veff:
    input:
        [f"data/triggered_events/{job['energy']}_n{job['n_events']}.hdf5"
         for job in config["jobs"]]
    params:
        trigg_folder="data/triggered_events/",
        script="01_Veff_simulation/T03visualizeVeff.py",
    output:
        plot_1="figures/results/Veff.pdf",
        plot_2="figures/results/limits.pdf"
    conda:
        config["conda_env"]
    log:
        "logs/plot_veff.log"
    shell:
        """
        python {params.script} \
            {params.trigg_folder} \
            {output.plot_1} \
            {output.plot_2} \
            2>&1 | sed 's/\\x1b\\[[0-9;]*m//g' > {log}
        """
