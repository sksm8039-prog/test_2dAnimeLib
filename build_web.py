import os
import json

class AnimationSpec:
    def __init__(self, anim_id, name, domain, duration, loop_type, description):
        self.id = anim_id
        self.name = name
        self.domain = domain
        self.duration = duration
        self.loop_type = loop_type
        self.description = description

RAW_DATA = [
    (1, "Double Pendulum", "Classical Mechanics", 10.0, "Chaotic", "Non-linear chaotic double pendulum via RK4 integration."),
    (2, "Spring-Mass Damper System", "Classical Mechanics", 4.0, "Damped Periodic", "Harmonic oscillator with viscous damping."),
    (3, "Bohr / Rutherford Atom Model", "Quantum Physics", 3.0, "Periodic Orbit", "Quantized orbital electrons with spontaneous emissions."),
    (4, "Optical Prism Dispersion", "Optics", 5.0, "Refraction Sweep", "Snell's Law wavelength dispersion across prism."),
    (5, "Convex & Concave Lenses", "Geometric Optics", 6.0, "Ray Tracing", "Ray matrix propagation showing focal conversions."),
    (6, "Aerodynamic Airfoil", "Fluid Dynamics", 4.0, "Streamline Flow", "Bernoulli streamlines showing velocity differentials."),
    (7, "Piston-Cylinder Heat Engine", "Thermodynamics", 4.0, "4-Stroke Periodic", "4-stroke internal combustion cycle with pressure dynamics."),
    (8, "Particle Accelerator", "High Energy Physics", 5.0, "Relativistic Loop", "Synchrotron RF cavities accelerating charged particles."),
    (9, "Bar Magnet & Field Lines", "Electromagnetism", 6.0, "Dipole Field", "Vector dipole field interacting with compass probes."),
    (10, "Standing Wave Generator", "Wave Mechanics", 3.0, "Harmonic Mode", "Superposition forming nodes and antinodes."),
    (11, "Keplerian Solar System", "Astrophysics", 12.0, "Orbital Mechanics", "N-body elliptical orbits following Kepler's 2nd law."),
    (12, "Multi-Stage Rocket", "Aerospace Engineering", 15.0, "Sequential Phase", "Rocket launch, staging separation, and burn plumes."),
    (13, "Artificial Satellite (CubeSat)", "Astronautics", 8.0, "Orbital Pass", "Solar wing deployment and ground telemetry pulses."),
    (14, "Black Hole Accretion Disk", "Relativistic Astro", 6.0, "Vortex Flow", "Doppler beaming and relativistic curvature."),
    (15, "Mars Rover Rocker-Bogie", "Robotics", 8.0, "Kinematic Drive", "Passive articulated suspension over rough terrain."),
    (16, "Lunar Lander Descent", "Orbital Mechanics", 10.0, "Newtonian Landing", "Thrust-vectoring lunar soft touchdown."),
    (17, "Radio Telescope Array", "Astronomy", 7.0, "Phased Slew", "Coordinated parabolic dishes focusing on coordinates."),
    (18, "Pulsar / Neutron Star", "Astrophysics", 2.0, "Periodic Lighthouse", "Rapid relativistic cone sweep from magnetic poles."),
    (19, "DNA Double Helix", "Molecular Biology", 6.0, "Helical Unzip", "Replication fork unzipping base pairs."),
    (20, "Water Molecule Network", "Chemistry", 4.0, "Dynamic Bonding", "Polar hydrogen bonding networks forming and cleaving."),
    (21, "Graphene Hexagonal Lattice", "Materials Science", 5.0, "Tensile Stress", "Carbon sp2 honeycomb structure under load."),
    (22, "Electrochemical Cell", "Physical Chemistry", 6.0, "Ion Diffusion", "Cathode-anode redox balance and ion migration."),
    (23, "Chemical Titration Setup", "Analytical Chemistry", 8.0, "Drop Reaction", "Volumetric burette dispensing to equivalence point."),
    (24, "Buckyball (C60) Molecule", "Nanotechnology", 6.0, "Cage Rotation", "3D-projected rotating truncated icosahedron."),
    (25, "Ideal Gas Chamber", "Statistical Mechanics", 5.0, "Kinetic Collisions", "Elastic molecular collisions exhibiting Maxwell-Boltzmann distribution."),
    (26, "Logic Gate Circuit", "Digital Electronics", 4.0, "Digital Propagation", "High/Low logic levels propagating through gates."),
    (27, "Microprocessor CPU Die", "Computer Architecture", 6.0, "Bus Multiplexing", "ALU, register files, and data bus activity."),
    (28, "Printed Circuit Board (PCB)", "Electronics", 5.0, "Pulse Network", "High-frequency signal packets along PCB traces."),
    (29, "Oscilloscope Display", "Instrumentation", 4.0, "CRT Raster", "Lissajous figures and triggered frequency waveforms."),
    (30, "2-Link Robotic Arm", "Robotics", 6.0, "Inverse Kinematics", "End-effector trajectory tracking via inverse kinematics."),
    (31, "Artificial Neural Network", "Machine Learning", 5.0, "Layer Activation", "Synaptic weight propagation and node activation."),
    (32, "Fiber Optic Cable", "Telecommunications", 4.0, "Total Reflection", "Light rays undergoing total internal reflection."),
    (33, "Radar Sweep Display", "Electromagnetics", 4.0, "Phosphor Sweep", "Radial antenna scan revealing target echoes."),
    (34, "Binary Search Tree", "Computer Science", 8.0, "Tree Traversal", "Recursive node search and dynamic self-balancing."),
    (35, "QR Code Scanner", "Optoelectronics", 3.0, "Linear Raster", "Laser sweep parsing matrix alignment markers."),
    (36, "Biological Cell", "Cytology", 10.0, "Organelle Transit", "Endoplasmic reticulum and vesicle transport."),
    (37, "Biological Neuron", "Neuroscience", 3.0, "Axonal Impulse", "Action potential propagation along Ranvier nodes."),
    (38, "Bacteriophage Virus", "Virology", 8.0, "Viral Injection", "Phage tail contraction injecting DNA into host."),
    (39, "Electrocardiogram (ECG)", "Biomedical Tech", 4.0, "PQRST Sweep", "Sinoatrial node depolarization plotting rhythm trace."),
    (40, "Capillary Blood Flow", "Hematology", 5.0, "Microcirculation", "Erythrocytes deforming through micro-capillary."),
    (41, "MRI Scanner Bore", "Medical Imaging", 6.0, "Spin Precession", "RF excitation and spin-lattice relaxation."),
    (42, "Bionic Prosthetic Hand", "Biomechatronics", 5.0, "Tendon Pull", "Actuated finger joints articulating grasp modes."),
    (43, "Wind Turbine", "Renewable Energy", 4.0, "Aerodynamic Rotation", "Pitch-controlled blades generating wake turbulence."),
    (44, "Photovoltaic Solar Cell", "Solid-State Physics", 4.0, "Charge Separation", "Photons exciting electron-hole pairs across p-n junction."),
    (45, "Nuclear Reactor Core", "Nuclear Engineering", 8.0, "Neutron Flux", "Control rod actuation damping fission rate."),
    (46, "Hydroelectric Dam Turbine", "Hydraulic Power", 6.0, "Fluid Momentum", "Water head pressure driving Francis turbine runners."),
    (47, "Seismograph", "Geophysics", 7.0, "Oscillatory Drum", "Inertial mass recording P and S seismic tremors."),
    (48, "Geothermal Power Loop", "Thermodynamics", 8.0, "Rankine Cycle", "Underground hydrothermal steam driving generator."),
    (49, "Atmospheric Water Cycle", "Meteorology", 10.0, "Convective Loop", "Evaporation, condensation, and precipitation."),
    (50, "EV Powertrain", "Automotive Tech", 6.0, "3-Phase Induction", "Inverter vector control driving stator rotor."),
    (51, "Newton's Cradle", "Classical Mechanics", 4.0, "Elastic Impact", "Conservation of momentum across metal spheres."),
    (52, "Young's Double-Slit", "Wave Optics", 6.0, "Interference", "Diffracted coherent wave interference fringes."),
    (53, "Michelson Interferometer", "Optics", 5.0, "Phase Fringe", "Coherent beam recombining to produce fringe shifts."),
    (54, "Stirling Engine", "Thermodynamics", 3.0, "Closed Regenerative", "Displacer and power pistons alternating in heat expansion."),
    (55, "Cathode Ray Tube (CRT)", "Electronics", 5.0, "Beam Steering", "Electrostatic deflection plates aiming electron beam."),
    (56, "Doppler Effect Emitter", "Acoustics", 6.0, "Wave Compression", "Moving transmitter compressing sound wavefronts."),
    (57, "Gyroscope Stabilizer", "Classical Mechanics", 8.0, "Precession", "Spinning rotor demonstrating gyroscopic rigidity."),
    (58, "Karman Vortex Street", "Fluid Dynamics", 6.0, "Vortex Shedding", "Periodic shed vortices forming wake pattern."),
    (59, "Brownian Motion Chamber", "Statistical Physics", 5.0, "Random Walk", "Kinetic jitter of particle bombarded by invisible atoms."),
    (60, "Van de Graaff Generator", "Electrostatics", 4.0, "Charge Transport", "Conveyor belt charging dome up to arc threshold."),
    (61, "Gravitational Slingshot", "Astrodynamics", 8.0, "Hyperbolic Flyby", "Spacecraft stealing orbital energy from planet."),
    (62, "Lagrange Points", "Orbital Mechanics", 10.0, "Equipotential", "L1-L5 gravitational saddle points with halo probe."),
    (63, "Ion Thruster Engine", "Space Propulsion", 4.0, "Plasma Glow", "Electrostatic acceleration of xenon ions."),
    (64, "Exoplanet Transit Curve", "Astronomy", 8.0, "Light Curve Dip", "Planetary occultation creating photometric drop."),
    (65, "Solar Flare Loop", "Solar Physics", 6.0, "Magnetic Arc", "Magnetic reconnection erupting high-energy coronal plasma."),
    (66, "Lunar Phases & Eclipse", "Astronomy", 12.0, "Shadow Geometry", "Umbra and penumbra geometry creating eclipses."),
    (67, "Planetary Ring Shepherds", "Celestial Mechanics", 8.0, "Resonant Clearing", "Moons gravitationally confining narrow ringlet borders."),
    (68, "Asteroid Impactor", "Planetary Defense", 7.0, "Kinetic Deflection", "Kinetic impact altering orbital trajectory."),
    (69, "Geneva Drive", "Machine Kinematics", 4.0, "Maltese Intermittent", "Continuous drive pin stepping intermittent gear wheel."),
    (70, "Planetary Gear Train", "Mechanical Engineering", 6.0, "Epicyclic Motion", "Sun, planet, and ring gears rotating in synchronization."),
    (71, "Turbofan Jet Engine", "Aerospace Engineering", 5.0, "Continuous Brayton", "Compressor, combustor, and bypass flow streams."),
    (72, "Hydraulic Press", "Fluid Mechanics", 6.0, "Force Multiplication", "Pascal's principle multiplying load force via liquid."),
    (73, "Centrifugal Governor", "Control Systems", 4.0, "Centrifugal Flyball", "Rotating flyweights throttling steam flow."),
    (74, "Automotive Differential", "Mechanical Engineering", 6.0, "Speed Split", "Bevel spider gears compensating wheel velocities."),
    (75, "Structural Truss Load", "Civil Engineering", 8.0, "Stress Distribution", "Dynamic tension and compression load redistribution."),
    (76, "Hovercraft Skirt Plenum", "Marine Engineering", 5.0, "Air Cushion", "Lift fan pressurizing flexible curtain."),
    (77, "Bloch Sphere Qubit", "Quantum Computing", 6.0, "State Rotation", "State vector evolving under quantum logic gates."),
    (78, "555 Timer Circuit", "Analog Electronics", 4.0, "Astable Oscillation", "Capacitor charging curves outputting clock pulses."),
    (79, "Dipole Antenna Radiation", "Electromagnetics", 3.0, "EM Wavelet", "Toroidal electromagnetic fields shedding into space."),
    (80, "MOSFET Switch", "Semiconductors", 4.0, "Channel Inversion", "Gate voltage toggling source-to-drain channel."),
    (81, "Superconducting Levitation", "Quantum Materials", 5.0, "Meissner Flux", "Flux lines expelled around levitating superconductor."),
    (82, "Electrical Transformer", "Power Systems", 4.0, "Inductive Coupling", "Primary coil inducing magnetic flux to secondary winding."),
    (83, "LiDAR Scanner", "Sensors", 5.0, "ToF Point Cloud", "Rotating laser rays mapping 2D obstacle vectors."),
    (84, "7-Segment Display", "Digital Logic", 7.0, "BCD Decoding", "Binary counter cycling decimal glyphs."),
    (85, "CRISPR-Cas9 Complex", "Biotechnology", 10.0, "Target Cleavage", "Guide RNA locating and cleaving double-stranded target."),
    (86, "Enzyme Catalysis", "Biochemistry", 6.0, "Induced Fit", "Substrate binding active site to yield reaction products."),
    (87, "Hemodialysis Machine", "Biomedical Tech", 8.0, "Countercurrent Dialysis", "Toxin diffusion across semipermeable membrane tubes."),
    (88, "PCR Thermal Cycler", "Molecular Biology", 9.0, "Thermal Denature", "Cyclic denaturation, annealing, and polymerisation."),
    (89, "Centrifuge Gradient", "Laboratory Tech", 6.0, "Centrifugal Separation", "Blood separating into distinct density layers."),
    (90, "Synaptic Exocytosis", "Neuroscience", 5.0, "Neurotransmission", "Vesicles fusing to synaptic cleft upon calcium trigger."),
    (91, "Syringe Infusion Pump", "Medical Devices", 6.0, "Precision Dispense", "Lead screw stepping fluid displacement."),
    (92, "Microfluidic Chip", "Nanotechnology", 5.0, "Laminar Droplets", "Micro-channel droplet generators creating uniform emulsion."),
    (93, "Subduction Zone", "Geophysics", 10.0, "Crustal Subduction", "Oceanic plate sinking to fuel volcanic arc."),
    (94, "Hydrogen PEM Fuel Cell", "Clean Energy", 6.0, "Proton Transport", "H2 oxidation and oxygen reduction forming H2O."),
    (95, "Cyclone Core", "Meteorology", 8.0, "Coriolis Vortex", "Atmospheric storm eye with inward spiral bands."),
    (96, "Coriolis Flow Meter", "Instrumentation", 4.0, "Vibrational Shift", "Phase difference across vibrating U-tube measuring mass flow."),
    (97, "Tidal Barrage", "Renewable Energy", 8.0, "Bidirectional Turbine", "Head differential driving reversible hydro-turbines."),
    (98, "Geyser Eruption", "Hydrogeology", 6.0, "Flash Evaporation", "Superheated underground column flashing into steam column."),
    (99, "Oscillating Water Column", "Ocean Energy", 5.0, "Wells Air Turbine", "Ocean wave compression driving bidirectional turbine."),
    (100, "Direct Air Capture", "Environmental Tech", 6.0, "Adsorption Cycle", "Air stream passing over chemical binding substrates.")
]

REGISTRY = {row[0]: AnimationSpec(*row) for row in RAW_DATA}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SciTech2D: 100 Science & Technology Animations</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body {
      background-color: #0d1117;
      color: #e6edf3;
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 16px;
    }
    .app-container {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.6);
      max-width: 900px;
      width: 100%;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid #21262d;
    }
    .title-box h1 { font-size: 1.25rem; color: #f0f6fc; }
    .title-box p { font-size: 0.85rem; color: #58a6ff; margin-top: 4px; }
    select.anim-select {
      background: #21262d;
      color: #f0f6fc;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 0.9rem;
      cursor: pointer;
    }
    .canvas-wrapper {
      width: 100%;
      display: flex;
      justify-content: center;
      background: #12161c;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid #21262d;
    }
    canvas { display: block; max-width: 100%; height: auto; }
    .progress-container {
      width: 100%;
      height: 8px;
      background: #21262d;
      border-radius: 4px;
      margin: 14px 0;
      overflow: hidden;
    }
    .progress-bar {
      height: 100%;
      background: linear-gradient(90deg, #00dca0, #58a6ff);
      width: 0%;
    }
    .controls {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
    }
    .btn-group { display: flex; flex-wrap: wrap; gap: 8px; }
    button.ctrl-btn {
      background: #21262d;
      color: #e6edf3;
      border: 1px solid #30363d;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
    }
    button.ctrl-btn:hover { background: #30363d; border-color: #00dca0; color: #fff; }
    button.ctrl-btn.primary { background: #1f6feb; border-color: #388bfd; }
    .status-box { font-family: monospace; font-size: 0.9rem; color: #7ee787; }
    .desc-bar {
      margin-top: 12px;
      font-size: 0.85rem;
      color: #8b949e;
      background: #0d1117;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid #21262d;
    }
  </style>
</head>
<body>
<div class="app-container">
  <div class="header">
    <div class="title-box">
      <h1 id="anim-title">[001/100] DOUBLE PENDULUM</h1>
      <p id="anim-meta">DOMAIN: Classical Mechanics | DURATION: 10.0s | TYPE: Chaotic</p>
    </div>
    <div>
      <select id="anim-dropdown" class="anim-select"></select>
    </div>
  </div>
  <div class="canvas-wrapper">
    <canvas id="simCanvas" width="850" height="480"></canvas>
  </div>
  <div class="progress-container">
    <div id="progress-fill" class="progress-bar"></div>
  </div>
  <div class="controls">
    <div class="btn-group">
      <button class="ctrl-btn" id="btn-prev">&#9664; PREV</button>
      <button class="ctrl-btn primary" id="btn-pause">PAUSE / PLAY</button>
      <button class="ctrl-btn" id="btn-next">NEXT &#9654;</button>
      <button class="ctrl-btn" id="btn-reset">RESET</button>
      <button class="ctrl-btn" id="btn-random">RANDOM</button>
    </div>
    <div class="status-box" id="status-text">STATUS: RUNNING | TIME: 0.0s</div>
  </div>
  <div class="desc-bar" id="anim-desc"></div>
</div>

<script>
const REGISTRY = __REGISTRY_JSON__;
const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;

let currentIndex = 0, elapsedTime = 0.0, paused = false;
let lastTimestamp = performance.now();
let dpState = [Math.PI / 2, Math.PI / 2, 0, 0], dpTrail = [];

const dropdown = document.getElementById('anim-dropdown');
REGISTRY.forEach((spec, idx) => {
  const opt = document.createElement('option');
  opt.value = idx;
  opt.textContent = String(spec.id).padStart(3, '0') + ' - ' + spec.name;
  dropdown.appendChild(opt);
});

function setAnimation(index) {
  if (index < 0) index = REGISTRY.length - 1;
  if (index >= REGISTRY.length) index = 0;
  currentIndex = index;
  elapsedTime = 0.0;
  dropdown.value = currentIndex;
  dpState = [Math.PI / 2, Math.PI / 2, 0, 0];
  dpTrail = [];
  const spec = REGISTRY[currentIndex];
  document.getElementById('anim-title').textContent = '[' + String(spec.id).padStart(3, '0') + '/100] ' + spec.name.toUpperCase();
  document.getElementById('anim-meta').textContent = 'DOMAIN: ' + spec.domain + ' | DURATION: ' + spec.duration.toFixed(1) + 's | TYPE: ' + spec.loop_type;
  document.getElementById('anim-desc').textContent = spec.description;
}

document.getElementById('btn-prev').addEventListener('click', () => setAnimation(currentIndex - 1));
document.getElementById('btn-next').addEventListener('click', () => setAnimation(currentIndex + 1));
document.getElementById('btn-pause').addEventListener('click', () => { paused = !paused; });
document.getElementById('btn-reset').addEventListener('click', () => setAnimation(currentIndex));
document.getElementById('btn-random').addEventListener('click', () => setAnimation(Math.floor(Math.random() * REGISTRY.length)));
dropdown.addEventListener('change', (e) => setAnimation(parseInt(e.target.value, 10)));

function dpDerivatives(st) {
  const [th1, th2, w1, w2] = st;
  const l1 = 105, l2 = 95, m1 = 10, m2 = 10, g = 9.81 * 40;
  const dth = th1 - th2;
  const den1 = 2 * m1 + m2 - m2 * Math.cos(2 * th1 - 2 * th2);
  let num1 = -g * (2 * m1 + m2) * Math.sin(th1) - m2 * g * Math.sin(th1 - 2 * th2);
  num1 -= 2 * Math.sin(dth) * m2 * (w2 * w2 * l2 + w1 * w1 * l1 * Math.cos(dth));
  const alpha1 = num1 / (l1 * den1);
  const num2 = 2 * Math.sin(dth) * (w1 * w1 * l1 * (m1 + m2) + g * (m1 + m2) * Math.cos(th1) + w2 * w2 * l2 * m2 * Math.cos(dth));
  const alpha2 = num2 / (l2 * den1);
  return [w1, w2, alpha1, alpha2];
}

function updateDoublePendulum(dt) {
  const subDt = Math.min(dt, 0.033) / 4.0;
  for (let n = 0; n < 4; n++) {
    const k1 = dpDerivatives(dpState);
    const s2 = dpState.map((s, i) => s + 0.5 * subDt * k1[i]);
    const k2 = dpDerivatives(s2);
    const s3 = dpState.map((s, i) => s + 0.5 * subDt * k2[i]);
    const k3 = dpDerivatives(s3);
    const s4 = dpState.map((s, i) => s + subDt * k3[i]);
    const k4 = dpDerivatives(s4);
    dpState = dpState.map((s, i) => s + (subDt / 6.0) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]));
  }
  const cx = W / 2, cy = H / 3 + 10;
  const x1 = cx + 105 * Math.sin(dpState[0]);
  const y1 = cy + 105 * Math.cos(dpState[0]);
  const x2 = x1 + 95 * Math.sin(dpState[1]);
  const y2 = y1 + 95 * Math.cos(dpState[1]);
  dpTrail.push([x2, y2]);
  if (dpTrail.length > 100) dpTrail.shift();
}

function renderScene(spec) {
  ctx.fillStyle = '#12161c';
  ctx.fillRect(0, 0, W, H);
  const cx = W / 2, cy = H / 2, t = elapsedTime, id = spec.id, domain = spec.domain;

  if (id === 1) {
    const px = W / 2, py = H / 3 + 10;
    const x1 = px + 105 * Math.sin(dpState[0]), y1 = py + 105 * Math.cos(dpState[0]);
    const x2 = x1 + 95 * Math.sin(dpState[1]), y2 = y1 + 95 * Math.cos(dpState[1]);
    for (let i = 0; i < dpTrail.length - 1; i++) {
      ctx.strokeStyle = 'rgba(0, 210, 255, ' + (i / dpTrail.length) + ')';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(dpTrail[i][0], dpTrail[i][1]); ctx.lineTo(dpTrail[i+1][0], dpTrail[i+1][1]); ctx.stroke();
    }
    ctx.strokeStyle = '#dcdfe4'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(x1, y1); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    ctx.fillStyle = '#ff6464'; ctx.beginPath(); ctx.arc(x1, y1, 11, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#64ff64'; ctx.beginPath(); ctx.arc(x2, y2, 9, 0, Math.PI * 2); ctx.fill();
  } else if (id === 3) {
    ctx.fillStyle = '#ff3232'; ctx.beginPath(); ctx.arc(cx, cy, 16, 0, Math.PI * 2); ctx.fill();
    [55, 105, 155].forEach((r, idx) => {
      ctx.strokeStyle = '#3c5078'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
      const ang = t * [3.0, 1.8, 1.1][idx] + idx * 2.1;
      ctx.fillStyle = '#00b4ff';
      ctx.beginPath(); ctx.arc(cx + r * Math.cos(ang), cy + r * Math.sin(ang), 6, 0, Math.PI * 2); ctx.fill();
    });
  } else if (id === 10 || id === 52) {
    const slitX = cx - 140, sy1 = cy - 40, sy2 = cy + 40;
    ctx.strokeStyle = '#b4b4b4'; ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(slitX, 40); ctx.lineTo(slitX, sy1 - 10);
    ctx.moveTo(slitX, sy1 + 10); ctx.lineTo(slitX, sy2 - 10);
    ctx.moveTo(slitX, sy2 + 10); ctx.lineTo(slitX, H - 40);
    ctx.stroke();
    for (let rb = 10; rb < 220; rb += 24) {
      const r = (rb + t * 80) % 220;
      ctx.strokeStyle = 'rgba(0, 200, 255, ' + (1.0 - r / 220) + ')';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(slitX, sy1, r, -1.4, 1.4); ctx.stroke();
      ctx.beginPath(); ctx.arc(slitX, sy2, r, -1.4, 1.4); ctx.stroke();
    }
  } else if (["Mechanics", "Kinematics", "Robotics", "Engineering"].some(k => domain.includes(k))) {
    const radius = 80, teeth = 12;
    ctx.strokeStyle = '#5a6473'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(cx, cy, radius, 0, Math.PI * 2); ctx.stroke();
    for (let i = 0; i < teeth; i++) {
      const ang = ((Math.PI * 2) / teeth) * i + t * 1.5 + id;
      ctx.fillStyle = '#a0afbe';
      ctx.beginPath(); ctx.arc(cx + (radius + 8) * Math.cos(ang), cy + (radius + 8) * Math.sin(ang), 6, 0, Math.PI * 2); ctx.fill();
    }
    const ax = cx + radius * Math.cos(-t * 1.5), ay = cy + radius * Math.sin(-t * 1.5);
    ctx.strokeStyle = '#ff8c00'; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(ax, ay); ctx.stroke();
    ctx.fillStyle = '#ffc832'; ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI * 2); ctx.fill();
  } else if (["Astrophysics", "Astronomy", "Astro", "Space", "Orbital"].some(k => domain.includes(k))) {
    ctx.fillStyle = '#ffdc50'; ctx.beginPath(); ctx.arc(cx, cy, 26, 0, Math.PI * 2); ctx.fill();
    [80, 135, 190].forEach((r, idx) => {
      ctx.strokeStyle = '#324664'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.ellipse(cx, cy, r, r * 0.55, 0, 0, Math.PI * 2); ctx.stroke();
      const ang = t * (2.0 / (idx + 1)) + id;
      ctx.fillStyle = '#64c8ff';
      ctx.beginPath(); ctx.arc(cx + r * Math.cos(ang), cy + (r * 0.55) * Math.sin(ang), 7 - idx, 0, Math.PI * 2); ctx.fill();
    });
  } else if (["Electronics", "Computing", "Sensors", "Telecommunications", "Digital"].some(k => domain.includes(k))) {
    [-70, 0, 70].forEach((yOff, i) => {
      const y = cy + yOff;
      ctx.strokeStyle = '#285032'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(100, y); ctx.lineTo(W - 100, y); ctx.stroke();
      const pulseX = 100 + ((t * 180 + i * 90 + id * 15) % (W - 200));
      ctx.fillStyle = '#00ff78'; ctx.fillRect(pulseX, y - 16, 28, 16);
      ctx.fillStyle = '#00ffc8'; ctx.beginPath(); ctx.arc(pulseX + 14, y, 5, 0, Math.PI * 2); ctx.fill();
    });
  } else {
    for (let i = 0; i < 8; i++) {
      const ang = t * 0.8 + ((Math.PI * 2) / 8) * i + id;
      const dist = 85 + 28 * Math.sin(t * 3.0 + i);
      const nx = cx + dist * Math.cos(ang), ny = cy + dist * Math.sin(ang);
      ctx.strokeStyle = '#5078a0'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(nx, ny); ctx.stroke();
      ctx.fillStyle = '#f0508c'; ctx.beginPath(); ctx.arc(nx, ny, 9, 0, Math.PI * 2); ctx.fill();
    }
    ctx.fillStyle = '#50dcb4'; ctx.beginPath(); ctx.arc(cx, cy, 16, 0, Math.PI * 2); ctx.fill();
  }
}

function loop(now) {
  const dt = Math.min((now - lastTimestamp) / 1000.0, 0.05);
  lastTimestamp = now;
  const spec = REGISTRY[currentIndex];
  if (!paused) {
    elapsedTime += dt;
    if (elapsedTime > spec.duration) elapsedTime %= spec.duration;
    if (spec.id === 1) updateDoublePendulum(dt);
  }
  renderScene(spec);
  const pct = ((elapsedTime % spec.duration) / spec.duration) * 100;
  document.getElementById('progress-fill').style.width = pct.toFixed(1) + '%';
  const stText = paused ? 'PAUSED' : 'RUNNING';
  document.getElementById('status-text').textContent = 'STATUS: ' + stText + ' | TIME: ' + elapsedTime.toFixed(1) + 's / ' + spec.duration.toFixed(1) + 's';
  document.getElementById('status-text').style.color = paused ? '#ffb432' : '#7ee787';
  requestAnimationFrame(loop);
}

setAnimation(0);
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

def generate_web_bundle():
    os.makedirs("build/web", exist_ok=True)
    specs_list = [
        {
            "id": s.id,
            "name": s.name,
            "domain": s.domain,
            "duration": s.duration,
            "loop_type": s.loop_type,
            "description": s.description
        }
        for s in REGISTRY.values()
    ]
    registry_json = json.dumps(specs_list, indent=2)
    final_html = HTML_TEMPLATE.replace("__REGISTRY_JSON__", registry_json)

    output_path = os.path.join("build", "web", "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"Successfully generated {output_path} with {len(specs_list)} animations.")

if __name__ == "__main__":
    generate_web_bundle()
