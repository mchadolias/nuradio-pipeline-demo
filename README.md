# NuRadioMC Snakemake Demo

This repository demonstrates how to use **Snakemake** to manage a simple simulation workflow using **NuRadioMC**. The objective is to calculate the effective volume of a radio detector.

## 🗂️ Repository Structure

```markdown
nuradio-snakemake-demo/
├── Snakefile
├── profiles/
├── logs/
├── snake_config.yaml
├── envs/
│   ├── snakemake_env.yaml
│   └── nuradio_env.yaml
├── 01_Veff_simulation/
│   ├── T01generate_event_list.py
│   ├── T02RunSimulation.py
│   ├── T03VisualizeVeff.py
│   ├── config.yaml
│   └── surface_station_1GHz.json
├── data/
│   ├── simulated_events/
│   └── triggered_events/
├── figures/
├── clean_datafile.sh
├── README.md
└── .gitignore
```
