/* Cairn Launcher site: progressive interactive cairn stacked nav & screenshot tour. */
(() => {
  'use strict';
  const doc = document;
  const $ = (s, c = doc) => c.querySelector(s);
  const $$ = (s, c = doc) => [...c.querySelectorAll(s)];
  const hasIO = 'IntersectionObserver' in window;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* The cairn: one stone per chapter. The stone of the chapter on screen is solid, the ones below it stay filled. */
  const chapters = $$('[data-chapter]');
  const stones = $$('.cairn li');
  if (chapters.length && stones.length && hasIO) {
    let current = -1;
    const set = (i) => {
      if (i === current || i < 0) return;
      current = i;
      stones.forEach((s, k) => {
        s.classList.toggle('is-on', k <= i);
        s.classList.toggle('is-current', k === i);
        const a = $('a', s);
        if (k === i) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    };
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          set(chapters.indexOf(e.target));
        }
      }
    }, { rootMargin: '-30% 0px -35% 0px', threshold: 0.1 });
    chapters.forEach((c) => io.observe(c));
    set(0);
  }

  /* The tour: while a step is in view, its screenshot is displayed in the sticky stage. */
  const tour = $('.tour');
  if (!tour) return;
  const steps = $$('.tour__step', tour);
  const stage = $('.tour__stage', tour);
  const img = stage && $('img', stage);
  const base = tour.dataset.shots;
  const state = { theme: 'dark', lang: doc.documentElement.lang.startsWith('zh') ? 'zh' : 'en' };
  const file = (name, small) => base + name + '-' + state.lang + '-' + state.theme + (small ? '-840' : '') + '.webp';
  const apply = (el, name) => {
    el.srcset = file(name, true) + ' 840w, ' + file(name) + ' 1680w';
    el.src = file(name);
  };
  const mq = matchMedia('(min-width: 980px)');
  let active = 0, token = 0;

  const show = (i, force) => {
    if (i < 0 || i >= steps.length) return;
    if (i === active && !force) return;
    active = i;
    steps.forEach((s, k) => s.classList.toggle('is-active', k === i));
    if (!mq.matches || !img) return;
    const name = steps[i].dataset.shot, alt = steps[i].dataset.alt, mine = ++token;
    const commit = () => {
      if (mine !== token) return;
      apply(img, name);
      img.alt = alt;
      requestAnimationFrame(() => stage.classList.remove('is-swapping'));
    };
    if (reduce) { commit(); return; }
    stage.classList.add('is-swapping');
    const probe = new Image();
    probe.sizes = img.sizes;
    probe.srcset = file(name, true) + ' 840w, ' + file(name) + ' 1680w';
    probe.onload = probe.onerror = () => setTimeout(commit, 80);
    probe.src = file(name);

    // Warm up the subsequent shot
    const next = steps[i + 1];
    if (next) {
      const warm = new Image();
      warm.srcset = file(next.dataset.shot, true) + ' 840w';
      warm.src = file(next.dataset.shot, true);
    }
  };

  const figs = $$('.tour__fig img', tour);
  const refreshFigs = () => figs.forEach((im) => apply(im, im.dataset.shot));
  const pin = () => {
    tour.classList.toggle('tour--pinned', mq.matches);
    if (mq.matches) show(active, true);
  };
  mq.addEventListener('change', pin);
  pin();

  if (hasIO) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting && mq.matches) {
          show(steps.indexOf(e.target));
        }
      }
    }, { rootMargin: '-20% 0px -30% 0px', threshold: 0.15 });
    steps.forEach((s) => io.observe(s));
  }

  // Click on step activates it directly
  steps.forEach((step, idx) => {
    step.addEventListener('click', () => {
      if (mq.matches) show(idx);
    });
  });

  // Switch theme and language
  $$('[data-set]', tour).forEach((btn) => btn.addEventListener('click', () => {
    const [key, value] = btn.dataset.set.split(':');
    state[key] = value;
    $$('[data-set^="' + key + ':"]', tour).forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    refreshFigs();
    show(active, true);
  }));
})();
