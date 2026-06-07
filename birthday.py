"""
🎂 Happy Birthday Surprise App
================================
Run this file to launch the birthday surprise!

Requirements: Python 3.6+  (no extra installs needed)
Usage:        python birthday.py
"""

import os
import sys
import webbrowser
import tempfile
import http.server
import threading
import time

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>🎂 Happy Birthday! 🎂</title>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@400;600;700&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --pink:   #ff6eb4;
    --purple: #a855f7;
    --gold:   #fbbf24;
    --cyan:   #22d3ee;
    --bg:     #0d0020;
    --card:   rgba(255,255,255,0.05);
  }

  body {
    background: var(--bg);
    font-family: 'Quicksand', sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    cursor: default;
  }

  /* ── Stars ── */
  #stars-canvas {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
  }

  /* ── Confetti canvas ── */
  #confetti-canvas {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 100;
  }

  /* ── Envelope scene ── */
  #scene-envelope {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    animation: fadeIn 1s ease;
  }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

  .glow-text {
    font-family: 'Pacifico', cursive;
    font-size: clamp(1.2rem, 4vw, 1.8rem);
    color: #ffcff7;
    text-shadow: 0 0 30px #ff6eb4, 0 0 60px #a855f780;
    text-align: center;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%,100% { opacity: .8; transform: scale(1); }
    50%      { opacity: 1;  transform: scale(1.05); }
  }

  .envelope-wrap {
    cursor: pointer;
    animation: floatY 3s ease-in-out infinite;
    filter: drop-shadow(0 0 24px #ff6eb488);
    transition: transform .15s;
  }
  .envelope-wrap:hover  { transform: scale(1.08); }
  .envelope-wrap:active { transform: scale(.95); }

  @keyframes floatY {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-14px); }
  }

  /* ── Card scene ── */
  #scene-card {
    display: none;
    position: relative;
    z-index: 10;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 1rem;
    max-width: 480px;
    width: 100%;
  }

  .card {
    background: var(--card);
    border: 1.5px solid rgba(255,110,180,.35);
    border-radius: 28px;
    padding: 2.5rem 2rem 2rem;
    width: 100%;
    text-align: center;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 80px rgba(168,85,247,.25), 0 0 40px rgba(255,110,180,.15);
    animation: cardReveal .7s cubic-bezier(.34,1.56,.64,1) both;
  }

  @keyframes cardReveal {
    from { opacity: 0; transform: scale(.6) rotate(-4deg); }
    to   { opacity: 1; transform: scale(1) rotate(0deg); }
  }

  /* rainbow border animation */
  .card::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 30px;
    background: conic-gradient(from 0deg, #ff6eb4, #a855f7, #22d3ee, #fbbf24, #ff6eb4);
    z-index: -1;
    animation: spin 4s linear infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* cupcake */
  .cupcake-wrap {
    margin: 0 auto 1.2rem;
    width: 130px;
    animation: cupcakeWiggle 2.5s ease-in-out infinite;
    filter: drop-shadow(0 6px 18px rgba(255,110,180,.5));
  }

  @keyframes cupcakeWiggle {
    0%,100% { transform: rotate(-3deg); }
    50%      { transform: rotate(3deg); }
  }

  .flame { animation: flicker .25s ease-in-out infinite alternate; transform-origin: 50% 100%; }
  @keyframes flicker {
    from { transform: scaleX(1) scaleY(1); }
    to   { transform: scaleX(.75) scaleY(1.2) rotate(5deg); }
  }

  /* texts */
  .title {
    font-family: 'Pacifico', cursive;
    font-size: clamp(1.8rem, 6vw, 2.4rem);
    background: linear-gradient(90deg, #ff6eb4, #fbbf24, #ff6eb4);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 2s linear infinite;
    line-height: 1.2;
    margin-bottom: .4rem;
  }

  @keyframes shimmer { to { background-position: -200% 0; } }

  .subtitle { font-size: 1rem; color: #d9b3ff; margin-bottom: 1.2rem; }

  .badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff6eb4, #a855f7);
    color: #fff;
    font-family: 'Pacifico', cursive;
    font-size: 1rem;
    padding: .45rem 1.6rem;
    border-radius: 50px;
    margin-bottom: 1.1rem;
    box-shadow: 0 0 24px #ff6eb466;
    animation: badgePop 1.5s ease-in-out infinite;
  }

  @keyframes badgePop {
    0%,100% { box-shadow: 0 0 24px #ff6eb466; }
    50%      { box-shadow: 0 0 48px #a855f7bb; }
  }

  .heart-line {
    font-family: 'Pacifico', cursive;
    font-size: 1.25rem;
    color: #ffcff7;
    text-shadow: 0 0 12px #ff6eb4;
    margin-bottom: .5rem;
  }

  .love-msg {
    font-size: .95rem;
    color: #c084fc;
    line-height: 1.7;
    margin-bottom: 1.2rem;
  }

  .emoji-row {
    font-size: 1.5rem;
    letter-spacing: .3rem;
    margin-bottom: .5rem;
    animation: emojiDance 1.2s ease-in-out infinite alternate;
  }

  @keyframes emojiDance {
    from { letter-spacing: .2rem; }
    to   { letter-spacing: .6rem; }
  }

  /* floating hearts */
  .fheart {
    position: fixed;
    bottom: -40px;
    font-size: 1.3rem;
    pointer-events: none;
    animation: riseHeart var(--d) ease-in var(--delay) infinite;
    opacity: 0;
    z-index: 50;
  }

  @keyframes riseHeart {
    0%   { transform: translateY(0) scale(.8); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: .5; }
    100% { transform: translateY(-110vh) scale(1.3); opacity: 0; }
  }

  .replay-btn {
    margin-top: 1rem;
    background: transparent;
    border: 1.5px solid rgba(255,110,180,.4);
    border-radius: 50px;
    color: #ff6eb4;
    font-family: 'Quicksand', sans-serif;
    font-weight: 600;
    font-size: .9rem;
    padding: .4rem 1.4rem;
    cursor: pointer;
    transition: background .2s, border-color .2s;
  }
  .replay-btn:hover { background: rgba(255,110,180,.15); border-color: #ff6eb4; }
</style>
</head>
<body>

<canvas id="stars-canvas"></canvas>
<canvas id="confetti-canvas"></canvas>

<!-- ══ Envelope Scene ══ -->
<div id="scene-envelope">
  <p class="glow-text">✨ Click the envelope to open your surprise! ✨</p>

  <div class="envelope-wrap" onclick="openSurprise()" role="button" aria-label="Open birthday surprise">
    <svg width="200" height="155" viewBox="0 0 200 155" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="envglow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="6" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <rect x="8" y="35" width="184" height="112" rx="14"
            fill="#2a0045" stroke="#ff6eb4" stroke-width="2.5" filter="url(#envglow)"/>
      <!-- flap -->
      <polygon points="8,35 100,98 192,35"
               fill="#3d005f" stroke="#ff6eb4" stroke-width="1.5"/>
      <!-- bottom folds -->
      <polyline points="8,147 72,88" fill="none" stroke="#ff6eb4" stroke-width="1.5"/>
      <polyline points="192,147 128,88" fill="none" stroke="#ff6eb4" stroke-width="1.5"/>
      <!-- heart seal -->
      <text x="100" y="82" text-anchor="middle" font-size="32"
            fill="#ff6eb4" style="filter:drop-shadow(0 0 8px #ff00cc)">💌</text>
      <text x="100" y="122" text-anchor="middle"
            font-family="Quicksand,sans-serif" font-weight="600" font-size="13"
            fill="#c084fc">for you 💜</text>
    </svg>
  </div>
</div>

<!-- ══ Card Scene ══ -->
<div id="scene-card">
  <div class="card">
    <!-- floating hearts container (injected by JS) -->
    <div id="hearts-container" style="position:fixed;inset:0;pointer-events:none;z-index:50;"></div>

    <!-- cupcake SVG -->
    <div class="cupcake-wrap">
      <svg viewBox="0 0 140 150" xmlns="http://www.w3.org/2000/svg">
        <!-- shadow -->
        <ellipse cx="70" cy="145" rx="35" ry="5" fill="rgba(0,0,0,.3)"/>
        <!-- cup -->
        <rect x="38" y="95" width="64" height="44" rx="12" fill="#b91c1c"/>
        <rect x="38" y="95" width="64" height="44" rx="12" fill="none" stroke="#ef4444" stroke-width="2"/>
        <!-- ridges -->
        <line x1="56" y1="95" x2="56" y2="139" stroke="#991b1b" stroke-width="2"/>
        <line x1="70" y1="95" x2="70" y2="139" stroke="#991b1b" stroke-width="2"/>
        <line x1="84" y1="95" x2="84" y2="139" stroke="#991b1b" stroke-width="2"/>
        <!-- frosting base -->
        <ellipse cx="70" cy="90" rx="34" ry="20" fill="#f9a8d4"/>
        <!-- frosting swirls -->
        <ellipse cx="50" cy="86" rx="16" ry="13" fill="#fce7f3"/>
        <ellipse cx="70" cy="78" rx="18" ry="15" fill="#fce7f3"/>
        <ellipse cx="90" cy="86" rx="16" ry="13" fill="#fce7f3"/>
        <!-- sprinkles -->
        <rect x="52" y="78" width="8" height="3" rx="1.5" fill="#a855f7" transform="rotate(-30,56,79)"/>
        <rect x="68" y="70" width="8" height="3" rx="1.5" fill="#22d3ee" transform="rotate(15,72,71)"/>
        <rect x="84" y="78" width="8" height="3" rx="1.5" fill="#fbbf24" transform="rotate(-20,88,79)"/>
        <rect x="60" y="85" width="7" height="3" rx="1.5" fill="#ff6eb4" transform="rotate(25,63,86)"/>
        <rect x="76" y="84" width="7" height="3" rx="1.5" fill="#4ade80" transform="rotate(-10,79,85)"/>
        <!-- dots on cup -->
        <circle cx="50" cy="112" r="3.5" fill="#fbbf24"/>
        <circle cx="70" cy="118" r="3"   fill="#22d3ee"/>
        <circle cx="90" cy="112" r="3.5" fill="#f9a8d4"/>
        <!-- candle -->
        <rect x="66" y="54" width="8" height="24" rx="4" fill="#fde68a"/>
        <rect x="66" y="54" width="8" height="24" rx="4" fill="none" stroke="#f59e0b" stroke-width="1"/>
        <!-- flame -->
        <ellipse cx="70" cy="50" rx="6" ry="10" fill="#fb923c" class="flame"/>
        <ellipse cx="70" cy="48" rx="4" ry="7"  fill="#fbbf24" class="flame"/>
        <ellipse cx="70" cy="47" rx="2" ry="4"  fill="#fff"    class="flame"/>
      </svg>
    </div>

    <div class="emoji-row">🎉🎂🎈🎊🎁</div>

    <h1 class="title">Happy Birthday!</h1>
    <p class="subtitle">wishing you the most magical day 🌙✨</p>

    <div class="badge">⭐ You're the BEST ⭐</div>

    <p class="heart-line">I love you choo much! 💜</p>
    <p class="love-msg">
      You make every single day sweeter,<br/>
      just like this little cupcake 🧁💕<br/>
      <em>Here's to YOU — forever &amp; always!</em>
    </p>

    <div class="emoji-row">💜🌸💛🌸💜</div>
    <button class="replay-btn" onclick="replay()">↺ Replay surprise</button>
  </div>
</div>

<script>
/* ── Stars ── */
(function() {
  const c = document.getElementById('stars-canvas');
  const ctx = c.getContext('2d');
  let stars = [];

  function resize() {
    c.width = window.innerWidth;
    c.height = window.innerHeight;
    stars = Array.from({length: 100}, () => ({
      x: Math.random() * c.width,
      y: Math.random() * c.height,
      r: Math.random() * 1.8 + .4,
      a: Math.random(),
      speed: Math.random() * .008 + .004
    }));
  }
  window.addEventListener('resize', resize);
  resize();

  function drawStars() {
    ctx.clearRect(0, 0, c.width, c.height);
    stars.forEach(s => {
      s.a += s.speed;
      const alpha = (.5 + .5 * Math.sin(s.a));
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${alpha})`;
      ctx.fill();
    });
    requestAnimationFrame(drawStars);
  }
  drawStars();
})();

/* ── Confetti ── */
const confCanvas = document.getElementById('confetti-canvas');
const confCtx = confCanvas.getContext('2d');
let particles = [];
let confAnim = false;

function resizeConf() { confCanvas.width = window.innerWidth; confCanvas.height = window.innerHeight; }
window.addEventListener('resize', resizeConf);
resizeConf();

function launchConfetti() {
  const colors = ['#ff6eb4','#a855f7','#fbbf24','#22d3ee','#4ade80','#fb923c'];
  for (let i = 0; i < 200; i++) {
    particles.push({
      x: Math.random() * confCanvas.width,
      y: -20,
      vx: (Math.random() - .5) * 7,
      vy: Math.random() * 5 + 2,
      color: colors[Math.floor(Math.random() * colors.length)],
      w: Math.random() * 10 + 4,
      h: Math.random() * 5 + 3,
      rot: Math.random() * 360,
      rs: (Math.random() - .5) * 10,
      life: 1
    });
  }
  if (!confAnim) animConf();
}

function animConf() {
  confAnim = true;
  confCtx.clearRect(0, 0, confCanvas.width, confCanvas.height);
  particles = particles.filter(p => p.life > 0);
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy; p.vy += .09; p.rot += p.rs;
    if (p.y > confCanvas.height + 30) p.life = 0;
    confCtx.save();
    confCtx.translate(p.x, p.y);
    confCtx.rotate(p.rot * Math.PI / 180);
    confCtx.fillStyle = p.color;
    confCtx.globalAlpha = Math.min(1, p.life);
    confCtx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
    confCtx.restore();
  });
  if (particles.length) requestAnimationFrame(animConf);
  else { confAnim = false; confCtx.clearRect(0, 0, confCanvas.width, confCanvas.height); }
}

/* ── Floating hearts ── */
let heartTimer = null;

function startHearts() {
  const emojis = ['💜','💕','🌸','💫','✨','💖','🎀'];
  const container = document.getElementById('hearts-container');
  heartTimer = setInterval(() => {
    const h = document.createElement('span');
    h.className = 'fheart';
    h.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    h.style.cssText = `
      left: ${Math.random() * 92}%;
      --d: ${(Math.random() * 2 + 3).toFixed(1)}s;
      --delay: ${(Math.random() * 1.5).toFixed(1)}s;
      font-size: ${(.9 + Math.random() * .8).toFixed(1)}rem;
    `;
    container.appendChild(h);
    setTimeout(() => h.remove(), 6500);
  }, 400);
}

function stopHearts() {
  clearInterval(heartTimer);
  document.getElementById('hearts-container').innerHTML = '';
}

/* ── Scene transitions ── */
function openSurprise() {
  document.getElementById('scene-envelope').style.display = 'none';
  const card = document.getElementById('scene-card');
  card.style.display = 'flex';
  launchConfetti();
  setTimeout(launchConfetti, 800);
  setTimeout(launchConfetti, 1600);
  startHearts();
}

function replay() {
  document.getElementById('scene-card').style.display = 'none';
  document.getElementById('scene-envelope').style.display = 'flex';
  stopHearts();
  particles = [];
  confCtx.clearRect(0, 0, confCanvas.width, confCanvas.height);
}
</script>
</body>
</html>"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))

    def log_message(self, *args):
        pass  # silence server logs


def find_free_port():
    import socket
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def main():
    port = find_free_port()
    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"

    print("=" * 50)
    print("  🎂  Happy Birthday Surprise App  🎂")
    print("=" * 50)
    print(f"  Server running at: {url}")
    print("  Opening in your browser...")
    print("  Press  Ctrl+C  to stop the app.")
    print("=" * 50)

    # Open browser after short delay
    def open_browser():
        time.sleep(0.8)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋  Bye! Hope they loved it!")
        server.shutdown()


if __name__ == "__main__":
    main()
