# Cluster computing: caratteristiche, funzionamento e applicazioni
## Il caso di studio di Netflix

## 1. Introduzione e caratteristiche

Il **cluster computing** è un modello di elaborazione in cui più computer, chiamati **nodi**, sono collegati tramite una rete e coordinati per svolgere attività che un singolo computer non potrebbe gestire altrettanto efficacemente. I nodi mettono a disposizione capacità di calcolo, memoria e altre risorse, e un sistema di gestione decide come distribuirvi il lavoro.

Un cluster è un **sistema distribuito** perché le sue risorse si trovano su macchine distinte, ciascuna con processori e memoria propri. Per collaborare, i nodi devono comunicare attraverso la rete. Non si tratta quindi di un unico computer dotato di molti processori, ma di più macchine autonome che lavorano come un sistema coordinato.

È importante distinguere **cluster computing** e **calcolo parallelo**. Il primo indica l'infrastruttura composta da diversi nodi; il secondo indica l'esecuzione contemporanea di più parti di un problema. Un cluster può eseguire un programma parallelo suddiviso tra molti nodi, ma può anche ospitare numerosi programmi o servizi indipendenti. Quest'ultima situazione è particolarmente importante nel caso delle grandi piattaforme online, come Netflix.

I cluster possono avere obiettivi diversi:

- **Alte prestazioni (HPC):** uniscono la potenza di molti nodi per simulazioni scientifiche e calcoli complessi.
- **Alta disponibilità:** mantengono operativi servizi importanti anche quando alcuni nodi si guastano.
- **Elaborazione di grandi quantità di dati:** distribuiscono archiviazione e analisi tra più macchine.
- **Gestione di applicazioni e servizi:** eseguono numerose applicazioni, spesso tramite container, ripartendo automaticamente le risorse.

Nel caso di **Netflix**, l'esempio più direttamente collegato al cluster computing è **Titus**, una piattaforma di gestione dei container sviluppata dall'azienda per organizzare applicazioni e operazioni di elaborazione su gruppi di macchine nel cloud di Amazon Web Services (AWS). Le caratteristiche qui descritte fanno riferimento all'architettura pubblicata da Netflix: la sua infrastruttura è stata successivamente aggiornata e non tutti i dettagli storici devono essere considerati ancora invariati. [1][2][3]

| Elemento | Funzione in un cluster |
|---|---|
| **Nodi** | Eseguono i programmi utilizzando CPU, memoria e altre risorse. |
| **Sistema di controllo** | Tiene traccia dei nodi e coordina le operazioni. |
| **Scheduler** | Decide su quali nodi collocare le attività. |
| **Rete** | Consente le comunicazioni tra i componenti del sistema. |
| **Archiviazione** | Conserva dati, applicazioni e risultati delle elaborazioni. |
| **Monitoraggio** | Rileva errori, sovraccarichi e problemi di funzionamento. |

## 2. Funzionamento e architettura

### Come viene distribuito il lavoro

In un cluster, l'utente o un'applicazione invia al sistema una richiesta di elaborazione. Uno **scheduler** controlla le risorse disponibili e sceglie le macchine più adatte. I nodi selezionati eseguono il lavoro e comunicano gli esiti al sistema di gestione. Se il carico cresce, è possibile attivare altri nodi; se diminuisce, alcune risorse possono essere liberate.

L'organizzazione cambia in base allo scopo del cluster. Nel calcolo scientifico, processi situati su nodi differenti possono scambiarsi dati attraverso strumenti come **MPI (Message Passing Interface)**. Nei cluster che ospitano servizi web, invece, i nodi eseguono spesso applicazioni differenti o più copie della stessa applicazione, comunicando tramite protocolli di rete e API. **Non è necessario che tutti i nodi eseguano parti dello stesso calcolo**: ciò che caratterizza il cluster è la gestione coordinata di risorse distribuite.

### L'architettura documentata di Netflix Titus

Titus è stato progettato per eseguire **container**, ambienti software isolati che contengono un'applicazione e le dipendenze necessarie al suo funzionamento. In questo modo Netflix può distribuire applicazioni senza configurare manualmente ogni macchina. La piattaforma è stata sviluppata a partire dal 2015 e pubblicata come progetto open source nel 2018. [1][3]

Nell'architettura descritta dalla documentazione ufficiale, Titus utilizza macchine virtuali **Amazon EC2** come nodi di esecuzione e si basa su **Apache Mesos** per la gestione delle risorse del cluster. I componenti principali sono: [1]

| Componente | Ruolo |
|---|---|
| **Titus Gateway** | Riceve le richieste degli utenti e dei sistemi automatici tramite API REST o gRPC e ne controlla la validità. |
| **Titus Master** | Coordina le attività, decide dove eseguirle e gestisce la disponibilità delle risorse. |
| **Titus Agents** | Operano sulle macchine EC2, avviano i container e ne controllano l'esecuzione. |
| **Apache Mesos** | Contribuisce alla gestione delle risorse disponibili tra le macchine del cluster. |
| **ZooKeeper e Cassandra** | Nell'architettura documentata supportano rispettivamente la scelta del controller attivo e la conservazione delle informazioni di gestione. |

Un processo semplificato si svolge così:

1. Uno sviluppatore o un servizio automatico richiede l'esecuzione di un'applicazione, specificandone l'immagine software, le risorse necessarie e il numero di attività da avviare.
2. Il **Gateway** riceve la richiesta e la trasmette al **Master**.
3. Il **Master**, tenendo conto delle risorse disponibili, assegna le attività agli **Agents** presenti sui nodi EC2.
4. Gli **Agents** avviano i container e ne sorvegliano lo stato.
5. Il sistema può avviare altre istanze, terminare quelle non necessarie o intervenire sui guasti secondo le regole previste.

In questo modello il lavoro passa quindi da una richiesta centralizzata a un'esecuzione distribuita su molte macchine. L'utente non deve scegliere manualmente il singolo server su cui avviare ogni applicazione. [1]

### Rete, container e distribuzione delle risorse

La **rete** permette al Gateway, al Master e agli Agents di comunicare. Le applicazioni containerizzate devono inoltre poter raggiungere i servizi e i dati di cui hanno bisogno. Netflix ha integrato Titus con le funzionalità di rete e sicurezza di AWS, comprese le reti virtuali **VPC**, i gruppi di sicurezza e i permessi di accesso. [3]

Un altro elemento fondamentale è il **bilanciamento del carico**. Se più macchine possono ospitare lo stesso servizio, il sistema cerca di ripartire le istanze in modo da utilizzare le risorse senza sovraccaricare un solo nodo. Per le attività che devono restare operative a lungo sono importanti anche la replicazione e il riavvio delle istanze non funzionanti; per le elaborazioni temporanee, dette **job batch**, conta soprattutto completare il lavoro e gestire gli eventuali tentativi successivi a un errore. [2][3]

Titus mette in evidenza una caratteristica dei cluster moderni: molti nodi non devono necessariamente cooperare a un unico calcolo, perché il loro scopo può essere quello di eseguire **molti servizi contemporaneamente**, con risorse assegnate e controllate da una piattaforma comune.

## 3. Vantaggi del cluster computing

Il primo vantaggio è la **scalabilità**. Aumentando il numero di nodi, un'organizzazione può eseguire più lavori contemporaneamente o servire un numero maggiore di richieste. Questa crescita viene chiamata *scalabilità orizzontale*, perché non richiede di rendere sempre più potente un unico computer. Nei sistemi cloud l'aumento delle risorse può essere automatizzato e adattato alla domanda.

Un secondo vantaggio è la **disponibilità del servizio**. Se un'applicazione è eseguita su più nodi e uno di essi si guasta, le altre istanze possono continuare a funzionare. Un sistema di gestione può inoltre riavviare le attività interrotte o ricollocarle su macchine disponibili. Questo risultato dipende dalla presenza di meccanismi di ridondanza: un cluster non è automaticamente immune ai guasti.

Il cluster permette anche di **utilizzare meglio l'hardware**. Invece di assegnare un'intera macchina a ogni applicazione, è possibile ospitare più container su uno stesso nodo e distribuire le risorse in base alle necessità. Netflix ha descritto, per Titus, strategie di collocazione dei container finalizzate sia all'efficienza sia all'affidabilità. [2][3]

Un altro beneficio è la **flessibilità di sviluppo**. I container consentono di preparare un'applicazione con le sue dipendenze e distribuirla su nodi differenti. Questo rende più semplice eseguire test, aggiornare i servizi e utilizzare in modo coerente gli stessi programmi in ambienti diversi. Netflix ha spiegato che la gestione tramite container ha permesso ai propri sviluppatori di accelerare sensibilmente la distribuzione di alcune applicazioni. [2]

Infine, i cluster permettono la **condivisione delle risorse**: più utenti, squadre di sviluppatori o servizi possono utilizzare la stessa infrastruttura, mentre uno scheduler ne coordina le richieste e le priorità.

## 4. Limiti e criticità

Il cluster computing introduce vantaggi importanti, ma anche problemi che non si presentano, o sono meno evidenti, su un singolo computer.

**Complessità di gestione.** Occorre controllare molte macchine, configurare rete, permessi, aggiornamenti e software di coordinamento. Inoltre, un errore nel sistema di gestione può avere conseguenze su numerose applicazioni. Per ridurre questo rischio si adottano controller ridondanti e sistemi di controllo dello stato dei nodi.

**Dipendenza dalla rete.** I componenti di un sistema distribuito devono comunicare. Ritardi, congestioni e interruzioni possono rallentare i programmi o rendere temporaneamente irraggiungibili servizi e dati. La disposizione delle applicazioni sui nodi influisce quindi anche sulle prestazioni.

**Bilanciamento e consumo delle risorse.** Uno scheduler deve evitare sia nodi sovraccarichi sia risorse lasciate inutilizzate. Quando più applicazioni condividono una macchina possono competere per CPU, memoria, disco o rete, peggiorando reciprocamente le prestazioni.

**Guasti e coerenza.** Il malfunzionamento di un nodo può interrompere i processi che vi sono in esecuzione. Riavviare un servizio è relativamente semplice quando non conserva informazioni locali importanti; diventa più difficile quando è necessario recuperare dati, impedire duplicazioni o mantenere coerenti le operazioni già effettuate.

**Sicurezza e costi.** Moltiplicare macchine, applicazioni e connessioni aumenta i componenti da proteggere. Nel cloud, inoltre, le risorse utilizzate e il traffico possono generare costi considerevoli: la scalabilità deve essere accompagnata da controlli sull'efficienza.

Un esempio concreto di difficoltà è stato raccontato dagli ingegneri di Netflix nel **novembre 2025**. Durante la modernizzazione della piattaforma container, l'avvio contemporaneo di molti container su alcune macchine provocava rallentamenti e blocchi dovuti alla competizione per risorse interne del sistema operativo. Il problema dimostra che aumentare il numero di processori o avviare più attività non produce necessariamente un miglioramento lineare: contano anche i limiti del software e dell'architettura hardware. Questo episodio riguarda la piattaforma container in evoluzione e non va attribuito automaticamente alla vecchia versione pubblica di Titus. [7]

## 5. Ambiti di utilizzo

Il cluster computing viene impiegato in molti settori, con obiettivi differenti.

**Ricerca scientifica.** Università e centri di ricerca utilizzano cluster HPC per simulazioni meteorologiche, analisi di fenomeni fisici, modellazione di materiali e ricerche mediche. In questi casi l'obiettivo principale è spesso accelerare calcoli che richiedono enormi quantità di operazioni.

**Intelligenza artificiale e analisi dei dati.** Molte attività, come l'addestramento di modelli, l'elaborazione di dataset e l'analisi statistica, richiedono risorse elevate oppure l'esecuzione di numerosi lavori. Netflix ha indicato tra gli impieghi di Titus l'addestramento di algoritmi, il machine learning e l'elaborazione dei dati. [2][3]

**Aziende e servizi cloud.** Piattaforme web, negozi online, gestionali e applicazioni aziendali utilizzano gruppi di server per rispondere alle richieste degli utenti, eseguire processi automatici e garantire continuità del servizio. La gestione di applicazioni containerizzate è una delle applicazioni più comuni di questa organizzazione.

**Produzione ed elaborazione multimediale.** Preparare file audio e video, convertirli in formati differenti e analizzarne le caratteristiche sono attività che possono essere distribuite tra molte macchine. Netflix ha citato espressamente la codifica dei contenuti fra i carichi gestiti dalla propria piattaforma container. [3]

**Vita quotidiana.** Gli utenti incontrano i risultati del cluster computing quando utilizzano servizi online che devono restare disponibili a molte persone contemporaneamente. Netflix è un caso particolarmente significativo: una semplice schermata di scelta di un film dipende da un'infrastruttura che esegue servizi e operazioni su numerose macchine.

## 6. Esempio reale: Netflix

### Perché Netflix è un caso di cluster computing

**Netflix** è una piattaforma di intrattenimento in streaming che deve far funzionare servizi informatici complessi per moltissimi utenti. La sua infrastruttura non è un unico cluster: comprende più sistemi distribuiti con funzioni distinte. Per questa ricerca, **Titus rappresenta il caso di cluster computing**, mentre **Open Connect** mostra come un'altra parte dell'architettura distribuita si occupi dell'effettiva consegna dei video. [1][5]

Titus nacque nel **2015** per gestire applicazioni containerizzate nel cloud AWS. Nella documentazione tecnica resa pubblica, la piattaforma coordina un insieme di nodi di esecuzione, assegna le risorse richieste e avvia i container sui server disponibili. È quindi un esempio concreto di cluster per l'esecuzione e l'organizzazione di applicazioni. [1][2]

Gli utilizzi documentati da Netflix comprendono servizi legati allo streaming, sistemi di raccomandazione, elaborazioni di dati, machine learning, codifica dei contenuti e strumenti interni. Alcune attività sono **servizi a lunga durata**, che devono rispondere continuamente alle richieste; altre sono **elaborazioni batch**, che vengono avviate, completano un compito e terminano. [2][3]

La dimensione raggiunta dal progetto è indicativa: nell'**aprile 2018** Netflix dichiarò che Titus era arrivato a gestire fino a **tre milioni di avvii di container alla settimana** e migliaia di applicazioni distribuite su diverse infrastrutture regionali. Questo dato è storico, non una misura aggiornata al 2026; serve a mostrare la scala raggiunta da una piattaforma di cluster computing in produzione. [3]

### Che cosa avviene quando un utente guarda un film

È utile distinguere due operazioni che possono sembrare identiche, ma non lo sono:

1. **Gestione dell'applicazione e dei servizi.** Quando un utente apre Netflix, il servizio deve gestire funzionalità come la navigazione del catalogo, le informazioni sui contenuti e i sistemi di raccomandazione. Netflix ha documentato Titus come piattaforma utilizzata per eseguire diversi servizi e carichi di questo tipo, distribuendoli su numerosi nodi. Ciò non significa che ogni richiesta attuale di Netflix venga necessariamente eseguita da Titus. [1][2]
2. **Consegna del film o della serie.** Una volta avviata la riproduzione, i dati audio e video vengono distribuiti attraverso **Netflix Open Connect**, una rete di distribuzione dei contenuti (*Content Delivery Network*, o **CDN**) che utilizza server specializzati chiamati **Open Connect Appliances (OCA)**. Questi server memorizzano copie dei contenuti e le forniscono agli utenti attraverso reti vicine alla loro connessione. [5][6]

Open Connect non coincide con Titus. I server OCA possono essere distribuiti o raggruppati per migliorare la consegna dei video, ma una CDN mondiale non è automaticamente un singolo cluster di calcolo. La distinzione è importante: **Titus riguarda soprattutto l'esecuzione coordinata di applicazioni; Open Connect riguarda soprattutto la distribuzione efficiente dei contenuti multimediali**.

Open Connect offre anche un esempio concreto di **tolleranza ai guasti**. La documentazione ufficiale mostra configurazioni in cui, se un'appliance non è disponibile, il traffico può essere indirizzato verso un'altra appliance o un altro punto della rete. Inoltre, Netflix monitora lo stato e il carico dei server per prendere decisioni sulla distribuzione dei contenuti. [5][6]

### L'evoluzione dell'infrastruttura

Netflix ha pubblicato Titus come progetto open source nel **2018**. Il repository pubblico principale è stato **archiviato nel luglio 2022**, perciò la documentazione disponibile rappresenta soprattutto un'architettura resa nota negli anni precedenti. Questo non prova, da solo, che ogni suo componente sia stato abbandonato nell'uso interno. [3][4]

Nel **2025**, Netflix ha descritto il passaggio da una piattaforma container precedente a una nuova soluzione basata su **kubelet e containerd**, raccontandone anche le difficoltà prestazionali. Il caso dimostra che i cluster non sono sistemi immutabili: vengono continuamente modificati per migliorare sicurezza, prestazioni e capacità di gestione. [7]

Nel complesso, Netflix è un esempio efficace perché mostra **come il cluster computing venga applicato a servizi che milioni di persone utilizzano senza vedere l'infrastruttura sottostante**. I nodi sono separati, le risorse vengono assegnate da sistemi di controllo e le applicazioni vengono distribuite in funzione delle necessità.

## 7. Conclusioni

Il **cluster computing** è una forma di sistema distribuito nella quale più nodi collegati in rete condividono il lavoro sotto un'organizzazione comune. Può servire ad accelerare calcoli scientifici, analizzare dati, aumentare la capacità di un'applicazione o mantenerla disponibile in presenza di guasti.

I suoi vantaggi principali sono **scalabilità, flessibilità, migliore utilizzo delle risorse e possibilità di aumentare l'affidabilità dei servizi**. I limiti riguardano soprattutto **complessità amministrativa, dipendenza dalla rete, sicurezza, costi e necessità di gestire correttamente i guasti**.

L'esempio di **Netflix Titus** dimostra che un cluster non deve necessariamente essere un supercomputer destinato alla ricerca: può essere un insieme coordinato di macchine su cui vengono avviati numerosi servizi e applicazioni. La differenza tra Titus e Open Connect evidenzia inoltre che il cluster computing è una delle tecnologie utilizzabili **all'interno di un'infrastruttura distribuita più ampia**, e non un sinonimo di qualsiasi sistema composto da molti server.

In definitiva, la forza di un cluster non dipende soltanto da quanti computer possiede, ma soprattutto da **quanto efficacemente riesce a coordinare le risorse, distribuire le attività e mantenere operativi i servizi**.

## 8. Bibliografia e sitografia

Le fonti seguenti sono principalmente documentazione ufficiale e pubblicazioni tecniche di Netflix. Le pubblicazioni meno recenti sono utilizzate per descrivere l'architettura e la storia di Titus, non per attestare automaticamente le configurazioni in uso nel 2026.

1. **Netflix, *Titus – Overview*.** Documentazione ufficiale sull'architettura e sui componenti Gateway, Master e Agent. https://netflix.github.io/titus/overview/
2. **Netflix Technology Blog, *The Evolution of Container Usage at Netflix*, 18 aprile 2017.** Descrizione dell'uso dei container, dei job batch e dei servizi, e dei benefici di Titus. https://medium.com/netflix-techblog/the-evolution-of-container-usage-at-netflix-3abfc096781b
3. **Netflix Technology Blog, *Titus, the Netflix container management platform, is now open source*, 18 aprile 2018.** Presentazione ufficiale della piattaforma, dei carichi di lavoro e dei dati storici sulla scala del sistema. https://medium.com/netflix-techblog/titus-the-netflix-container-management-platform-is-now-open-source-f868c9fb5436
4. **Netflix, *Repository open source di Titus* (GitHub).** Codice e documentazione pubblici; repository archiviato nel luglio 2022. https://github.com/Netflix/titus
5. **Netflix, *Open Connect*.** Sito ufficiale sulla distribuzione dei contenuti, la collaborazione con i provider Internet e le architetture di continuità del servizio. https://openconnect.netflix.com/
6. **Netflix, *Open Connect Appliances*.** Documentazione ufficiale su hardware, software, monitoraggio e alta disponibilità dei server OCA. https://openconnect.netflix.com/en/appliances/
7. **Netflix Technology Blog, *Mount Mayhem at Netflix: Scaling Containers on Modern CPUs*, 7 novembre 2025.** Caso tecnico sulle difficoltà incontrate durante la modernizzazione della piattaforma container. https://netflixtechblog.com/mount-mayhem-at-netflix-scaling-containers-on-modern-cpus-f3b09b68beac

*Fonti consultate il 21 ottobre 2026.*
