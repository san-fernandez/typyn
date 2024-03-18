import typer
import curses
from asciimatics.screen import Screen
from asciimatics.effects import BannerText
from asciimatics.renderers import FigletText
import time
from asciimatics.effects import Cycle, Stars, Print
from asciimatics.scene import Scene
from asciimatics.event import KeyboardEvent

# Función para la animación
def run_animation(screen, duration):
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time >= duration:
            break
        
        effects = [
            Cycle(
                screen,
                FigletText("TyPy", font='big'),
                int(screen.height / 2 - 4)),
            Stars(screen, 200),
            Print(screen,
                FigletText("Press space to start", font='small'),
                x=int(screen.width // 1),
                y=int(screen.height // 2 + 6),
                start_frame=50),
    ]
        screen.play(effects, stop_on_resize=False)
        screen.refresh()

# Función para el juego
def start_game(stdscr):
    # Configurar la ventana de curses
    stdscr.clear()

    # Duración de la animación en segundos
    animation_duration = 5

    # Ejecutar la animación
    run_animation(stdscr, animation_duration)

    # Aquí iría la lógica del juego

# Función principal
def main():
    typer.echo("Presiona la barra espaciadora para comenzar la animación y el juego.")

    # Iniciar la aplicación de curses
    curses.wrapper(start_game)

# Ejecutar la aplicación
if __name__ == "__main__":
    typer.run(main)
