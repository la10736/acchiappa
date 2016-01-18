from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from plyer import vibrator


class Talpa(Button):
    id = "talpa"


class Start(Button):
    pass


class AcchiappaLaTalpa(FloatLayout):
    prese = NumericProperty(0)
    mancate = NumericProperty(0)
    dimansione_talpa = 0.1
    durata_talpa = 2.0
    intervallo_talpe = 1.5
    bottone_start = None
    rapporto_tempi = 0.75
    numero_aumento = 5

    def aggiungi_start(self):
        self.bottone_start = Start()
        self.add_widget(self.bottone_start)
        self.bottone_start.bind(on_press=self.start_premuto)

    def start_premuto(self, pressed):
        self.remove_widget(self.bottone_start)
        self.start()

    def start(self):
        self.prese = 0
        self.mancate = 0
        Clock.schedule_interval(self.talpa, self.intervallo_talpe)

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
        self.vibra(0.5)

    def talpa_mancata(self, talpa):
        self.mancate += 1
        self.rimuovi_talpa(talpa)

    def rimuovi_talpa(self, talpa):
        Animation.cancel_all(talpa)
        self.remove_widget(talpa)

    def on_mancate(self, instance, mancate):
        if self.mancate == 3:
            self.stop()

    def on_prese(self, instance, prese):
        if self.prese == 0:
            self.durata_talpa = AcchiappaLaTalpa.durata_talpa
            self.intervallo_talpe = AcchiappaLaTalpa.intervallo_talpe
        elif self.cambiare_frequenza():
            self.cambia_frequenza(self.rapporto_tempi)

    def cambiare_frequenza(self):
        return self.prese / self.numero_aumento * self.numero_aumento == self.prese

    def cambia_frequenza(self, rapporto):
        self.durata_talpa *= rapporto
        self.intervallo_talpe *= rapporto
        Clock.unschedule(self.talpa)
        Clock.schedule_interval(self.talpa, self.intervallo_talpe)

    def talpe(self):
        talpe = []
        for talpa in self.children:
            if talpa.id == "talpa":
                talpe.append(talpa)
        return talpe

    def stop(self):
        Clock.unschedule(self.talpa)
        for talpa in self.talpe():
            self.rimuovi_talpa(talpa)
        self.aggiungi_start()

    def vibra(self, tempo):
        animazione = Animation(x=self.width * 0.01, duration=tempo/8.0)
        animazione += Animation(x=0, duration=tempo*7/8.0, transition="out_elastic")
        animazione.start(self)
        try:
            vibrator.vibrate(tempo/3)
        except NotImplementedError:
            pass


class AcchiappaApp(App):
    def build(self):
        acchiappa = AcchiappaLaTalpa()
        acchiappa.aggiungi_start()
        return acchiappa


if __name__ == "__main__":
    AcchiappaApp().run()
