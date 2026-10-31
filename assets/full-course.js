(() => {
  const lang=document.documentElement.lang;
  const ui=JSON.parse(document.getElementById('full-course-ui')?.textContent||'{}');
  // The same page and slide remain selected when changing languages.
  function syncLanguageLinks(){
    const hash=window.Reveal?.isReady()? '#/'+Reveal.getIndices().h : location.hash;
    document.querySelectorAll('[data-course-languages] a').forEach(a=>{a.hash=hash;});
  }
  window.syncCourseLanguageLinks=syncLanguageLinks;
  window.addEventListener('hashchange',syncLanguageLinks);syncLanguageLinks();
  if(!document.documentElement.classList.contains('full-deck')) return;
  const controls=document.querySelector('.narration-controls');
  const status=controls.querySelector('[data-narration-status]');
  const voiceSelect=controls.querySelector('[data-narration-voice]');
  const rate=controls.querySelector('[data-narration-rate]');
  const rateOutput=controls.querySelector('[data-narration-rate-value]');
  const panelTitle=document.querySelector('[data-full-slide-title]');
  const panelNotes=document.querySelector('[data-full-slide-notes]');
  const pause=controls.querySelector('[data-narration-pause]');
  let run=0,auto=false,paused=false;
  let speech;
  const setStatus=text=>{status.textContent=text;};
  function stop(){run++;auto=false;paused=false;if('speechSynthesis'in window)speechSynthesis.cancel();pause.textContent=ui.pause;}
  function voices(){
    if(!('speechSynthesis'in window))return;
    const previous=voiceSelect.value;
    voiceSelect.replaceChildren(...speechSynthesis.getVoices().filter(v=>v.lang.toLowerCase().split(/[-_]/)[0]===lang).map(v=>{const o=document.createElement('option');o.value=v.name;o.textContent=v.name+' ('+v.lang+')';return o;}));
    if([...voiceSelect.options].some(o=>o.value===previous))voiceSelect.value=previous;
  }
  function reflectSlide(){
    stop();const slide=Reveal.getCurrentSlide();
    if(!slide)return;
    panelTitle.textContent=slide.dataset.slideTitle;
    panelNotes.textContent=slide.querySelector('aside.notes')?.textContent.trim()||'';
    setStatus(ui.ready);syncLanguageLinks();
  }
  function speak(advance=false){
    stop();voices();
    const voice='speechSynthesis'in window&&speechSynthesis.getVoices().find(v=>v.name===voiceSelect.value&&v.lang.toLowerCase().split(/[-_]/)[0]===lang);
    if(!voice){setStatus(ui.noVoice);return;}
    const text=Reveal.getCurrentSlide()?.querySelector('aside.notes')?.textContent.trim();
    if(!text){setStatus(ui.noNotes);return;}
    auto=advance;const token=run;
    const parts=text.match(/[^.!?։]+[.!?։]*\s*/g)||[text];
    const chunks=[];parts.forEach(p=>{if(chunks.length&&chunks[chunks.length-1].length+p.length<230)chunks[chunks.length-1]+=p;else chunks.push(p);});
    function next(){
      if(token!==run)return;
      const chunk=chunks.shift();
      if(!chunk){setStatus(ui.ready);if(auto&&!Reveal.isLastSlide()){Reveal.next();window.setTimeout(()=>speak(true),300);}return;}
      speech=new SpeechSynthesisUtterance(chunk);speech.voice=voice;speech.lang=voice.lang;speech.rate=Number(rate.value);
      speech.onend=next;speech.onerror=e=>{if(token===run&&e.error!=='canceled'&&e.error!=='interrupted'){stop();setStatus(ui.noVoice);}};
      speechSynthesis.speak(speech);setStatus(ui.speaking);
    }next();
  }
  function togglePause(){if(!('speechSynthesis'in window))return;if(paused){speechSynthesis.resume();paused=false;pause.textContent=ui.pause;}else{speechSynthesis.pause();paused=true;pause.textContent=ui.resume;}}
  function adjust(n){rate.value=Math.max(Number(rate.min),Math.min(Number(rate.max),Number(rate.value)+n));rateOutput.textContent=Number(rate.value).toFixed(2)+'x';}
  controls.querySelector('[data-narration-current]').onclick=()=>speak(false);
  controls.querySelector('[data-narration-auto]').onclick=()=>speak(true);
  controls.querySelector('[data-narration-stop]').onclick=()=>{stop();setStatus(ui.stopped);};
  pause.onclick=togglePause;controls.querySelector('[data-narration-slower]').onclick=()=>adjust(-.1);controls.querySelector('[data-narration-faster]').onclick=()=>adjust(.1);rate.oninput=()=>adjust(0);
  window.addEventListener('keydown',e=>{if(e.target.closest('input,select,textarea,button,a')||e.ctrlKey||e.metaKey||e.altKey)return;const k=e.key.toLowerCase();if('napx'.includes(k)&&k.length===1){e.preventDefault();if(k==='n')speak();if(k==='a')speak(true);if(k==='p')togglePause();if(k==='x'){stop();setStatus(ui.stopped);}}});
  if('speechSynthesis'in window){voices();speechSynthesis.addEventListener('voiceschanged',voices);}
  Reveal.on('slidechanged',reflectSlide);Reveal.on('ready',reflectSlide);if(Reveal.isReady())reflectSlide();
  window.addEventListener('pagehide',stop);
})();
