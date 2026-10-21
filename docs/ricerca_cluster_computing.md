# Cluster computing: caratteristiche, funzionamento e applicazioni

## Caratteristiche: perché è un sistema distribuito?

Il **cluster computing** è un modello informatico nel quale più computer autonomi, chiamati **nodi**, sono collegati attraverso una rete e coordinati per svolgere attività comuni. Invece di affidare tutto il lavoro a una sola macchina, un cluster mette insieme le risorse di più sistemi: processori, memoria, capacità di archiviazione ed eventualmente GPU. Dal punto di vista di chi lo utilizza, questi computer possono apparire come un'unica infrastruttura di elaborazione.

Un cluster è un **sistema distribuito** perché il lavoro e le risorse sono collocati su macchine fisicamente o logicamente distinte. Ogni nodo dispone di un proprio sistema operativo, di propri processori e, normalmente, di una propria memoria. Quando i nodi devono collaborare, comunicano tramite la rete: non condividono automaticamente lo stesso spazio di memoria come avviene in un tradizionale computer multiprocessore.

È utile distinguere il _cluster computing_ dal **calcolo parallelo**. Il cluster indica l'insieme coordinato di computer; il calcolo parallelo è una tecnica che suddivide un problema in parti eseguibili contemporaneamente. Un cluster può essere utilizzato per un unico grande calcolo parallelo, ma anche per eseguire numerosi programmi indipendenti o più copie dello stesso servizio.

In base al loro obiettivo, si distinguono principalmente:

- **Cluster ad alte prestazioni (HPC):** accelerano simulazioni e calcoli molto impegnativi, facendo cooperare molti processori o GPU.
- **Cluster ad alta disponibilità (HA):** mantengono accessibili applicazioni e servizi anche quando uno dei nodi si guasta, attraverso ridondanza e procedure di recupero.
- **Cluster per Big Data:** distribuiscono grandi quantità di dati e le relative elaborazioni fra più macchine.
- **Cluster per applicazioni e servizi:** ospitano programmi, servizi web e container, ripartendo le richieste e le risorse disponibili.

Queste categorie non sono completamente separate: uno stesso cluster può essere progettato per unire, ad esempio, prestazioni elevate e continuità del servizio.

## Funzionamento: architettura, interazione tra nodi, utenti e rete

### Architettura di un cluster

L'organizzazione concreta dipende dall'utilizzo, ma molti cluster prevedono componenti ricorrenti:

| Componente                          | Funzione                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------- |
| **Nodi di calcolo o di esecuzione** | Eseguono programmi e operazioni utilizzando CPU, RAM e, se presenti, GPU.             |
| **Sistema di controllo**            | Monitora i nodi e coordina il funzionamento complessivo.                              |
| **Scheduler**                       | Decide quando eseguire un'attività e su quali nodi assegnarla.                        |
| **Rete di interconnessione**        | Permette lo scambio di dati e messaggi tra nodi e componenti di gestione.             |
| **Storage**                         | Conserva programmi, dati di ingresso e risultati; può essere condiviso o distribuito. |
| **Monitoraggio**                    | Controlla disponibilità, prestazioni, errori e utilizzo delle risorse.                |

Un'architettura molto diffusa prevede un **sistema di controllo** che gestisce diversi **nodi di esecuzione**. Il controllo può essere affidato a un nodo dedicato o distribuito su più macchine per evitare un singolo punto di guasto. In altri modelli alcune decisioni possono essere decentralizzate.

### Dalla richiesta all'esecuzione

Il funzionamento può essere descritto attraverso cinque passaggi:

1. **Invio della richiesta.** Un utente o un'applicazione richiede l'esecuzione di un programma o l'avvio di un servizio, indicando eventualmente CPU, memoria e altre risorse necessarie.
2. **Assegnazione delle risorse.** Lo scheduler controlla quali nodi sono disponibili e sceglie dove collocare il lavoro.
3. **Esecuzione.** I nodi selezionati avviano i processi o i container e utilizzano le risorse assegnate.
4. **Comunicazione e monitoraggio.** I processi possono scambiarsi dati attraverso la rete; il sistema controlla lo stato delle attività e rileva eventuali errori.
5. **Completamento o continuità del servizio.** Un'elaborazione termina e restituisce i risultati; un servizio, invece, può restare attivo e ricevere nuove richieste.

Nei cluster scientifici, un software come **Slurm** gestisce le code dei lavori (_job_), assegna i nodi e ne sorveglia l'esecuzione. Nei cluster di applicazioni, una piattaforma come **Kubernetes** utilizza un _control plane_ per organizzare i nodi e i carichi di lavoro containerizzati. Sono due esempi di strumenti con finalità differenti, ma basati sul coordinamento di risorse distribuite.

### Come comunicano i nodi

La **rete** è un elemento essenziale: collega i nodi tra loro, permette l'accesso degli utenti e consente ai sistemi di controllo di inviare istruzioni. Per i servizi web vengono normalmente utilizzati protocolli di rete e API; nei calcoli scientifici distribuiti si impiega spesso **MPI (Message Passing Interface)**, uno standard che consente ai processi in esecuzione su nodi differenti di scambiarsi messaggi.

Anche la gestione dei dati cambia a seconda dell'applicazione. Alcuni cluster utilizzano uno storage condiviso; altri distribuiscono i dati su più nodi. Nei sistemi per Big Data si cerca spesso di svolgere i calcoli vicino ai dati già presenti su una macchina, in modo da ridurre i trasferimenti attraverso la rete.

L'interazione dell'utente, quindi, avviene di norma con un punto di accesso, un'interfaccia o un sistema di gestione: **non è necessario collegarsi e controllare manualmente ogni singolo nodo**.

## Vantaggi: perché viene utilizzato?

Uno dei vantaggi principali è l'aumento della **capacità di elaborazione**. Se un problema può essere suddiviso in attività indipendenti, diversi nodi possono lavorarci nello stesso momento. Questo permette di ridurre i tempi di calcolo oppure di affrontare problemi troppo grandi per una sola macchina.

Un secondo vantaggio è la **scalabilità orizzontale**, cioè la possibilità di aumentare le risorse aggiungendo nuovi nodi invece di sostituire un singolo computer con uno sempre più potente. Nei cluster destinati ai servizi online, ciò permette anche di gestire un numero maggiore di utenti e richieste.

Un altro beneficio è la **continuità del servizio**. Nei cluster progettati per l'alta disponibilità, più nodi possono ospitare componenti ridondanti: se una macchina smette di funzionare, un'altra può continuare a offrire il servizio o assumerne il controllo tramite una procedura di _failover_. Questa caratteristica non è automatica, ma richiede un'architettura appositamente progettata.

Il cluster può migliorare anche l'**utilizzo delle risorse**. Uno scheduler assegna CPU, memoria e acceleratori alle attività che ne hanno bisogno, evitando, per quanto possibile, macchine inutilizzate mentre altre sono sovraccariche. Inoltre più utenti o gruppi di lavoro possono condividere un'infrastruttura costosa senza dover acquistare ciascuno un sistema equivalente.

Infine, i cluster offrono **flessibilità**: si possono usare nodi specializzati, distribuire software su più macchine e adattare l'infrastruttura a esigenze differenti. Il rapporto tra costi e benefici può essere favorevole quando l'aggiunta di server relativamente standard evita il ricorso a un'unica macchina estremamente potente, ma dipende dal tipo di applicazione e dalle spese di gestione.

## Limiti e criticità: quali problemi presenta?

Il principale svantaggio è la **complessità**. Un cluster richiede la configurazione e la manutenzione di molte macchine, oltre alla gestione di rete, sistemi operativi, accessi, aggiornamenti, scheduler e strumenti di monitoraggio. Un problema in un componente centrale, se non è prevista ridondanza, può compromettere l'intera infrastruttura.

Un'altra criticità è la **dipendenza dalla rete**. Quando i nodi devono scambiarsi grandi quantità di dati, la comunicazione introduce tempi di attesa. Una rete lenta o congestionata può diventare un collo di bottiglia e ridurre il vantaggio di avere molti processori disponibili. Nei cluster scientifici contano soprattutto larghezza di banda e latenza; nei servizi distribuiti è essenziale anche l'affidabilità delle connessioni.

La **scalabilità non è illimitata**. Aggiungere nodi non significa rendere automaticamente un programma due, dieci o cento volte più veloce. Alcune operazioni non possono essere eseguite in parallelo e altre richiedono sincronizzazione e scambio di risultati. La _legge di Amdahl_ descrive proprio il limite imposto dalla parte sequenziale di un programma.

È inoltre necessario garantire un buon **bilanciamento del carico**: se un nodo riceve molti più compiti degli altri, alcuni computer terminano presto e rimangono inattivi mentre il lavoro complessivo è ancora in corso. Nei cluster che ospitano più applicazioni, queste possono anche competere per memoria, CPU, disco e rete.

La gestione dei **guasti** è particolarmente delicata. Se un nodo si arresta durante un'elaborazione, il sistema deve capire se ripetere il lavoro, recuperare risultati intermedi o trasferire il servizio altrove. Quando più nodi conservano copie di dati, occorre inoltre evitare informazioni incoerenti. Nei cluster HA vengono utilizzati meccanismi come il _fencing_, che isola i nodi malfunzionanti per proteggere l'integrità dei dati.

Infine vanno considerati **sicurezza, costi ed energia**. Moltiplicare server e connessioni aumenta i componenti da proteggere e mantenere aggiornati. Acquisto, consumi elettrici, raffreddamento e personale specializzato possono incidere molto sul costo totale; nel cloud, invece, si pagano anche le risorse e i servizi utilizzati.

## Ambiti di utilizzo: aziende, ricerca e vita quotidiana

Il cluster computing viene utilizzato in contesti diversi, a seconda dell'obiettivo da raggiungere.

**Ricerca scientifica.** Università e centri di ricerca utilizzano cluster HPC per simulazioni climatiche e meteorologiche, studio dei materiali, fluidodinamica, fisica e analisi scientifiche. Questi problemi richiedono spesso l'esecuzione simultanea di moltissime operazioni e l'elaborazione di grandi quantità di dati.

**Intelligenza artificiale.** L'addestramento di modelli complessi e l'analisi di grandi dataset possono richiedere numerose CPU e GPU. Distribuire le attività tra più nodi consente di affrontare carichi di lavoro che sarebbero difficili da sostenere su un computer ordinario.

**Aziende e servizi cloud.** Siti di commercio elettronico, piattaforme aziendali, gestionali e servizi online possono usare cluster per ospitare applicazioni, distribuire richieste, aggiornare servizi e mantenere attive più istanze della stessa funzione. Nei moderni ambienti cloud è diffusa la gestione di applicazioni containerizzate tramite sistemi come Kubernetes.

**Big Data e analisi delle informazioni.** Sistemi come **Apache Hadoop** permettono di ripartire dati e operazioni di elaborazione tra diverse macchine. Questa organizzazione è utile, ad esempio, per analizzare grandi archivi di transazioni, registrazioni di eventi o dati raccolti da sensori.

**Servizi critici.** Banche, sistemi di prenotazione e infrastrutture aziendali possono utilizzare cluster ad alta disponibilità per ridurre le interruzioni e ripristinare rapidamente i servizi in caso di guasto. L'obiettivo principale, in questo caso, non è necessariamente eseguire i programmi più velocemente, ma mantenerli accessibili.

**Multimedia e vita quotidiana.** L'elaborazione di immagini e video, la conversione di file multimediali e il funzionamento di molti servizi digitali possono appoggiarsi a gruppi di server coordinati. Gli utenti normalmente vedono soltanto l'applicazione finale, senza accorgersi che dietro di essa lavorano più nodi.

## Esempio reale: Netflix e la piattaforma Titus

Un caso concreto di cluster computing nell'ambito dei servizi digitali è **Titus**, una piattaforma sviluppata da **Netflix** per gestire l'esecuzione di applicazioni all'interno di **container**. I container sono ambienti software che racchiudono un programma e le dipendenze necessarie al suo funzionamento, facilitandone l'esecuzione su macchine differenti.

Titus nacque nel **2015** e venne pubblicato come progetto _open source_ nel **2018**. Netflix lo utilizzava per gestire carichi di lavoro differenti, tra cui servizi legati allo streaming, sistemi di raccomandazione, elaborazione di dati, machine learning e codifica dei contenuti. L'infrastruttura si appoggiava alle macchine virtuali **Amazon EC2** ospitate su **AWS**.

### Come funzionava il cluster Titus

Nell'architettura resa pubblica da Netflix, i componenti principali erano:

- **Titus Gateway:** riceveva le richieste provenienti da utenti e applicazioni attraverso API.
- **Titus Master:** coordinava le attività, controllava le risorse disponibili e decideva su quali nodi eseguirle.
- **Titus Agents:** operavano sulle macchine EC2, avviavano i container assegnati e ne monitoravano lo stato.
- **Apache Mesos:** contribuiva alla gestione delle risorse presenti nel cluster.

In pratica, quando era necessario avviare un'applicazione, il sistema riceveva una richiesta che specificava il programma e le risorse necessarie. Il Master sceglieva i nodi disponibili e gli Agents avviavano i container. Se il carico aumentava, la piattaforma poteva ampliare le risorse utilizzate. Non serviva quindi configurare manualmente ogni singolo server per ogni attività.

La dimensione del sistema mostra l'utilità del modello: nell'**aprile 2018** Netflix dichiarava che Titus era in grado di gestire fino a **tre milioni di avvii di container alla settimana**. È un dato storico, non una misura attuale, ma rende evidente la necessità di coordinare automaticamente un numero elevato di elaborazioni.

È importante non confondere questo caso con l'intera infrastruttura Netflix. **Titus** era una piattaforma di esecuzione distribuita delle applicazioni; la distribuzione dei file video agli spettatori è invece legata anche a una diversa infrastruttura, chiamata **Open Connect**. Netflix non deve quindi essere considerata un unico cluster.

**Precisazione sull'evoluzione tecnologica.** La documentazione pubblica di Titus descrive un'architettura storica e il suo repository principale è stato archiviato nel **2022**. In un articolo tecnico pubblicato nel **novembre 2025**, Netflix ha raccontato la migrazione da una precedente piattaforma container a una nuova soluzione che utilizza componenti come **kubelet** e **containerd**. Per questa ragione, la struttura di Titus non va presentata come una descrizione verificata dell'intera infrastruttura Netflix nel 2026. Rimane però un esempio reale e ben documentato dei principi del cluster computing: nodi autonomi, coordinamento centralizzato, assegnazione delle risorse, esecuzione distribuita e scalabilità.

## Bibliografia e sitografia

Le fonti sono prevalentemente documentazioni ufficiali e pubblicazioni tecniche. Le prime sei fonti riguardano il **cluster computing in generale**; le ultime quattro documentano il **caso Netflix**.

1. **Lawrence Livermore National Laboratory**, _Introduction to Parallel Computing Tutorial_. Architetture a memoria distribuita, parallelismo, comunicazione e limiti della scalabilità. https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial
2. **SchedMD**, _Slurm Workload Manager – Overview_. Funzionamento degli scheduler, gestione dei nodi e assegnazione dei lavori. https://slurm.schedmd.com/overview.html
3. **MPI Forum**, _MPI Documents_. Standard per la comunicazione tra processi in sistemi a memoria distribuita. https://www.mpi-forum.org/docs/
4. **Kubernetes**, _Cluster Architecture_. Organizzazione in control plane e nodi di esecuzione per applicazioni containerizzate. https://kubernetes.io/docs/concepts/architecture/
5. **Apache Software Foundation**, _Apache Hadoop MapReduce Tutorial_. Elaborazione distribuita dei dati e gestione dei lavori nei cluster. https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html
6. **Red Hat**, _Configuring and Managing High Availability Clusters_, Red Hat Enterprise Linux 9. Alta disponibilità, recupero dai guasti e gestione dei nodi. https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_high_availability_clusters/index
7. **Netflix**, _Titus – Overview_. Documentazione ufficiale dell'architettura di Titus. https://netflix.github.io/titus/overview/
8. **Netflix Technology Blog**, _Titus, the Netflix Container Management Platform, Is Now Open Source_, 18 aprile 2018. Presentazione della piattaforma e dimensioni storiche. https://netflixtechblog.com/titus-the-netflix-container-management-platform-is-now-open-source-f868c9fb5436
9. **Netflix**, _Titus – GitHub Repository_. Archivio pubblico del progetto, archiviato il 27 luglio 2022. https://github.com/Netflix/titus
10. **Netflix Technology Blog**, _Mount Mayhem at Netflix: Scaling Containers on Modern CPUs_, 7 novembre 2025. Evoluzione e difficoltà della piattaforma container. https://netflixtechblog.com/mount-mayhem-at-netflix-scaling-containers-on-modern-cpus-f3b09b68beac
