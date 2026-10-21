from pathlib import Path
import re, html, shutil
root=Path('.')
md=(root/'docs/ricerca_cluster_computing.md').read_text(encoding='utf-8')
def inline(s):
 s=html.escape(s)
 s=re.sub(r'(https://[^\s<]+)',r'<a href="\1" target="_blank" rel="noopener noreferrer">\1 ↗</a>',s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
def render(s):
 out=[]; ls=s.strip().splitlines(); i=0
 while i<len(ls):
  l=ls[i].strip()
  if not l: i+=1; continue
  if l.startswith('|'):
   rows=[]
   while i<len(ls) and ls[i].strip().startswith('|'):
    cells=[c.strip() for c in ls[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r'[-: ]+',c) for c in cells): rows.append(cells)
    i+=1
   out.append('<div class="table-scroll"><table>'+''.join('<tr>'+''.join(f'<{ "th" if n==0 else "td"}>{inline(c)}</{ "th" if n==0 else "td"}>' for c in row)+'</tr>' for n,row in enumerate(rows))+'</table></div>'); continue
  if l.startswith('### '): out.append('<h3>'+inline(l[4:])+'</h3>')
  elif re.match(r'^(- |\d+\. )',l):
   tag='ul' if l.startswith('- ') else 'ol'; items=[]
   while i<len(ls) and re.match(r'^(- |\d+\. )',ls[i].strip()):
    items.append('<li>'+inline(re.sub(r'^(- |\d+\. )','',ls[i].strip()))+'</li>'); i+=1
   out.append(f'<{tag}>'+''.join(items)+f'</{tag}>'); continue
  else: out.append('<p>'+inline(l)+'</p>')
  i+=1
 return ''.join(out)
parts=re.split(r'^## \d+\. ',md,flags=re.M)[1:]
ids=['concetti','architettura','vantaggi','limiti','applicazioni','netflix','fonti']
names=['Il sistema, in breve','Dentro il cluster','Più nodi, più possibilità','Anche la potenza ha dei limiti','Dove lo incontriamo','Il caso Netflix / Titus','Le fonti della ricerca']
labels=['Fondamenti','Funzionamento','Vantaggi','Criticità','Applicazioni','Caso reale','Bibliografia']
intros=['Computer autonomi. Risorse distribuite. Un obiettivo comune.','Dalla richiesta al risultato: chi decide, chi esegue e come si comunica.','Prestazioni, crescita e continuità: i benefici dipendono dal progetto.','La rete, le parti sequenziali e la gestione dei guasti contano quanto i processori.','Dalle simulazioni scientifiche ai servizi che usiamo ogni giorno.','Una piattaforma reale per capire il coordinamento su larga scala.','Documentazioni ufficiali e pubblicazioni tecniche, raccolte nel documento originale.']
sections=[]
for i,p in enumerate(parts):
 body=p.split('\n',1)[1]
 extra=''
 if i==0:
  extra='<div class="types">'+''.join(f'<article><span>0{j+1} /</span><h3>{a}</h3><p>{b}</p></article>' for j,(a,b) in enumerate([('HPC','Accelerare simulazioni e calcoli intensivi.'),('Alta disponibilità','Mantenere accessibili servizi e applicazioni.'),('Big Data','Distribuire dati ed elaborazioni.'),('Applicazioni','Coordinare servizi, richieste e container.')]))+'</div>'
 if i==1:
  extra='<div class="workflow">'+''.join(f'<div><b>0{j+1}</b><span>{x}</span></div>' for j,x in enumerate(['Invio richiesta','Assegnazione','Esecuzione','Monitoraggio','Risultato o servizio']))+'</div>'
 if i==5:
  extra='<div class="netflix-stat"><span class="netflix-word">NETFLIX</span><div><strong>3 milioni</strong><p>di avvii di container alla settimana<br><small>Dato storico dichiarato nell’aprile 2018</small></p></div></div><p class="notice">Un caso storico, con il suo contesto: Titus nasce nel 2015, diventa open source nel 2018 e il repository viene archiviato nel 2022. La ricerca riporta anche l’evoluzione descritta da Netflix nel 2025. Titus non coincide con Open Connect né con l’intera infrastruttura Netflix.</p>'
 content=render(body)
 if i<6: content='<details><summary>Leggi l’approfondimento completo <span>＋</span></summary><div class="reading">'+content+'</div></details>'
 sections.append(f'<section id="{ids[i]}" class="chapter"><div class="chapter-label"><span>0{i+1}</span>{labels[i]}</div><div class="chapter-content"><h2>{names[i]}</h2><p class="intro">{intros[i]}</p>{extra}{content}</div></section>')
page='''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Un percorso visuale nel cluster computing: nodi, architettura, vantaggi, limiti e il caso storico Netflix Titus."><meta name="theme-color" content="#10120f"><title>Cluster — La forza di lavorare insieme</title><link rel="stylesheet" href="style.css"><script src="script.js" defer></script></head><body><a class="skip" href="#concetti">Salta al contenuto</a><div class="progress" aria-hidden="true"></div><header><a class="brand" href="#"><span class="brand-icon">⠿</span> cluster<span class="brand-dot">.</span></a><nav aria-label="Navigazione principale"><a href="#concetti">Fondamenti</a><a href="#architettura">Architettura</a><a href="#applicazioni">Applicazioni</a><a href="#netflix">Caso Netflix ↗</a></nav><a class="nav-source" href="#fonti">Fonti <span>↗</span></a></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> SISTEMI DISTRIBUITI / UNA RICERCA VISUALE</p><h1>La forza di<br>lavorare <em>insieme.</em></h1><p class="hero-description">Un computer risolve un problema.<br>Un cluster apre nuove possibilità.</p><p class="hero-sub">Scopri come macchine indipendenti mettono in comune le proprie risorse per affrontare sfide più grandi.</p><a class="button" href="#concetti">Esplora il cluster <span>↘</span></a></div><div class="visual"><div class="visual-top"><span>CLUSTER TOPOLOGY</span><span class="live">● MODELLO INTERATTIVO</span></div><div class="network" role="group" aria-label="Schema illustrativo di un cluster. Seleziona un nodo per conoscerne il ruolo."><svg viewBox="0 0 500 390" aria-hidden="true"><g fill="none" stroke="currentColor"><path d="M250 185L90 80M250 185L410 80M250 185L70 265M250 185L430 265M250 185L250 330"/><path class="secondary" d="M90 80L410 80L430 265L250 330L70 265Z"/></g></svg><button class="node master selected" data-node="control" aria-label="Sistema di controllo" aria-pressed="true"><span>⌘</span><small>CONTROL</small></button><button class="node n1" data-node="cpu" aria-label="Nodo di calcolo 01" aria-pressed="false"><span>▥</span><small>NODE 01</small></button><button class="node n2" data-node="gpu" aria-label="Nodo con GPU 02" aria-pressed="false"><span>▥</span><small>NODE 02</small></button><button class="node n3" data-node="cpu" aria-label="Nodo di calcolo 03" aria-pressed="false"><span>▥</span><small>NODE 03</small></button><button class="node n4" data-node="cpu" aria-label="Nodo di calcolo 04" aria-pressed="false"><span>▥</span><small>NODE 04</small></button><button class="node n5" data-node="storage" aria-label="Storage" aria-pressed="false"><span>▤</span><small>STORAGE</small></button></div><div class="node-description" aria-live="polite"><span id="node-title">Sistema di controllo</span><p id="node-text">Coordina i nodi e monitora il funzionamento complessivo del cluster.</p></div><div class="visual-bottom"><span>● Nodi autonomi</span><span>↔ Risorse connesse</span></div></div><div class="hero-footer"><span>PIÙ MACCHINE. UN’INFRASTRUTTURA.</span><span>Scorri per scoprire <b>↓</b></span></div></section><div class="overview"><p>Il principio è semplice.</p><h2>Distribuire il lavoro.<br><span>Moltiplicare le possibilità.</span></h2><p>Ogni nodo ha processori, sistema operativo e memoria propri. La rete li connette; il software ne coordina il lavoro. È così che nasce un sistema distribuito.</p><div class="distinction"><b>Cluster ≠ calcolo parallelo</b><span>Il cluster è l’infrastruttura. Il parallelismo è una delle tecniche che può utilizzare.</span></div></div><div class="contents"><span>IL PERCORSO</span>'''+''.join(f'<a href="#{a}">{i+1:02d} {b}</a>' for i,(a,b) in enumerate(zip(ids,labels)))+'''</div>'''+''.join(sections)+'''<section class="closing"><p class="eyebrow">CONNESSI, PER ANDARE OLTRE</p><h2>La potenza è nelle<br><em>connessioni.</em></h2><a class="button" href="docs/ricerca_cluster_computing.md" download>Scarica la ricerca originale <span>↓</span></a></section></main><footer><a class="brand" href="#">cluster.</a><p>Ricerca di Perla · Ciarlo · Doganieri</p><a href="#">Torna all’inizio ↑</a></footer></body></html>'''
(root/'index.html').write_text(page,encoding='utf-8')
