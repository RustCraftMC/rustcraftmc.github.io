/* Shared by the organization page and the Cairn Launcher site. Vanilla, no dependencies, no network, no cookies.
   Everything here is progressive: without it the pages read fine, they just do not move.
   With prefers-reduced-motion every effect is skipped and content is shown in place. */
(() => {
  'use strict';
  window.__ok = true;
  const doc = document;
  const root = doc.documentElement;
  const $ = (s, c = doc) => c.querySelector(s);
  const $$ = (s, c = doc) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const hasIO = 'IntersectionObserver' in window;
  const zh = root.lang.startsWith('zh');

  /* Text is shown in place: there are no split headings, count-ups or scroll reveals. */

  /* ---- mobile menu: a toggle is added next to the language switch on narrow screens ---- */
  const nav = $('.nav');
  const links = nav && $('.nav__links', nav);
  const menuOpen = () => root.classList.contains('menu-open');
  if (links) {
    const btn = doc.createElement('button');
    btn.type = 'button';
    btn.className = 'nav__toggle';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', zh ? '菜单' : 'Menu');
    if (!links.id) links.id = 'site-menu';
    btn.setAttribute('aria-controls', links.id);
    btn.innerHTML = '<span></span><span></span>';
    ($('.nav__end', nav) || $('.nav__in', nav)).append(btn);
    const setOpen = (open) => {
      root.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', String(open));
      tick();
    };
    btn.addEventListener('click', () => setOpen(!menuOpen()));
    links.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && menuOpen()) { setOpen(false); btn.focus(); } });
    matchMedia('(min-width: 861px)').addEventListener('change', (m) => { if (m.matches) setOpen(false); });
  }

  /* ---- one scroll loop, one requestAnimationFrame per frame: nav, reading progress, parallax, scroll tilt ---- */
  const bar = $('.progress i');
  const barBox = bar && bar.parentElement;
  const isBar = barBox && barBox.getAttribute('role') === 'progressbar';
  if (isBar) { barBox.setAttribute('aria-valuemin', '0'); barBox.setAttribute('aria-valuemax', '100'); }
  const canHide = nav && !nav.classList.contains('is-always') && !doc.body.classList.contains('doc-page');
  if (canHide) nav.addEventListener('focusin', () => nav.classList.remove('is-hidden'));
  const items = reduce ? [] : $$('[data-parallax]').map((el) => ({ el, f: parseFloat(el.dataset.parallax) || 0.08, box: el.parentElement, on: false }));
  const tilts = reduce ? [] : $$('[data-scrolltilt]');
  let queued = false, lastY = window.scrollY, lastPct = -1;
  function tick() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  function frame() {
    queued = false;
    const y = window.scrollY, vh = window.innerHeight;
    if (nav) {
      if (!nav.classList.contains('is-always')) nav.classList.toggle('is-stuck', y > 24 || menuOpen());
      const d = y - lastY;
      if (canHide && Math.abs(d) > 6) {
        nav.classList.toggle('is-hidden', d > 0 && y > vh * 0.7 && !menuOpen());
        lastY = y;
      }
    }
    if (bar) {
      const k = Math.min(1, y / Math.max(1, root.scrollHeight - vh));
      bar.style.transform = 'scaleX(' + k.toFixed(4) + ')';
      const pct = Math.round(k * 100);
      if (isBar && pct !== lastPct) { barBox.setAttribute('aria-valuenow', String(pct)); lastPct = pct; }
    }
    for (const el of tilts) el.style.setProperty('--p', Math.min(1, y / (vh * 0.55)).toFixed(3));
    const live = items.filter((p) => p.on).map((p) => [p, p.box.getBoundingClientRect()]); // reads first, then writes
    for (const [p, r] of live) {
      p.el.style.translate = '0 ' + ((vh / 2 - (r.top + r.height / 2)) * p.f).toFixed(1) + 'px';
    }
  }
  if (items.length && hasIO) {
    const pio = new IntersectionObserver((entries) => {
      for (const e of entries) { const p = items.find((x) => x.box === e.target); if (p) p.on = e.isIntersecting; }
      tick();
    }, { rootMargin: '25% 0px 25% 0px' });
    items.forEach((p) => pio.observe(p.box));
  }
  addEventListener('scroll', tick, { passive: true });
  addEventListener('resize', tick, { passive: true });
  tick();

  /* ---- pointer effects, only for a real mouse: spotlight, 3D tilt, magnetic buttons, cursor glow ---- */
  if (fine && !reduce) {
    $$('[data-spot], [data-tilt]').forEach((el) => {
      const tilt = el.hasAttribute('data-tilt');
      const max = parseFloat(el.dataset.tilt) || 6;
      let raf = 0, px = 0, py = 0;
      const apply = () => {
        raf = 0;
        const r = el.getBoundingClientRect();
        const x = (px - r.left) / r.width, y = (py - r.top) / r.height;
        el.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
        el.style.setProperty('--my', (y * 100).toFixed(1) + '%');
        if (tilt) {
          el.style.setProperty('--rx', ((0.5 - y) * max).toFixed(2) + 'deg');
          el.style.setProperty('--ry', ((x - 0.5) * max).toFixed(2) + 'deg');
        }
      };
      el.addEventListener('pointermove', (e) => {
        px = e.clientX; py = e.clientY;
        if (tilt) el.classList.add('is-tilting');
        if (!raf) raf = requestAnimationFrame(apply);
      });
      el.addEventListener('pointerleave', () => {
        if (!tilt) return;
        el.classList.remove('is-tilting');
        el.style.setProperty('--rx', '0deg');
        el.style.setProperty('--ry', '0deg');
      });
    });

    $$('[data-magnetic]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const dx = (e.clientX - r.left - r.width / 2) * 0.22;
        const dy = (e.clientY - r.top - r.height / 2) * 0.32;
        el.style.translate = dx.toFixed(1) + 'px ' + dy.toFixed(1) + 'px';
      });
      el.addEventListener('pointerleave', () => { el.style.translate = ''; });
    });

    const glow = doc.createElement('div');
    glow.className = 'glow';
    glow.setAttribute('aria-hidden', 'true');
    doc.body.append(glow);
    let gx = innerWidth / 2, gy = innerHeight / 3, tx = gx, ty = gy, graf = 0;
    const gstep = () => {
      gx += (tx - gx) * 0.12;
      gy += (ty - gy) * 0.12;
      glow.style.transform = 'translate3d(' + gx.toFixed(1) + 'px,' + gy.toFixed(1) + 'px,0)';
      graf = Math.abs(tx - gx) + Math.abs(ty - gy) > 0.4 ? requestAnimationFrame(gstep) : 0;
    };
    addEventListener('pointermove', (e) => {
      tx = e.clientX; ty = e.clientY;
      glow.classList.add('on');
      if (!graf) graf = requestAnimationFrame(gstep);
    }, { passive: true });
    doc.documentElement.addEventListener('pointerleave', () => glow.classList.remove('on'));
  }

  /* ---- table of contents of the legal pages: mark the section being read ---- */
  const toc = $$('.doc__toc a');
  if (toc.length && hasIO) {
    const box = $('.doc__toc');
    const byId = new Map(toc.map((a) => [a.getAttribute('href').slice(1), a]));
    const spy = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        toc.forEach((a) => a.classList.remove('is-on'));
        const a = byId.get(e.target.id);
        if (!a) continue;
        a.classList.add('is-on');
        // On narrow screens the contents are a horizontal strip: keep the current entry in view.
        if (box && box.scrollWidth > box.clientWidth) {
          box.scrollTo({ left: a.offsetLeft - box.clientWidth / 2 + a.offsetWidth / 2, behavior: reduce ? 'auto' : 'smooth' });
        }
      }
    }, { rootMargin: '-12% 0px -80% 0px' });
    [...byId.keys()].map((id) => doc.getElementById(id)).filter(Boolean).forEach((h) => spy.observe(h));
  }

  /* ---- copy buttons: <button data-copy="#selector" data-done="Copied"> ---- */
  $$('[data-copy]').forEach((btn) => btn.addEventListener('click', async () => {
    const src = $(btn.dataset.copy);
    if (!src) return;
    const text = src.textContent.trim();
    try {
      await navigator.clipboard.writeText(text);
    } catch (_) {
      const t = doc.createElement('textarea');
      t.value = text; t.setAttribute('readonly', ''); t.style.cssText = 'position:fixed;opacity:0';
      doc.body.appendChild(t); t.select();
      try { doc.execCommand('copy'); } catch (__) { /* nothing else to try */ }
      t.remove();
    }
    const label = $('span', btn) || btn, old = label.textContent;
    label.textContent = btn.dataset.done || 'OK';
    btn.classList.add('is-done');
    setTimeout(() => { label.textContent = old; btn.classList.remove('is-done'); }, 1600);
  }));
})();
