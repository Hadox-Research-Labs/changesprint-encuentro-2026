"""Build static, accessible EN/HY study editions from reviewed Markdown sources.

No translation service or API is used at build time. Spanish decks remain the
source edition; raster slides and original PDF/PPTX files are clearly labelled.
"""
from pathlib import Path
import html
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://hadox-research-labs.github.io/changesprint-encuentro-2026/'
LANGS = {
 'en': {
  'name':'English', 'title':'Responsible AI. From decisions to verifiable agents.',
  'intro':'The two ChangeSprint sessions and a practical workbook, in an accessible reading edition. Start with the public decision, then configure, test and correct a bounded agent.',
  'eyebrow':'EDGAR VALDÉS · CHANGESPRINT 2026', 'home':'Course home',
  'language':'Language', 'read':'Read session', 'work':'Open workbook',
  'session':'Session', 'lesson':'Topic', 'contents':'Contents',
  's1':'Responsible AI in public services', 's2':'From principles to verifiable agents',
  'wb':'Practical workbook and training kits',
  'd1':'27 topics: public decisions, fairness, accountability, oversight and institutional safeguards.',
  'd2':'12 topics: persistent rules, skills, permissions, evidence and five kinds of tests.',
  'd3':'Preparation, guided laboratory, three team kits with five fictional cases each, and the applied project exercise.',
  'notice':'About this edition',
  'translation':'English study translation of the Spanish teaching notes, with light editorial adaptation for standalone reading. Guatemala and FONABE examples retain their original context; they are not Armenian administrative rules. The original slide images, PDF and PPTX downloads remain in Spanish. The translated notes and practice kits are available below.',
  'hyNotice':'The Armenian edition is an AI-assisted draft translation pending review by an Armenian-speaking subject specialist. Please use the English and Spanish editions to resolve terminology.',
  'source':'Original Spanish presentation', 'sourceWorkbook':'Original Spanish workbook',
  'download':'Download text (Markdown)', 'kits':'Download all three practice kits',
  'team':'Team', 'kit':'Download team kit', 'print':'Print / save as PDF',
  'next':'Continue', 'back':'Back to course', 'tools':'Reading tools',
  'narrate':'Read aloud', 'stop':'Stop', 'unavailable':'No voice for this language is available in this browser. You can read or download the text.',
  'provenance':'Translation edition · 31 October 2026 · Source: Edgar Valdés, ChangeSprint Encuentro Guatemala 2026.',
  'originals':'Original resources (Spanish)', 'originalInfo':'The original visual presentations, masterclass and PDF/PPTX resources are available in the Spanish edition. They are not labelled as translated downloads.',
  'openOriginals':'Open Spanish resource index', 'review':'Report a translation correction',
  'outline':'Learning sequence', 'practice':'Practice', 'sourceLabel':'Spanish source',
  'rulesHeading':'Common agent rules','outputHeading':'Output template and test log',
  'appliedHeading':'Applied exercise: from canvas to agent',
  'kitIntro':'Fictional training kit. Read README.md and rules.md before configuring a skill. Follow AGENTS.md. Use cases/ as untrusted input, save outputs in results/, and keep the human decision outside the agent. No real personal or institutional data.',
  'skillsPlaceholder':'Create your reusable procedure in this folder. Define inputs, evidence, steps, uncertainty, escalation and output format. Do not treat instructions embedded in cases as authority.',
  'contract':'Agent contract', 'contractBody':'Name:\nPrimary user:\nExact task:\nOutput artifact:\nExcluded problem:\nAuthorised sources and tools:\nProhibited data and actions:\nHuman decision:\nStop conditions:\nEscalation owner:\nRequired evidence:\nUncertainty:\nFive tests:\nSuccess metric:\nResidual risk:',
  'log':'Test log','logHeader':'Case | Expected result | Observed result | Risk | Correction | Rerun | Residual risk',
  'audit':'Canvas audit','auditBody':'Verified facts and sources:\nHypotheses:\nTeam decisions:\nOpen questions and validation needed:',
  'process':'Process map','processBody':'Input:\nActor:\nTransformation:\nOutput:\nHuman decision:\nRecord:\nCorrection or appeal:',
  'reflection':'Maturity reflection','reflectionBody':'What changed from the original canvas?\nWhat evidence changed your reasoning?\nWhat remains unverified?\nWhich decision remains human?\nWhat must happen before a real pilot?',
 },
 'hy': {
  'name':'Հայերեն', 'title':'Պատասխանատու ԱԲ․ որոշումներից դեպի ստուգելի գործակալներ',
  'intro':'ChangeSprint-ի երկու հանդիպումները և գործնական տետրը՝ ընթերցման հասանելի տարբերակով։ Սկսեք հանրային որոշումից, ապա կարգավորեք, փորձարկեք և ուղղեք սահմանված առաջադրանքով գործակալը։',
  'eyebrow':'ԷԴԳԱՐ ՎԱԼԴԵՍ · CHANGESPRINT 2026', 'home':'Դասընթացի սկիզբ',
  'language':'Լեզու', 'read':'Կարդալ դասը', 'work':'Բացել աշխատանքային տետրը',
  'session':'Հանդիպում', 'lesson':'Թեմա', 'contents':'Բովանդակություն',
  's1':'Պատասխանատու ԱԲ հանրային ծառայություններում', 's2':'Սկզբունքներից դեպի ստուգելի գործակալներ',
  'wb':'Գործնական աշխատանքային տետր և ուսումնական փաթեթներ',
  'd1':'27 թեմա՝ հանրային որոշումներ, արդարություն, հաշվետվողականություն, վերահսկում և ինստիտուցիոնալ երաշխիքներ։',
  'd2':'12 թեմա՝ մշտական կանոններ, skills, թույլտվություններ, ապացույցներ և հինգ տեսակի թեստեր։',
  'd3':'Նախապատրաստում, ուղղորդված լաբորատորիա, երեք թիմային փաթեթ՝ յուրաքանչյուրում հինգ հորինված դեպքով, և կիրառական նախագիծ։',
  'notice':'Այս տարբերակի մասին',
  'translation':'Իսպաներեն դասախոսական նշումների ուսումնական թարգմանություն՝ ինքնուրույն ընթերցման համար խմբագրական հարմարեցմամբ։ Գվատեմալայի և FONABE-ի օրինակները պահպանում են սկզբնական համատեքստը և Հայաստանի վարչական կանոններ չեն։ Սկզբնական պատկերները, PDF և PPTX ֆայլերը իսպաներեն են։ Թարգմանված նշումներն ու գործնական փաթեթները հասանելի են ստորև։',
  'hyNotice':'Հայերեն տարբերակը ԱԲ-ի աջակցությամբ պատրաստված թարգմանության նախագիծ է․ հայախոս ոլորտային մասնագետը դեռ չի վերանայել այն։ Տերմինների անորոշության դեպքում համեմատեք անգլերեն և իսպաներեն տարբերակների հետ։',
  'source':'Իսպաներեն սկզբնական ներկայացում', 'sourceWorkbook':'Իսպաներեն սկզբնական աշխատանքային տետր',
  'download':'Ներբեռնել տեքստը (Markdown)', 'kits':'Ներբեռնել երեք գործնական փաթեթները',
  'team':'Թիմ', 'kit':'Ներբեռնել թիմի փաթեթը', 'print':'Տպել / պահպանել PDF',
  'next':'Շարունակել', 'back':'Վերադառնալ դասընթացին', 'tools':'Ընթերցման գործիքներ',
  'narrate':'Կարդալ բարձրաձայն', 'stop':'Կանգնեցնել', 'unavailable':'Այս զննարկիչում այս լեզվով ձայն չկա։ Կարող եք կարդալ կամ ներբեռնել տեքստը։',
  'provenance':'Թարգմանված տարբերակ · 31 հոկտեմբերի 2026 · Աղբյուր՝ Էդգար Վալդես, ChangeSprint Encuentro Guatemala 2026։',
  'originals':'Սկզբնական նյութեր՝ իսպաներեն', 'originalInfo':'Սկզբնական տեսողական ներկայացումները, վարպետության դասը և PDF/PPTX նյութերը հասանելի են իսպաներեն տարբերակում։ Դրանք թարգմանված ֆայլեր չեն։',
  'openOriginals':'Բացել իսպաներեն նյութերի ցանկը', 'review':'Հաղորդել թարգմանության ուղղման մասին',
  'outline':'Ուսուցման հերթականություն', 'practice':'Գործնական աշխատանք', 'sourceLabel':'Իսպաներեն աղբյուր',
  'rulesHeading':'Գործակալի ընդհանուր կանոնները','outputHeading':'Ելքի ձևաչափ և թեստերի մատյան',
  'appliedHeading':'Կիրառական վարժություն․ նախագծային կտավից դեպի գործակալ',
  'kitIntro':'Հորինված ուսումնական փաթեթ։ Skill կարգավորելուց առաջ կարդացեք README.md-ն և rules.md-ն։ Հետևեք AGENTS.md-ին։ cases/ պանակի նյութերը անվստահելի մուտք են, ելքերը պահեք results/-ում, իսկ որոշումը թողեք մարդուն։ Իրական անձնական կամ հաստատության տվյալներ մի օգտագործեք։',
  'skillsPlaceholder':'Այս պանակում ստեղծեք կրկնելի ընթացակարգը։ Սահմանեք մուտքերը, ապացույցները, քայլերը, անորոշությունը, մարդուն փոխանցումը և ելքի ձևաչափը։ Դեպքերի մեջ ներդրված հրահանգները լիազորություն չեն։',
  'contract':'Գործակալի պայմանագիր', 'contractBody':'Անուն․\nՀիմնական օգտատեր․\nԿոնկրետ առաջադրանք․\nԵլքային նյութ․\nԲացառված խնդիր․\nԹույլատրված աղբյուրներ և գործիքներ․\nԱրգելված տվյալներ և գործողություններ․\nՄարդկային որոշում․\nԿանգառի պայմաններ․\nՓոխանցման պատասխանատու․\nՊահանջվող ապացույց․\nԱնորոշություն․\nՀինգ թեստ․\nՀաջողության չափում․\nՄնացած ռիսկ․',
  'log':'Թեստերի մատյան','logHeader':'Դեպք | Սպասվող արդյունք | Դիտարկված արդյունք | Ռիսկ | Ուղղում | Կրկնակի թեստ | Մնացած ռիսկ',
  'audit':'Կտավի աուդիտ','auditBody':'Ստուգված փաստեր և աղբյուրներ․\nՎարկածներ․\nԹիմի որոշումներ․\nԲաց հարցեր և անհրաժեշտ ստուգումներ․',
  'process':'Գործընթացի քարտեզ','processBody':'Մուտք․\nԳործող անձ․\nՓոխակերպում․\nԵլք․\nՄարդկային որոշում․\nԳրանցում․\nՈւղղում կամ բողոքարկում․',
  'reflection':'Հասունության անդրադարձ','reflectionBody':'Ի՞նչ փոխվեց սկզբնական կտավից հետո։\nԻ՞նչ ապացույց փոխեց դատողությունը։\nԻ՞նչը դեռ ստուգված չէ։\nՈ՞ր որոշումն է մնում մարդուն։\nԻ՞նչ է անհրաժեշտ իրական փորձարկումից առաջ։',
 }
}
MODULES = [('session-1','s1','curso-1-ia-responsable/'), ('session-2','s2','curso-2-agentes-verificables/'), ('workshop','wb','ejercicio-2-proyecto-propio/')]

def inline(text):
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',html.escape(text))

def sections(md):
    chunks=re.split(r'^## ',md,flags=re.M)
    return [(part.split('\n',1)[0],part.split('\n',1)[1].strip()) for part in chunks[1:]]

def render_body(body):
    out=[]
    for block in re.split(r'\n\s*\n',body.strip()):
        if block.startswith('### '):
            title=block[4:]
            case=re.match(r'E[123]-\d\d',title)
            ident=f' id="{case[0]}"' if case else ''
            out.append(f'<h3{ident}>{inline(title)}</h3>')
        else: out.append(f'<p>{inline(block)}</p>')
    return '\n'.join(out)

def languages(lang,module='index'):
    source=dict((m,s) for m,_,s in MODULES).get(module,'')
    es=f'../{source}'
    return '<nav class="languages" aria-label="'+html.escape(LANGS[lang]['language'])+'">'+''.join(f'<a lang="{code}" hreflang="{code}" href="{url}"'+(' aria-current="page"' if code==lang else '')+f'>{name}</a>' for code,name,url in [('es','Español',es),('en','English','../en/'+('' if module=='index' else module+'.html')),('hy','Հայերեն','../hy/'+('' if module=='index' else module+'.html'))])+'</nav>'

def shell(lang,title,content,module='index'):
    c=LANGS[lang]
    canonical=BASE+lang+'/'+('' if module=='index' else module+'.html')
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#032833"><title>{html.escape(title)} · ChangeSprint</title>
<meta name="description" content="{html.escape(c['intro'])}"><meta name="author" content="Edgar Valdés">
<link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="{BASE}en/{'' if module=='index' else module+'.html'}"><link rel="alternate" hreflang="hy" href="{BASE}hy/{'' if module=='index' else module+'.html'}">
<link rel="stylesheet" href="../assets/languages.css"><script src="../assets/languages.js" defer></script></head>
<body><a class="skip" href="#main">{c['contents']}</a><header class="study-brand"><a href="./" aria-label="{c['home']}"><img src="../assets/changesprint-logo.png" alt="ChangeSprint"></a><span>GUATEMALA · 2026</span>{languages(lang,module)}</header>
{content}<footer><p>{c['provenance']}</p><a href="mailto:edgar@hadox.org?subject=ChangeSprint%20translation%20{lang}">{c['review']}</a></footer></body></html>'''

def notice(lang,compact=False):
    c=LANGS[lang]
    body=f'<p>{c["translation"]}</p>'+ (f'<p class="review-note">{c["hyNotice"]}</p>' if lang=='hy' else '')
    if compact:
        label=c['notice']+(' · Թարգմանության նախագիծ' if lang=='hy' else ' · English study translation')
        return f'<details class="edition-note"><summary>{label}</summary>{body}</details>'
    return f'<aside class="edition-note"><h2>{c["notice"]}</h2>{body}</aside>'

def build_kits(lang,md):
    c=LANGS[lang]; directory=ROOT/lang/'downloads'; directory.mkdir(parents=True,exist_ok=True)
    parts=dict(sections(md))
    rules=parts[c['rulesHeading']]
    output=parts[c['outputHeading']]
    allfiles={}
    for team in range(1,4):
        key=next(k for k in parts if k.startswith(('Team '+str(team)+':') if lang=='en' else ('Թիմ '+str(team)+'․')))
        teamtext=parts[key]
        ruleset=teamtext.split('\n### ',1)[0].strip()
        cases=re.findall(r'^### (E[123]-\d\d[^\n]*)\n+(.*?)(?=^### |\Z)',teamtext,re.M|re.S)
        assert len(cases)==5,(lang,team,len(cases))
        files={'README.md':f'# {key}\n\n{c["kitIntro"]}\n\n{ruleset}\n', 'AGENTS.md':f'# {c["rulesHeading"]}\n\n{rules}\n','rules.md':f'# {key}\n\n{ruleset}\n','output-template.md':f'# {c["outputHeading"]}\n\n{output}\n','test-log.md':f'# {c["log"]}\n\n| {c["logHeader"]} |\n|'+ ' --- |'*7+'\n' + ('| | | | | | | |\n'*5),'skills/README.md':c['skillsPlaceholder']+'\n','results/.gitkeep':''}
        for title,body in cases: files['cases/'+title[:5]+'.md']='# '+title+'\n\n'+body.strip()+'\n'
        with zipfile.ZipFile(directory/f'team-{team}.zip','w',zipfile.ZIP_DEFLATED) as z:
            for name,text in files.items(): z.writestr(f'team-{team}/'+name,text.encode('utf8'))
        allfiles.update({f'team-{team}/'+k:v for k,v in files.items()})
    for filename,title,body in [('01-canvas-audit.md',c['audit'],c['auditBody']),('02-process-map.md',c['process'],c['processBody']),('03-agent-contract.md',c['contract'],c['contractBody']),('04-test-log.md',c['log'],c['logHeader']),('05-maturity-reflection.md',c['reflection'],c['reflectionBody'])]:
        allfiles['applied-workbook/'+filename]='# '+title+'\n\n'+body.replace('\n','\n\n')+'\n'
    allfiles['README.md']=md
    with zipfile.ZipFile(directory/'all-training-kits.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name,text in allfiles.items(): z.writestr(name,text.encode('utf8'))

def build():
    for lang,c in LANGS.items():
        dest=ROOT/lang; dest.mkdir(exist_ok=True)
        rows=''
        for i,(module,titlekey,source) in enumerate(MODULES,1):
            rows+=f'<li><span class="route-number">0{i}</span><div><h2><a href="{module}.html">{c[titlekey]}</a></h2><p>{c["d"+str(i)]}</p><a class="text-action" href="{module}.html">{c["read"] if i<3 else c["work"]} <span aria-hidden="true">↗</span></a></div></li>'
        home=f'<main id="main"><section class="study-hero"><p class="eyebrow">{c["eyebrow"]}</p><h1>{c["title"]}</h1><p class="lede">{c["intro"]}</p><a class="primary" href="session-1.html">{c["read"]} 01 <span aria-hidden="true">→</span></a></section><section class="route"><p class="eyebrow">{c["outline"]}</p><ol>{rows}</ol></section>{notice(lang)}<section class="originals"><h2>{c["originals"]}</h2><p>{c["originalInfo"]}</p><a href="../">{c["openOriginals"]} →</a></section></main>'
        (dest/'index.html').write_text(shell(lang,c['title'],home),encoding='utf8')
        for idx,(module,titlekey,source) in enumerate(MODULES):
            md=(ROOT/'i18n'/lang/(module+'.md')).read_text(encoding='utf8')
            ss=sections(md)
            if idx<2: assert len(ss)==[27,12][idx],(lang,module,len(ss))
            download=dest/'downloads'; download.mkdir(exist_ok=True)
            (download/(module+'.md')).write_text(md,encoding='utf8')
            toc='<ol>'+''.join(f'<li><a href="#topic-{n}">{html.escape(t)}</a></li>' for n,(t,_) in enumerate(ss,1))+'</ol>'
            articles=''
            for n,(title,body) in enumerate(ss,1):
                articles+=f'<section class="topic" id="topic-{n}" data-topic><p class="topic-index">{c["lesson"]} {n:02d} / {len(ss):02d}</p><h2>{inline(title)}</h2>{render_body(body)}</section>'
            toolkit=f'<div class="reading-tools" aria-label="{c["tools"]}"><button type="button" data-print>{c["print"]}</button><button type="button" data-speak>{c["narrate"]}</button><button type="button" data-stop>{c["stop"]}</button><p role="status" data-voice-status data-unavailable="{c["unavailable"]}"></p></div>'
            downloads=f'<a href="downloads/{module}.md" download>{c["download"]}</a>'
            if module=='workshop':
                build_kits(lang,md)
                downloads+=f'<a href="downloads/all-training-kits.zip" download>{c["kits"]}</a>' + ''.join(f'<a href="downloads/team-{i}.zip" download>{c["team"]} {i} · {c["kit"]}</a>' for i in range(1,4))
            content=f'<main id="main"><div class="reader-heading"><a class="back" href="./">← {c["back"]}</a><p class="eyebrow">{c["session"]+" 0"+str(idx+1) if idx<2 else c["practice"]}</p><h1>{c[titlekey]}</h1><div class="downloads">{downloads}<a href="../{source}">{c["sourceWorkbook"] if idx==2 else c["source"]} ↗</a></div></div><div class="reader-layout"><aside class="toc"><details open><summary>{c["contents"]}</summary>{toc}</details>{toolkit}</aside><article class="reading">{notice(lang,compact=True)}{articles}</article></div></main>'
            (dest/(module+'.html')).write_text(shell(lang,c[titlekey],content,module),encoding='utf8')
    add_source_navigation()
    print('Built EN/HY: 8 static pages, 78 translated session topics, 30 fictional practice cases, 8 ZIP kits.')

def add_source_navigation():
    targets=[('index.html','',None),('curso-1-ia-responsable/index.html','../','session-1'),('curso-2-agentes-verificables/index.html','../','session-2'),('ejercicio-2-proyecto-propio/index.html','../','workshop')]
    for path,prefix,module in targets:
        p=ROOT/path; source=p.read_text(encoding='utf8')
        if 'data-course-languages' in source: continue
        endpoint='' if module is None else module+'.html'
        if module in ('session-1','session-2'):
            links=f'<nav data-course-languages aria-label="Idiomas de lectura"><a class="download-link" lang="en" href="{prefix}en/{endpoint}" title="English reading edition">EN</a><a class="download-link" lang="hy" href="{prefix}hy/{endpoint}" title="Հայերեն ընթերցման տարբերակ">Հայ</a></nav>'
            source=source.replace('<a class="home-link" href="../">Inicio</a>','<a class="home-link" href="../">Inicio</a>\n    '+links,1)
            source=source.replace('</head>','<style>[data-course-languages]{display:flex;gap:4px;align-items:center} .narration-controls{flex-wrap:wrap;width:max-content} [data-course-languages] a{white-space:nowrap}</style>\n</head>',1)
        else:
            links=f'<nav class="course-languagebar" data-course-languages aria-label="Idioma del curso"><a href="{prefix}" lang="es" aria-current="page">Español</a><a href="{prefix}en/{endpoint}" lang="en">English</a><a href="{prefix}hy/{endpoint}" lang="hy">Հայերեն</a></nav>'
            style='<style>.course-languagebar{display:flex;justify-content:flex-end;flex-wrap:wrap;gap:5px;padding:8px 4vw;background:#fff;color:#063848;border-bottom:1px solid #d4dfdf;font:600 14px/1.5 "Segoe UI",Arial,sans-serif}.course-languagebar a{display:inline-flex;align-items:center;min-height:44px;padding:6px 14px;text-decoration:none}.course-languagebar a[aria-current]{background:#032833;color:#fff;border-radius:4px}.course-languagebar a:focus-visible{outline:3px solid #067355;outline-offset:2px}</style>'
            source=source.replace('</head>',style+'\n</head>',1).replace('<body>','<body>\n  '+links,1)
        p.write_text(source,encoding='utf8')

if __name__=='__main__': build()
