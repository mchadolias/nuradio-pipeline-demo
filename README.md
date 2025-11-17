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

## 🔀 Directed acyclic graph of the workflow (DAG)

For the simple example, where the user wants to produce three files with energies `1e17`, `1e18` and `1e18` respectively and `10k` events each; the workflow will run the following steps as seen in the diagram below.

![Directed acyclic graph](./figures/screenshots/dag.pdf)

## 🚀 Usage

#### Dependecies: conda manager

### Step 1st: Clone directory

```cmd
git clone git@github.com:mchadolias/nuradio-pipeline-demo.git
```

### Step 2nd: Prepare conda environments

```cmd
# Create monitoring environment
conda env create -f envs/snakemake_env.yaml

# Create analysis environment
conda env create -f envs/nuradio_env.yaml
```

#### Note

You should modify **first** for the path of the environement to be saved

### Step 3rd: Create snake_config.yaml

```cmd
python generate_jobs_yaml.py
```

### Step 4th: Run the example

```cmd
# Activate environment
conda activate snakemake-workdlow

# Run snakemake example
snakemake --profile profiles/local
```

Before running the example, you can run the following command `snakemake -n`, to dry-run the potential jobs that would be created.
