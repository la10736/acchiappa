import random
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty


class Talpa(Button):
    numero = NumericProperty(1)
    path = StringProperty()


class Start(Button):
    pass


class AcchiappaLaTalpa(FloatLayout):
    prese = NumericProperty(0)
    mancate = NumericProperty(0)
    start_button = None
    dimensione_talpa = 0.06
    intervallo_talpe = 1.5
    massimo_errori = 3
    talpe = set()

    def aggiungi_start(self):
        s = Start()
        s.on_press = self.start
        self.add_widget(s)
        self.start_button = s

    def start(self):
        self.remove_widget(self.start_button)
        self.prese = 0
        self.mancate = 0
        Clock.schedule_interval(self.talpa, self.intervallo_talpe)

    def talpa(self, *args):
        talpa = self.crea_talpa()
        size = self.dimensione_talpa
        talpa.bind(on_press=self.talpa_colpita)
        talpa.pos_hint = {"center_x": self.centro_casuale(size), "center_y": self.centro_casuale(size)}
        tempo = self.intervallo_talpe * 1.2
        self.animazione(size, tempo).start(talpa)
        self.aggiungi_talpa(talpa)

    def crea_talpa(self):
        numero = random.randint(1, 5)
        talpa = Talpa(numero=numero)
        talpa.size_hint_x = talpa.size_hint_y = 0.0001
        return talpa

    def centro_casuale(self, dimensione):
        return dimensione / 2 + (1 - dimensione) * random.random()

    def talpa_colpita(self, talpa):
        self.prese += 1
        self.rimuovi_talpa(talpa)

    def talpa_mancata(self, talpa):
        self.mancate += 1
        self.rimuovi_talpa(talpa)

    def rimuovi_talpa(self, talpa):
        Animation.cancel_all(talpa)
        self.remove_widget(talpa)

    def aggiungi_talpa(self, talpa):
        self.add_widget(talpa)
        self.talpe.add(talpa)

    def animazione(self, dimensione_finale, durata):
        animazione = Animation(size_hint_x=dimensione_finale, size_hint_y=dimensione_finale,
                               duration=durata, t="out_elastic")
        animazione.on_complete = self.talpa_mancata
        return animazione

    def fine(self):
        Clock.unschedule(self.talpa)
        for talpa in self.talpe:
            self.rimuovi_talpa(talpa)
        self.aggiungi_start()

    def on_mancate(self, *args):
        if self.mancate >= self.massimo_errori:
            self.fine()


class AcchiappaApp(App):
    def build(self):
        acchiappa = AcchiappaLaTalpa()
        acchiappa.aggiungi_start()
        return acchiappa


if __name__ == "__main__":
    AcchiappaApp().run()
