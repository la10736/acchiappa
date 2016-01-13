# La Talpa Animata

La talpa deve 

1. Nascere piccola e ingrandirsi
2. Scomaparire dopo un certo tempo
3. Aumentare le talpe mancate se non viene colpita

## Animazione

Volgliamo creare una animazione dove la talpa modifica la sua dimensione nel tempo. **kivy** dispone di uno strumento
molto comodo per questo tipo di animazioni: `Animation`.

E' sufficiente costruire una `Animation` dicendo 

1. Quali caratteristiche devono cambiare nel tempo
2. Quanto deve durare
3. ( *Opzionale* ) come eseguire questa animazione

e applicarla alla talpa.

Quindi dove costruiamo la talpa (in fondo alla funzione `talpa()`) costruiamo una animazione e facciamo partire: la
funzione `talpa()` diventa quindi la seguente
 
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
    ... e altra roba (NON SCRIVETELO)

    dimansione_talpa = 0.1
    durata_talpa = 2

    ... e altra roba (NON SCRIVETELO)
    
    def talpa(self, *args):
        talpa = Talpa()
        talpa.bind(on_press=self.talpa_colpita)
        self.add_widget(talpa)
        animazione = Animation(size_hint=(self.dimansione_talpa, self.dimansione_talpa), duration=self.durata_talpa)
        animazione.start(talpa)

    ... e altra roba (NON SCRIVETELO)
```

Ora proviamo a cambiare il tipo di animazione sostituendo `animazione = Animation(...)` con:

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

