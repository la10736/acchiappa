# La Talpa Animata

La talpa deve 

1. Nascere piccola e per poi ingrandirsi
2. Scomaparire dopo un certo tempo
3. Aumentare le talpe mancate se non viene colpita

## Animazione

Volgliamo creare una animazione dove la talpa modifica la sua dimensione nel tempo. **kivy** dispone di uno strumento
molto comodo per questo tipo di attività: `Animation`.

E' sufficiente costruire una `Animation` dicendo 

1. Quali caratteristiche devono cambiare nel tempo
2. Quanto deve durare
3. ( *Opzionale* ) come eseguire questa animazione

e applicarla a quello che si vuole animare.

Quindi dove costruiamo la talpa (in fondo alla funzione `talpa()`) definiamo anche una animazione e la facciamo partire: la
funzione `talpa()` diventa quindi
 
```python
    def talpa(self, *args):
        talpa = Talpa()
        talpa.bind(on_press=self.talpa_colpita)
        self.add_widget(talpa)
        animazione = Animation(size_hint=(0.1, 0.1), duration=2)
        animazione.start(talpa)
```

Provatela e provate anche a cambiare i valori. Ora ci interessa che questi valori siano facili da cambiare e con dei
nomi chiari. Aggiungiamo quindi alla classe `AcchiappaLaTalpa` i parametri `dimensione_talpa = 0.1` e `durata_talpa = 2`
; ora usiamo questi parametri quando costruiamo l'animazione:

```python
class AcchiappaLaTalpa(FloatLayout):
    ... altro (NON TOCCARE E NON SCRIVERE)

    dimansione_talpa = 0.1
    durata_talpa = 2.0

    ... altro (NON TOCCARE E NON SCRIVERE)
    
    def talpa(self, *args):
        talpa = Talpa()
        talpa.bind(on_press=self.talpa_colpita)
        self.add_widget(talpa)
        animazione = Animation(size_hint=(self.dimansione_talpa, self.dimansione_talpa), duration=self.durata_talpa)
        animazione.start(talpa)

    ... altro (NON TOCCARE E NON SCRIVERE)
```

Ora proviamo a cambiare il tipo di animazione aggiungendo il parametro `transition="out_elastic"`:

```python
animazione = Animation(size_hint=(self.dimansione_talpa, self.dimansione_talpa), duration=self.durata_talpa, 
                       transition="out_elastic")
```

Provate.... **CARINO**

Esistono un sacco di [transizioni](https://kivy.org/docs/api-kivy.animation.html#kivy.animation.AnimationTransition) 
(cercate *kivy Animation* in Google),  qui do solo un po di esempi da provare:

* `in_quint`
* `out_quint`
* `in_out_quint`
* `in_back`
* `out_back`
* `in_out_back`
* `in_circ`
* `out_circ`
* `in_out_circ`
 
Inoltre e' possibile aggiungere animazioni successive con un semplice `+` o farle in parallelo usando `&`.... se 
qualcuno volesse giocare.

## Scomparire

Quando l'animazione finisce la talpa deve scoparire e il numero dell talpe perse aumentare. Per fare questo dobbiano
aggiungere una una funzione `talpa_mancata()` molto simile a `talpa_colpita()` ma invece di aumentare `prese` aumenta
`mancate`. Questa funzione deve essere collagata a `on_complete` di `animazione` nella funzione `talpa()`.

Aggiungiamo quindi alla classe `AcchiappaLaTalpa` la funzione `talpa_mancata()`:

```python
    def talpa_mancata(self, talpa):
        self.mancate += 1
        self.rimuovi_talpa(talpa)
```

e modifichiamo `talpa()` aggiungendo `animazione.on_complete = self.talpa_mancata` appena prima di 
`animazione.start(talpa)`. La funzione `talpa()` diventa quindi:

```python
    def talpa(self, *args):
        talpa = Talpa()
        talpa.bind(on_press=self.talpa_colpita)
        self.add_widget(talpa)
        animazione = Animation(size_hint=(self.dimansione_talpa, self.dimansione_talpa), duration=self.durata_talpa,
                               transition="out_elastic")
        animazione.on_complete = self.talpa_mancata
        animazione.start(talpa)
```

Provate, la talpa sparisce e il numero di quelle mancate aumenta. **Ma provate a cliccarla, aumenteranno sia le 
prese che le mancate.**

Quello che succede è che l'animazione viene completata anche dopo che la talpa viene rimossa: dobbiamo interrompere 
l'animazione prima di rimuovere la talpa. Per farlo basta aggiungere `Animation.cancel_all(talpa)` a `rimuovi_talpa()` 
che quindi diventa:

```python
    def rimuovi_talpa(self, talpa):
        Animation.cancel_all(talpa)
        self.remove_widget(talpa)
```

## Riassumendo

Abbiamo aggiunto l'animazione della talpa e la rimozione alla fine con il controllo del punteggio delle talpe mancate.

`main.kv`
```python
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty


class Talpa(Button):
    pass


class AcchiappaLaTalpa(FloatLayout):
    prese = NumericProperty(0)
    mancate = NumericProperty(0)
    dimansione_talpa = 0.1
    durata_talpa = 2.0

    def start(self):
        self.prese = 0
        self.mancate = 0
        self.talpa()

    def talpa(self, *args):
        talpa = Talpa()
        talpa.bind(on_press=self.talpa_colpita)
        self.add_widget(talpa)
        animazione = Animation(size_hint=(self.dimansione_talpa, self.dimansione_talpa), duration=self.durata_talpa,
                               transition="out_elastic")
        animazione.on_complete = self.talpa_mancata
        animazione.start(talpa)

    def talpa_colpita(self, talpa):
        self.prese += 1
        self.rimuovi_talpa(talpa)

    def talpa_mancata(self, talpa):
        self.mancate += 1
        self.rimuovi_talpa(talpa)

    def rimuovi_talpa(self, talpa):
        Animation.cancel_all(talpa)
        self.remove_widget(talpa)


class AcchiappaApp(App):
    def build(self):
        acchiappa = AcchiappaLaTalpa()
        acchiappa.start()
        return acchiappa


if __name__ == "__main__":
    AcchiappaApp().run()
```

`acchiappa.kv` non è cambiato.

* [**NEXT** Un sacco di talpe](talpe.md)
* [**PREV** La comparsa di una talpa](una_talpa.md)
* [**INDEX** Indice](start.md)
