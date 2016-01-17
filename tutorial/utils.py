from kivy.core.window import Window


class KeyHandler(object):
    def __init__(self, **kwargs):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'escape':
            keyboard.release()
        return True


class PrintScreenshoot(KeyHandler):
    widget = None
    screenshotname = "screenshot.png"

    def __init__(self, widget, screenshotname=None, **kwargs):
        super(PrintScreenshoot, self).__init__(**kwargs)
        self.widget = widget
        if screenshotname is not None:
            self.screenshotname = screenshotname

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Per stampare le schermate
        if text == "p" and self.widget is not None:
            self.widget.export_to_png(self.screenshotname)
        return super(PrintScreenshoot, self)._on_keyboard_down(keyboard, keycode, text, modifiers)