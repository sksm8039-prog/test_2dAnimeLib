"""
SciTech2D - Master Science and Technology Animation Engine
Compiled for WebAssembly (Pygbag) and native Python desktop execution.
"""

import sys
import math
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Tuple
import pygame

# ==============================================================================
# 1. METADATA REGISTRY (ALL 100 ANIMATIONS)
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
    58: AnimationSpec(58, "Karman Vortex Street", "Fluid Dynamics", 6.0, "Vortex Shedding", "Periodic shed vortices forming wake pattern."),
    59: AnimationSpec(59, "Brownian Motion Chamber", "Statistical Physics", 5.0, "Random Walk", "Kinetic jitter of particle bombarded by invisible atoms."),
    60: AnimationSpec(60, "Van de Graaff Generator", "Electrostatics", 4.0, "Charge Transport", "Conveyor belt charging dome up to arc threshold."),
    61: AnimationSpec(61, "Gravitational Slingshot", "Astrodynamics", 8.0, "Hyperbolic Flyby", "Spacecraft stealing orbital energy from planet."),
    62: AnimationSpec(62, "Lagrange Points", "Orbital Mechanics", 10.0, "Equipotential", "L1-L5 gravitational saddle points with halo probe."),
    63: AnimationSpec(63, "Ion Thruster Engine", "Space Propulsion", 4.0, "Plasma Glow", "Electrostatic acceleration of xenon ions."),
    64: AnimationSpec(64, "Exoplanet Transit Curve", "Astronomy", 8.0, "Light Curve Dip", "Planetary occultation creating photometric drop."),
    65: AnimationSpec(65, "Solar Flare Loop", "Solar Physics", 6.0, "Magnetic Arc", "Magnetic reconnection erupting high-energy coronal plasma."),
    66: AnimationSpec(66, "Lunar Phases & Eclipse", "Astronomy", 12.0, "Shadow Geometry", "Umbra and penumbra geometry creating eclipses."),
    67: AnimationSpec(67, "Planetary Ring Shepherds", "Celestial Mechanics", 8.0, "Resonant Clearing", "Moons gravitationally confining narrow ringlet borders."),
    68: AnimationSpec(68, "Asteroid Impactor", "Planetary Defense", 7.0, "Kinetic Deflection", "Kinetic impact altering orbital trajectory."),
    69: AnimationSpec(69, "Geneva Drive", "Machine Kinematics", 4.0, "Maltese Intermittent", "Continuous drive pin stepping intermittent gear wheel."),
    70: AnimationSpec(70, "Planetary Gear Train", "Mechanical Engineering", 6.0, "Epicyclic Motion", "Sun, planet, and ring gears rotating in synchronization."),
    71: AnimationSpec(71, "Turbofan Jet Engine", "Aerospace Engineering", 5.0, "Continuous Brayton", "Compressor, combustor, and bypass flow streams."),
    72: AnimationSpec(72, "Hydraulic Press", "Fluid Mechanics", 6.0, "Force Multiplication", "Pascal's principle multiplying load force via liquid."),
    73: AnimationSpec(73, "Centrifugal Governor", "Control Systems", 4.0, "Centrifugal Flyball", "Rotating flyweights throttling steam flow."),
    74: AnimationSpec(74, "Automotive Differential", "Mechanical Engineering", 6.0, "Speed Split", "Bevel spider gears compensating wheel velocities."),
    75: AnimationSpec(75, "Structural Truss Load", "Civil Engineering", 8.0, "Stress Distribution", "Dynamic tension and compression load redistribution."),
    76: AnimationSpec(76, "Hovercraft Skirt Plenum", "Marine Engineering", 5.0, "Air Cushion", "Lift fan pressurizing flexible curtain."),
    77: AnimationSpec(77, "Bloch Sphere Qubit", "Quantum Computing", 6.0, "State Rotation", "State vector evolving under quantum logic gates."),
    78: AnimationSpec(78, "555 Timer Circuit", "Analog Electronics", 4.0, "Astable Oscillation", "Capacitor charging curves outputting clock pulses."),
    79: AnimationSpec(79, "Dipole Antenna Radiation", "Electromagnetics", 3.0, "EM Wavelet", "Toroidal electromagnetic fields shedding into space."),
    80: AnimationSpec(80, "MOSFET Switch", "Semiconductors", 4.0, "Channel Inversion", "Gate voltage toggling source-to-drain channel."),
    81: AnimationSpec(81, "Superconducting Levitation", "Quantum Materials", 5.0, "Meissner Flux", "Flux lines expelled around levitating superconductor."),
    82: AnimationSpec(82, "Electrical Transformer", "Power Systems", 4.0, "Inductive Coupling", "Primary coil inducing magnetic flux to secondary winding."),
    83: AnimationSpec(83, "LiDAR Scanner", "Sensors", 5.0, "ToF Point Cloud", "Rotating laser rays mapping 2D obstacle vectors."),
    84: AnimationSpec(84, "7-Segment Display", "Digital Logic", 7.0, "BCD Decoding", "Binary counter cycling decimal glyphs."),
    85: AnimationSpec(85, "CRISPR-Cas9 Complex", "Biotechnology", 10.0, "Target Cleavage", "Guide RNA locating and cleaving double-stranded target."),
    86: AnimationSpec(86, "Enzyme Catalysis", "Biochemistry", 6.0, "Induced Fit", "Substrate binding active site to yield reaction products."),
    87: AnimationSpec(87, "Hemodialysis Machine", "Biomedical Tech", 8.0, "Countercurrent Dialysis", "Toxin diffusion across semipermeable membrane tubes."),
    88: AnimationSpec(88, "PCR Thermal Cycler", "Molecular Biology", 9.0, "Thermal Denature", "Cyclic denaturation, annealing, and polymerisation."),
    89: AnimationSpec(89, "Centrifuge Gradient", "Laboratory Tech", 6.0, "Centrifugal Separation", "Blood separating into distinct density layers."),
    90: AnimationSpec(90, "Synaptic Exocytosis", "Neuroscience", 5.0, "Neurotransmission", "Vesicles fusing to synaptic cleft upon calcium trigger."),
    91: AnimationSpec(91, "Syringe Infusion Pump", "Medical Devices", 6.0, "Precision Dispense", "Lead screw stepping fluid displacement."),
    92: AnimationSpec(92, "Microfluidic Chip", "Nanotechnology", 5.0, "Laminar Droplets", "Micro-channel droplet generators creating uniform emulsion."),
    93: AnimationSpec(93, "Subduction Zone", "Geophysics", 10.0, "Crustal Subduction", "Oceanic plate sinking to fuel volcanic arc."),
    94: AnimationSpec(94, "Hydrogen PEM Fuel Cell", "Clean Energy", 6.0, "Proton Transport", "H2 oxidation and oxygen reduction forming H2O."),
    95: AnimationSpec(95, "Cyclone Core", "Meteorology", 8.0, "Coriolis Vortex", "Atmospheric storm eye with inward spiral bands."),
    96: AnimationSpec(96, "Coriolis Flow Meter", "Instrumentation", 4.0, "Vibrational Shift", "Phase difference across vibrating U-tube measuring mass flow."),
    97: AnimationSpec(97, "Tidal Barrage", "Renewable Energy", 8.0, "Bidirectional Turbine", "Head differential driving reversible hydro-turbines."),
    98: AnimationSpec(98, "Geyser Eruption", "Hydrogeology", 6.0, "Flash Evaporation", "Superheated underground column flashing into steam column."),
    99: AnimationSpec(99, "Oscillating Water Column", "Ocean Energy", 5.0, "Wells Air Turbine", "Ocean wave compression driving bidirectional turbine."),
    100: AnimationSpec(100, "Direct Air Capture", "Environmental Tech", 6.0, "Adsorption Cycle", "Air stream passing over chemical binding substrates.")
}

# ==============================================================================
# 2. ANIMATION BASE CLASS & RENDERING ENGINES
# ==============================================================================

class BaseSciTechAnimation:
    def __init__(self, spec: AnimationSpec, width: int = 800, height: int = 600):
        self.spec = spec
        self.width = width
        self.height = height
        self.elapsed_time = 0.0

    def reset(self):
        self.elapsed_time = 0.0

    def update(self, dt: float):
        self.elapsed_time += dt
        if self.elapsed_time > self.spec.duration:
            self.elapsed_time %= self.spec.duration

    def render(self, surface: pygame.Surface):
        raise NotImplementedError

class DoublePendulumAnimation(BaseSciTechAnimation):
    """Numerical Runge-Kutta 4th Order Chaotic Double Pendulum."""
    def __init__(self, spec: AnimationSpec, width: int, height: int):
        super().__init__(spec, width, height)
        self.l1, self.l2 = 120.0, 110.0
        self.m1, self.m2 = 10.0, 10.0
        self.g = 9.81 * 40.0
        self.state = [math.pi / 2.0, math.pi / 2.0, 0.0, 0.0]
        self.trail: List[Tuple[float, float]] = []

    def _derivatives(self, state):
        th1, th2, w1, w2 = state
        dth = th1 - th2
        den1 = (2 * self.m1 + self.m2 - self.m2 * math.cos(2 * th1 - 2 * th2))
        num1 = -self.g * (2 * self.m1 + self.m2) * math.sin(th1) - self.m2 * self.g * math.sin(th1 - 2 * th2)
        num1 -= 2 * math.sin(dth) * self.m2 * (w2**2 * self.l2 + w1**2 * self.l1 * math.cos(dth))
        alpha1 = num1 / (self.l1 * den1)

        num2 = 2 * math.sin(dth) * (w1**2 * self.l1 * (self.m1 + self.m2) + self.g * (self.m1 + self.m2) * math.cos(th1) + w2**2 * self.l2 * self.m2 * math.cos(dth))
        alpha2 = num2 / (self.l2 * den1)
        return [w1, w2, alpha1, alpha2]

    def update(self, dt: float):
        super().update(dt)
        sub_dt = dt / 4.0
        for _ in range(4):
            k1 = self._derivatives(self.state)
            s2 = [s + 0.5 * sub_dt * k for s, k in zip(self.state, k1)]
            k2 = self._derivatives(s2)
            s3 = [s + 0.5 * sub_dt * k for s, k in zip(self.state, k2)]
            k3 = self._derivatives(s3)
            s4 = [s + sub_dt * k for s, k in zip(self.state, k3)]
            k4 = self._derivatives(s4)
            self.state = [s + (sub_dt / 6.0) * (a + 2*b + 2*c + d) for s, a, b, c, d in zip(self.state, k1, k2, k3, k4)]

        cx, cy = self.width // 2, self.height // 3
        x1 = cx + self.l1 * math.sin(self.state[0])
        y1 = cy + self.l1 * math.cos(self.state[0])
        x2 = x1 + self.l2 * math.sin(self.state[1])
        y2 = y1 + self.l2 * math.cos(self.state[1])
        self.trail.append((x2, y2))
        if len(self.trail) > 120:
            self.trail.pop(0)

    def render(self, surface: pygame.Surface):
        cx, cy = self.width // 2, self.height // 3
        x1 = cx + self.l1 * math.sin(self.state[0])
        y1 = cy + self.l1 * math.cos(self.state[0])
        x2 = x1 + self.l2 * math.sin(self.state[1])
        y2 = y1 + self.l2 * math.cos(self.state[1])

        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                pygame.draw.line(surface, (0, min(255, alpha + 60), 255), self.trail[i], self.trail[i+1], 2)

        pygame.draw.circle(surface, (180, 180, 180), (cx, cy), 6)
        pygame.draw.line(surface, (220, 220, 220), (cx, cy), (int(x1), int(y1)), 4)
        pygame.draw.circle(surface, (255, 100, 100), (int(x1), int(y1)), 12)
        pygame.draw.line(surface, (220, 220, 220), (int(x1), int(y1)), (int(x2), int(y2)), 3)
        pygame.draw.circle(surface, (100, 255, 100), (int(x2), int(y2)), 10)

class BohrAtomAnimation(BaseSciTechAnimation):
    """Bohr Atom Model with Quantized Orbits and Radiative Photons."""
    def render(self, surface: pygame.Surface):
        cx, cy = self.width // 2, self.height // 2
        pygame.draw.circle(surface, (255, 50, 50), (cx, cy), 16)
        pygame.draw.circle(surface, (255, 200, 50), (cx + 4, cy - 4), 6)

        radii = [60, 110, 160]
        speeds = [3.0, 1.8, 1.1]
        for idx, (r, spd) in enumerate(zip(radii, speeds)):
            pygame.draw.circle(surface, (60, 80, 120), (cx, cy), r, 1)
            angle = self.elapsed_time * spd + (idx * 2.1)
            ex = cx + r * math.cos(angle)
            ey = cy + r * math.sin(angle)
            pygame.draw.circle(surface, (0, 180, 255), (int(ex), int(ey)), 6)
            pygame.draw.circle(surface, (180, 240, 255), (int(ex), int(ey)), 2)

            wave_phase = (self.elapsed_time * 2.0 + idx) % 3.0
            if wave_phase < 1.0:
                pw_x = ex + wave_phase * 60.0 * math.cos(angle + math.pi/2)
                pw_y = ey + wave_phase * 60.0 * math.sin(angle + math.pi/2)
                pygame.draw.circle(surface, (255, 255, 100), (int(pw_x), int(pw_y)), 3)

class WaveInterferenceAnimation(BaseSciTechAnimation):
    """Young's Double-Slit Wave Interference Propagation."""
    def render(self, surface: pygame.Surface):
        cx, cy = self.width // 2, self.height // 2
        slit_y1, slit_y2 = cy - 40, cy + 40
        slit_x = cx - 140

        pygame.draw.line(surface, (180, 180, 180), (slit_x, 50), (slit_x, slit_y1 - 10), 6)
        pygame.draw.line(surface, (180, 180, 180), (slit_x, slit_y1 + 10), (slit_x, slit_y2 - 10), 6)
        pygame.draw.line(surface, (180, 180, 180), (slit_x, slit_y2 + 10), (slit_x, self.height - 50), 6)

        max_r = 240
        speed = 80.0
        for r_base in range(0, max_r, 20):
            r = (r_base + self.elapsed_time * speed) % max_r
            alpha = max(0, min(255, int(255 * (1.0 - r / max_r))))
            color = (0, int(alpha * 0.8), alpha)
            pygame.draw.arc(surface, color, (slit_x - r, slit_y1 - r, 2*r, 2*r), -math.pi/2, math.pi/2, 2)
            pygame.draw.arc(surface, color, (slit_x - r, slit_y2 - r, 2*r, 2*r), -math.pi/2, math.pi/2, 2)

        screen_x = slit_x + 240
        pygame.draw.line(surface, (240, 240, 240), (screen_x, 60), (screen_x, self.height - 60), 4)
        for y in range(80, self.height - 80, 4):
            d1 = math.hypot(screen_x - slit_x, y - slit_y1)
            d2 = math.hypot(screen_x - slit_x, y - slit_y2)
            phase_diff = 2.0 * math.pi * (d1 - d2) / 20.0
            intensity = (math.cos(phase_diff) + 1.0) / 2.0
            c = int(255 * intensity)
            pygame.draw.line(surface, (c, c, 50), (screen_x + 5, y), (screen_x + 5 + int(40 * intensity), y), 2)

class UniversalProceduralAnimation(BaseSciTechAnimation):
    """Domain-themed vector kinematics engine for all other systems."""
    def render(self, surface: pygame.Surface):
        cx, cy = self.width // 2, self.height // 2
        t = self.elapsed_time
        domain = self.spec.domain

        if any(k in domain for k in ["Mechanics", "Kinematics", "Robotics", "Engineering"]):
            radius, teeth = 80, 12
            pygame.draw.circle(surface, (90, 100, 115), (cx, cy), radius, 4)
            for i in range(teeth):
                ang = (2 * math.pi / teeth) * i + t * 1.5
                tx = cx + (radius + 8) * math.cos(ang)
                ty = cy + (radius + 8) * math.sin(ang)
                pygame.draw.circle(surface, (160, 175, 190), (int(tx), int(ty)), 6)
            arm_x = cx + radius * math.cos(-t * 1.5)
            arm_y = cy + radius * math.sin(-t * 1.5)
            pygame.draw.line(surface, (255, 140, 0), (cx, cy), (int(arm_x), int(arm_y)), 6)
            pygame.draw.circle(surface, (255, 200, 50), (int(arm_x), int(arm_y)), 10)

        elif any(k in domain for k in ["Astrophysics", "Astronomy", "Astro", "Space"]):
            pygame.draw.circle(surface, (255, 220, 80), (cx, cy), 28)
            for idx, r in enumerate([90, 150, 210]):
                pygame.draw.ellipse(surface, (50, 70, 100), (cx - r, cy - r // 2, 2 * r, r), 1)
                ang = t * (2.0 / (idx + 1))
                px = cx + r * math.cos(ang)
                py = cy + (r // 2) * math.sin(ang)
                pygame.draw.circle(surface, (100, 200, 255), (int(px), int(py)), 7 - idx)

        elif any(k in domain for k in ["Electronics", "Computing", "Sensors", "Telecommunications"]):
            for i, y_off in enumerate([-80, 0, 80]):
                y = cy + y_off
                pygame.draw.line(surface, (40, 80, 50), (100, y), (self.width - 100, y), 2)
                pulse_x = 100 + ((t * 180 + i * 90) % (self.width - 200))
                pygame.draw.rect(surface, (0, 255, 120), (int(pulse_x), y - 18, 30, 18))
                pygame.draw.circle(surface, (0, 255, 200), (int(pulse_x + 15), y), 5)

        else:
            for i in range(8):
                ang = t * 0.8 + (2 * math.pi / 8) * i
                dist = 90 + 30 * math.sin(t * 3.0 + i)
                nx = cx + dist * math.cos(ang)
                ny = cy + dist * math.sin(ang)
                pygame.draw.line(surface, (80, 120, 160), (cx, cy), (int(nx), int(ny)), 2)
                pygame.draw.circle(surface, (240, 80, 140), (int(nx), int(ny)), 10)
            pygame.draw.circle(surface, (80, 220, 180), (cx, cy), 18)

class AnimationFactory:
    @staticmethod
    def create(anim_id: int, width: int = 800, height: int = 600) -> BaseSciTechAnimation:
        spec = REGISTRY.get(anim_id, REGISTRY[1])
        if anim_id == 1:
            return DoublePendulumAnimation(spec, width, height)
        elif anim_id == 3:
            return BohrAtomAnimation(spec, width, height)
        elif anim_id in [10, 52]:
            return WaveInterferenceAnimation(spec, width, height)
        return UniversalProceduralAnimation(spec, width, height)

# ==============================================================================
# 3. ASYNC RUNTIME ENGINE (WEB & DESKTOP COMPATIBLE)
# ==============================================================================

class SciTechEngine:
    def __init__(self, width: int = 850, height: int = 620):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("SciTech2D: 100 Science & Technology Systems")
        self.clock = pygame.time.Clock()

        # Using system-agnostic default font for WebAssembly safety
        self.font_title = pygame.font.Font(None, 24)
        self.font_ui = pygame.font.Font(None, 18)

        self.current_id = 1
        self.current_anim = AnimationFactory.create(self.current_id, self.width, self.height)
        self.paused = False

    def set_animation(self, anim_id: int):
        self.current_id = max(1, min(100, anim_id))
        self.current_anim = AnimationFactory.create(self.current_id, self.width, self.height)
        self.current_anim.reset()

    async def run_async(self):
        """Asynchronous execution loop required by Pygbag / WebAssembly."""
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_RIGHT:
                        self.set_animation(self.current_id + 1)
                    elif event.key == pygame.K_LEFT:
                        self.set_animation(self.current_id - 1)
                    elif event.key == pygame.K_r:
                        self.current_anim.reset()

            if not self.paused:
                self.current_anim.update(dt)

            self.screen.fill((18, 22, 28))
            self.current_anim.render(self.screen)
            self._render_overlay()

            pygame.display.flip()
            # Non-blocking yield for browser event loop
            await asyncio.sleep(0)

        pygame.quit()
        sys.exit()

    def _render_overlay(self):
        spec = self.current_anim.spec
        title_text = f"[{spec.id:03d}/100] {spec.name.upper()}"
        domain_text = f"DOMAIN: {spec.domain} | LOOP DURATION: {spec.duration:.1f}s | TYPE: {spec.loop_type}"

        t_surf = self.font_title.render(title_text, True, (240, 240, 240))
        d_surf = self.font_ui.render(domain_text, True, (120, 200, 255))
        self.screen.blit(t_surf, (20, 16))
        self.screen.blit(d_surf, (20, 42))

        bar_x, bar_y, bar_w, bar_h = 20, self.height - 35, self.width - 40, 6
        progress = (self.current_anim.elapsed_time % spec.duration) / spec.duration
        pygame.draw.rect(self.screen, (50, 60, 75), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        pygame.draw.rect(self.screen, (0, 220, 160), (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=3)

        info_text = f"Time: {self.current_anim.elapsed_time:.2f}s / {spec.duration:.1f}s | [LEFT/RIGHT]: Switch | [SPACE]: Pause | [R]: Reset"
        i_surf = self.font_ui.render(info_text, True, (160, 170, 185))
        self.screen.blit(i_surf, (20, self.height - 24))

def main():
    engine = SciTechEngine(width=850, height=620)
    asyncio.run(engine.run_async())

if __name__ == "__main__":
    main()
