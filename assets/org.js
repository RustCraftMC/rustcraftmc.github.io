/* RustCraftMC Team: the floating voxel island behind the hero and the 404 page. Canvas 2D, no dependencies.
   Columns of grass blocks breathe in a slow wave, rise toward the pointer, and ripple where you click.
   With prefers-reduced-motion one still frame is drawn. */
(() => {
  'use strict';
  const canvas = document.querySelector('[data-world]');
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext('2d');
  const host = canvas.parentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ground = canvas.dataset.layout === 'ground';

  const N = 13;
  const C = (N - 1) / 2;
  const hash = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };

  /* The island: a ragged disc of columns, deeper in the middle like a floating chunk of earth. */
  const cells = [];
  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      const d = Math.hypot(i - C, j - C);
      if (d > C + 0.55 - hash(i, j) * 1.7) continue;
      const r = hash(j + 7, i + 3);
      const ore = r > 0.92;
      cells.push({
        i, j, d,
        base: 0.8 * Math.sin(i * 0.62 + 0.4) * Math.cos(j * 0.5 - 0.3) + 0.9 * (1 - d / C) + r * 0.3,
        depth: 1.4 + (1 - Math.min(1, d / (C + 0.5))) * 5 + hash(i * 3, j * 5) * 1.4,
        ore,
        tint: hash(i + 11, j + 17),
        delay: d * 0.07 + hash(i + 5, j + 9) * 0.35,
        specks: [0, 1, 2].map((k) => ({ u: 0.15 + hash(i + k, j * 2 + k) * 0.7, v: 0.6 + hash(i * 2 + k, j + k) * 3.2, side: k % 2 })),
        h: 0,
      });
    }
  }
  cells.sort((a, b) => (a.i + a.j) - (b.i + b.j) || a.i - b.i); // back to front

  const parts = Array.from({ length: 26 }, (_, k) => ({ seed: k, x: 0, y: 0, life: Math.random() }));
  const ripples = [];

  let w = 0, h = 0, dpr = 1, W = 0, hw = 0, hh = 0, unit = 0, cx = 0, cy = 0;
  const resize = () => {
    const r = canvas.getBoundingClientRect();
    if (!r.width || !r.height) return;
    dpr = Math.min(2, window.devicePixelRatio || 1);
    w = r.width; h = r.height;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    const wide = w >= 860;
    if (ground) {
      W = Math.min(w * 0.86, wide ? 460 : 400);
      cx = w * 0.5; cy = h - W * 0.52 - 24;
    } else if (wide) {
      W = Math.min(w * 0.46, 660);
      cx = w * 0.73; cy = h * 0.47;
    } else {
      W = Math.min(w * 0.9, 420);
      cx = w * 0.5; cy = h - W * 0.52 - 24;
    }
    hw = W / N / 2; hh = hw / 2; unit = hh * 1.8;
  };

  /* Pointer -> grid coordinates on the island's base plane. */
  let mx = 0, my = 0, hover = false, bob = 0;
  const toGrid = (x, y) => {
    const a = (x - cx) / hw, b = (y - cy - bob) / hh + 2 * C;
    return [(a + b) / 2, (b - a) / 2];
  };
  if (!reduce) {
    host.addEventListener('pointermove', (e) => {
      const r = canvas.getBoundingClientRect();
      mx = e.clientX - r.left; my = e.clientY - r.top; hover = true;
    });
    host.addEventListener('pointerleave', () => { hover = false; });
    host.addEventListener('pointerdown', (e) => {
      if (e.target.closest('a, button')) return;
      const r = canvas.getBoundingClientRect();
      const [gi, gj] = toGrid(e.clientX - r.left, e.clientY - r.top);
      if (gi < -2 || gj < -2 || gi > N + 1 || gj > N + 1) return;
      ripples.push({ i: gi, j: gj, t0: performance.now() / 1000 });
      if (ripples.length > 4) ripples.shift();
    });
  }

  const poly = (pts, fill) => {
    ctx.beginPath();
    ctx.moveTo(pts[0], pts[1]);
    for (let k = 2; k < pts.length; k += 2) ctx.lineTo(pts[k], pts[k + 1]);
    ctx.closePath();
    ctx.fillStyle = fill;
    ctx.fill();
  };

  let t0 = 0;
  const draw = (now) => {
    if (!w) return;
    if (!t0) t0 = now;
    const t = reduce ? 4 : (now - t0) / 1000;
    bob = reduce ? 0 : Math.sin(t * 0.8) * 6;
    let gi = 1e3, gj = 1e3;
    if (hover) [gi, gj] = toGrid(mx, my);

    for (const c of cells) {
      let target = c.base + Math.sin(t * 1.1 - c.d * 0.75) * 0.32;
      const dm = Math.hypot(c.i - gi, c.j - gj);
      if (dm < 3.2) target += (1 - dm / 3.2) ** 2 * 1.8;
      for (const r of ripples) {
        const age = t + t0 / 1000 - r.t0;
        const k = age * 8 - Math.hypot(c.i - r.i, c.j - r.j);
        if (k > 0 && k < Math.PI) target += Math.sin(k) * 1.3 * Math.max(0, 1 - age / 2.4);
      }
      c.h = reduce ? target : c.h + (target - c.h) * 0.12;
    }
    while (ripples.length && t + t0 / 1000 - ripples[0].t0 > 3) ripples.shift();

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);

    // Warm glow beneath the island.
    const g = ctx.createRadialGradient(cx, cy + W * 0.2, 0, cx, cy + W * 0.2, W * 0.75);
    g.addColorStop(0, 'rgba(232, 98, 44, .20)');
    g.addColorStop(1, 'rgba(232, 98, 44, 0)');
    ctx.fillStyle = g;
    ctx.fillRect(cx - W, cy - W, W * 2, W * 2);

    const lip = hh * 0.8;
    const sp = Math.max(1.5, hh * 0.32);
    for (const c of cells) {
      const enter = reduce ? 1 : Math.min(1, Math.max(0, (t - c.delay) / 0.9));
      if (enter <= 0) continue;
      const e = 1 - Math.pow(1 - enter, 3);
      const x = cx + (c.i - c.j) * hw;
      const y = cy + bob + (c.i + c.j - 2 * C) * hh - (1 - e) * 160;
      const top = y - c.h * unit;
      const bot = y + c.depth * unit;
      ctx.globalAlpha = e;

      const lift = Math.max(-1, Math.min(3, c.h));
      if (c.ore) {
        poly([x - hw, top, x, top + hh, x, bot + hh, x - hw, bot], '#a8431b');
        poly([x, top + hh, x + hw, top, x + hw, bot, x, bot + hh], '#86351a');
        poly([x, top - hh, x + hw, top, x, top + hh, x - hw, top], `hsl(18 80% ${52 + lift * 4 + c.tint * 6}%)`);
        ctx.fillStyle = 'rgba(255, 214, 170, .5)';
        ctx.fillRect(x - sp, top - sp / 2, sp * 2, sp);
      } else {
        poly([x - hw, top, x, top + hh, x, bot + hh, x - hw, bot], '#6b4a2f');
        poly([x, top + hh, x + hw, top, x + hw, bot, x, bot + hh], '#523822');
        ctx.fillStyle = 'rgba(0, 0, 0, .22)';
        for (const s of c.specks) {
          const sx = s.side ? x + s.u * hw : x - hw + s.u * hw;
          const sy = (s.side ? top + hh - s.u * hh : top + s.u * hh) + lip + s.v * unit;
          if (sy < bot) ctx.fillRect(sx - sp / 2, sy, sp, sp);
        }
        poly([x - hw, top, x, top + hh, x, top + hh + lip, x - hw, top + lip], '#4c7f2c');
        poly([x, top + hh, x + hw, top, x + hw, top + lip, x, top + hh + lip], '#3f6b25');
        poly([x, top - hh, x + hw, top, x, top + hh, x - hw, top], `hsl(${92 + c.tint * 14} 46% ${36 + lift * 4 + c.tint * 7}%)`);
      }
    }
    ctx.globalAlpha = 1;

    // Pixel motes drifting up from the island.
    if (!reduce) {
      for (const p of parts) {
        p.life += 0.0035 + (p.seed % 5) * 0.0006;
        if (p.life >= 1) p.life -= 1;
        const sx = cx + (hash(p.seed, Math.floor(t / 7 + p.seed)) - 0.5) * W * 1.05;
        const sy = cy + bob - p.life * W * 0.75;
        const a = Math.sin(p.life * Math.PI) * 0.8;
        const s = 2 + (p.seed % 3);
        ctx.fillStyle = p.seed % 4 === 0 ? `rgba(255, 138, 82, ${a})` : `rgba(160, 220, 110, ${a * 0.7})`;
        ctx.fillRect(sx, sy, s, s);
      }
    }
  };

  let running = false, raf = 0, visible = true;
  const loop = (now) => { draw(now); raf = running ? requestAnimationFrame(loop) : 0; };
  const start = () => {
    if (running || reduce || !visible || document.hidden) return;
    running = true;
    raf = requestAnimationFrame(loop);
  };
  const stop = () => { running = false; cancelAnimationFrame(raf); };

  resize();
  if (reduce) draw(performance.now());
  if ('ResizeObserver' in window) {
    new ResizeObserver(() => { resize(); if (!running) draw(performance.now()); }).observe(canvas);
  } else {
    addEventListener('resize', resize);
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      if (visible) start(); else stop();
    }).observe(canvas);
  }
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); else start(); });
  start();
})();
