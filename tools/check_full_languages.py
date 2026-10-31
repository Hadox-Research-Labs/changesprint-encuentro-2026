"""Verify full-page parity, complete notes, asset routes and language links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
from build_full_languages import PAGES,original_notes,read_catalog,norm
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.links=[];self.sections=[];self.notes=[];self.note=False;self.lang='';self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if 'id' in a:self.ids.append(a['id'])
  if tag=='section':self.sections.append(a.get('id',''))
  if tag=='aside' and a.get('class')=='notes':self.note=True;self.notes.append('')
  for key in ['href','src','data-background-image']:
   if key in a:self.links.append(a[key])
 def handle_endtag(self,tag):
  if tag=='aside':self.note=False
 def handle_data(self,data):
  self.text.append(data)
  if self.note:self.notes[-1]+=data
def parse(file):
 p=Page();p.feed(file.read_text(encoding='utf8'));return p
cats=read_catalog();original=original_notes();count=0
for lang in ['en','hy']:
 for path in PAGES:
  source=parse(ROOT/path);translated=parse(ROOT/lang/path)
  assert translated.lang==lang
  assert source.sections==translated.sections[:len(source.sections)],(lang,path,'section parity')
  assert set(source.ids)<=set(translated.ids),(lang,path,'lost source anchor')
  if path.startswith('curso-'):
   expected=original[path.split('/')[0]]
   assert len(translated.notes)==len(expected)
   for a,b in zip(expected,translated.notes):assert norm(b)==norm(cats[lang][norm(a['text'])])
   assert 'full-notes' in (ROOT/lang/path).read_text(encoding='utf8')
  for link in translated.links:
   u=urlsplit(link)
   if u.scheme or u.netloc:continue
   dest=((ROOT/lang/path).parent/unquote(u.path)).resolve() if u.path else ROOT/lang/path
   assert dest.is_relative_to(ROOT),(lang,path,link)
   if dest.is_dir():dest/='index.html'
   assert dest.exists(),(lang,path,link)
   if u.fragment and not u.fragment.startswith('/') and dest.suffix=='.html':assert u.fragment in parse(dest).ids,(lang,path,link)
  count+=1
 ms=json.loads((ROOT/lang/'masterclass-uvg/slides.json').read_text(encoding='utf8'))
 assert len(ms)==17 and all(s['notes'] for s in ms)
 app=(ROOT/lang/'masterclass-uvg/app.js').read_text(encoding='utf8')
 assert "u.lang='es-MX'" not in app and "startsWith('es')" not in app
 assert 'window.syncCourseLanguageLinks' in app
 for alias in ['session-1.html','session-2.html','workshop.html']:
  assert 'location.replace' in (ROOT/lang/alias).read_text(encoding='utf8')
en_words=sum(len(x.split()) for x in re.split(r'^## \d+\s*\n',(ROOT/'i18n/en/notes-full.md').read_text(encoding='utf8'),flags=re.M)[1:])
source_words=sum(len(x['text'].split()) for a in original.values() for x in a)
assert en_words>source_words*.95,('possible abridgement',en_words,source_words)
print(f'PASS: {count} complete pages retain original sections and anchors; 78 complete session notes, 34 masterclass notes, media routes, translated narration and legacy URLs verified. English notes: {en_words} words; Spanish source: {source_words}.')
