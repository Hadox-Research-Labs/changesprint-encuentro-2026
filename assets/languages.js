(() => {
  const language = document.documentElement.lang;
  const links = [...document.querySelectorAll('.toc a[href^="#topic-"]')];
  const topics = [...document.querySelectorAll('[data-topic]')];
  const status = document.querySelector('[data-voice-status]');
  let utterance;
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
  function stop() { if ('speechSynthesis' in window) window.speechSynthesis.cancel(); utterance = null; }
  document.querySelector('[data-stop]')?.addEventListener('click', stop);
  document.querySelector('[data-speak]')?.addEventListener('click', () => {
    stop();
    const voice = 'speechSynthesis' in window && window.speechSynthesis.getVoices().find(v => v.lang.toLowerCase().split('-')[0] === language);
    if (!voice) { if(status) status.textContent = status.dataset.unavailable; return; }
    if(status) status.textContent = '';
    const active = topics.find(t => '#'+t.id === location.hash) || topics.find(t => t.getBoundingClientRect().bottom > 150) || topics[0];
    if (!active) return;
    // Speak one paragraph at a time: long utterances can be truncated by browsers.
    const chunks = [...active.querySelectorAll('h2,h3,p:not(.topic-index)')].map(e => e.textContent);
    function speakNext() {
      const text = chunks.shift();
      if (!text) return;
      utterance = new SpeechSynthesisUtterance(text); utterance.voice = voice; utterance.lang = voice.lang; utterance.rate = .95;
      utterance.onend = speakNext; window.speechSynthesis.speak(utterance);
    }
    speakNext();
  });
  if ('speechSynthesis' in window) window.speechSynthesis.getVoices();
  window.addEventListener('pagehide',stop);
  const mark = id => links.forEach(a => { if(a.hash==='#'+id) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current'); });
  if ('IntersectionObserver' in window) {
    const observer=new IntersectionObserver(entries=>{const visible=entries.find(e=>e.isIntersecting);if(visible)mark(visible.target.id);},{rootMargin:'-5% 0px -65% 0px'});
    topics.forEach(t=>observer.observe(t));
  }
  const details=document.querySelector('.toc details');
  if(details && window.matchMedia('(max-width:850px)').matches) details.open=false;
  // Preserve the current topic when switching between the two reading editions.
  function syncLanguages() {
    document.querySelectorAll('.languages a[hreflang="en"],.languages a[hreflang="hy"]').forEach(a=>{a.hash=location.hash;});
  }
  window.addEventListener('hashchange',syncLanguages); syncLanguages();
})();
