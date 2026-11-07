/* Shared by the organization page and the Cairn Launcher site. Vanilla, no dependencies, no network, no cookies.
   Everything here is progressive: without it the pages read fine, they just do not move. */
(() => {
  'use strict';
  window.__ok = true;
  const doc = document;
  const $ = (s, c = doc) => c.querySelector(s);
  const $$ = (s, c = doc) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasIO = 'IntersectionObserver' in window;

  /* Scroll reveal: each element rises and fades in once. */
  const reveals = $$('[data-reveal]');
  if (reduce || !hasIO) {
    reveals.forEach((e) => e.classList.add('in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      }
    }, { rootMargin: '0px 0px -7% 0px', threshold: 0.06 });
    reveals.forEach((e) => io.observe(e));
  }

  /* One scroll loop, one requestAnimationFrame per frame: nav background, reading progress, parallax. */
  const nav = $('.nav');
  const bar = $('.progress i');
  const items = reduce ? [] : $$('[data-parallax]').map((el) => ({ el, f: parseFloat(el.dataset.parallax) || 0.08, box: el.parentElement, on: false }));
  let queued = false;
  const tick = () => { if (!queued) { queued = true; requestAnimationFrame(frame); } };
  function frame() {
    queued = false;
    const y = window.scrollY, vh = window.innerHeight;
    if (nav && !nav.classList.contains('is-always')) nav.classList.toggle('is-stuck', y > 24);
    if (bar) bar.style.transform = 'scaleX(' + Math.min(1, y / Math.max(1, doc.documentElement.scrollHeight - vh)).toFixed(4) + ')';
    const live = items.filter((p) => p.on).map((p) => [p, p.box.getBoundingClientRect()]); // reads first, then writes
    for (const [p, r] of live) {
      p.el.style.transform = 'translate3d(0,' + ((vh / 2 - (r.top + r.height / 2)) * p.f).toFixed(1) + 'px,0)';
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

  /* Table of contents of the legal pages: mark the section being read. */
  const toc = $$('.doc__toc a');
  if (toc.length && hasIO) {
    const byId = new Map(toc.map((a) => [a.getAttribute('href').slice(1), a]));
    const spy = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        toc.forEach((a) => a.classList.remove('is-on'));
        const a = byId.get(e.target.id);
        if (a) a.classList.add('is-on');
      }
    }, { rootMargin: '-12% 0px -80% 0px' });
    [...byId.keys()].map((id) => doc.getElementById(id)).filter(Boolean).forEach((h) => spy.observe(h));
  }

  /* Copy buttons: <button data-copy="#selector" data-done="Copied">. */
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
