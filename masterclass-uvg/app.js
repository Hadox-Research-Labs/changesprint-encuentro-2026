'use strict';
(async function(){
 const $=id=>document.getElementById(id), status=$('status'), video=$('video');
 const release='cover-20260909';
 let slides=[],current=0,media=null;
 function stop(){if('speechSynthesis' in window)window.speechSynthesis.cancel();}
 function go(index,update=true){
  stop();video.pause();current=Math.max(0,Math.min(slides.length-1,index));
  const s=slides[current],src=`assets/slides/${s.file}?v=${release}`;
  $('slide-image').src=src;$('slide-image').alt=s.title;$('zoom').href=src;
  $('slide-title').textContent=s.title;$('notes').textContent=s.notes;$('slide-select').value=String(current);
  $('previous').disabled=current===0;$('next').disabled=current===slides.length-1;
  video.hidden=!s.video||!media;$('video-label').hidden=!s.video;
  if(s.video&&media){video.src=`${media.src}?v=${release}`;video.poster=media.poster?`${media.poster}?v=${release}`:'';video.setAttribute('aria-label',media.label);$('video-label').textContent=media.label;}
  if(s.video&&!media)$('video-label').textContent='El video no está disponible. Podemos continuar con las escenas y las notas.';
  status.textContent=s.cover?`Portada · ${s.title}`:`Lámina ${s.index} de 15 · ${s.title}`;
  if(update)history.replaceState(null,'',s.cover?'#portada':`#${s.index}`);
  if(slides[current+1]){const preload=new Image();preload.src=`assets/slides/${slides[current+1].file}`;}
 }
 async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else if($('presentation').requestFullscreen)await $('presentation').requestFullscreen();else status.textContent='Usa Ampliar para abrir la lámina.';}catch{status.textContent='Pantalla completa no disponible. Usa Ampliar.'}}
 try{const r=await fetch(`slides.json?v=${release}`,{cache:'no-store'});if(!r.ok)throw new Error();slides=await r.json();}catch{status.textContent='No se pudo cargar la presentación. Puedes descargar el PDF o PowerPoint.';return;}
 try{const r=await fetch(`video.json?v=${release}`,{cache:'no-store'});if(r.ok)media=await r.json();}catch{}
 $('slide-select').replaceChildren(...slides.map((s,i)=>{const option=document.createElement('option');option.value=String(i);option.textContent=s.cover?`Portada · ${s.title}`:`${s.index} · ${s.title}`;return option;}));
 const hashIndex=()=>{if(!location.hash||location.hash==='#portada')return 0;const n=Number(location.hash.slice(1));const found=slides.findIndex(s=>s.index===n&&!s.cover);return found>=0?found:0;};
 go(hashIndex(),false);
 $('previous').onclick=()=>go(current-1);$('next').onclick=()=>go(current+1);
 $('slide-select').onchange=e=>go(Number(e.target.value));$('fullscreen').onclick=fullscreen;
 $('stop').onclick=()=>{stop();video.pause();status.textContent='Reproducción detenida.';};
 $('speak').onclick=()=>{if(!('speechSynthesis' in window)){status.textContent='Este navegador no ofrece narración. Las notas están disponibles como texto.';return;}stop();video.pause();const u=new SpeechSynthesisUtterance(slides[current].notes);u.lang='es-MX';u.rate=.95;const voices=speechSynthesis.getVoices();u.voice=voices.find(v=>v.lang==='es-MX')||voices.find(v=>v.lang.startsWith('es'))||null;u.onend=()=>{status.textContent='Narración terminada.';};u.onerror=()=>{status.textContent='Narración detenida o no disponible.';};speechSynthesis.speak(u);status.textContent='Narrando las notas de esta lámina…';};
 video.addEventListener('play',stop);video.addEventListener('error',()=>{status.textContent='No se pudo reproducir el video. Continúa con la lámina y las notas.';});
 document.addEventListener('keydown',e=>{if(e.target.closest('input,select,textarea,button,video,a')||e.ctrlKey||e.metaKey||e.altKey)return;if(e.key==='ArrowRight'){e.preventDefault();go(current+1);}if(e.key==='ArrowLeft'){e.preventDefault();go(current-1);}if(e.key==='Home'){e.preventDefault();go(0);}if(e.key==='End'){e.preventDefault();go(slides.length-1);}if(e.key.toLowerCase()==='f')fullscreen();});
 window.addEventListener('hashchange',()=>go(hashIndex(),false));window.addEventListener('pagehide',()=>{stop();video.pause();});
})();
