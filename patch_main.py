"""
patch_main.py - run next to main.py:  python patch_main.py
Backs up main.py to main.py.bak, applies fixes, then run: python main.py
"""
import re, shutil, sys

SRC = "main.py"
src = open(SRC, encoding="utf-8").read()
if "EXTRA_JS" in src:
    sys.exit("main.py is already patched.")
shutil.copy(SRC, SRC + ".bak")

# JS overrides. Plain string (not an f-string), so braces are written normally.
EXTRA_JS = r'''
const EXTRA = {};
const S = {};
const TAU = Math.PI * 2;
function circ(x, y, r, c) { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); }
function seg(x1, y1, x2, y2, c, w) { ctx.strokeStyle = c; ctx.lineWidth = w || 2; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); }
function flick(t, k) { return 0.5 + 0.5 * Math.sin(t * 47 + k) * Math.sin(t * 31 + k * 2.3); } // deterministic "random" (freezes on pause)
function resetSims() {
  S.dp = { th1: Math.PI / 2, th2: Math.PI / 2 + 0.01, w1: 0, w2: 0, trail: [] };
  S.gas = Array.from({ length: 45 }, () => { const a = Math.random() * TAU, v = 60 + Math.random() * 120;
    return { x: W / 2 - 130 + Math.random() * 260, y: H / 2 - 60 + Math.random() * 120, vx: Math.cos(a) * v, vy: Math.sin(a) * v }; });
  S.br = { x: W / 2, y: H / 2, trail: [] };
}
resetSims();

// 1. Double pendulum: standard equations (m=1, L=1), RK4, g=9.81, dt-based
function dpAcc(a, b, w1, w2) {
  const g = 9.81, d = a - b, den = 3 - Math.cos(2 * d);
  return [(-3 * g * Math.sin(a) - g * Math.sin(a - 2 * b) - 2 * Math.sin(d) * (w2 * w2 + w1 * w1 * Math.cos(d))) / den,
          (2 * Math.sin(d) * (2 * w1 * w1 + 2 * g * Math.cos(a) + w2 * w2 * Math.cos(d))) / den];
}
EXTRA[1] = (cx, cy, t, dt) => {
  const p = S.dp; let rem = dt;
  while (rem > 1e-6) {
    const h = Math.min(rem, 0.004); rem -= h;
    const f = (s) => { const ac = dpAcc(s[0], s[1], s[2], s[3]); return [s[2], s[3], ac[0], ac[1]]; };
    const s0 = [p.th1, p.th2, p.w1, p.w2], add = (s, k, m) => s.map((v, i) => v + k[i] * m);
    const k1 = f(s0), k2 = f(add(s0, k1, h / 2)), k3 = f(add(s0, k2, h / 2)), k4 = f(add(s0, k3, h));
    const n = s0.map((v, i) => v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
    [p.th1, p.th2, p.w1, p.w2] = n;
  }
  const ox = cx, oy = cy - 70, L = 100;
  const x1 = ox + L * Math.sin(p.th1), y1 = oy + L * Math.cos(p.th1), x2 = x1 + L * Math.sin(p.th2), y2 = y1 + L * Math.cos(p.th2);
  if (dt > 0) { p.trail.push([x2, y2]); if (p.trail.length > 220) p.trail.shift(); }
  p.trail.forEach((pt, i) => { if (i) { ctx.strokeStyle = `rgba(0,220,160,${i / p.trail.length})`; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(p.trail[i - 1][0], p.trail[i - 1][1]); ctx.lineTo(pt[0], pt[1]); ctx.stroke(); } });
  seg(ox, oy, x1, y1, '#e6edf3', 3); seg(x1, y1, x2, y2, '#e6edf3', 3);
  circ(ox, oy, 4, '#8b949e'); circ(x1, y1, 10, '#ff6464'); circ(x2, y2, 10, '#64ff64');
};

// 12. Two-stage rocket with separation at t=7s
EXTRA[12] = (cx, cy, t) => {
  const alt = 0.5 * 9 * t * t * (t < 7 ? 1 : 1), ry = Math.max(40, cy + 90 - alt * 0.9);
  for (let i = 0; i < 6; i++) circ(80 + (i * 143) % 700, (i * 97 + t * 40) % H, 1.5, '#4a5560');
  ctx.fillStyle = '#21262d'; ctx.fillRect(0, H - 30, W, 30);
  const sep = t > 7, by = sep ? ry + 40 + (t - 7) * (t - 7) * 14 : ry + 40;
  ctx.fillStyle = '#e6edf3'; ctx.fillRect(cx - 12, ry, 24, 40);                       // upper stage
  ctx.fillStyle = '#f85149'; ctx.beginPath(); ctx.moveTo(cx - 12, ry); ctx.lineTo(cx, ry - 22); ctx.lineTo(cx + 12, ry); ctx.fill();
  ctx.fillStyle = '#8b949e'; ctx.fillRect(cx - 14, by + (sep ? 8 : 0), 28, 50);       // booster
  const fl = flick(t, 1), fy = sep ? ry + 40 : by + 58 + (sep ? 8 : 0);
  ctx.fillStyle = `rgba(240,136,62,${0.6 + 0.4 * fl})`; ctx.beginPath(); ctx.moveTo(cx - 9, fy); ctx.lineTo(cx + 9, fy); ctx.lineTo(cx, fy + 35 + 25 * fl); ctx.fill();
  ctx.fillStyle = '#e3b341'; ctx.font = '13px monospace'; ctx.fillText(sep ? 'STAGE 2 BURN' : 'STAGE 1 BURN', 20, 28);
};

// 16. Lunar lander: suicide-burn style deceleration, soft touchdown
EXTRA[16] = (cx, cy, t) => {
  const gy = cy + 90, T = 9, u = Math.min(t / T, 1), y = (cy - 130) + 200 * (1 - Math.pow(1 - u, 2));
  seg(cx - 220, gy, cx + 220, gy, '#8b949e', 4);
  for (let i = 0; i < 10; i++) seg(cx - 200 + i * 44, gy, cx - 190 + i * 44, gy + 8, '#30363d', 3);
  ctx.fillStyle = '#d29922'; ctx.fillRect(cx - 24, y, 48, 30);
  seg(cx - 24, y + 30, cx - 38, y + 46, '#e6edf3', 3); seg(cx + 24, y + 30, cx + 38, y + 46, '#e6edf3', 3);
  if (u < 1) { const fl = flick(t, 3), len = 20 + 30 * (1 - u) * (0.7 + 0.3 * fl);
    ctx.fillStyle = 'rgba(88,166,255,0.8)'; ctx.beginPath(); ctx.moveTo(cx - 10, y + 30); ctx.lineTo(cx + 10, y + 30); ctx.lineTo(cx, y + 30 + len); ctx.fill(); }
  ctx.fillStyle = '#7ee787'; ctx.font = '13px monospace';
  ctx.fillText('ALT ' + Math.max(0, (gy - 46 - y) / 2).toFixed(0) + ' m   V ' + (u < 1 ? (20 * (1 - u)).toFixed(1) : '0.0') + ' m/s', 20, 28);
};

// 25. Ideal gas: dt-based, particle-particle collisions, speed-coloured
EXTRA[25] = (cx, cy, t, dt) => {
  const x0 = cx - 140, x1 = cx + 140, y0 = cy - 80, y1 = cy + 80, r = 5, g = S.gas;
  ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 3; ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);
  if (dt > 0) {
    g.forEach(p => { p.x += p.vx * dt; p.y += p.vy * dt;
      if (p.x < x0 + r) { p.x = x0 + r; p.vx = Math.abs(p.vx); } if (p.x > x1 - r) { p.x = x1 - r; p.vx = -Math.abs(p.vx); }
      if (p.y < y0 + r) { p.y = y0 + r; p.vy = Math.abs(p.vy); } if (p.y > y1 - r) { p.y = y1 - r; p.vy = -Math.abs(p.vy); } });
    for (let i = 0; i < g.length; i++) for (let j = i + 1; j < g.length; j++) {
      const a = g[i], b = g[j], dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy;
      if (d2 < 4 * r * r && d2 > 0) { const d = Math.sqrt(d2), nx = dx / d, ny = dy / d, dv = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny;
        if (dv > 0) { a.vx -= dv * nx; a.vy -= dv * ny; b.vx += dv * nx; b.vy += dv * ny; } } }
  }
  g.forEach(p => { const s = Math.min(1, Math.hypot(p.vx, p.vy) / 220); circ(p.x, p.y, r, `rgb(${Math.round(60 + 195 * s)},${Math.round(140 - 60 * s)},${Math.round(255 - 200 * s)})`); });
};

// 47. Seismograph drum: P wave at 1.5s, S wave at 3.5s, decaying coda
EXTRA[47] = (cx, cy, t) => {
  ctx.fillStyle = '#161b22'; ctx.fillRect(cx - 200, cy - 80, 400, 160); ctx.strokeStyle = '#30363d'; ctx.strokeRect(cx - 200, cy - 80, 400, 160);
  const amp = (tt) => tt < 1.5 ? 1 : tt < 3.5 ? 10 * Math.exp(-(tt - 1.5) * 0.3) : 38 * Math.exp(-(tt - 3.5) * 0.45);
  ctx.strokeStyle = '#f85149'; ctx.lineWidth = 1.5; ctx.beginPath();
  for (let x = -190; x <= 190; x += 2) { const tt = t - (190 - x) / 55; if (tt < 0) { x === -190 ? ctx.moveTo(cx + x, cy) : ctx.lineTo(cx + x, cy); continue; }
    const f = tt < 3.5 ? 22 : 11, y = cy + amp(tt) * Math.sin(tt * f) * (0.8 + 0.2 * Math.sin(tt * 53));
    x === -190 ? ctx.moveTo(cx + x, y) : ctx.lineTo(cx + x, y); }
  ctx.stroke(); circ(cx + 190, cy + amp(t) * Math.sin(t * (t < 3.5 ? 22 : 11)), 4, '#e3b341');
  ctx.fillStyle = '#8b949e'; ctx.font = '12px monospace'; ctx.fillText(t > 3.5 ? 'S-WAVE' : t > 1.5 ? 'P-WAVE' : 'QUIET', cx - 190, cy - 88);
};

// 59. Brownian motion: dt-scaled random walk, bombarded by small molecules
EXTRA[59] = (cx, cy, t, dt) => {
  const b = S.br, hw = 250, hh = 150;
  if (dt > 0) { const k = Math.sqrt(dt) * 90; b.x = Math.min(cx + hw, Math.max(cx - hw, b.x + (Math.random() - 0.5) * 2 * k)); b.y = Math.min(cy + hh, Math.max(cy - hh, b.y + (Math.random() - 0.5) * 2 * k));
    b.trail.push([b.x, b.y]); if (b.trail.length > 400) b.trail.shift(); }
  for (let i = 0; i < 40; i++) circ(cx + Math.sin(t * (3 + i % 5) + i * 7.1) * hw, cy + Math.cos(t * (2.5 + i % 4) + i * 3.3) * hh, 2, 'rgba(88,166,255,0.5)');
  ctx.beginPath(); b.trail.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.strokeStyle = 'rgba(139,148,158,0.7)'; ctx.lineWidth = 1.5; ctx.stroke();
  circ(b.x, b.y, 9, '#f85149');
};

// 63. Ion thruster: ions accelerate through grids (spacing grows with speed)
EXTRA[63] = (cx, cy, t) => {
  ctx.fillStyle = '#30363d'; ctx.fillRect(cx - 120, cy - 40, 100, 80); seg(cx - 20, cy - 40, cx - 20, cy + 40, '#e3b341', 4); seg(cx, cy - 40, cx, cy + 40, '#e3b341', 4);
  for (let i = 0; i < 14; i++) { const u = ((t * 0.5 + i / 14) % 1), x = cx - 70 + 300 * u * u + 40 * u, y = cy - 30 + ((i * 37) % 60);
    circ(x, y, 3, `rgba(88,166,255,${1 - u * 0.6})`); if (x > cx) seg(x, y, x - 10 - 20 * u, y, `rgba(88,166,255,${0.5 - u * 0.4})`, 2); }
  ctx.fillStyle = '#7ee787'; ctx.font = '12px monospace'; ctx.fillText('Xe+ ions  ->  ~30 km/s', cx - 120, cy + 62);
};

// 65. Solar flare: magnetic loops stretch, reconnect, plasma erupts
EXTRA[65] = (cx, cy, t) => {
  const gy = cy + 90, ph = t % 6; ctx.fillStyle = '#e3b341'; ctx.fillRect(0, gy, W, H - gy);
  for (let k = 0; k < 3; k++) { const lift = Math.min(1, ph / 3) * 40 * (k + 1) * (ph > 3.4 ? 0 : 1), hgt = 60 + k * 25 + lift * 0.6, wd = 70 + k * 30;
    ctx.strokeStyle = `rgba(240,136,62,${0.9 - k * 0.2})`; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(cx - wd, gy); ctx.bezierCurveTo(cx - wd, gy - hgt * 1.4, cx + wd, gy - hgt * 1.4, cx + wd, gy); ctx.stroke(); }
  if (ph > 3.2 && ph < 3.5) { circ(cx, gy - 70, 10 + 40 * (ph - 3.2), 'rgba(255,255,255,0.7)'); }
  if (ph >= 3.4) { const e = ph - 3.4; for (let i = 0; i < 24; i++) { const a = -Math.PI / 2 + (i - 12) * 0.05, r = e * (90 + (i % 5) * 25);
    circ(cx + Math.cos(a) * r, gy - 70 + Math.sin(a) * r, 3 + (i % 3), `rgba(255,${120 + i * 4},60,${Math.max(0, 1 - e / 2.6)})`); } }
};

// 81. Meissner effect: magnet hovers above superconductor, field lines pushed aside
EXTRA[81] = (cx, cy, t) => {
  const hover = Math.sin(t * 2.5) * 5, my = cy - 40 + hover;
  ctx.fillStyle = '#8957e5'; ctx.fillRect(cx - 110, cy + 20, 220, 30);
  for (let i = -3; i <= 3; i++) { ctx.strokeStyle = 'rgba(88,166,255,0.6)'; ctx.lineWidth = 1.5; ctx.beginPath();
    const s = i * 22; ctx.moveTo(cx + s * 0.5, my + 15); ctx.bezierCurveTo(cx + s * 2.2, my + 30, cx + s * 2.4, cy + 5, cx + s * 2.6 + (i < 0 ? -20 : 20), cy + 20); ctx.stroke(); }
  ctx.fillStyle = '#f85149'; ctx.fillRect(cx - 35, my - 14, 35, 28); ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx, my - 14, 35, 28);
  ctx.fillStyle = 'rgba(0,220,255,' + (0.1 + 0.08 * flick(t, 9)) + ')'; ctx.fillRect(cx - 110, cy + 50, 220, 14);
};

// 86. Enzyme catalysis: substrate binds, induced fit, split into products, release
EXTRA[86] = (cx, cy, t) => {
  const ph = (t % 6) / 6, close = ph > 0.3 && ph < 0.65 ? 1 : (ph >= 0.65 ? 1 : 0), gap = ph < 0.3 ? 14 : ph < 0.65 ? 0 : 0;
  ctx.fillStyle = '#d29922'; ctx.beginPath(); ctx.arc(cx, cy + 40, 85, Math.PI, 0); ctx.lineTo(cx + 85, cy + 90); ctx.lineTo(cx - 85, cy + 90); ctx.fill();
  const jaw = ph < 0.3 ? 28 : ph < 0.65 ? 16 : 28 + 10 * Math.min(1, (ph - 0.65) * 6);
  ctx.fillStyle = '#12161c'; ctx.beginPath(); ctx.arc(cx, cy - 30, jaw, 0, TAU); ctx.fill();
  let sx, sy;
  if (ph < 0.3) { const u = ph / 0.3; sx = cx + 170 * (1 - u); sy = cy - 120 + 90 * u; } else sx = cx, sy = cy - 30;
  if (ph < 0.65) { circ(sx - 8, sy, 10, '#3fb950'); circ(sx + 8, sy, 10, '#58a6ff'); }
  else { const u = Math.min(1, (ph - 0.65) / 0.35); circ(sx - 8 - 70 * u, sy - 80 * u, 10, '#3fb950'); circ(sx + 8 + 70 * u, sy - 80 * u, 10, '#58a6ff'); }
  ctx.fillStyle = '#8b949e'; ctx.font = '13px monospace'; ctx.fillText(ph < 0.3 ? 'APPROACH' : ph < 0.65 ? 'INDUCED FIT -> LOWER Ea' : 'PRODUCTS RELEASED', 20, 28);
};

// 93. Subduction: oceanic plate dives, melt rises to volcano
EXTRA[93] = (cx, cy, t) => {
  ctx.fillStyle = '#6e4b3a'; ctx.fillRect(0, cy - 10, W, H); ctx.fillStyle = '#1f6feb'; ctx.fillRect(0, cy - 40, cx - 80, 30);
  ctx.fillStyle = '#4a5560'; ctx.beginPath(); ctx.moveTo(0, cy - 10); ctx.lineTo(cx - 80, cy - 10); ctx.lineTo(cx + 200, cy + 150); ctx.lineTo(cx + 200, cy + 190); ctx.lineTo(cx - 80, cy + 30); ctx.lineTo(0, cy + 30); ctx.fill();
  ctx.fillStyle = '#8b3a2f'; ctx.beginPath(); ctx.ellipse(cx + 120, cy + 70, 55, 28, 0, 0, TAU); ctx.fill();
  for (let i = 0; i < 8; i++) { const u = (t * 0.25 + i / 8) % 1; circ(cx + 120 + Math.sin(u * 9 + i) * 8, cy + 60 - u * 110, 4, '#ff7b32'); }
  ctx.fillStyle = '#795548'; ctx.beginPath(); ctx.moveTo(cx + 70, cy - 10); ctx.lineTo(cx + 120, cy - 80); ctx.lineTo(cx + 170, cy - 10); ctx.fill();
  const e = (t % 5) / 5; if (e > 0.6) for (let i = 0; i < 10; i++) circ(cx + 120 + (i - 5) * 8 * (e - 0.5) * 4, cy - 85 - (e - 0.6) * 130 * (0.5 + (i % 4) / 4), 4, `rgba(80,80,80,${1 - e})`);
  seg(40, cy + 10, 150, cy + 55, '#e6edf3', 2); ctx.fillStyle = '#e6edf3'; ctx.font = '12px monospace'; ctx.fillText('SLAB MOTION', 30, cy + 8);
};

// 94. PEM fuel cell: H2 -> H+ through membrane; electrons through external load; water at cathode
EXTRA[94] = (cx, cy, t) => {
  ctx.fillStyle = '#30363d'; ctx.fillRect(cx - 130, cy - 70, 90, 140); ctx.fillRect(cx + 40, cy - 70, 90, 140);
  ctx.fillStyle = '#bc8cff'; ctx.fillRect(cx - 40, cy - 70, 80, 140);
  ctx.fillStyle = '#8b949e'; ctx.font = '12px monospace'; ctx.fillText('H2 in', cx - 128, cy - 78); ctx.fillText('O2 in', cx + 70, cy - 78); ctx.fillText('PEM', cx - 12, cy - 78);
  for (let i = 0; i < 5; i++) { const u = (t * 0.4 + i / 5) % 1;
    circ(cx - 120 + 70 * u, cy - 50 + i * 24, 5, u < 0.8 ? '#fff' : 'rgba(255,255,255,0)');
    circ(cx - 30 + 60 * u, cy - 44 + i * 24 + Math.sin(u * 8) * 3, 4, '#f85149');   // H+
    const w = (t * 0.4 + i / 5 + 0.3) % 1; circ(cx + 50 + 70 * w, cy - 50 + i * 24, 5, `rgba(88,166,255,${w})`); }
  ctx.strokeStyle = '#e3b341'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx - 85, cy - 70); ctx.lineTo(cx - 85, cy - 110); ctx.lineTo(cx + 85, cy - 110); ctx.lineTo(cx + 85, cy - 70); ctx.stroke();
  for (let i = 0; i < 4; i++) circ(cx - 85 + 170 * (((t * 0.5 + i / 4) % 1)), cy - 110, 4, '#58a6ff');
  ctx.fillStyle = '#e3b341'; ctx.fillRect(cx - 14, cy - 122, 28, 24); ctx.fillStyle = '#12161c'; ctx.fillText('LOAD', cx - 14, cy - 106);
};

// 97. Tidal barrage: sinusoidal tide, head difference drives turbine, flow reverses
EXTRA[97] = (cx, cy, t) => {
  const sea = Math.sin(t * 0.8) * 30, basin = Math.sin(t * 0.8 - 0.9) * 22;
  ctx.fillStyle = '#6e4b3a'; ctx.fillRect(cx - 12, cy - 70, 24, 200);
  ctx.fillStyle = '#1f6feb'; ctx.fillRect(cx + 12, cy - basin, 230, 140); ctx.fillStyle = '#0969da'; ctx.fillRect(cx - 242, cy - sea, 230, 140);
  const flow = (sea - basin), dir = Math.sign(flow);
  ctx.save(); ctx.translate(cx, cy + 60); ctx.rotate(t * flow * 0.4); seg(-16, 0, 16, 0, '#e3b341', 4); seg(0, -16, 0, 16, '#e3b341', 4); ctx.restore();
  for (let i = 0; i < 4; i++) { const u = (t * 0.6 + i / 4) % 1; if (Math.abs(flow) > 3) circ(cx - dir * 40 + dir * 80 * u - 0, cy + 60 + Math.sin(u * 6) * 6, 3, '#e6edf3'); }
  ctx.fillStyle = '#e6edf3'; ctx.font = '13px monospace'; ctx.fillText(Math.abs(flow) < 3 ? 'SLACK TIDE' : (flow > 0 ? 'EBB/FILL ->' : '<- GENERATING'), 20, 28);
};

// 100. Direct air capture: air passes sorbent; CO2 gets trapped, others pass
EXTRA[100] = (cx, cy, t) => {
  ctx.fillStyle = '#21262d'; ctx.fillRect(cx - 40, cy - 90, 80, 180);
  for (let r = 0; r < 9; r++) for (let c = 0; c < 3; c++) circ(cx - 22 + c * 22, cy - 76 + r * 19, 5, '#30363d');
  const cap = Math.min(1, (t % 12) / 6);
  for (let i = 0; i < 28; i++) { const u = (t * 0.22 + i / 28) % 1, x = cx - 260 + 520 * u, y = cy - 80 + ((i * 53) % 160), co2 = i % 3 === 0;
    if (co2 && x > cx - 30 && x < cx + 30 && (i % 6 === 0 || cap > i / 28)) circ(cx - 22 + (i % 3) * 22, cy - 76 + (i % 9) * 19, 6, '#f85149');
    else if (co2 && x > cx + 40 && (i % 6 === 0)) continue;
    else circ(x, y, co2 ? 5 : 3, co2 ? '#f85149' : 'rgba(88,166,255,0.6)'); }
  ctx.fillStyle = '#7ee787'; ctx.font = '13px monospace'; ctx.fillText('CO2 CAPTURED: ' + Math.round(cap * 100) + '%', 20, 28);
};
'''

def rep(old, new):
    global src
    assert src.count(old) == 1, "Could not find (or found duplicates of):\n" + old
    src = src.replace(old, new)

# 1) Inject JS overrides into the generated HTML (placeholder is filled by the f-string)
rep("def build_web_app():", "EXTRA_JS = r'''" + EXTRA_JS.replace("'''", "") + "'''\n\ndef build_web_app():")
rep("function render(aid, cx, cy, t) {{\n  ctx.fillStyle = '#10141a'; ctx.fillRect(0, 0, W, H);\n",
    "{EXTRA_JS}\nfunction render(aid, cx, cy, t, dt) {{\n  ctx.fillStyle = '#10141a'; ctx.fillRect(0, 0, W, H);\n  if (EXTRA[aid]) {{ EXTRA[aid](cx, cy, t, dt); return; }}\n")

# 2) Pass dt (0 while paused) so simulation state only advances when running
rep("render(s.id, W/2, H/2 - 10, elapsed);", "render(s.id, W/2, H/2 - 10, elapsed, paused ? 0 : dt);")

# 3) Full reset (pendulum, gas, Brownian) on any animation change / reset
rep("bx = W/2; by = H/2; btrail = [];\n  const s = REGISTRY[idx];", "resetSims();\n  const s = REGISTRY[idx];")

# 4) GitHub Pages: also publish to docs/index.html (Settings > Pages > main branch /docs)
rep('    print(f"Successfully compiled {out_file} with 100 individual simulations.")',
    '    import shutil\n    os.makedirs("docs", exist_ok=True)\n    shutil.copyfile(out_file, os.path.join("docs", "index.html"))\n    print(f"Successfully compiled {out_file} (+ docs/index.html) with 100 individual simulations.")')

# 5) Remove the old branches that the new code replaces, so main.py has no dead code
dead = {int(n) for n in re.findall(r"^EXTRA\[(\d+)\]", EXTRA_JS, re.M)}
a = src.index("function render(aid, cx, cy, t, dt) {{")
b = src.index("function loop(now) {{")
body = src[a:b]
close = body.rstrip().rfind("}}")
fn_close, body = body[close:], body[:close]
parts = re.split(r"(?m)^(?=  (?:else )?if \(aid === \d+\) \{\{)", body)
kept = [parts[0]]
for p in parts[1:]:
    if int(re.match(r"\s*(?:else )?if \(aid === (\d+)\)", p).group(1)) not in dead:
        kept.append(p)
src = src[:a] + "".join(kept) + fn_close + "\n\n" + src[b:]

open(SRC, "w", encoding="utf-8").write(src)
print("Patched main.py (backup: main.py.bak). Now run: python main.py")
