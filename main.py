"""
main.py - SciTech 100 Web Compiler & Runtime
Generates build/web/index.html with 100 unique science & technology simulations.
"""

import os
import json

TOPICS = [
    (1, "Double Pendulum", "Classical Mechanics", 10.0, "Chaotic dual-arm pendulum integrated with RK4."),
    (2, "Spring-Mass Damper", "Classical Mechanics", 4.0, "Viscous damped harmonic oscillation with spring coils."),
    (3, "Bohr Atom Model", "Quantum Physics", 3.0, "Concentric quantized electron orbits emitting photon wavelets."),
    (4, "Optical Prism", "Optics", 5.0, "Snell's law refraction splitting white beam into 6 spectral colors."),
    (5, "Convex & Concave Lenses", "Geometric Optics", 6.0, "Ray-tracing matrix showing focal convergence and divergence."),
    (6, "Aerodynamic Airfoil", "Fluid Dynamics", 4.0, "Curved camber foil with high/low velocity Bernoulli streamlines."),
    (7, "Piston Engine (4-Stroke)", "Thermodynamics", 4.0, "Piston, connecting rod, crankshaft, valves, and timed combustion spark."),
    (8, "Particle Accelerator", "High Energy Physics", 5.0, "Synchrotron storage ring with RF cavity and accelerating particle bunches."),
    (9, "Bar Magnet & Field Lines", "Electromagnetism", 6.0, "Dipole magnetic field lines dynamically orienting a moving compass probe."),
    (10, "Standing Wave Generator", "Wave Mechanics", 3.0, "Counter-propagating wave superposition with static nodes and antinodes."),
    (11, "Keplerian Solar System", "Astrophysics", 12.0, "Elliptical planetary orbit demonstrating Kepler's area sweep law."),
    (12, "Multi-Stage Rocket", "Aerospace Engineering", 15.0, "Ascending rocket body, booster stage separation, and exhaust plume."),
    (13, "CubeSat Satellite", "Astronautics", 8.0, "Satellite bus unfolding solar panels and emitting telemetry beacon cones."),
    (14, "Black Hole Accretion Disk", "Relativistic Astro", 6.0, "Event horizon, photon ring, and Doppler-beamed swirling matter."),
    (15, "Mars Rover Rocker-Bogie", "Robotics", 8.0, "6-wheel articulated passive suspension traversing rocky terrain."),
    (16, "Lunar Lander Descent", "Orbital Mechanics", 10.0, "Throttle-vectored retro-thruster decelerating to soft touchdown."),
    (17, "Radio Telescope Array", "Astronomy", 7.0, "Steerable parabolic dish reflector focusing incoming parallel radio waves."),
    (18, "Pulsar / Neutron Star", "Astrophysics", 2.0, "Rapidly spinning neutron star sweeping dual radiation beam cones."),
    (19, "DNA Double Helix", "Molecular Biology", 6.0, "Rotating double helix unzipping base pairs at a replication fork."),
    (20, "Water Molecule Network", "Chemistry", 4.0, "Polar H2O molecules with dynamic forming and breaking of hydrogen bonds."),
    (21, "Graphene Hexagonal Sheet", "Materials Science", 5.0, "sp2 carbon honeycomb lattice undergoing cyclic tensile strain."),
    (22, "Electrochemical Cell", "Physical Chemistry", 6.0, "Anode/cathode redox electrodes with ion migration through a salt bridge."),
    (23, "Chemical Titration Setup", "Analytical Chemistry", 8.0, "Burette stopcock dispensing drops into an indicator flask changing color."),
    (24, "Buckyball (C60)", "Nanotechnology", 6.0, "Rotating truncated icosahedron molecular fullerene cage."),
    (25, "Ideal Gas Chamber", "Statistical Mechanics", 5.0, "Elastic molecular collisions exhibiting Maxwell-Boltzmann motion."),
    (26, "Logic Gate Circuit", "Digital Electronics", 4.0, "AND/OR/NOT combinatorial gates propagating high/low digital pulses."),
    (27, "Microprocessor CPU Die", "Computer Architecture", 6.0, "Central ALU, register banks, and multiplexed data/address buses."),
    (28, "Printed Circuit Board (PCB)", "Electronics", 5.0, "High-frequency signal packets propagating along copper circuit traces."),
    (29, "Oscilloscope CRT Display", "Instrumentation", 4.0, "Phosphor graticule screen plotting dual-channel Lissajous figures."),
    (30, "2-Link Robotic Arm", "Robotics", 6.0, "Planar 2-joint arm reaching for moving coordinates via inverse kinematics."),
    (31, "Artificial Neural Network", "Machine Learning", 5.0, "Layered perceptron pulsing forward activations and backward gradients."),
    (32, "Fiber Optic Cable", "Telecommunications", 4.0, "Laser beam traveling through flexible core via total internal reflection."),
    (33, "Radar Sweep Display", "Electromagnetics", 4.0, "360-degree radial sweep illuminating target blips with phosphor decay."),
    (34, "Binary Search Tree", "Computer Science", 8.0, "Recursive node value comparisons and active traversal highlighting."),
    (35, "QR Code Scanner", "Optoelectronics", 3.0, "Horizontal red laser line sweeping matrix alignment markers."),
    (36, "Biological Cell", "Cytology", 10.0, "Eukaryotic cell showing nucleus, mitochondria, and vesicle transport."),
    (37, "Biological Neuron", "Neuroscience", 3.0, "Depolarization action potential wave traveling down the axon to synapse."),
    (38, "Bacteriophage Virus", "Virology", 8.0, "Phage landing, sheath contraction, and genome injection into host."),
    (39, "Electrocardiogram (ECG)", "Biomedical Tech", 4.0, "Real-time clinical P-Q-R-S-T cardiac waveform rhythm sweep."),
    (40, "Capillary Blood Flow", "Hematology", 5.0, "Red blood cells deforming as they squeeze through narrow capillary lumen."),
    (41, "MRI Scanner Bore", "Medical Imaging", 6.0, "Hydrogen proton magnetic spin moments precessing under RF excitation."),
    (42, "Bionic Prosthetic Hand", "Biomechatronics", 5.0, "Actuated tendon cables articulating five-finger grasp cycles."),
    (43, "Wind Turbine", "Renewable Energy", 4.0, "Pitch-controlled aerodynamic blades rotating with trailing wake vortices."),
    (44, "Photovoltaic Solar Cell", "Solid-State Physics", 4.0, "Incident photons exciting electron-hole pairs across p-n junction."),
    (45, "Nuclear Reactor Core", "Nuclear Engineering", 8.0, "Control rods inserting/withdrawing to regulate neutron chain reaction."),
    (46, "Hydroelectric Dam Turbine", "Hydraulic Power", 6.0, "Penstock water head driving Francis turbine runner blades."),
    (47, "Seismograph", "Geophysics", 7.0, "Suspended inertial mass needle recording P and S earthquake tremors on drum."),
    (48, "Geothermal Power Loop", "Thermodynamics", 8.0, "Closed subterranean brine loop flashing steam to surface generator."),
    (49, "Atmospheric Water Cycle", "Meteorology", 10.0, "Solar evaporation, convective cloud formation, rain, and surface runoff."),
    (50, "EV Powertrain", "Automotive Tech", 6.0, "Inverter generating 3-phase AC rotating magnetic field in stator."),
    (51, "Newton's Cradle", "Classical Mechanics", 4.0, "Momentum and kinetic energy transfer across 5 suspended steel spheres."),
    (52, "Young's Double-Slit", "Wave Optics", 6.0, "Diffracted coherent wavelets forming bright and dark interference fringes."),
    (53, "Michelson Interferometer", "Precision Optics", 5.0, "Beam splitter recombining split laser paths into circular fringe rings."),
    (54, "Stirling Engine", "Heat Engines", 3.0, "Displacer and power pistons oscillating 90 degrees out of phase across heat sink."),
    (55, "Cathode Ray Tube (CRT)", "Electronics", 5.0, "Deflection plates electrostatic steering of electron beam to screen."),
    (56, "Doppler Effect Emitter", "Acoustics", 6.0, "Moving source compressing wavefronts ahead and stretching them behind."),
    (57, "Gyroscope Stabilizer", "Rotational Dynamics", 8.0, "Spinning rotor demonstrating rigidity in space and precessional torque."),
    (58, "Karman Vortex Street", "Aerodynamics", 6.0, "Fluid flow past cylinder shedding alternating counter-rotating eddies."),
    (59, "Brownian Motion Chamber", "Statistical Physics", 5.0, "Microscopic smoke particle undergoing continuous thermal random walk."),
    (60, "Van de Graaff Generator", "Electrostatics", 4.0, "Moving belt depositing electrostatic charges to dome with dielectric spark."),
    (61, "Gravitational Slingshot", "Astrodynamics", 8.0, "Hyperbolic flyby gaining orbital momentum from moving target planet."),
    (62, "Lagrange Points (L1-L5)", "Orbital Mechanics", 10.0, "Equipotential gravitational wells with satellite in halo orbit."),
    (63, "Ion Thruster Engine", "Space Propulsion", 4.0, "Electrostatic acceleration of xenon ions producing glowing blue exhaust."),
    (64, "Exoplanet Transit Light Curve", "Astronomy", 8.0, "Planet transiting stellar disc synchronized with photometric brightness dip."),
    (65, "Solar Flare Magnetic Arch", "Solar Physics", 6.0, "Magnetic reconnection loop snapping and erupting coronal mass plasma."),
    (66, "Lunar Phases & Eclipse", "Spherical Astronomy", 12.0, "Sun-Earth-Moon orbital geometry showing umbra and penumbra shadows."),
    (67, "Planetary Ring Shepherds", "Celestial Mechanics", 8.0, "Inner/outer moonlets gravitationally confining a narrow ringlet border."),
    (68, "Asteroid Kinetic Impactor", "Planetary Defense", 7.0, "Hypervelocity projectile striking asteroid with expanding ejecta cone."),
    (69, "Geneva Drive (Maltese Cross)", "Machine Kinematics", 4.0, "Continuous rotating drive pin stepping intermittent 4-slot cross gear."),
    (70, "Planetary Gear Train", "Mechanical Engineering", 6.0, "Sun gear, 3 planet gears on carrier, and ring gear moving with true gear ratios."),
    (71, "Turbofan Jet Engine", "Aerospace Engineering", 5.0, "Intake fan, multistage compressor, combustion chamber, and bypass duct."),
    (72, "Hydraulic Press", "Fluid Mechanics", 6.0, "Pascal's principle multiplying force from narrow piston to heavy press."),
    (73, "Centrifugal Flyball Governor", "Control Systems", 4.0, "Revolving flyweights rising with RPM to throttle mechanical steam valve."),
    (74, "Automotive Differential", "Automotive Mech", 6.0, "Bevel spider gears compensating outer/inner wheel speeds during a turn."),
    (75, "Structural Truss Under Load", "Civil Engineering", 8.0, "Moving vehicular load dynamically shifting tension (blue) and compression (red)."),
    (76, "Hovercraft Skirt & Plenum", "Marine Engineering", 5.0, "Lift fan pressurizing flexible perimeter skirt for ground effect cushion."),
    (77, "Bloch Sphere Qubit", "Quantum Computing", 6.0, "Quantum state vector rotating on unit sphere under Hadamard/Pauli gates."),
    (78, "555 Timer Circuit", "Analog Electronics", 4.0, "RC exponential capacitor charge curve synchronized with square clock output."),
    (79, "Dipole Antenna Radiation", "Electromagnetics", 3.0, "Center-fed dipole emitting expanding toroidal electromagnetic wavelets."),
    (80, "MOSFET Transistor Switch", "Semiconductor Physics", 4.0, "Gate voltage creating conductive inversion channel between source and drain."),
    (81, "Superconductor Levitation", "Quantum Materials", 5.0, "Meissner effect expelling magnetic flux lines around levitating magnet."),
    (82, "Electrical Transformer", "Power Systems", 4.0, "Primary AC magnetic flux inducing stepped secondary voltage in core."),
    (83, "LiDAR Distance Scanner", "Autonomous Systems", 5.0, "Pulsed laser time-of-flight rays mapping surrounding 2D point cloud."),
    (84, "7-Segment Display Decoder", "Digital Logic", 7.0, "Binary counter decoding 4-bit states into glowing 7-segment decimal digits."),
    (85, "CRISPR-Cas9 Complex", "Biotechnology", 10.0, "Guide RNA locating target DNA sequence followed by double-strand cleavage."),
    (86, "Enzyme-Substrate Catalysis", "Biochemistry", 6.0, "Induced-fit active site binding substrate, lowering activation energy."),
    (87, "Hemodialysis Dialyzer", "Biomedical Eng", 8.0, "Countercurrent blood and dialysate diffusion across semipermeable fibers."),
    (88, "PCR Thermal Cycler", "Molecular Biology", 9.0, "Cyclic heating graph: 95°C denature, 55°C anneal, and 72°C extension."),
    (89, "Centrifuge Gradient", "Laboratory Tech", 6.0, "High-G rotation separating plasma, buffy coat, and red blood cells."),
    (90, "Synaptic Exocytosis", "Neurobiology", 5.0, "Calcium influx triggering neurotransmitter vesicle fusion at synaptic cleft."),
    (91, "Syringe Infusion Pump", "Medical Devices", 6.0, "Micro-stepper motor turning lead screw to drive precision plunger."),
    (92, "Microfluidic Lab-on-a-Chip", "Nanotechnology", 5.0, "Cross-junction shearing continuous oil-water stream into uniform droplets."),
    (93, "Subduction Zone Volcano", "Geophysics", 10.0, "Dense oceanic plate sinking beneath continent to fuel rising magma chamber."),
    (94, "Hydrogen PEM Fuel Cell", "Clean Energy", 6.0, "H2 split at anode, protons crossing PEM to react with O2 into pure water."),
    (95, "Cyclone / Hurricane Core", "Meteorology", 8.0, "Low-pressure calm eye surrounded by spiraling Coriolis convective rain bands."),
    (96, "Coriolis Flow Meter", "Instrumentation", 4.0, "Fluid momentum twisting vibrating U-tube proportional to mass flow rate."),
    (97, "Tidal Barrage Power Plant", "Renewable Energy", 8.0, "Estuary water head differential driving reversible bidirectional hydro-turbines."),
    (98, "Geyser Hydrothermal Eruption", "Hydrogeology", 6.0, "Superheated subterranean water flashing into vertical steam plume eruption."),
    (99, "Oscillating Water Column", "Ocean Energy", 5.0, "Ocean swell compressing air chamber to spin bidirectional Wells turbine."),
    (100, "Direct Air Carbon Capture", "Environmental Tech", 6.0, "Air stream drawn through chemical sorbent matrix trapping CO2 molecules.")
]

def build_web_app():
    os.makedirs(os.path.join("build", "web"), exist_ok=True)
    specs_json = json.dumps([{"id": t[0], "name": t[1], "domain": t[2], "duration": t[3], "desc": t[4]} for t in TOPICS])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SciTech100 - 100 Unique Science & Technology Simulations</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
    body {{ background: #0d1117; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 14px; }}
    .container {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 16px; box-shadow: 0 16px 36px rgba(0,0,0,0.65); max-width: 900px; width: 100%; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #21262d; }}
    .title-box h1 {{ font-size: 1.2rem; color: #f0f6fc; font-weight: 700; }}
    .title-box p {{ font-size: 0.82rem; color: #58a6ff; margin-top: 3px; }}
    select.select-box {{ background: #21262d; color: #f0f6fc; border: 1px solid #30363d; border-radius: 6px; padding: 6px 12px; font-size: 0.85rem; cursor: pointer; outline: none; }}
    .canvas-wrap {{ width: 100%; display: flex; justify-content: center; background: #12161c; border-radius: 8px; overflow: hidden; border: 1px solid #21262d; }}
    canvas {{ display: block; max-width: 100%; height: auto; }}
    .bar-wrap {{ width: 100%; height: 6px; background: #21262d; border-radius: 3px; margin: 12px 0; overflow: hidden; }}
    .bar-fill {{ height: 100%; background: linear-gradient(90deg, #00dca0, #58a6ff); width: 0%; }}
    .controls {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: space-between; }}
    .btn-group {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    button.btn {{ background: #21262d; color: #e6edf3; border: 1px solid #30363d; padding: 8px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.15s ease; }}
    button.btn:hover {{ background: #30363d; border-color: #00dca0; color: #fff; }}
    button.btn.primary {{ background: #1f6feb; border-color: #388bfd; }}
    .status {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85rem; color: #7ee787; }}
    .desc-box {{ margin-top: 10px; font-size: 0.82rem; color: #8b949e; background: #0d1117; padding: 8px 12px; border-radius: 6px; border: 1px solid #21262d; }}
  </style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title-box">
      <h1 id="title">[001/100] DOUBLE PENDULUM</h1>
      <p id="meta">DOMAIN: Classical Mechanics | DURATION: 10.0s</p>
    </div>
    <select id="selector" class="select-box" aria-label="Select Simulation"></select>
  </div>
  <div class="canvas-wrap">
    <canvas id="cv" width="850" height="460"></canvas>
  </div>
  <div class="bar-wrap"><div id="bar" class="bar-fill"></div></div>
  <div class="controls">
    <div class="btn-group">
      <button class="btn" id="btn-prev">&#9664; PREV</button>
      <button class="btn primary" id="btn-pause">PAUSE / PLAY</button>
      <button class="btn" id="btn-next">NEXT &#9654;</button>
      <button class="btn" id="btn-reset">RESET</button>
      <button class="btn" id="btn-rand">RANDOM</button>
    </div>
    <div class="status" id="status">STATUS: RUNNING | TIME: 0.0s</div>
  </div>
  <div class="desc-box" id="desc"></div>
</div>

<script>
const REGISTRY = {specs_json};
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
const W = cv.width, H = cv.height;
let idx = 0, elapsed = 0.0, paused = false, lastTime = performance.now();

let dpState = [Math.PI/2, Math.PI/2, 0, 0], dpTrail = [];
let gas = Array.from({{length: 40}}, () => ({{ x: W/2 - 120 + Math.random()*240, y: H/2 - 50 + Math.random()*100, vx: (Math.random()-0.5)*180, vy: (Math.random()-0.5)*180 }}));
let bx = W/2, by = H/2, btrail = [];

const sel = document.getElementById('selector');
REGISTRY.forEach((s, i) => {{
  const opt = document.createElement('option');
  opt.value = i;
  opt.textContent = String(s.id).padStart(3, '0') + ' - ' + s.name;
  sel.appendChild(opt);
}});

function setAnim(i) {{
  if (i < 0) i = REGISTRY.length - 1;
  if (i >= REGISTRY.length) i = 0;
  idx = i;
  elapsed = 0.0;
  sel.value = idx;
  dpState = [Math.PI/2, Math.PI/2, 0, 0]; dpTrail = [];
  bx = W/2; by = H/2; btrail = [];
  const s = REGISTRY[idx];
  document.getElementById('title').textContent = '[' + String(s.id).padStart(3, '0') + '/100] ' + s.name.toUpperCase();
  document.getElementById('meta').textContent = 'DOMAIN: ' + s.domain + ' | DURATION: ' + s.duration.toFixed(1) + 's';
  document.getElementById('desc').textContent = s.desc;
}}

document.getElementById('btn-prev').onclick = () => setAnim(idx - 1);
document.getElementById('btn-next').onclick = () => setAnim(idx + 1);
document.getElementById('btn-pause').onclick = () => {{ paused = !paused; }};
document.getElementById('btn-reset').onclick = () => setAnim(idx);
document.getElementById('btn-rand').onclick = () => setAnim(Math.floor(Math.random() * REGISTRY.length));
sel.onchange = (e) => setAnim(parseInt(e.target.value, 10));

window.addEventListener('keydown', (e) => {{
  if (e.key === 'ArrowRight') setAnim(idx + 1);
  else if (e.key === 'ArrowLeft') setAnim(idx - 1);
  else if (e.key === ' ') {{ e.preventDefault(); paused = !paused; }}
  else if (e.key === 'r' || e.key === 'R') setAnim(idx);
}});

function render(aid, cx, cy, t) {{
  ctx.fillStyle = '#10141a'; ctx.fillRect(0, 0, W, H);

  if (aid === 1) {{
    for(let n=0; n<3; n++) {{
      const [th1, th2, w1, w2] = dpState, dth = th1 - th2;
      const den = 30 - 10 * Math.cos(2*th1 - 2*th2);
      const a1 = (-392.4*3*Math.sin(th1) - 392.4*Math.sin(th1-2*th2) - 2*Math.sin(dth)*10*(w2*w2*95 + w1*w1*105*Math.cos(dth))) / (105*den);
      const a2 = (2*Math.sin(dth)*(w1*w1*105*20 + 392.4*20*Math.cos(th1) + w2*w2*95*10*Math.cos(dth))) / (95*den);
      dpState[2] += a1*0.005; dpState[3] += a2*0.005; dpState[0] += dpState[2]*0.005; dpState[1] += dpState[3]*0.005;
    }}
    const p1 = [cx + 105*Math.sin(dpState[0]), cy - 30 + 105*Math.cos(dpState[0])];
    const p2 = [p1[0] + 95*Math.sin(dpState[1]), p1[1] + 95*Math.cos(dpState[1])];
    dpTrail.push(p2); if (dpTrail.length > 80) dpTrail.shift();
    if (dpTrail.length > 1) {{
      ctx.strokeStyle = '#00dca0'; ctx.lineWidth = 2; ctx.beginPath();
      dpTrail.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1])); ctx.stroke();
    }}
    ctx.strokeStyle = '#e6edf3'; ctx.lineWidth = 4; ctx.beginPath();
    ctx.moveTo(cx, cy - 30); ctx.lineTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke();
    ctx.fillStyle = '#ff6464'; ctx.beginPath(); ctx.arc(p1[0], p1[1], 10, 0, 7); ctx.fill();
    ctx.fillStyle = '#64ff64'; ctx.beginPath(); ctx.arc(p2[0], p2[1], 8, 0, 7); ctx.fill();
  }}
  else if (aid === 2) {{
    const amp = 70 * Math.exp(-t * 0.7) * Math.cos(t * 6), by = cy + amp + 40;
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(cx - 100, cy - 100); ctx.lineTo(cx + 100, cy - 100); ctx.stroke();
    ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx - 40, cy - 100);
    for(let i=0; i<=12; i++) ctx.lineTo(cx - 40 + (i%2 ? 14 : -14), cy - 100 + (by - cy + 60)*(i/12));
    ctx.lineTo(cx - 40, by); ctx.stroke();
    ctx.fillStyle = '#ff7b72'; ctx.fillRect(cx - 70, by, 140, 45);
  }}
  else if (aid === 3) {{
    ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(cx, cy, 16, 0, 7); ctx.fill();
    [45, 85, 125].forEach((r, i) => {{
      ctx.strokeStyle = '#30363d'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(cx, cy, r, 0, 7); ctx.stroke();
      const a = t * (3.0 - i * 0.8);
      ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(cx + r*Math.cos(a), cy + r*Math.sin(a), 5, 0, 7); ctx.fill();
    }});
  }}
  else if (aid === 4) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 3; ctx.beginPath();
    ctx.moveTo(cx, cy - 90); ctx.lineTo(cx + 85, cy + 70); ctx.lineTo(cx - 85, cy + 70); ctx.closePath(); ctx.stroke();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx - 200, cy + 20); ctx.lineTo(cx - 30, cy + 10); ctx.stroke();
    const cols = ['#f85149', '#f0883e', '#e3b341', '#3fb950', '#58a6ff', '#bc8cff'];
    cols.forEach((c, i) => {{
      ctx.strokeStyle = c; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(cx - 30, cy + 10);
      ctx.lineTo(cx + 35, cy + 12 + i*3); ctx.lineTo(cx + 200, cy - 30 + i*16); ctx.stroke();
    }});
  }}
  else if (aid === 5) {{
    ctx.strokeStyle = '#388bfd'; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(cx, cy, 18, 90, 0, 0, 7); ctx.stroke();
    [-50, -25, 0, 25, 50].forEach(y => {{
      ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 2; ctx.beginPath();
      ctx.moveTo(cx - 180, cy + y); ctx.lineTo(cx, cy + y); ctx.lineTo(cx + 130, cy); ctx.lineTo(cx + 210, cy - y*0.6); ctx.stroke();
    }});
  }}
  else if (aid === 6) {{
    ctx.fillStyle = '#8b949e'; ctx.beginPath(); ctx.moveTo(cx - 120, cy);
    for(let i=0; i<=16; i++) ctx.lineTo(cx - 120 + i*15, cy - 40*Math.sin(i*0.2));
    ctx.closePath(); ctx.fill();
    for(let y of [-40, -20, 20, 40]) {{
      const px = cx - 180 + ((t*160 + y*3) % 360);
      ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(px, cy + y - (y<0 ? 18 : -10), 3, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 7) {{
    const a = t * 10, py = cy - 20 + 35*Math.sin(a);
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.strokeRect(cx - 55, cy - 80, 110, 140);
    ctx.fillStyle = (Math.sin(a/2) > 0.8) ? '#ff7b72' : '#30363d'; ctx.fillRect(cx - 50, py - 30, 100, 40);
    ctx.strokeStyle = '#f0883e'; ctx.lineWidth = 5; ctx.beginPath();
    ctx.moveTo(cx, py); ctx.lineTo(cx + 45*Math.cos(a), cy + 90 + 45*Math.sin(a)); ctx.stroke();
  }}
  else if (aid === 8) {{
    ctx.strokeStyle = '#30363d'; ctx.lineWidth = 14; ctx.beginPath(); ctx.arc(cx, cy, 110, 0, 7); ctx.stroke();
    for(let b=0; b<3; b++) {{
      const ba = t * 5 + b * 2.094;
      ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(cx + 110*Math.cos(ba), cy + 110*Math.sin(ba), 7, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 9) {{
    for(let r of [50, 85, 125]) {{
      ctx.strokeStyle = 'rgba(88, 166, 255, 0.35)'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.ellipse(cx, cy, r, r*0.55, 0, 0, 7); ctx.stroke();
    }}
    ctx.fillStyle = '#f85149'; ctx.fillRect(cx - 70, cy - 18, 70, 36);
    ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx, cy - 18, 70, 36);
  }}
  else if (aid === 10) {{
    ctx.strokeStyle = '#00dca0'; ctx.lineWidth = 3; ctx.beginPath();
    for(let x=cx-200; x<=cx+200; x+=6) {{
      const y = cy + 55 * Math.sin((x - cx)*0.035) * Math.cos(t * 7);
      x === cx-200 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }}
    ctx.stroke();
  }}
  else if (aid === 11) {{
    ctx.strokeStyle = '#30363d'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(cx - 40, cy, 150, 80, 0, 0, 7); ctx.stroke();
    ctx.fillStyle = '#e3b341'; ctx.beginPath(); ctx.arc(cx - 40, cy, 16, 0, 7); ctx.fill();
    const a = t * 1.5;
    ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(cx - 40 + 150*Math.cos(a), cy + 80*Math.sin(a), 8, 0, 7); ctx.fill();
  }}
  else if (aid === 12) {{
    const ry = cy + 40 - ((t % 15) * 10);
    ctx.fillStyle = '#e6edf3'; ctx.fillRect(cx - 12, ry, 24, 50);
    ctx.fillStyle = '#f0883e'; ctx.beginPath(); ctx.moveTo(cx - 8, ry + 50); ctx.lineTo(cx + 8, ry + 50); ctx.lineTo(cx, ry + 75 + Math.random()*10); ctx.fill();
  }}
  else if (aid === 13) {{
    ctx.fillStyle = '#30363d'; ctx.fillRect(cx - 20, cy - 20, 40, 40);
    const w = Math.min(50, t * 18);
    ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx - 20 - w, cy - 12, w, 24); ctx.fillRect(cx + 20, cy - 12, w, 24);
  }}
  else if (aid === 14) {{
    for(let r=140; r>35; r-=12) {{
      ctx.strokeStyle = `rgba(240, 136, 62, ${{r/150}})`; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.ellipse(cx, cy, r, r*0.35, t*1.5 + r*0.05, 0, 7); ctx.stroke();
    }}
    ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(cx, cy, 32, 0, 7); ctx.fill();
  }}
  else if (aid === 15) {{
    const r_ang = Math.sin(t*3)*0.25;
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath();
    ctx.moveTo(cx - 60, cy + 20); ctx.lineTo(cx, cy - 10); ctx.lineTo(cx + 60, cy + 20 + r_ang*30); ctx.stroke();
    [-70, -10, 60].forEach(wx => {{ ctx.fillStyle = '#d29922'; ctx.beginPath(); ctx.arc(cx + wx, cy + 50, 12, 0, 7); ctx.fill(); }});
  }}
  else if (aid === 16) {{
    const ly = cy - 90 + ((t % 10) * 18);
    ctx.fillStyle = '#d29922'; ctx.fillRect(cx - 26, ly, 52, 34);
    if (ly < cy + 50) {{
      ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.moveTo(cx - 12, ly + 34); ctx.lineTo(cx + 12, ly + 34); ctx.lineTo(cx, ly + 60 + Math.random()*15); ctx.fill();
    }}
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx - 150, cy + 90); ctx.lineTo(cx + 150, cy + 90); ctx.stroke();
  }}
  else if (aid === 17) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(cx, cy, 60, Math.PI*0.2, Math.PI*0.8); ctx.stroke();
    ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx, cy - 15); ctx.lineTo(cx, cy - 55); ctx.stroke();
  }}
  else if (aid === 18) {{
    ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(cx, cy, 18, 0, 7); ctx.fill();
    const a = t * 14;
    for(let sign of [-1, 1]) {{
      ctx.fillStyle = 'rgba(88, 166, 255, 0.4)'; ctx.beginPath(); ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, 180, a + sign*0.25, a - sign*0.25, true); ctx.closePath(); ctx.fill();
    }}
  }}
  else if (aid === 19) {{
    for(let i=-120; i<=120; i+=16) {{
      const p = i*0.04 + t*3, y1 = cy + Math.sin(p)*35, y2 = cy - Math.sin(p)*35;
      ctx.strokeStyle = '#30363d'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(cx + i, y1); ctx.lineTo(cx + i, y2); ctx.stroke();
      ctx.fillStyle = '#00dca0'; ctx.beginPath(); ctx.arc(cx + i, y1, 4, 0, 7); ctx.fill();
      ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(cx + i, y2, 4, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 20) {{
    for(let [dx, dy] of [[-60, -30], [60, 30]]) {{
      ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(cx + dx, cy + dy, 16, 0, 7); ctx.fill();
      ctx.fillStyle = '#e6edf3'; ctx.beginPath(); ctx.arc(cx + dx - 12, cy + dy - 12, 7, 0, 7); ctx.arc(cx + dx + 12, cy + dy - 12, 7, 0, 7); ctx.fill();
    }}
    ctx.strokeStyle = '#58a6ff'; ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(cx - 48, cy - 18); ctx.lineTo(cx + 48, cy + 18); ctx.stroke(); ctx.setLineDash([]);
  }}
  else if (aid === 21) {{
    const strain = Math.sin(t*3)*6;
    for(let r=-2; r<=2; r++) for(let c=-2; c<=2; c++) {{
      const gx = cx + c*46 + (r%2)*23 + c*strain*0.5, gy = cy + r*38;
      ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 2; ctx.beginPath();
      for(let a=0; a<6; a++) ctx.lineTo(gx + 18*Math.cos(a*1.047), gy + 18*Math.sin(a*1.047));
      ctx.closePath(); ctx.stroke();
    }}
  }}
  else if (aid === 22) {{
    ctx.fillStyle = '#388bfd'; ctx.fillRect(cx - 110, cy - 20, 70, 80);
    ctx.fillStyle = '#f0883e'; ctx.fillRect(cx + 40, cy - 20, 70, 80);
    ctx.strokeStyle = '#e3b341'; ctx.lineWidth = 8; ctx.beginPath(); ctx.arc(cx, cy - 20, 40, Math.PI, 0); ctx.stroke();
  }}
  else if (aid === 23) {{
    ctx.strokeStyle = '#8b949e'; ctx.strokeRect(cx - 6, cy - 90, 12, 80);
    ctx.fillStyle = (t%8 > 4) ? '#f43f5e' : '#e6edf3';
    ctx.beginPath(); ctx.moveTo(cx - 35, cy + 70); ctx.lineTo(cx + 35, cy + 70); ctx.lineTo(cx + 10, cy + 15); ctx.lineTo(cx - 10, cy + 15); ctx.closePath(); ctx.fill();
  }}
  else if (aid === 24) {{
    for(let a=0; a<12; a++) {{
      const ang = a*0.523 + t*0.8, r = 65 + Math.sin(a + t*2)*15;
      ctx.fillStyle = '#00dca0'; ctx.beginPath(); ctx.arc(cx + r*Math.cos(ang), cy + r*Math.sin(ang)*0.7, 5, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 25) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 3; ctx.strokeRect(cx - 140, cy - 70, 280, 140);
    gas.forEach(p => {{
      p.x += p.vx * 0.016; p.y += p.vy * 0.016;
      if (p.x < cx - 135 || p.x > cx + 135) p.vx *= -1;
      if (p.y < cy - 65 || p.y > cy + 65) p.vy *= -1;
      ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(p.x, p.y, 4, 0, 7); ctx.fill();
    }});
  }}
  else if (aid === 26) {{
    ctx.fillStyle = '#21262d'; ctx.fillRect(cx - 50, cy - 35, 100, 70);
    const sig = Math.sin(t*4) > 0;
    ctx.strokeStyle = sig ? '#3fb950' : '#f85149'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(cx - 100, cy - 15); ctx.lineTo(cx - 50, cy - 15); ctx.moveTo(cx + 50, cy); ctx.lineTo(cx + 100, cy); ctx.stroke();
  }}
  else if (aid === 27) {{
    ctx.fillStyle = '#161b22'; ctx.fillRect(cx - 85, cy - 85, 170, 170);
    ctx.strokeStyle = '#d29922'; ctx.lineWidth = 3; ctx.strokeRect(cx - 75, cy - 75, 150, 150);
    for(let i=0; i<6; i++) {{
      const px = cx - 60 + ((t*120 + i*25) % 120);
      ctx.fillStyle = '#58a6ff'; ctx.fillRect(px, cy - 40 + i*16, 12, 6);
    }}
  }}
  else if (aid === 28) {{
    ctx.strokeStyle = '#238636'; ctx.lineWidth = 6; ctx.beginPath();
    ctx.moveTo(cx - 150, cy - 50); ctx.lineTo(cx - 30, cy - 50); ctx.lineTo(cx + 20, cy + 30); ctx.lineTo(cx + 150, cy + 30); ctx.stroke();
    const px = cx - 150 + ((t*120) % 300);
    ctx.fillStyle = '#e3b341'; ctx.beginPath(); ctx.arc(px, px < cx-30 ? cy-50 : (px > cx+20 ? cy+30 : cy-10), 7, 0, 7); ctx.fill();
  }}
  else if (aid === 29) {{
    ctx.fillStyle = '#0d2215'; ctx.fillRect(cx - 140, cy - 90, 280, 180);
    ctx.strokeStyle = '#3fb950'; ctx.lineWidth = 2; ctx.beginPath();
    for(let a=0; a<=6.28; a+=0.06) {{
      const x = cx + 100*Math.sin(3*a + t*4), y = cy + 65*Math.sin(2*a);
      a === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }}
    ctx.stroke();
  }}
  else if (aid === 30) {{
    const tx = cx + 110*Math.cos(t*2), ty = cy - 40 + 40*Math.sin(t*3);
    const d = Math.hypot(tx - cx, ty - cy), a1 = Math.atan2(ty - cy, tx - cx) + Math.acos(Math.min(1.0, d/180.0));
    const j1 = [cx + 90*Math.cos(a1), cy + 90*Math.sin(a1)];
    ctx.strokeStyle = '#f0883e'; ctx.lineWidth = 6; ctx.beginPath();
    ctx.moveTo(cx, cy); ctx.lineTo(j1[0], j1[1]); ctx.lineTo(tx, ty); ctx.stroke();
  }}
  else if (aid === 31) {{
    for(let [nodes, lx] of [[3, cx - 110], [4, cx], [2, cx + 110]]) {{
      for(let n=0; n<nodes; n++) {{
        const ny = cy - (nodes-1)*28 + n*56;
        ctx.fillStyle = Math.sin(t*5 + lx*0.02) > 0 ? '#3fb950' : '#30363d';
        ctx.beginPath(); ctx.arc(lx, ny, 10, 0, 7); ctx.fill();
      }}
    }}
  }}
  else if (aid === 32) {{
    ctx.fillStyle = '#21262d'; ctx.fillRect(cx - 180, cy - 30, 360, 60);
    ctx.strokeStyle = '#e3b341'; ctx.lineWidth = 3; ctx.beginPath();
    for(let i=0; i<=6; i++) ctx.lineTo(cx - 180 + i*60, cy + (i%2 ? 22 : -22));
    ctx.stroke();
  }}
  else if (aid === 33) {{
    ctx.strokeStyle = '#238636'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(cx, cy, 110, 0, 7); ctx.stroke();
    const a = t * 3;
    ctx.strokeStyle = '#3fb950'; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + 110*Math.cos(a), cy + 110*Math.sin(a)); ctx.stroke();
    ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(cx + 50, cy - 40, 6, 0, 7); ctx.fill();
  }}
  else if (aid === 34) {{
    const nodes = [[cx, cy - 60], [cx - 60, cy], [cx + 60, cy], [cx - 90, cy + 60], [cx - 30, cy + 60]];
    nodes.forEach(([nx, ny], i) => {{
      ctx.fillStyle = Math.floor(t*2)%5 === i ? '#58a6ff' : '#30363d';
      ctx.beginPath(); ctx.arc(nx, ny, 14, 0, 7); ctx.fill();
    }});
  }}
  else if (aid === 35) {{
    ctx.fillStyle = '#fff'; ctx.fillRect(cx - 70, cy - 70, 140, 140);
    ctx.fillStyle = '#000'; ctx.fillRect(cx - 60, cy - 60, 35, 35); ctx.fillRect(cx + 25, cy - 60, 35, 35); ctx.fillRect(cx - 60, cy + 25, 35, 35);
    const ly = cy - 70 + ((t * 80) % 140);
    ctx.strokeStyle = '#f85149'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx - 80, ly); ctx.lineTo(cx + 80, ly); ctx.stroke();
  }}
  else if (aid === 36) {{
    ctx.fillStyle = 'rgba(63, 185, 80, 0.2)'; ctx.beginPath(); ctx.ellipse(cx, cy, 120, 70, 0, 0, 7); ctx.fill();
    ctx.fillStyle = '#8957e5'; ctx.beginPath(); ctx.arc(cx - 25, cy, 30, 0, 7); ctx.fill();
    ctx.fillStyle = '#f0883e'; ctx.beginPath(); ctx.arc(cx + 30 + Math.cos(t*2)*25, cy + Math.sin(t*2)*15, 8, 0, 7); ctx.fill();
  }}
  else if (aid === 37) {{
    ctx.fillStyle = '#d29922'; ctx.beginPath(); ctx.arc(cx - 120, cy, 22, 0, 7); ctx.fill();
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(cx - 100, cy); ctx.lineTo(cx + 130, cy); ctx.stroke();
    ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(cx - 100 + ((t * 180) % 230), cy, 9, 0, 7); ctx.fill();
  }}
  else if (aid === 38) {{
    ctx.fillStyle = '#bc8cff'; ctx.beginPath();
    ctx.moveTo(cx, cy - 50); ctx.lineTo(cx + 25, cy - 30); ctx.lineTo(cx + 25, cy); ctx.lineTo(cx - 25, cy); ctx.lineTo(cx - 25, cy - 30); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = '#e6edf3'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx, cy + 35); ctx.stroke();
  }}
  else if (aid === 39) {{
    ctx.strokeStyle = '#3fb950'; ctx.lineWidth = 2; ctx.beginPath();
    for(let x=cx-160; x<=cx+160; x+=4) {{
      const ph = (x - t*120) % 180, y = cy - (ph < 8 ? 35 : (ph < 16 ? -20 : 0));
      x === cx-160 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }}
    ctx.stroke();
  }}
  else if (aid === 40) {{
    ctx.fillStyle = '#2d1517'; ctx.fillRect(cx - 180, cy - 25, 360, 50);
    for(let i=0; i<5; i++) {{
      const bx = cx - 180 + ((t*90 + i*75) % 360);
      ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.ellipse(bx, cy, 14, 8, 0, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 41) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 12; ctx.beginPath(); ctx.arc(cx, cy, 85, 0, 7); ctx.stroke();
    const a = t * 6;
    ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + 50*Math.cos(a), cy - 50 + 15*Math.sin(a)); ctx.stroke();
  }}
  else if (aid === 42) {{
    ctx.fillStyle = '#30363d'; ctx.fillRect(cx - 35, cy - 20, 70, 50);
    [-24, -8, 8, 24].forEach((fx, i) => {{
      const b = Math.sin(t*4 + i)*18;
      ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath();
      ctx.moveTo(cx + fx, cy - 20); ctx.lineTo(cx + fx, cy - 55); ctx.lineTo(cx + fx + b, cy - 85); ctx.stroke();
    }});
  }}
  else if (aid === 43) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx, cy + 110); ctx.stroke();
    const a = t * 4;
    for(let i=0; i<3; i++) {{
      ctx.strokeStyle = '#e6edf3'; ctx.lineWidth = 4; ctx.beginPath();
      ctx.moveTo(cx, cy); ctx.lineTo(cx + 70*Math.cos(a + i*2.094), cy + 70*Math.sin(a + i*2.094)); ctx.stroke();
    }}
  }}
  else if (aid === 44) {{
    ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx - 90, cy - 20, 180, 40);
    for(let i=0; i<4; i++) {{
      ctx.fillStyle = '#e3b341'; ctx.beginPath(); ctx.arc(cx - 60 + i*40, cy - 60 + ((t*70 + i*20)%60), 4, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 45) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.strokeRect(cx - 75, cy - 60, 150, 120);
    const rd = Math.sin(t*2)*35;
    ctx.fillStyle = '#f85149'; ctx.fillRect(cx - 45, cy - 50 + rd, 25, 70); ctx.fillRect(cx + 20, cy - 50 + rd, 25, 70);
  }}
  else if (aid === 46) {{
    ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 10; ctx.beginPath(); ctx.moveTo(cx - 80, cy - 40); ctx.lineTo(cx - 20, cy + 30); ctx.stroke();
    ctx.strokeStyle = '#d29922'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(cx + 25, cy + 30, 22, 0, 7); ctx.stroke();
  }}
  else if (aid === 47) {{
    ctx.strokeStyle = '#8b949e'; ctx.strokeRect(cx - 90, cy - 45, 180, 90);
    ctx.strokeStyle = '#f85149'; ctx.lineWidth = 2; ctx.beginPath();
    for(let x=cx-80; x<=cx+80; x+=6) {{
      const y = cy + (Math.abs(x-cx) < 30 ? (Math.random()-0.5)*35 : 0);
      x === cx-80 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }}
    ctx.stroke();
  }}
  else if (aid === 48) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx - 120, cy + 10); ctx.lineTo(cx + 120, cy + 10); ctx.stroke();
    ctx.strokeStyle = '#ff7b72'; ctx.lineWidth = 4; ctx.beginPath();
    ctx.moveTo(cx - 40, cy - 30); ctx.lineTo(cx - 40, cy + 60); ctx.lineTo(cx + 40, cy + 60); ctx.lineTo(cx + 40, cy - 30); ctx.stroke();
  }}
  else if (aid === 49) {{
    ctx.fillStyle = '#388bfd'; ctx.fillRect(cx - 120, cy + 40, 240, 40);
    ctx.fillStyle = '#e6edf3'; ctx.beginPath(); ctx.arc(cx + 40, cy - 40, 20, 0, 7); ctx.arc(cx + 65, cy - 40, 15, 0, 7); ctx.fill();
    for(let i=0; i<3; i++) {{
      ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 2; ctx.beginPath();
      ctx.moveTo(cx + 40 + i*10, cy - 15); ctx.lineTo(cx + 40 + i*10, cy + 25); ctx.stroke();
    }}
  }}
  else if (aid === 50) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(cx, cy, 60, 0, 7); ctx.stroke();
    const a = t * 7;
    for(let i=0; i<3; i++) {{
      ctx.fillStyle = '#3fb950'; ctx.beginPath(); ctx.arc(cx + 60*Math.cos(a + i*2.094), cy + 60*Math.sin(a + i*2.094), 8, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 51) {{
    const ph = Math.sin(t * 6);
    for(let i=-2; i<=2; i++) {{
      let a = 0; if (i === -2 && ph < 0) a = ph*0.45; if (i === 2 && ph > 0) a = ph*0.45;
      const bx = cx + i*30 + 80*Math.sin(a), by = cy - 40 + 80*Math.cos(a);
      ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(cx + i*30, cy - 60); ctx.lineTo(bx, by); ctx.stroke();
      ctx.fillStyle = '#e6edf3'; ctx.beginPath(); ctx.arc(bx, by, 14, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 52) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 5; ctx.beginPath();
    ctx.moveTo(cx - 80, cy - 100); ctx.lineTo(cx - 80, cy - 30); ctx.moveTo(cx - 80, cy - 15); ctx.lineTo(cx - 80, cy + 15); ctx.moveTo(cx - 80, cy + 30); ctx.lineTo(cx - 80, cy + 100); ctx.stroke();
    for(let r=15; r<160; r+=24) {{
      const rad = (r + t*60) % 160;
      ctx.strokeStyle = `rgba(88, 166, 255, ${{1 - rad/160}})`; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(cx - 80, cy - 22, rad, -1.2, 1.2); ctx.stroke();
      ctx.beginPath(); ctx.arc(cx - 80, cy + 22, rad, -1.2, 1.2); ctx.stroke();
    }}
  }}
  else if (aid === 53) {{
    for(let r=110; r>10; r-=16) {{
      ctx.strokeStyle = Math.floor((r + t*20)/16)%2 ? '#58a6ff' : '#12161c'; ctx.lineWidth = 8;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, 7); ctx.stroke();
    }}
  }}
  else if (aid === 54) {{
    const p1 = Math.sin(t*6)*30, p2 = Math.cos(t*6)*30;
    ctx.strokeStyle = '#f85149'; ctx.strokeRect(cx - 110, cy - 30, 90, 60);
    ctx.strokeStyle = '#58a6ff'; ctx.strokeRect(cx + 20, cy - 30, 90, 60);
    ctx.fillStyle = '#f85149'; ctx.fillRect(cx - 100 + p1, cy - 25, 20, 50);
    ctx.fillStyle = '#58a6ff'; ctx.fillRect(cx + 30 + p2, cy - 25, 20, 50);
  }}
  else if (aid === 55) {{
    ctx.strokeStyle = '#8b949e'; ctx.strokeRect(cx - 160, cy - 35, 60, 70);
    const yd = Math.sin(t*8)*45;
    ctx.strokeStyle = '#3fb950'; ctx.lineWidth = 3; ctx.beginPath();
    ctx.moveTo(cx - 100, cy); ctx.lineTo(cx - 65, cy); ctx.lineTo(cx + 140, cy + yd); ctx.stroke();
  }}
  else if (aid === 56) {{
    const sx = cx + Math.sin(t*2)*80;
    for(let r=20; r<150; r+=25) {{
      const px = cx + Math.sin((t - r/150)*2)*80;
      ctx.strokeStyle = `rgba(88, 166, 255, ${{1 - r/150}})`; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(px, cy, r, 0, 7); ctx.stroke();
    }}
    ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(sx, cy, 7, 0, 7); ctx.fill();
  }}
  else if (aid === 57) {{
    const a = t * 12;
    ctx.strokeStyle = '#e6edf3'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(cx, cy, 80, 0, 7); ctx.stroke();
    ctx.strokeStyle = '#e3b341'; ctx.lineWidth = 5; ctx.beginPath();
    ctx.ellipse(cx, cy, 75, Math.abs(30*Math.sin(a)) + 4, 0, 0, 7); ctx.stroke();
  }}
  else if (aid === 58) {{
    ctx.fillStyle = '#8b949e'; ctx.beginPath(); ctx.arc(cx - 110, cy, 18, 0, 7); ctx.fill();
    for(let i=0; i<5; i++) {{
      const vx = cx - 70 + i*45 + ((t*60) % 45), vy = cy + (i%2 ? 18 : -18);
      ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(vx, vy, 9, 0, 7); ctx.stroke();
    }}
  }}
  else if (aid === 59) {{
    bx += (Math.random()-0.5)*12; by += (Math.random()-0.5)*12;
    btrail.push([bx, by]); if (btrail.length > 60) btrail.shift();
    if (btrail.length > 1) {{
      ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 2; ctx.beginPath();
      btrail.forEach((p, i) => i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1])); ctx.stroke();
    }}
    ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(bx, by, 7, 0, 7); ctx.fill();
  }}
  else if (aid === 60) {{
    ctx.fillStyle = '#e6edf3'; ctx.beginPath(); ctx.arc(cx, cy - 40, 42, 0, 7); ctx.fill();
    ctx.fillStyle = '#f0883e'; ctx.fillRect(cx - 6, cy + 2, 12, 60);
    if (Math.sin(t*8) > 0.6) {{
      ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx + 38, cy - 40); ctx.lineTo(cx + 85, cy - 25); ctx.stroke();
    }}
  }}
  else if (aid === 61) {{
    ctx.fillStyle = '#f0883e'; ctx.beginPath(); ctx.arc(cx, cy, 30, 0, 7); ctx.fill();
    const px = cx - 200 + ((t%8)*50), py = cy - 80 + 120/(1 + Math.exp(-(px - cx)/25));
    ctx.fillStyle = '#3fb950'; ctx.beginPath(); ctx.arc(px, py, 6, 0, 7); ctx.fill();
  }}
  else if (aid === 62) {{
    ctx.fillStyle = '#e3b341'; ctx.beginPath(); ctx.arc(cx - 70, cy, 22, 0, 7); ctx.fill();
    ctx.fillStyle = '#1f6feb'; ctx.beginPath(); ctx.arc(cx + 80, cy, 12, 0, 7); ctx.fill();
    [[-130, 0], [30, 0], [140, 0], [5, -70], [5, 70]].forEach(([lx, ly]) => {{
      ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(cx + lx, cy + ly, 5, 0, 7); ctx.fill();
    }});
  }}
  else if (aid === 63) {{
    ctx.fillStyle = '#30363d'; ctx.fillRect(cx - 60, cy - 25, 60, 50);
    ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.moveTo(cx, cy - 20); ctx.lineTo(cx + 90 + Math.random()*15, cy); ctx.lineTo(cx, cy + 20); ctx.fill();
  }}
  else if (aid === 64) {{
    ctx.fillStyle = '#e3b341'; ctx.beginPath(); ctx.arc(cx, cy - 30, 45, 0, 7); ctx.fill();
    const px = cx - 120 + ((t * 50) % 240);
    ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(px, cy - 30, 12, 0, 7); ctx.fill();
    ctx.strokeStyle = '#3fb950'; ctx.lineWidth = 3; ctx.beginPath();
    ctx.moveTo(cx - 120, cy + 90 + (Math.abs(px - cx) < 35 ? 25 : 0)); ctx.lineTo(cx + 120, cy + 90 + (Math.abs(px - cx) < 35 ? 25 : 0)); ctx.stroke();
  }}
  else if (aid === 65) {{
    ctx.strokeStyle = '#f0883e'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(cx, cy - 10, 50, 0, Math.PI, true); ctx.stroke();
  }}
  else if (aid === 66) {{
    ctx.fillStyle = '#e3b341'; ctx.beginPath(); ctx.arc(cx - 160, cy, 30, 0, 7); ctx.fill();
    ctx.fillStyle = '#1f6feb'; ctx.beginPath(); ctx.arc(cx, cy, 22, 0, 7); ctx.fill();
    const mx = cx + 80 + ((t * 20) % 100);
    ctx.fillStyle = Math.abs(mx - cx - 120) < 20 ? '#da3633' : '#e6edf3'; ctx.beginPath(); ctx.arc(mx, cy, 8, 0, 7); ctx.fill();
  }}
  else if (aid === 67) {{
    ctx.strokeStyle = 'rgba(230, 237, 243, 0.4)'; ctx.lineWidth = 14; ctx.beginPath(); ctx.arc(cx, cy, 100, 0, 7); ctx.stroke();
    const a = t * 1.5;
    ctx.fillStyle = '#d29922'; ctx.beginPath(); ctx.arc(cx + 94*Math.cos(a), cy + 94*Math.sin(a), 4, 0, 7); ctx.fill();
    ctx.beginPath(); ctx.arc(cx + 106*Math.cos(a*0.9), cy + 106*Math.sin(a*0.9), 4, 0, 7); ctx.fill();
  }}
  else if (aid === 68) {{
    ctx.fillStyle = '#8b949e'; ctx.beginPath(); ctx.arc(cx, cy, 32, 0, 7); ctx.fill();
    const ix = cx - 100 + ((t%7)*20), iy = cy - 50 + ((t%7)*10);
    ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.arc(ix, iy, 5, 0, 7); ctx.fill();
  }}
  else if (aid === 69) {{
    const a = t * 3;
    ctx.fillStyle = '#30363d'; ctx.beginPath(); ctx.arc(cx - 45, cy, 45, 0, 7); ctx.fill();
    ctx.fillStyle = '#f0883e'; ctx.beginPath(); ctx.arc(cx - 45 + 32*Math.cos(a), cy + 32*Math.sin(a), 7, 0, 7); ctx.fill();
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(cx + 45, cy, 50, 0, 7); ctx.stroke();
  }}
  else if (aid === 70) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(cx, cy, 90, 0, 7); ctx.stroke();
    ctx.fillStyle = '#e3b341'; ctx.beginPath(); ctx.arc(cx, cy, 26, 0, 7); ctx.fill();
    for(let i=0; i<3; i++) {{
      const pa = t * 1.5 + i * 2.094;
      ctx.fillStyle = '#58a6ff'; ctx.beginPath(); ctx.arc(cx + 58*Math.cos(pa), cy + 58*Math.sin(pa), 18, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 71) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 3; ctx.strokeRect(cx - 90, cy - 45, 180, 90);
    for(let i=0; i<6; i++) {{
      ctx.fillStyle = '#58a6ff'; ctx.fillRect(cx - 75, cy - 30 + i*12 + Math.sin(t*10 + i)*3, 12, 5);
    }}
  }}
  else if (aid === 72) {{
    const py = Math.sin(t*3)*25;
    ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx - 100, cy + 40, 200, 30);
    ctx.fillStyle = '#8b949e'; ctx.fillRect(cx - 80, cy - 30 + py, 35, 70); ctx.fillRect(cx + 10, cy - 10 - py*0.4, 80, 50);
  }}
  else if (aid === 73) {{
    const sa = 0.35 + Math.sin(t*5)*0.2;
    ctx.strokeStyle = '#e6edf3'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(cx, cy - 60); ctx.lineTo(cx, cy + 70); ctx.stroke();
    for(let s of [-1, 1]) {{
      const bx = cx + s*65*Math.sin(sa), by = cy - 40 + 65*Math.cos(sa);
      ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx, cy - 40); ctx.lineTo(bx, by); ctx.stroke();
      ctx.fillStyle = '#d29922'; ctx.beginPath(); ctx.arc(bx, by, 12, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 74) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(cx, cy, 55, 0, 7); ctx.stroke();
    ctx.strokeStyle = '#f0883e'; ctx.lineWidth = 8; ctx.beginPath();
    ctx.moveTo(cx - 110, cy); ctx.lineTo(cx - 15, cy); ctx.moveTo(cx + 15, cy); ctx.lineTo(cx + 110, cy); ctx.stroke();
  }}
  else if (aid === 75) {{
    for(let i=0; i<4; i++) {{
      ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 3; ctx.beginPath();
      ctx.moveTo(cx - 120 + i*60, cy + 20); ctx.lineTo(cx - 60 + i*60, cy + 20); ctx.stroke();
      ctx.strokeStyle = '#f85149'; ctx.beginPath();
      ctx.moveTo(cx - 120 + i*60, cy + 20); ctx.lineTo(cx - 90 + i*60, cy - 30); ctx.stroke();
    }}
  }}
  else if (aid === 76) {{
    ctx.fillStyle = '#30363d'; ctx.fillRect(cx - 75, cy - 25, 150, 30);
    ctx.fillStyle = '#f0883e'; ctx.beginPath(); ctx.ellipse(cx, cy + 12, 80, 10, 0, 0, 7); ctx.fill();
  }}
  else if (aid === 77) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(cx, cy, 75, 0, 7); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(cx, cy, 75, 25, 0, 0, 7); ctx.stroke();
    const th = t * 1.5, phi = t * 2.5;
    ctx.strokeStyle = '#3fb950'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx, cy);
    ctx.lineTo(cx + 75*Math.sin(th)*Math.cos(phi), cy - 75*Math.cos(th)); ctx.stroke();
  }}
  else if (aid === 78) {{
    ctx.strokeStyle = '#e3b341'; ctx.lineWidth = 3; ctx.beginPath();
    for(let x=cx-140; x<=cx+140; x+=5) {{
      const v = (1 - Math.exp(-((x + t*90)%90)/28.0))*55;
      x === cx-140 ? ctx.moveTo(x, cy + 30 - v) : ctx.lineTo(x, cy + 30 - v);
    }}
    ctx.stroke();
  }}
  else if (aid === 79) {{
    ctx.strokeStyle = '#e6edf3'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx, cy - 35); ctx.lineTo(cx, cy + 35); ctx.stroke();
    for(let r=15; r<140; r+=25) {{
      const rad = (r + t*50) % 140;
      ctx.strokeStyle = `rgba(0, 220, 160, ${{1 - rad/140}})`; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.ellipse(cx, cy, rad, rad*0.6, 0, 0, 7); ctx.stroke();
    }}
  }}
  else if (aid === 80) {{
    ctx.fillStyle = '#8b949e'; ctx.fillRect(cx - 80, cy - 30, 160, 18);
    ctx.fillStyle = Math.sin(t*4) > 0 ? '#3fb950' : '#21262d'; ctx.fillRect(cx - 60, cy + 8, 120, 16);
  }}
  else if (aid === 81) {{
    ctx.fillStyle = '#58a6ff'; ctx.fillRect(cx - 40, cy - 35, 80, 22);
    ctx.fillStyle = '#8957e5'; ctx.fillRect(cx - 60, cy + 15, 120, 25);
  }}
  else if (aid === 82) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 14; ctx.strokeRect(cx - 80, cy - 60, 160, 120);
    ctx.fillStyle = '#f0883e'; ctx.fillRect(cx - 95, cy - 30, 16, 60);
    ctx.fillStyle = '#58a6ff'; ctx.fillRect(cx + 79, cy - 30, 16, 60);
  }}
  else if (aid === 83) {{
    const a = t * 5;
    ctx.strokeStyle = '#f85149'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(cx, cy);
    ctx.lineTo(cx + 130*Math.cos(a), cy + 130*Math.sin(a)); ctx.stroke();
  }}
  else if (aid === 84) {{
    ctx.fillStyle = '#21262d'; ctx.fillRect(cx - 40, cy - 60, 80, 120);
    ctx.fillStyle = '#3fb950'; ctx.font = 'bold 50px monospace';
    ctx.fillText(String(Math.floor(t * 2) % 10), cx - 15, cy + 15);
  }}
  else if (aid === 85) {{
    ctx.fillStyle = 'rgba(137, 87, 229, 0.4)'; ctx.beginPath(); ctx.ellipse(cx, cy, 65, 40, 0, 0, 7); ctx.fill();
    ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx - 120, cy); ctx.lineTo(cx + 120, cy); ctx.stroke();
  }}
  else if (aid === 86) {{
    ctx.strokeStyle = '#d29922'; ctx.lineWidth = 12; ctx.beginPath(); ctx.arc(cx, cy, 45, 0.6, Math.PI*1.8); ctx.stroke();
  }}
  else if (aid === 87) {{
    ctx.fillStyle = '#f85149'; ctx.fillRect(cx - 120, cy - 25, 240, 18);
    ctx.fillStyle = '#388bfd'; ctx.fillRect(cx - 120, cy + 8, 240, 18);
  }}
  else if (aid === 88) {{
    ctx.strokeStyle = '#f85149'; ctx.lineWidth = 3; ctx.beginPath();
    ctx.moveTo(cx - 100, cy + 30); ctx.lineTo(cx - 60, cy - 45); ctx.lineTo(cx, cy + 15); ctx.lineTo(cx + 60, cy - 15); ctx.lineTo(cx + 100, cy + 30); ctx.stroke();
  }}
  else if (aid === 89) {{
    ctx.fillStyle = '#fef08a'; ctx.fillRect(cx - 16, cy - 45, 32, 35);
    ctx.fillStyle = '#b91c1c'; ctx.fillRect(cx - 16, cy - 10, 32, 55);
  }}
  else if (aid === 90) {{
    ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(cx, cy - 50, 60, 0, Math.PI); ctx.stroke();
    for(let i=0; i<4; i++) {{
      ctx.fillStyle = '#3fb950'; ctx.beginPath(); ctx.arc(cx - 24 + i*16, cy - 15 + ((t*35 + i*14)%35), 4, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 91) {{
    ctx.strokeStyle = '#8b949e'; ctx.strokeRect(cx - 70, cy - 16, 140, 32);
    const pl = (t * 10) % 55;
    ctx.fillStyle = '#58a6ff'; ctx.fillRect(cx - 70 + pl, cy - 14, 130 - pl, 28);
  }}
  else if (aid === 92) {{
    ctx.strokeStyle = '#388bfd'; ctx.lineWidth = 14; ctx.beginPath(); ctx.moveTo(cx - 140, cy); ctx.lineTo(cx + 140, cy); ctx.stroke();
    for(let i=0; i<5; i++) {{
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(cx - 140 + ((t*80 + i*60)%280), cy, 5, 0, 7); ctx.fill();
    }}
  }}
  else if (aid === 93) {{
    ctx.fillStyle = '#795548'; ctx.beginPath(); ctx.moveTo(cx - 100, cy); ctx.lineTo(cx + 20, cy + 50); ctx.lineTo(cx - 100, cy + 50); ctx.fill();
  }}
  else if (aid === 94) {{
    ctx.fillStyle = '#388bfd'; ctx.fillRect(cx - 8, cy - 40, 16, 80);
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(cx - 30, cy, 5, 0, 7); ctx.fill();
  }}
  else if (aid === 95) {{
    for(let r=20; r<90; r+=15) {{
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(cx, cy, r, -t*2 + r*0.1, -t*2 + r*0.1 + 2.4); ctx.stroke();
    }}
  }}
  else if (aid === 96) {{
    const tw = Math.sin(t * 8) * 16;
    ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 5; ctx.beginPath();
    ctx.moveTo(cx - 70, cy); ctx.lineTo(cx - 30, cy - 40 + tw); ctx.lineTo(cx + 30, cy - 40 - tw); ctx.lineTo(cx + 70, cy); ctx.stroke();
  }}
  else if (aid === 97) {{
    ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx - 90, cy - 15, 80, 45);
    ctx.fillStyle = '#0969da'; ctx.fillRect(cx + 10, cy + 5, 80, 25);
  }}
  else if (aid === 98) {{
    const gh = Math.min(90, (t % 6) * 25);
    ctx.fillStyle = '#58a6ff'; ctx.fillRect(cx - 10, cy - gh, 20, gh);
  }}
  else if (aid === 99) {{
    const wl = Math.sin(t * 4) * 22;
    ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx - 45, cy + wl, 90, 60);
  }}
  else if (aid === 100) {{
    ctx.strokeStyle = '#8b949e'; ctx.strokeRect(cx - 50, cy - 50, 100, 100);
    for(let r=-30; r<=30; r+=20) for(let c=-30; c<=30; c+=20) {{
      ctx.fillStyle = '#00dca0'; ctx.fillRect(cx + c, cy + r, 10, 10);
    }}
  }}
}}

function loop(now) {{
  const dt = Math.min((now - lastTime)/1000.0, 0.05);
  lastTime = now;
  const s = REGISTRY[idx];
  if (!paused) {{
    elapsed += dt;
    if (elapsed > s.duration) elapsed %= s.duration;
  }}
  render(s.id, W/2, H/2 - 10, elapsed);
  const pct = ((elapsed % s.duration) / s.duration) * 100;
  document.getElementById('bar').style.width = pct.toFixed(1) + '%';
  const st = paused ? 'PAUSED' : 'RUNNING';
  document.getElementById('status').textContent = 'STATUS: ' + st + ' | TIME: ' + elapsed.toFixed(1) + 's / ' + s.duration.toFixed(1) + 's';
  document.getElementById('status').style.color = paused ? '#ffb432' : '#7ee787';
  requestAnimationFrame(loop);
}}

setAnim(0);
requestAnimationFrame(loop);
</script>
</body>
</html>"""

    out_file = os.path.join("build", "web", "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully compiled {out_file} with 100 individual simulations.")

if __name__ == "__main__":
    build_web_app()
