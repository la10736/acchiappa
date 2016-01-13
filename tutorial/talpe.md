# Un sacco di talpe

Ora ci manca solo far nascere le talpe regolarmente (diciamo ogni secondo e mezzo) e interrompere il gioco quando ne
sbagliamo 3.

# La comparsa delle talpe

Quello che dobbiamo fare è chiamare a intervalli regolari la funzione `talpa()`. Per fare questo usiamo un 
`Clock.schedule_interval(self.talpa, self.intervallo_talpe)` nella funzione `start()` dove : questa riga significa 
*chiama `talpa()` ogni `intervallo_talpe` secondi*. Quindi in alto in `main.py` ricordiamo che vogliamo usare `Clock` 
con

```python
from kivy.clock import Clock
```

e modifichiamo `AcchiappaLaTalpa` e la funzion `start()` come:

```python
class AcchiappaLaTalpa(FloatLayout):
    ... e altra roba (DA NON SCRIVERE)

    intervallo_talpe = 1.5

    def start(self):
        self.prese = 0
        self.mancate = 0
        Clock.schedule_interval(self.talpa, self.intervallo_talpe)

    ... e altra roba (DA NON SCRIVERE)
```

## Massimo 3 errori

E' possibile definire una funzione che viene chiamata tutte le volte che una proprietà cambia valore. Questa funzione
deve semplicemente avere il nome `on_<property>` e prendere due argomenti. Facciamo un esempio pratico: se alla
clase `AcchiappaLaTalpa` aggiungiamo la seguente funzione

```python
    def on_mancate(self, instance, mancate):
        print("MANCATE " + str(mancate))
```

vedremo sulla console

```
MANCATE 1
MANCATE 2
MANCATE 3
....
```

... una riga per ogni talpa mancata.

Quindi quando il numero di talpe mancate supera il 3 ... interropiamo l'aggiunta di talpe con 
`Clock.unschedule(self.talpa)`. Quindi:

```python
    def on_mancate(self, instance, mancate):
        if self.mancate == 3:
            Clock.unschedule(self.talpa)
```

**BUG** Le talpe mancate possono diventare 4 e comunque dopo che ne ho mancate 3 posso comunque aumentare le prese.

Prima di risolvere il baco mettiamoci nelle condizioni di poter lavorare comodi: definiamo una funzione `stop()` che
per ora esegue solo `Clock.unschedule(self.talpa)` e chiamiamo questa quando mancate è `3`: questo sarà il punto dove 
faremo l'interruzione.

```python
    def on_mancate(self, instance, mancate):
        if self.mancate == 3:
            self.stop()
    
    def stop(self):
        Clock.unschedule(self.talpa)
```

## Correzzione del Baco

Ora potremmo iniziare a sperimentare un sacco di strade come interrompere l'animazione bloccare i punteggi, ma il vero
problema è che il nostro punto attivo sono le talpe, la cosa migliore è rimuoverle tutte: infatti rimuovendo la talpa
si evita qualsiasi altro evento di punteggio.

Sarebbe possibile guardare tutti i componenti dentro a `AcchiappaLaTalpa` con `self.children` e selezionare solo le 
talpe direttamente o usando qualche trucco sui nomi; ma facciamo le cose direttamente: creiamo un contenitore e tutte
le volte che aggiungiamo una talpa la aggiungiamo anche al contenitore e quando rimuoviamo, rimuoviamo anche dal 
contenitore.

Il contenitore è in `AcchiappaLaTalpa`, si chiama `talpe` e è un `set()` (insieme vuoto). Per aggiungere a un insieme
si usa la funzione `add()` e per rimuovere `discard()` (o `remove()`). Qundi modifichiamo la classe `AcchiappaLaTalpa` 
per definire `talpe` e aggiornarlo quando la talpa viene aggiunta e rimossa.

```python
class AcchiappaLaTalpa(FloatLayout):
    ... e altra roba (DA NON SCRIVERE)
    talpe = set()

    def start(self):
        self.prese = 0
        self.mancate = 0
        self.talpe = set()
        Clock.schedule_interval(self.talpa, self.intervallo_talpe)

    def talpa(self, *args):
        ... e altra roba (DA NON SCRIVERE)
        self.talpe.add(talpa)

    ... e altra roba (DA NON SCRIVERE)

    def rimuovi_talpa(self, talpa):
        Animation.cancel_all(talpa)
        self.remove_widget(talpa)
        self.talpe.discard(talpa)

    ... e altra roba (DA NON SCRIVERE)
```

Le righe da aggiungere alla classe `AcchiappaLaTalpa` sono 4:

1. `talpe = set()` all'inizio
2. `self.talpe = set()` nella funzione `start()`
3. `self.talpe.add(talpa)` in fondo alla funzione `talpa()`
4. `self.talpe.discard(talpa)` in fondo alla funzione `rimuovi_talpa()`

Provate, tutto funzionerà come prima ma... ora conosciamo **Esattamente** quali sono le talpe presenti al momemto dello 
`stop()`: modifichiamo quindi `stop()` per rimuoverle

```python
    def stop(self):
        Clock.unschedule(self.talpa)
        for talpa in self.talpe.copy():
            self.rimuovi_talpa(talpa)
```

Abbiamo usato `self.talpe.copy()` invece che semplicemnete `self.talpe` dato che `rimuovi_talpa()` modifica talpe e non
si può fare un ciclo su una cosa che cambia.

## Riassumendo

![Talpe e Punteggio](talpe_e_punteggio.png)

`main.py`
```python
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock


class Talpa(Button):
    pass


class AcchiappaLaTalpa(FloatLayout):
    prese = NumericProperty(0)
    mancate = NumericProperty(0)
    dimansione_talpa = 0.1
    durata_talpa = 2
    intervallo_talpe = 1.5
    talpe = set()

    def start(self):
        self.prese = 0
        self.mancate = 0
        self.talpe = set()
        Clock.schedule_interval(self.talpa, self.intervallo_talpe)

    def talpa(self, *args):
        talpa = Talpa()
        talpa.bind(on_press=self.talpa_colpita)
        self.add_widget(talpa)
        animazione = Animation(size_hint=(self.dimansione_talpa, self.dimansione_talpa), duration=self.durata_talpa,
                               transition="out_elastic")
        animazione.on_complete = self.talpa_mancata
        animazione.start(talpa)
        self.talpe.add(talpa)

    def talpa_colpita(self, talpa):
        self.prese += 1
        self.rimuovi_talpa(talpa)

    def talpa_mancata(self, talpa):
        self.mancate += 1
        self.rimuovi_talpa(talpa)

    def rimuovi_talpa(self, talpa):
        Animation.cancel_all(talpa)
        self.remove_widget(talpa)
        self.talpe.discard(talpa)

    def on_mancate(self, instance, mancate):
        if self.mancate == 3:
            self.stop()

    def stop(self):
        Clock.unschedule(self.talpa)
        for talpa in self.talpe.copy():
            self.rimuovi_talpa(talpa)


class AcchiappaApp(App):
    def build(self):
        acchiappa = AcchiappaLaTalpa()
        acchiappa.start()
        return acchiappa


if __name__ == "__main__":
    AcchiappaApp().run()
```

`acchiappa.kv` non è cambiato.

* [**NEXT** Bottone di Start](btn_start.md)
* [**PREV** La talpa animata](talpa_animata.md)
* [**INDEX** Indice](start.md)
