# Nox2
This repository contains scripts and CellProfiler pipelines used for the manuscript:  "Neutrophil NADPH oxidase breaks the inflammatory IL-1β/IL-17A circuit to enhance pathogen clearance during respiratory virus infections."

## Contents

- `scripts/`:
    Colocalisation script - used to calculate colocalisation of p47-phox and gp91phox subunits by Pearson R coefficient from immunofluorescence images of isolated neutrophils
  count_tdTom_Ly6G_classes - used to calculate %percentage of tdTomato and Ly6G expressing cells identified with Cellprofiler pipeline TdTom_vs_Ly6G_populations.cppipe
    

- `cellprofiler_pipelines/`: CellProfiler `.cppipe` pipelines
    Nox2_pixel_intensity: used to calculate Nox2 pixel intensity in tdTomato+ cells in immunofluorescence images of lung sections
    TdTom_vs_Ly6G_populations: used measure mean intensity of tdTomato and Ly6G expression per cells in immunofluorescence images of lung sections
  
- `metadata/`: example metadata files or input templates

## Software

- CellProfiler version: 4.2.8
- JupyterLab version: v3.6.7
- Python version: 3.9.19
