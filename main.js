// progressive enhancement flag (used by the FAQ accordion CSS)
document.documentElement.classList.add('js');

// ---- Cookie consent + consent-gated analytics ----
(function () {
  const banner = document.getElementById('consent');
  if (!banner) return;
  const KEY = 'csc-consent';
  const gaId = window.CSC_GA_ID;
  const store = {
    get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
    set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  };
  function loadAnalytics() {
    if (!gaId || gaId.indexOf('XXXX') > -1 || window.__ga) return; // not configured yet
    window.__ga = true;
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + gaId;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', gaId, { anonymize_ip: true });
  }
  function choose(v) { store.set(v); banner.hidden = true; if (v === 'accept') loadAnalytics(); }
  const prior = store.get();
  if (prior === 'accept') loadAnalytics();
  else if (prior !== 'decline') banner.hidden = false;
  document.getElementById('consentAccept').addEventListener('click', () => choose('accept'));
  document.getElementById('consentDecline').addEventListener('click', () => choose('decline'));
  document.addEventListener('click', (e) => {
    if (e.target.closest('[data-cookie-prefs]')) { e.preventDefault(); banner.hidden = false; }
  });
})();

// year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// mobile menu
const toggle = document.getElementById('toggle');
const menu = document.getElementById('menu');
if (toggle && menu) {
  toggle.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    menu.classList.remove('open');
    toggle.setAttribute('aria-expanded', false);
  }));
}

// ---- Nav dropdowns: hover-intent with a close delay (desktop only) ----
// Pure CSS :hover dismisses the menu the instant the cursor slips off the
// trigger or crosses the gap. We drive an .open class in JS and hold it open
// for a short grace period so brief slips don't snap it shut.
(function () {
  const desktop = () => window.matchMedia('(min-width: 821px)').matches;
  document.querySelectorAll('.nav-links .has-menu').forEach((item) => {
    let timer;
    const open = () => { clearTimeout(timer); item.classList.add('open'); };
    const close = (delay) => {
      clearTimeout(timer);
      timer = setTimeout(() => item.classList.remove('open'), delay);
    };
    item.addEventListener('mouseenter', () => { if (desktop()) open(); });
    item.addEventListener('mouseleave', () => { if (desktop()) close(260); });
    // keyboard accessibility
    item.addEventListener('focusin', () => { if (desktop()) open(); });
    item.addEventListener('focusout', (e) => {
      if (desktop() && !item.contains(e.relatedTarget)) close(0);
    });
  });
  // Escape closes any open menu and returns focus to its trigger
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.nav-links .has-menu.open').forEach((item) => {
      item.classList.remove('open');
      const trigger = item.querySelector('a');
      if (trigger && item.contains(document.activeElement)) trigger.focus();
    });
  });
})();

// ---- Dark / light theme toggle ----
const themeBtn = document.getElementById('themeToggle');
if (themeBtn) {
  themeBtn.addEventListener('click', () => {
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    const next = dark ? 'light' : 'dark';
    if (next === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
    themeBtn.setAttribute('aria-pressed', String(next === 'dark'));
    try { localStorage.setItem('csc-theme', next); } catch (e) {}
  });
}

// ---- Back-to-top button ----
const toTop = document.getElementById('toTop');
if (toTop) {
  const onScroll = () => { toTop.hidden = window.scrollY < 600; };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  toTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// scroll reveal
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// count-up numbers (home stats)
const counters = document.querySelectorAll('.count');
if (counters.length) {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt = (v, dec, comma) => {
    let s = dec > 0 ? v.toFixed(dec) : Math.round(v).toString();
    if (comma) {
      const parts = s.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      s = parts.join('.');
    }
    return s;
  };
  const run = (el) => {
    const to = parseFloat(el.dataset.to) || 0;
    const dec = parseInt(el.dataset.dec || '0', 10);
    const comma = el.dataset.comma === '1';
    if (reduce) { el.textContent = fmt(to, dec, comma); return; }
    const dur = 1300, t0 = performance.now();
    const tick = (t) => {
      const p = Math.min(1, (t - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(to * e, dec, comma);
      if (p < 1) requestAnimationFrame(tick); else el.textContent = fmt(to, dec, comma);
    };
    requestAnimationFrame(tick);
  };
  const co = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { run(e.target); co.unobserve(e.target); } });
  }, { threshold: 0.4 });
  counters.forEach((c) => co.observe(c));
}

// contact form: submit to the configured backend (Netlify Forms works with no
// extra setup), show an inline success state, and fall back to a mailto draft
// if there's no live backend (e.g. local preview or a non-Netlify host).
const enquiry = document.getElementById('enquiry');
if (enquiry) {
  const mailtoFallback = (f) => {
    const to = 'hello@clear-sky-consulting.au';
    const subject = encodeURIComponent('Meeting enquiry - ' + f.topic.value);
    const phone = f.phone ? f.phone.value : '';
    const body = encodeURIComponent(
      'Name: ' + f.name.value + '\n' +
      'Email: ' + f.email.value + '\n' +
      (phone ? 'Phone: ' + phone + '\n' : '') +
      'Topic: ' + f.topic.value + '\n' +
      'Preferred office: ' + f.office.value + '\n\n' +
      f.message.value
    );
    window.location.href = 'mailto:' + to + '?subject=' + subject + '&body=' + body;
  };
  enquiry.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const f = ev.target;
    if (!f.checkValidity()) { f.reportValidity(); return; }
    const btn = f.querySelector('button[type=submit]');
    const done = document.getElementById('enquiryDone');
    if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    fetch(f.getAttribute('action') || '/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(new FormData(f)).toString()
    }).then((r) => {
      if (!r.ok) throw new Error('no live backend');
      f.querySelectorAll('.field, .form-title, .form-note, button').forEach((el) => { el.style.display = 'none'; });
      if (done) { done.hidden = false; done.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    }).catch(() => {
      if (btn) { btn.disabled = false; btn.textContent = 'Send enquiry'; }
      mailtoFallback(f);
    });
  });
}

// ---- Accordion: any .qa on the page (service pages, FAQ, etc.) ----
document.querySelectorAll('.qa > .qa-q').forEach((btn) => {
  btn.addEventListener('click', () => {
    const qa = btn.closest('.qa');
    const open = qa.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
});

// ---- FAQ page: search, expand-all, scrollspy ----
const faqMain = document.querySelector('.faq-main');
if (faqMain) {
  const items = Array.from(faqMain.querySelectorAll('.qa'));
  const groups = Array.from(faqMain.querySelectorAll('.faq-group'));
  faqMain.addEventListener('click', (e) => { if (e.target.closest('.qa-q')) syncExpandLabel(); });

  // expand / collapse all
  const expandBtn = document.getElementById('faqExpand');
  function syncExpandLabel() {
    if (!expandBtn) return;
    const allOpen = items.every((qa) => qa.classList.contains('open'));
    expandBtn.textContent = allOpen ? 'Collapse all' : 'Expand all';
  }
  if (expandBtn) {
    expandBtn.addEventListener('click', () => {
      const allOpen = items.every((qa) => qa.classList.contains('open'));
      items.forEach((qa) => {
        qa.classList.toggle('open', !allOpen);
        qa.querySelector('.qa-q').setAttribute('aria-expanded', !allOpen ? 'true' : 'false');
      });
      syncExpandLabel();
    });
  }

  // live search
  const search = document.getElementById('faqSearch');
  const countEl = document.getElementById('faqCount');
  const noResults = document.getElementById('faqNoResults');
  const totalLabel = countEl ? countEl.textContent : '';
  if (search) {
    search.addEventListener('input', () => {
      const q = search.value.trim().toLowerCase();
      let shown = 0;
      items.forEach((qa) => {
        const match = !q || (qa.dataset.q || '').includes(q);
        qa.classList.toggle('hide', !match);
        if (match) { shown++; if (q) qa.classList.add('open'); }
        else qa.classList.remove('open');
      });
      groups.forEach((g) => {
        const anyVisible = g.querySelectorAll('.qa:not(.hide)').length > 0;
        g.classList.toggle('hide', !anyVisible);
      });
      if (countEl) countEl.textContent = q ? (shown + ' result' + (shown === 1 ? '' : 's')) : totalLabel;
      if (noResults) noResults.hidden = shown !== 0;
      syncExpandLabel();
    });
  }

  // sticky-nav scrollspy
  const navLinks = Array.from(document.querySelectorAll('.faq-nav a[data-spy]'));
  if (navLinks.length && 'IntersectionObserver' in window) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          navLinks.forEach((l) => l.classList.toggle('active', l.dataset.spy === e.target.id));
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });
    groups.forEach((g) => spy.observe(g));
  }
}

// ---- Generic category filter (case studies, newsroom, ...) ----
document.querySelectorAll('.cs-filter').forEach((bar) => {
  const grid = document.getElementById(bar.dataset.target || 'csGrid');
  if (!grid) return;
  const empty = document.getElementById(bar.dataset.empty || 'csEmpty');
  const chips = Array.from(bar.querySelectorAll('.cs-chip'));
  const cards = Array.from(grid.children);
  bar.addEventListener('click', (ev) => {
    const chip = ev.target.closest('.cs-chip');
    if (!chip) return;
    const f = chip.dataset.filter;
    chips.forEach((c) => c.classList.toggle('active', c === chip));
    let shown = 0;
    cards.forEach((card) => {
      const match = f === 'all' || card.dataset.cat === f;
      card.classList.toggle('hide', !match);
      if (match) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
  });
});

// ---- Insights: topic filter ----
const insFilter = document.querySelector('.ins-filter');
if (insFilter) {
  const chips = Array.from(insFilter.querySelectorAll('.ins-chip'));
  const cards = Array.from(document.querySelectorAll('#insGrid .ins-card'));
  const empty = document.getElementById('insEmpty');
  insFilter.addEventListener('click', (ev) => {
    const chip = ev.target.closest('.ins-chip');
    if (!chip) return;
    const f = chip.dataset.filter;
    chips.forEach((c) => c.classList.toggle('active', c === chip));
    let shown = 0;
    cards.forEach((card) => {
      const match = f === 'all' || card.dataset.cat === f;
      card.classList.toggle('hide', !match);
      if (match) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
  });
}

// ---- "Which service fits you?" quiz ----
const quiz = document.getElementById('quiz');
if (quiz) {
  const SVC = {
    clarity: { t: 'Decision clarity session', href: 'service-decision-clarity.html',
      why: "You're weighing a single, significant decision and want an impartial, expert sounding board to reach a clear next step - fast." },
    planning: { t: 'Planning & strategy', href: 'service-planning-strategy.html',
      why: "You have a goal that matters and want it turned into a concrete, sequenced plan with milestones you can actually track." },
    second: { t: 'Second opinion review', href: 'service-second-opinion.html',
      why: "You've got a proposal or quote in hand and want an honest, independent read on whether it stacks up before you commit." },
    ongoing: { t: 'Ongoing advisory', href: 'service-ongoing-advisory.html',
      why: "Important decisions keep coming up, and you'd value a trusted advisor on call who already understands your situation." }
  };
  const order = ['clarity', 'planning', 'second', 'ongoing'];
  const steps = Array.from(quiz.querySelectorAll('.quiz-step'));
  const result = document.getElementById('quizResult');
  const back = document.getElementById('quizBack');
  const bar = document.getElementById('quizBar');
  const count = document.getElementById('quizCount');
  const total = steps.length;
  let current = 0;
  const votes = [];

  const show = (i) => {
    current = i;
    steps.forEach((s, n) => { s.hidden = n !== i; s.classList.toggle('is-active', n === i); });
    result.hidden = true;
    back.hidden = i === 0;
    count.style.display = '';
    count.textContent = 'Question ' + (i + 1) + ' of ' + total;
    bar.style.width = Math.round(((i + 1) / total) * 100) + '%';
  };

  const finish = () => {
    const tally = {};
    votes.forEach((v) => { tally[v] = (tally[v] || 0) + 1; });
    let best = order[0], bestN = -1;
    order.forEach((k) => { if ((tally[k] || 0) > bestN) { bestN = tally[k] || 0; best = k; } });
    const s = SVC[best];
    steps.forEach((st) => { st.hidden = true; });
    back.hidden = false;
    count.style.display = 'none';
    bar.style.width = '100%';
    result.innerHTML =
      '<span class="eyebrow">Your best match</span>' +
      '<h2>' + s.t + '</h2>' +
      '<p>' + s.why + '</p>' +
      '<div class="quiz-cta"><a class="btn btn-primary" href="contact.html">Book a free meeting</a>' +
      '<a class="btn btn-ghost" href="' + s.href + '">Learn about this service &rarr;</a></div>' +
      '<p class="quiz-foot">Not quite right? <a href="services.html">Compare all four services</a> or <a href="contact.html">just ask us</a>.</p>';
    result.hidden = false;
  };

  quiz.addEventListener('click', (e) => {
    const opt = e.target.closest('.quiz-opt');
    if (!opt) return;
    votes[current] = opt.dataset.svc;
    if (current < total - 1) show(current + 1);
    else finish();
  });
  back.addEventListener('click', () => {
    if (!result.hidden) { show(current); return; }   // result -> last question
    if (current > 0) show(current - 1);
  });
}

// ---- Newsletter signup (front-end demo only) ----
const newsletter = document.getElementById('newsletter');
if (newsletter) {
  newsletter.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const email = document.getElementById('newsEmail');
    if (!email.value || !email.checkValidity()) { email.focus(); return; }
    const row = newsletter.querySelector('.news-row');
    const done = document.getElementById('newsDone');
    if (row) row.style.display = 'none';
    if (done) done.hidden = false;
  });
}
