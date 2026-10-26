"""
SciTech2D - Master Science and Technology Animation Engine
WebAssembly-stabilized (flicker-free) with full mouse/touch GUI controls.
"""

import sys
import math
import random
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Tuple
import pygame

# ==============================================================================
# 1. METADATA REGISTRY (100 SYSTEMS)
# ==============================================================================

@dataclass
class AnimationSpec:
    id: int
    name: str
    domain: str
    duration: float
    loop_type: str
    description: str

REGISTRY: Dict[int, AnimationSpec] = {
    1: AnimationSpec(1, "Double Pendulum", "Classical Mechanics", 10.0, "Chaotic", "Non-linear chaotic double pendulum via RK4 integration."),
    2: AnimationSpec(2, "Spring-Mass Damper System", "Classical Mechanics", 4.0, "Damped Periodic", "Harmonic oscillator with viscous damping."),
    3: AnimationSpec(3, "Bohr / Rutherford Atom Model", "Quantum Physics", 3.0, "Periodic Orbit", "Quantized orbital electrons with spontaneous emissions."),
    4: AnimationSpec(4, "Optical Prism Dispersion", "Optics", 5.0, "Refraction Sweep", "Snell's Law wavelength dispersion across prism."),
    5: AnimationSpec(5, "Convex & Concave Lenses", "Geometric Optics", 6.0, "Ray Tracing", "Ray matrix propagation showing focal conversions."),
    6: AnimationSpec(6, "Aerodynamic Airfoil", "Fluid Dynamics", 4.0, "Streamline Flow", "Bernoulli streamlines showing velocity differentials."),
    7: AnimationSpec(7, "Piston-Cylinder Heat Engine", "Thermodynamics", 4.0, "4-Stroke Periodic", "4-stroke internal combustion cycle with pressure dynamics."),
    8: AnimationSpec(8, "Particle Accelerator", "High Energy Physics", 5.0, "Relativistic Loop", "Synchrotron RF cavities accelerating charged particles."),
    9: AnimationSpec(9, "Bar Magnet & Field Lines", "Electromagnetism", 6.0, "Dipole Field", "Vector dipole field interacting with compass probes."),
    10: AnimationSpec(10, "Standing Wave Generator", "Wave Mechanics", 3.0, "Harmonic Mode", "Superposition forming nodes and antinodes."),
    11: AnimationSpec(11, "Keplerian Solar System", "Astrophysics", 12.0, "Orbital Mechanics", "N-body elliptical orbits following Kepler's 2nd law."),
    12: AnimationSpec(12, "Multi-Stage Rocket", "Aerospace Engineering", 15.0, "Sequential Phase", "Rocket launch, staging separation, and burn plumes."),
    13: AnimationSpec(13, "Artificial Satellite (CubeSat)", "Astronautics", 8.0, "Orbital Pass", "Solar wing deployment and ground telemetry pulses."),
    14: AnimationSpec(14, "Black Hole Accretion Disk", "Relativistic Astro", 6.0, "Vortex Flow", "Doppler beaming and relativistic curvature."),
    15: AnimationSpec(15, "Mars Rover Rocker-Bogie", "Robotics", 8.0, "Kinematic Drive", "Passive articulated suspension over rough terrain."),
    16: AnimationSpec(16, "Lunar Lander Descent", "Orbital Mechanics", 10.0, "Newtonian Landing", "Thrust-vectoring lunar soft touchdown."),
    17: AnimationSpec(17, "Radio Telescope Array", "Astronomy", 7.0, "Phased Slew", "Coordinated parabolic dishes focusing on coordinates."),
    18: AnimationSpec(18, "Pulsar / Neutron Star", "Astrophysics", 2.0, "Periodic Lighthouse", "Rapid relativistic cone sweep from magnetic poles."),
    19: AnimationSpec(19, "DNA Double Helix", "Molecular Biology", 6.0, "Helical Unzip", "Replication fork unzipping base pairs."),
    20: AnimationSpec(20, "Water Molecule Network", "Chemistry", 4.0, "Dynamic Bonding", "Polar hydrogen bonding networks forming and cleaving."),
    21: AnimationSpec(21, "Graphene Hexagonal Lattice", "Materials Science", 5.0, "Tensile Stress", "Carbon sp2 honeycomb structure under load."),
    22: AnimationSpec(22, "Electrochemical Cell", "Physical Chemistry", 6.0, "Ion Diffusion", "Cathode-anode redox balance and ion migration."),
    23: AnimationSpec(23, "Chemical Titration Setup", "Analytical Chemistry", 8.0, "Drop Reaction", "Volumetric burette dispensing to equivalence point."),
    24: AnimationSpec(24, "Buckyball (C60) Molecule", "Nanotechnology", 6.0, "Cage Rotation", "3D-projected rotating truncated icosahedron."),
    25: AnimationSpec(25, "Ideal Gas Chamber", "Statistical Mechanics", 5.0, "Kinetic Collisions", "Elastic molecular collisions exhibiting Maxwell-Boltzmann distribution."),
    26: AnimationSpec(26, "Logic Gate Circuit", "Digital Electronics", 4.0, "Digital Propagation", "High/Low logic levels propagating through gates."),
    27: AnimationSpec(27, "Microprocessor CPU Die", "Computer Architecture", 6.0, "Bus Multiplexing", "ALU, register files, and data bus activity."),
    28: AnimationSpec(28, "Printed Circuit Board (PCB)", "Electronics", 5.0, "Pulse Network", "High-frequency signal packets along PCB traces."),
    29: AnimationSpec(29, "Oscilloscope Display", "Instrumentation", 4.0, "CRT Raster", "Lissajous figures and triggered frequency waveforms."),
    30: AnimationSpec(30, "2-Link Robotic Arm", "Robotics", 6.0, "Inverse Kinematics", "End-effector trajectory tracking via inverse kinematics."),
    31: AnimationSpec(31, "Artificial Neural Network", "Machine Learning", 5.0, "Layer Activation", "Synaptic weight propagation and node activation."),
    32: AnimationSpec(32, "Fiber Optic Cable", "Telecommunications", 4.0, "Total Reflection", "Light rays undergoing total internal reflection."),
    33: AnimationSpec(33, "Radar Sweep Display", "Electromagnetics", 4.0, "Phosphor Sweep", "Radial antenna scan revealing target echoes."),
    34: AnimationSpec(34, "Binary Search Tree", "Computer Science", 8.0, "Tree Traversal", "Recursive node search and dynamic self-balancing."),
    35: AnimationSpec(35, "QR Code Scanner", "Optoelectronics", 3.0, "Linear Raster", "Laser sweep parsing matrix alignment markers."),
    36: AnimationSpec(36, "Biological Cell", "Cytology", 10.0, "Organelle Transit", "Endoplasmic reticulum and vesicle transport."),
    37: AnimationSpec(37, "Biological Neuron", "Neuroscience", 3.0, "Axonal Impulse", "Action potential propagation along Ranvier nodes."),
    38: AnimationSpec(38, "Bacteriophage Virus", "Virology", 8.0, "Viral Injection", "Phage tail contraction injecting DNA into host."),
    39: AnimationSpec(39, "Electrocardiogram (ECG)", "Biomedical Tech", 4.0, "PQRST Sweep", "Sinoatrial node depolarization plotting rhythm trace."),
    40: AnimationSpec(40, "Capillary Blood Flow", "Hematology", 5.0, "Microcirculation", "Erythrocytes deforming through micro-capillary."),
    41: AnimationSpec(41, "MRI Scanner Bore", "Medical Imaging", 6.0, "Spin Precession", "RF excitation and spin-lattice relaxation."),
    42: AnimationSpec(42, "Bionic Prosthetic Hand", "Biomechatronics", 5.0, "Tendon Pull", "Actuated finger joints articulating grasp modes."),
    43: AnimationSpec(43, "Wind Turbine", "Renewable Energy", 4.0, "Aerodynamic Rotation", "Pitch-controlled blades generating wake turbulence."),
    44: AnimationSpec(44, "Photovoltaic Solar Cell", "Solid-State Physics", 4.0, "Charge Separation", "Photons exciting electron-hole pairs across p-n junction."),
    45: AnimationSpec(45, "Nuclear Reactor Core", "Nuclear Engineering", 8.0, "Neutron Flux", "Control rod actuation damping fission rate."),
    46: AnimationSpec(46, "Hydroelectric Dam Turbine", "Hydraulic Power", 6.0, "Fluid Momentum", "Water head pressure driving Francis turbine runners."),
    47: AnimationSpec(47, "Seismograph", "Geophysics", 7.0, "Oscillatory Drum", "Inertial mass recording P and S seismic tremors."),
    48: AnimationSpec(48, "Geothermal Power Loop", "Thermodynamics", 8.0, "Rankine Cycle", "Underground hydrothermal steam driving generator."),
    49: AnimationSpec(49, "Atmospheric Water Cycle", "Meteorology", 10.0, "Convective Loop", "Evaporation, condensation, and precipitation."),
    50: AnimationSpec(50, "EV Powertrain", "Automotive Tech", 6.0, "3-Phase Induction", "Inverter vector control driving stator rotor."),
    51: AnimationSpec(51, "Newton's Cradle", "Classical Mechanics", 4.0, "Elastic Impact", "Conservation of momentum across metal spheres."),
    52: AnimationSpec(52, "Young's Double-Slit", "Wave Optics", 6.0, "Interference", "Diffracted coherent wave interference fringes."),
    53: AnimationSpec(53, "Michelson Interferometer", "Optics", 5.0, "Phase Fringe", "Coherent beam recombining to produce fringe shifts."),
    54: AnimationSpec(54, "Stirling Engine", "Thermodynamics", 3.0, "Closed Regenerative", "Displacer and power pistons alternating in heat expansion."),
    55: AnimationSpec(55, "Cathode Ray Tube (CRT)", "Electronics", 5.0, "Beam Steering", "Electrostatic deflection plates aiming electron beam."),
    56: AnimationSpec(56, "Doppler Effect Emitter", "Acoustics", 6.0, "Wave Compression", "Moving transmitter compressing sound wavefronts."),
    57: AnimationSpec(57, "Gyroscope Stabilizer", "Classical Mechanics", 8.0, "Precession", "Spinning rotor demonstrating gyroscopic rigidity."),
    58: AnimationSpec(58, "Karman Vortex Street", "Fluid Dynamics", 6.0, "Vortex Shedding", "Periodic shed vo
