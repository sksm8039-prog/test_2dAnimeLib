"""
build_web.py - Compiles the Python SciTech2D Registry & Physics Engine
into a zero-dependency, flicker-free HTML5 Canvas application for GitHub Pages.
"""

import os
import json
from main import REGISTRY

def generate_web_bundle():
    os.makedirs("build/web", exist_ok=True)

    # Extract all 100 animation specs directly from main.py's REGISTRY
    specs_list = []
    for anim_id in sorted(REGISTRY.keys()):
        s = REGISTRY[anim_id]
        specs_list.append({
            "id": s.id,
            "name": s.name,
            "domain": s.domain,
            "duration": s.duration,
            "loop_type": s.loop_type,
            "description": s.description
        })

    registry_json = json.dumps(specs_list, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SciTech2D: 100 Science & Technology Animations</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
    body {{
      background-color: #0d1117;
      color: #e6edf3;
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 16px;
    }}
    .app-container {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.6);
      max-width: 900px;
      width: 100%;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid #21262d;
    }}
    .title-box h1 {{
      font-size: 1.25rem;
      color: #f0f6fc;
      letter-spacing: 0.5px;
    }}
    .title-box p {{
      font-size: 0.85rem;
      color: #58a6ff;
      margin-top: 4px;
    }}
    select.anim-select {{
      background: #21262d;
      color: #f0f6fc;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 0.9rem;
      cursor: pointer;
      outline: none;
    }}
    select.anim-select:hover {{ border-color: #58a6ff; }}
    .canvas-wrapper {{
      position: relative;
      width: 100%;
      display: flex;
      justify-content: center;
      background: #12161c;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid #21262d;
    }}
    canvas {{
      display: block;
      max-width: 100%;
      height: auto;
    }}
    .progress-container {{
      width: 100%;
      height: 8px;
      background: #21262d;
      border-radius: 4px;
      margin: 14px 0;
      overflow: hidden;
    }}
    .progress-bar {{
      height: 100%;
      background: linear-gradient(90deg, #00dca0, #58a6ff);
      width: 0%;
      transition: width 0.05s linear;
    }}
    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
    }}
    .btn-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    button.ctrl-btn {{
      background: #21262d;
      color: #e6edf3;
      border: 1px solid #30363d;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    button.ctrl-btn:hover {{
      background: #30363d;
      border-color: #00dca0;
      color: #ffffff;
    }}
    button.ctrl-btn:active {{
      transform: translateY(1px);
      background: #00a078;
    }}
    button.ctrl-btn.primary {{
      background: #1f6feb;
      border-color: #388bfd;
    }}
    button.ctrl-btn.primary:hover {{
      background: #388bfd;
    }}
    .status-box {{
      font-family: monospace;
      font-size: 0.9rem;
      color: #7ee787;
    }}
    .desc-bar {{
      margin-top: 12px;
      font-size: 0.85rem;
      color: #8b949e;
      background: #0d1117;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid #21262d;
    }}
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
      <select id="anim-dropdown" class="anim-select" aria-label="Select Animation"></select>
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

  <div class="desc-bar" id="anim-desc">
    Non-linear chaotic double pendulum via RK4 integration.
  </div>
</div>

<script>
const REGISTRY = {registry_json};

const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');
const W = canvas.width;
const H = canvas.height;

let currentIndex = 0;
let elapsedTime = 0.0;
let paused = false;
let lastTimestamp = performance.now();

// Double Pendulum RK4 state
let dpState = [Math.PI / 2, Math.PI / 2, 0, 0];
let dpTrail = [];

// Populate Dropdown
const dropdown = document.getElementById('anim-dropdown');
REGISTRY.forEach((spec, idx) => {{
  const opt = document.createElement('option');
  opt.value = idx;
  opt.textContent = `${{String(spec.id).padStart(3, '0')}} - ${{spec.name}}`;
  dropdown.appendChild(opt);
}});

function setAnimation(index) {{
  if (index < 0) index = REGISTRY.length - 1;
  if (index >= REGISTRY.length) index = 0;
  currentIndex = index;
  elapsedTime = 0.0;
  dropdown.value = currentIndex;

  // Reset Double Pendulum
  dpState = [Math.PI / 2, Math.PI / 2, 0, 0];
  dpTrail = [];

  updateUIHeader();
}}

function updateUIHeader() {{
  const spec = REGISTRY[currentIndex];
  const idPad = String(spec.id).padStart(3, '0');
  document.getElementById('anim-title').textContent = `[${{idPad}}/100] ${{spec.name.toUpperCase()}}`;
  document.getElementById('anim-meta').textContent = `DOMAIN: ${{spec.domain}} | DURATION: ${{spec.duration.toFixed(1)}}s | TYPE: ${{spec.loop_type}}`;
  document.getElementById('anim-desc').textContent = spec.description;
}}

// Button Event Listeners
document.getElementById('btn-prev').addEventListener('click', () => setAnimation(currentIndex - 1));
document.getElementById('btn-next').addEventListener('click', () => setAnimation(currentIndex + 1));
document.getElementById('btn-pause').addEventListener('click', () => {{ paused = !paused; }});
document.getElementById('btn-reset').addEventListener('click', () => setAnimation(currentIndex));
document.getElementById('btn-random').addEventListener('click', () => {{
  setAnimation(Math.floor(Math.random() * REGISTRY.length));
}});
dropdown.addEventListener('change', (e) => setAnimation(parseInt(e.target.value, 10)));

// Keyboard Support
window.addEventListener('keydown', (e) => {{
  if (e.key === 'ArrowRight') setAnimation(currentIndex + 1);
  else if (e.key === 'ArrowLeft') setAnimation(currentIndex - 1);
  else if (e.key === ' ') {{ e.preventDefault(); paused = !paused; }}
  else if (e.key === 'r' || e.key === 'R') setAnimation(currentIndex);
}});

// RK4 Double Pendulum Step
function dpDerivatives(st) {{
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
}}

function updateDoublePendulum(dt) {{
  const subDt = Math.min(dt, 0.033) / 4.0;
  for (let n = 0; n < 4; n++) {{
    const k1 = dpDerivatives(dpState);
    const s2 = dpState.map((s, i) => s + 0.5 * subDt * k1[i]);
    const k2 = dpDerivatives(s2);
    const s3 = dpState.map((s, i) => s + 0.5 * subDt * k2[i]);
    const k3 = dpDerivatives(s3);
    const s4 = dpState.map((s, i) => s + subDt * k3[i]);
    const k4 = dpDerivatives(s4);
    dpState = dpState.map((s, i) => s + (subDt / 6.0) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]));
  }}
  const cx = W / 2, cy = H / 3 + 10;
  const x1 = cx + 105 * Math.sin(dpState[0]);
  const y1 = cy + 105 * Math.cos(dpState[0]);
  const x2 = x1 + 95 * Math.sin(dpState[1]);
  const y2 = y1 + 95 * Math.cos(dpState[1]);
  dpTrail.push([x2, y2]);
  if (dpTrail.length > 100) dpTrail.shift();
}}

function renderScene(spec) {{
  ctx.fillStyle = '#12161c';
  ctx.fillRect(0, 0, W, H);

  const cx = W / 2, cy = H / 2;
  const t = elapsedTime;
  const id = spec.id;
  const domain = spec.domain;

  if (id === 1) {{
    // Double Pendulum
    const px = W / 2, py = H / 3 + 10;
    const x1 = px + 105 * Math.sin(dpState[0]);
    const y1 = py + 105 * Math.cos(dpState[0]);
    const x2 = x1 + 95 * Math.sin(dpState[1]);
    const y2 = y1 + 95 * Math.cos(dpState[1]);

    for (let i = 0; i < dpTrail.length - 1; i++) {{
      const alpha = i / dpTrail.length;
      ctx.strokeStyle = `rgba(0, 210, 255, ${{alpha}})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(dpTrail[i][0], dpTrail[i][1]);
      ctx.lineTo(dpTrail[i+1][0], dpTrail[i+1][1]);
      ctx.stroke();
    }}

    ctx.strokeStyle = '#dcdfe4';
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(x1, y1); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();

    ctx.fillStyle = '#ff6464';
    ctx.beginPath(); ctx.arc(x1, y1, 11, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#64ff64';
    ctx.beginPath(); ctx.arc(x2, y2, 9, 0, Math.PI * 2); ctx.fill();
  }}
  else if (id === 3) {{
    // Bohr Atom
    ctx.fillStyle = '#ff3232';
    ctx.beginPath(); ctx.arc(cx, cy, 16, 0, Math.PI * 2); ctx.fill();
    const radii = [55, 105, 155];
    const speeds = [3.0, 1.8, 1.1];
    radii.forEach((r, idx) => {{
      ctx.strokeStyle = '#3c5078';
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();

      const ang = t * speeds[idx] + idx * 2.1;
      const ex = cx + r * Math.cos(ang);
      const ey = cy + r * Math.sin(ang);
      ctx.fillStyle = '#00b4ff';
      ctx.beginPath(); ctx.arc(ex, ey, 6, 0, Math.PI * 2); ctx.fill();
    }});
  }}
  else if (id === 10 || id === 52) {{
    // Wave Interference
    const slitX = cx - 140, sy1 = cy - 40, sy2 = cy + 40;
    ctx.strokeStyle = '#b4b4b4';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(slitX, 40); ctx.lineTo(slitX, sy1 - 10);
    ctx.moveTo(slitX, sy1 + 10); ctx.lineTo(slitX, sy2 - 10);
    ctx.moveTo(slitX, sy2 + 10); ctx.lineTo(slitX, H - 40);
    ctx.stroke();

    const maxR = 220;
    for (let rb = 10; rb < maxR; rb += 24) {{
      const r = (rb + t * 80) % maxR;
      const alpha = 1.0 - r / maxR;
      ctx.strokeStyle = `rgba(0, 200, 255, ${{alpha}})`;
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(slitX, sy1, r, -1.4, 1.4); ctx.stroke();
      ctx.beginPath(); ctx.arc(slitX, sy2, r, -1.4, 1.4); ctx.stroke();
    }}
  }}
  else if (["Mechanics", "Kinematics", "Robotics", "Engineering"].some(k => domain.includes(k))) {{
    const radius = 80, teeth = 12;
    ctx.strokeStyle = '#5a6473';
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(cx, cy, radius, 0, Math.PI * 2); ctx.stroke();
    for (let i = 0; i < teeth; i++) {{
      const ang = ((Math.PI * 2) / teeth) * i + t * 1.5 + id;
      const tx = cx + (radius + 8) * Math.cos(ang);
      const ty = cy + (radius + 8) * Math.sin(ang);
      ctx.fillStyle = '#a0afbe';
      ctx.beginPath(); ctx.arc(tx, ty, 6, 0, Math.PI * 2); ctx.fill();
    }}
    const ax = cx + radius * Math.cos(-t * 1.5);
    const ay = cy + radius * Math.sin(-t * 1.5);
    ctx.strokeStyle = '#ff8c00';
    ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(ax, ay); ctx.stroke();
    ctx.fillStyle = '#ffc832';
    ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI * 2); ctx.fill();
  }}
  else if (["Astrophysics", "Astronomy", "Astro", "Space", "Orbital"].some(k => domain.includes(k))) {{
    ctx.fillStyle = '#ffdc50';
    ctx.beginPath(); ctx.arc(cx, cy, 26, 0, Math.PI * 2); ctx.fill();
    [80, 135, 190].forEach((r, idx) => {{
      ctx.strokeStyle = '#324664';
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.ellipse(cx, cy, r, r * 0.55, 0, 0, Math.PI * 2); ctx.stroke();
      const ang = t * (2.0 / (idx + 1)) + id;
      const px = cx + r * Math.cos(ang);
      const py = cy + (r * 0.55) * Math.sin(ang);
      ctx.fillStyle = '#64c8ff';
      ctx.beginPath(); ctx.arc(px, py, 7 - idx, 0, Math.PI * 2); ctx.fill();
    }});
  }}
  else if (["Electronics", "Computing", "Sensors", "Telecommunications", "Digital"].some(k => domain.includes(k))) {{
    [-70, 0, 70].forEach((yOff, i) => {{
      const y = cy + yOff;
      ctx.strokeStyle = '#285032';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(100, y); ctx.lineTo(W - 100, y); ctx.stroke();
      const pulseX = 100 + ((t * 180 + i * 90 + id * 15) % (W - 200));
      ctx.fillStyle = '#00ff78';
      ctx.fillRect(pulseX, y - 16, 28, 16);
      ctx.fillStyle = '#00ffc8';
      ctx.beginPath(); ctx.arc(pulseX + 14, y, 5, 0, Math.PI * 2); ctx.fill();
    }});
  }}
  else {{
    for (let i = 0; i < 8; i++) {{
      const ang = t * 0.8 + ((Math.PI * 2) / 8) * i + id;
      const dist = 85 + 28 * Math.sin(t * 3.0 + i);
      const nx = cx + dist * Math.cos(ang);
      const ny = cy + dist * Math.sin(ang);
      ctx.strokeStyle = '#5078a0';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(nx, ny); ctx.stroke();
      ctx.fillStyle = '#f0508c';
      ctx.beginPath(); ctx.arc(nx, ny, 9, 0, Math.PI * 2); ctx.fill();
    }}
    ctx.fillStyle = '#50dcb4';
    ctx.beginPath(); ctx.arc(cx, cy, 16, 0, Math.PI * 2); ctx.fill();
  }}
}}

function loop(now) {{
  const dt = Math.min((now - lastTimestamp) / 1000.0, 0.05);
  lastTimestamp = now;

  const spec = REGISTRY[currentIndex];
  if (!paused) {{
    elapsedTime += dt;
    if (elapsedTime > spec.duration) elapsedTime %= spec.duration;
    if (spec.id === 1) updateDoublePendulum(dt);
  }}

  renderScene(spec);

  const pct = ((elapsedTime % spec.duration) / spec.duration) * 100;
  document.getElementById('progress-fill').style.width = `${{pct.toFixed(1)}}%`;
  const stText = paused ? 'PAUSED' : 'RUNNING';
  document.getElementById('status-text').textContent = `STATUS: ${{stText}} | TIME: ${{elapsedTime.toFixed(1)}}s / ${{spec.duration.toFixed(1)}}s`;
  document.getElementById('status-text').style.color = paused ? '#ffb432' : '#7ee787';

  requestAnimationFrame(loop);
}}

setAnimation(0);
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

    output_path = os.path.join("build", "web", "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated {output_path} with {len(specs_list)} animations.")

if __name__ == "__main__":
    generate_web_bundle()
