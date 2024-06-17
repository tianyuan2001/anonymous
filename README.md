# Anonymous Repo

## Overview

This repository contains scripts and resources to sample data from the CARLA simulator version 0.9.14. It includes modules for handling reflections, road infrastructure, shadows, and traffic participants.

## Requirements

- CARLA Simulator v0.9.14
- Python 3.8.10

## Modules

### Reflection
Contains scripts for handling reflections, including street light and sunlight reflections.

### RoadInfrastructure
Scripts for different road infrastructures such as fences and road signs.

### Shadow
Scripts managing shadows for different road elements like fences, rails, street lights, and wires.

### TrafficParticipants
Includes modules related to vehicles and other participants in the traffic simulation.

### Attention Area Mixing (AAM)
Includes scripts for implementing the Attention Area Mixing method, designed to enhance model performance by focusing on high-attention areas.

## Scripts

- `generate_traffic.py`: Script to generate traffic in the CARLA simulator.
- `nav_sync_mode.py`: Navigation and synchronization script for the simulator.
- `photo.py`: Script for taking photos in the simulator environment.
- `show_spawn_points.py`: Displays spawn points in the CARLA simulator.
- `sync_mode.py`: Synchronization mode script for CARLA.
- `test.py`: Test script to run and verify the setup.
- `main_AAM.py`: Modified main script for LaneATT model to include AAM.
- `train_AAM.py`: Modified training script for UFLD model to include AAM.

## Usage



1. **Run CARLA Server:**
   Make sure the CARLA server is running before executing any scripts.

2. **Generate Traffic:**
   To generate traffic in the simulator, run:
   ```bash
   python generate_traffic.py
   ```

3. **Test the Setup:**
   To sample the data, run:

   ```bash
   python test.py
   ```



1. **Train LaneATT Model with AAM:**
   To train the LaneATT model with AAM, run:

   ```bash
   python main_AAM.py train --exp_name my_experiment --cfg config.yaml
   ```

2. **Train UFLD Model with AAM:**
   To train the UFLD model with AAM, run:

   ```bash
   python train_AAM.py
   ```

## Notes

- Ensure that the CARLA server is running before executing any scripts to avoid connection errors.
- Refer to the `readme.txt` files within each module directory for additional details and specific usage instructions.
- The high-attention areas (HAA) used in AAM are stored in the `haa_images` directory.
