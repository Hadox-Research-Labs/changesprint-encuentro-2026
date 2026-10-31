"""Full translations of the original HTML pages, not alternative summaries.

Every source text/attribute has an explicit translation. Missing strings abort
the build. The original DOM structure, slide images and navigation are retained.
"""
from pathlib import Path
from html.parser import HTMLParser
import html,json,re,posixpath,os,zipfile
from urllib.parse import urlsplit,urlunsplit,unquote

ROOT=Path(__file__).resolve().parents[1]
PAGES=['index.html','curso-1-ia-responsable/index.html','curso-2-agentes-verificables/index.html','ejercicio-2-proyecto-propio/index.html','masterclass-uvg/index.html']
norm=lambda s:re.sub(r'\s+',' ',s).strip()
def original_notes():
 out={}
 for folder in ['curso-1-ia-responsable','curso-2-agentes-verificables']:
  src=(ROOT/folder/'index.html').read_text(encoding='utf8')
  out[folder]=[{'title':html.unescape(t),'text':html.unescape(re.sub('<[^>]+>','',n)).strip()} for t,n in re.findall(r'<section[^>]+data-slide-title="([^"]+)"[^>]*>\s*<aside class="notes">(.*?)</aside>',src,re.S)]
 return out
LOCAL={
 'en':{'language':'Language','notes':'Complete slide notes','images':'Slide artwork and original PDF/PPTX files remain in Spanish. All page text and speaker notes are translated in full.','draft':'','pause':'Pause','resume':'Resume','ready':'Ready','stopped':'Stopped','speaking':'Narrating slide','noVoice':'No English narration voice is available in this browser. The complete notes are shown below.','noNotes':'This slide has no notes.','spanish':'Spanish original','openScreen':'Open screen','cover':'Cover','slide':'Slide','of':'of','fullscreenFallback':'Use Enlarge to open the slide.','fullscreenUnavailable':'Fullscreen is unavailable. Use Enlarge.','loadError':'The presentation could not be loaded. You can download the PDF or PowerPoint.','noVideo':'The video is unavailable. Continue with the scenes and notes.','narrationEnd':'Narration finished.','narrationError':'Narration stopped or unavailable.','videoError':'The video could not play. Continue with the slide and notes.'},
 'hy':{'language':'Լեզու','notes':'Սահիկի ամբողջական նշումները','images':'Սահիկների պատկերները և սկզբնական PDF/PPTX ֆայլերը դեռ իսպաներեն են։ Էջերի ամբողջ տեքստը և դասախոսական նշումները թարգմանված են ամբողջությամբ։','draft':'Հայերենը ԱԲ-ի աջակցությամբ թարգմանություն է և դեռ սպասում է հայախոս մասնագետի լեզվական վերանայմանը։','pause':'Դադար','resume':'Շարունակել','ready':'Պատրաստ է','stopped':'Կանգնեցված է','speaking':'Սահիկը ընթերցվում է','noVoice':'Այս զննարկիչում հայերեն ձայն հասանելի չէ։ Ամբողջական նշումները ցուցադրված են ստորև։','noNotes':'Այս սահիկը նշումներ չունի։','spanish':'Իսպաներեն բնօրինակ','openScreen':'Բացել էկրանը','cover':'Շապիկ','slide':'Սահիկ','of':'/','fullscreenFallback':'Սահիկը բացելու համար օգտագործեք «Մեծացնել»-ը։','fullscreenUnavailable':'Ամբողջ էկրանը հասանելի չէ։ Օգտագործեք «Մեծացնել»-ը։','loadError':'Ներկայացումը չհաջողվեց բեռնել։ Կարող եք ներբեռնել PDF-ը կամ PowerPoint-ը։','noVideo':'Տեսանյութը հասանելի չէ։ Շարունակեք տեսարաններով և նշումներով։','narrationEnd':'Ընթերցումն ավարտված է։','narrationError':'Ընթերցումը կանգնեցվել է կամ հասանելի չէ։','videoError':'Տեսանյութը չհաջողվեց նվագարկել։ Շարունակեք սահիկով և նշումներով։'}
}

def read_catalog():
 source=json.loads((ROOT/'i18n/full-ui-source.json').read_text(encoding='utf8'))
 cats={'en':{},'hy':{}}
 seen=set()
 for line in (ROOT/'i18n/full-ui.tsv').read_text(encoding='utf8').splitlines():
  if not line.strip():continue
  ident,en,hy=line.split('|');assert ident not in seen;seen.add(ident)
  cats['en'][source[ident]]=en;cats['hy'][source[ident]]=hy
 assert seen==set(source),set(source)-seen
 for lang in cats:
  raw=(ROOT/'i18n'/lang/'notes-full.md').read_text(encoding='utf8')
  notes=[x.strip() for x in re.split(r'^## \d+\s*\n',raw,flags=re.M)[1:]]
  assert len(notes)==39,(lang,len(notes))
  original=original_notes()
  originals=original['curso-1-ia-responsable']+original['curso-2-agentes-verificables']
  for item,text in zip(originals,notes):cats[lang][norm(item['text'])]=text
 return cats

def strip_language_bar(src):
 return re.sub(r'<nav[^>]*data-course-languages.*?</nav>','',src,flags=re.S)

def links(lang,page):
 parent=(ROOT/lang/page).parent
 names={'es':'Español','en':'English','hy':'Հայերեն'}
 return '<nav class="course-languagebar" data-course-languages aria-label="'+LOCAL[lang]['language']+'">'+''.join('<a href="'+os.path.relpath((ROOT/page if code=='es' else ROOT/code/page),parent).replace('\\','/')+'" lang="'+code+'" hreflang="'+code+'"'+(' aria-current="page"' if code==lang else '')+'>'+name+'</a>' for code,name in names.items())+'</nav>'

class Translate(HTMLParser):
 def __init__(self,lang,path,cat):
  super().__init__(convert_charrefs=True);self.lang=lang;self.path=path;self.cat=cat;self.output=[];self.raw=[];self.download_es=False
 def tr(self,text):
  key=norm(text)
  if not key:return text
  if key in self.cat:
   left=text[:len(text)-len(text.lstrip())];right=text[len(text.rstrip()):]
   return left+self.cat[key]+right
  if re.search('[A-Za-zÁÉÍÓÚáéíóúñÑ]',key):raise ValueError(('Missing translation',self.lang,self.path,key))
  return text
 def url(self,url):
  u=urlsplit(url)
  if u.scheme or u.netloc or not u.path:return url
  target=(ROOT/self.path).parent/unquote(u.path)
  target=target.resolve()
  assert target.is_relative_to(ROOT),(self.path,url)
  candidate=target/'index.html' if target.is_dir() else target
  rel=candidate.relative_to(ROOT).as_posix()
  translated=rel in PAGES or (ROOT/'i18n/full-docs'/self.lang/rel).exists()
  if rel in ['masterclass-uvg/app.js','masterclass-uvg/guion.md','curso-2-agentes-verificables/discurso-edgar.md']:new=ROOT/self.lang/rel
  elif rel in ('masterclass-uvg/slides.json','masterclass-uvg/video.json'):new=ROOT/self.lang/rel
  else:new=ROOT/self.lang/rel if translated else target
  path=os.path.relpath(new,(ROOT/self.lang/self.path).parent).replace('\\','/')
  if u.path.endswith('/') and path.endswith('/index.html'):path=path[:-10]
  return urlunsplit(('','',path,u.query,u.fragment))
 def handle_decl(self,decl):self.output.append('<!'+decl+'>')
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='script' and a.get('src')=='narration.js':self.raw.append('skip-script');return
  if tag=='html':
   a['lang']=self.lang
   if self.path.startswith('curso-'):a['class']=(a.get('class','')+' full-deck').strip()
  for key in ['title','aria-label','alt','data-slide-title']:
   if key in a:a[key]=self.tr(a[key])
  if tag=='meta' and a.get('name')=='description':a['content']=self.tr(a['content'])
  for key in ['href','src','data-background-image']:
   if key in a:a[key]=self.url(a[key])
  if tag=='a':
   href=a.get('href','').split('?')[0]
   self.download_es=bool(href.endswith(('.pdf','.pptx','.zip','.md')) and not (ROOT/self.lang) in ((ROOT/self.lang/self.path).parent/href).resolve().parents)
  if tag=='script':self.raw.append(tag)
  if tag=='style':self.raw.append(tag)
  self.output.append('<'+tag+''.join(' '+k+('="'+html.escape(v,quote=True)+'"' if v is not None else '') for k,v in a.items())+'>')
  if tag=='body' and not self.path.startswith('curso-'):
   self.output.append(links(self.lang,self.path)+self.context())
  if tag=='div' and a.get('class')=='narration-controls':self.output.append(links(self.lang,self.path))
 def context(self):
  c=LOCAL[self.lang]
  return '<aside class="translation-context"><p>'+c['images']+'</p>'+('<p>'+c['draft']+'</p>' if c['draft'] else '')+'</aside>'
 def handle_endtag(self,tag):
  if tag=='script' and self.raw and self.raw[-1]=='skip-script':self.raw.pop();return
  if tag=='a' and self.download_es:self.output.append(' <span class="original-language">('+LOCAL[self.lang]['spanish']+')</span>');self.download_es=False
  if tag=='head':
   css=os.path.relpath(ROOT/'assets/full-course.css',(ROOT/self.lang/self.path).parent).replace('\\','/')
   js=os.path.relpath(ROOT/'assets/full-course.js',(ROOT/self.lang/self.path).parent).replace('\\','/')
   self.output.append('<link rel="stylesheet" href="'+css+'"><script id="full-course-ui" type="application/json">'+json.dumps(LOCAL[self.lang],ensure_ascii=False)+'</script><script src="'+js+'" defer></script>')
  if tag=='body' and self.path.startswith('curso-'):
   self.output.append('<section class="full-notes" aria-label="'+LOCAL[self.lang]['notes']+'"><p class="note-label">'+LOCAL[self.lang]['notes']+'</p><h2 data-full-slide-title></h2><p data-full-slide-notes></p>'+self.context()+'</section>')
  self.output.append('</'+tag+'>')
  if self.raw and self.raw[-1]==tag:self.raw.pop()
 def handle_data(self,data):
  if self.raw:self.output.append(data)
  else:self.output.append(html.escape(self.tr(data),quote=False))
 def handle_comment(self,data):self.output.append('<!--'+data+'-->')

def master_js(lang):
 c=LOCAL[lang];s=(ROOT/'masterclass-uvg/app.js').read_text(encoding='utf8')
 s=s.replace('assets/slides/','../../masterclass-uvg/assets/slides/')
 changes={'Abrir pantalla':c['openScreen'],'Ampliar':'Enlarge' if lang=='en' else 'Մեծացնել','El video no está disponible. Podemos continuar con las escenas y las notas.':c['noVideo'],'Usa Ampliar para abrir la lámina.':c['fullscreenFallback'],'Pantalla completa no disponible. Usa Ampliar.':c['fullscreenUnavailable'],'No se pudo cargar la presentación. Puedes descargar el PDF o PowerPoint.':c['loadError'],'Reproducción detenida.':c['stopped'],'Este navegador no ofrece narración. Las notas están disponibles como texto.':c['noVoice'],'Narración terminada.':c['narrationEnd'],'Narración detenida o no disponible.':c['narrationError'],'Narrando las notas de esta lámina…':c['speaking'],'No se pudo reproducir el video. Continúa con la lámina y las notas.':c['videoError']}
 for a,b in changes.items():s=s.replace("'"+a+"'",json.dumps(b,ensure_ascii=False))
 if 'window.syncCourseLanguageLinks?.();' not in s:s=s.replace('if(slides[current+1])','window.syncCourseLanguageLinks?.();\n  if(slides[current+1])')
 s=s.replace('Portada · ${s.title}',c['cover']+' · ${s.title}').replace('Lámina ${s.index} de ${slides.length-1}',c['slide']+' ${s.index} '+c['of']+' ${slides.length-1}')
 s=s.replace("u.lang='es-MX'",'u.lang='+json.dumps(lang))
 s=s.replace("u.voice=voices.find(v=>v.lang==='es-MX')||voices.find(v=>v.lang.startsWith('es'))||null;",'u.voice=voices.find(v=>v.lang.toLowerCase().split(/[-_]/)[0]==='+json.dumps(lang)+');if(!u.voice){status.textContent='+json.dumps(c['noVoice'],ensure_ascii=False)+';return;}')
 return s

def build():
 cats=read_catalog()
 master=json.loads((ROOT/'masterclass-uvg/slides.json').read_text(encoding='utf8'))
 mtranslations={}
 for line in (ROOT/'i18n/masterclass-full.tsv').read_text(encoding='utf8').splitlines():
  if line.strip():i,en,hy=line.split('|');mtranslations[int(i)]={'en':en,'hy':hy}
 assert set(mtranslations)==set(range(17))
 coverage=[]
 for lang,cat in cats.items():
  for translated_doc in (ROOT/'i18n/full-docs'/lang).rglob('*.md'):
   out=ROOT/lang/translated_doc.relative_to(ROOT/'i18n/full-docs'/lang);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(translated_doc.read_text(encoding='utf8'),encoding='utf8')
  for path in PAGES:
   src=strip_language_bar((ROOT/path).read_text(encoding='utf8'))
   parser=Translate(lang,path,cat);parser.feed(src)
   out=ROOT/lang/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(re.sub(r'[ \t]+\n','\n',''.join(parser.output)),encoding='utf8')
   coverage.append({'language':lang,'page':path,'source':path,'source_notes':len(re.findall('<aside class="notes">',src))})
  ms=[]
  for item in master:
   translated=dict(item);translated['title']=cat[item['title']];translated['notes']=mtranslations[item['index']][lang];ms.append(translated)
  dest=ROOT/lang/'masterclass-uvg'
  (dest/'slides.json').write_text(json.dumps(ms,ensure_ascii=False,indent=2),encoding='utf8')
  (dest/'app.js').write_text(master_js(lang),encoding='utf8')
  v=json.loads((ROOT/'masterclass-uvg/video.json').read_text(encoding='utf8'))
  v['src']='../../masterclass-uvg/'+v['src'];v['poster']='../../masterclass-uvg/'+v['poster'];v['label']=cat[v['label']]
  (dest/'video.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
  (dest/'guion.md').write_text('# '+cat['Uso ético y responsable de la IA en política pública']+'\n\n'+'\n\n'.join('## '+str(s['index'])+'. '+s['title']+'\n\n'+s['notes'] for s in ms),encoding='utf8')
  for alias,target in [('session-1.html','curso-1-ia-responsable/'),('session-2.html','curso-2-agentes-verificables/'),('workshop.html','ejercicio-2-proyecto-propio/')]:
   # Keep previously shared URLs working, now pointing at the complete originals.
   (ROOT/lang/alias).write_text('<!doctype html><html lang="'+lang+'"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url='+target+'"><title>ChangeSprint</title><a href="'+target+'">ChangeSprint</a><script>const m=location.hash.match(/^#topic-(\\d+)$/);location.replace('+json.dumps(target)+'+(m?"#/"+(Number(m[1])-1):location.hash));</script></html>',encoding='utf8')
  original=original_notes()
  for n,(key,items) in enumerate(original.items(),1):
   md='# '+cat['IA responsable en lo público' if n==1 else 'De principios a agentes verificables']+'\n\n'+'\n\n'.join('## '+str(i+1)+'. '+cat[x['title']]+'\n\n'+cat[norm(x['text'])] for i,x in enumerate(items))
   (ROOT/lang/'downloads'/f'session-{n}.md').write_text(md,encoding='utf8')
   if n==2:(ROOT/lang/'curso-2-agentes-verificables/discurso-edgar.md').write_text(md,encoding='utf8')
 (ROOT/'i18n/full-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf8')
 print('Built full translations of all 5 original pages in EN/HY, 78 complete session notes and 34 complete masterclass notes. Source DOM, images and sections retained.')

if __name__=='__main__':build()
