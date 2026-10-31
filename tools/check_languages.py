"""Check published language routes, complete lesson coverage and usable kits."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[];self.links=[];self.lang=None;self.topic_count=0;self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='section' and 'data-topic' in a:self.topic_count+=1
        for key in ('href','src'):
            if key in a:self.links.append(a[key])

count=0
for lang in ['en','hy']:
    for file in (ROOT/lang).glob('*.html'):
        doc=Page(); doc.feed(file.read_text(encoding='utf8'))
        assert doc.lang==lang and doc.h1==1,file
        assert len(doc.ids)==len(set(doc.ids)),('duplicate id',file)
        if file.stem.startswith('session-'):
            assert doc.topic_count=={'session-1':27,'session-2':12}[file.stem],file
        if lang=='hy':
            text=file.read_text(encoding='utf8'); assert 'pending' not in text
            assert len(re.findall('[\u0531-\u0587]',text))>150,file
        for link in doc.links:
            u=urlsplit(link)
            if u.scheme or u.netloc:continue
            dest=(file.parent/unquote(u.path)).resolve() if u.path else file
            assert dest.is_relative_to(ROOT),('outside root',link)
            if dest.is_dir():dest/='index.html'
            assert dest.exists(),(file,link)
            if u.fragment and dest.suffix=='.html':
                target=Page();target.feed(dest.read_text(encoding='utf8'))
                assert u.fragment in target.ids,(file,link)
        count+=1
    for team in range(1,4):
        with zipfile.ZipFile(ROOT/lang/'downloads'/f'team-{team}.zip') as z:
            names=z.namelist(); cases=[n for n in names if '/cases/' in n]
            assert len(cases)==5,(lang,team,cases)
            for required in ['AGENTS.md','README.md','rules.md','output-template.md','test-log.md','skills/README.md']:
                assert f'team-{team}/'+required in names
            rules=z.read(f'team-{team}/AGENTS.md').decode('utf8')
            assert len(rules)>500
            for name in names:z.read(name).decode('utf8')
    with zipfile.ZipFile(ROOT/lang/'downloads/all-training-kits.zip') as z:
        assert len([n for n in z.namelist() if '/cases/' in n])==15
        assert len([n for n in z.namelist() if n.startswith('applied-workbook/')])==5
    source=(ROOT/'i18n'/lang/'workshop.md').read_text(encoding='utf8')
    assert len(re.findall(r'^### E[123]-\d\d',source,re.M))==15

for path in ['index.html','curso-1-ia-responsable/index.html','curso-2-agentes-verificables/index.html','ejercicio-2-proyecto-propio/index.html']:
    assert 'data-course-languages' in (ROOT/path).read_text(encoding='utf8')
print(f'PASS: {count} pages, 78 translated topics, 30 fictional cases, 8 ZIP downloads; local links, anchors, language metadata and source navigation verified.')
