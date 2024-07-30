from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText, SpeechBubble
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.particles import  ShootScreen

def intro(screen):

    scenes = []

    effects = [
        Cycle(
            screen,
            FigletText("TyPyn", font='big'),
            int(screen.height / 2 - 4)),
        Stars(screen, 200),
        Cycle(screen,
              SpeechBubble("Press space bar to play"),
              screen.height - 3,
              #transparent=False,
              start_frame=10),
    ]

    scenes.append(Scene(effects, 0, clear=True))

    effects = [
        ShootScreen(screen, screen.width // 2, screen.height // 2, 100),
    ]

    scenes.append(Scene(effects, 10, clear=False))

    screen.play(scenes, stop_on_resize=False, repeat=False )

if __name__ == "__main__":
    Screen.wrapper(intro)
 