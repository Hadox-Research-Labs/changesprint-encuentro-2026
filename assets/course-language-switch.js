(() => {
  function sync(){
    const hash=window.Reveal?.isReady()?'#/'+Reveal.getIndices().h:location.hash;
    document.querySelectorAll('[data-course-languages] a').forEach(a=>{a.hash=hash;});
  }
  window.syncCourseLanguageLinks=sync;
  window.addEventListener('hashchange',sync);
  if(window.Reveal){Reveal.on('ready',sync);Reveal.on('slidechanged',sync);}
  sync();
})();
