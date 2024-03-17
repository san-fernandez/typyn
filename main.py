import typer
import random
import yaspin
import inquirer
import json
import time
import pyfiglet
import os
import termcolor

VERSION = 1.0

DEFAULT_LANGUAGE = "english"
DEFAULT_WORDS = 20
DEFAULT_QUOTES = False
DEFAULT_TIME = 30
DEFAULT_SOUND = False

app = typer.Typer()

def select_random_words(path, count):

    with open(path, "r", encoding="utf-8") as file:
        word_list = file.read().splitlines()

    random_words = random.sample(word_list, count)

    return random_words

def select_random_quote(path):

    with open(path, "r", encoding="utf-8") as file:
        quotes = json.load(file)
    
    random_quote = random.choice(quotes)
    quote_text = random_quote["quote"]
    author = random_quote["author"]
    quote_length = len(quote_text)
    
    return quote_text, author, quote_length

def calculate_wpm(start_time: float, end_time: float, word_count: int) -> float:

    elapsed_time = end_time - start_time
    minutes = elapsed_time / 60 
    wpm = word_count / minutes

    return wpm

def calculate_accuracy(correct_letters: int, total_letters: int) -> float:

    if total_letters == 0:
        return 0.0
    
    accuracy = (correct_letters / total_letters) * 100

    return accuracy

def clear_console():

    if os.name == "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")

@app.command()
def typy(quotes: bool = typer.Option(DEFAULT_QUOTES, "-quotes", help="Select quotes instead of words"),
         sound: bool = typer.Option(DEFAULT_SOUND, "-sound", help="Turn on music and sound effects"),
         language: str = typer.Option(DEFAULT_LANGUAGE, "-lang", help="Language to use"),
         words: int = typer.Option(DEFAULT_WORDS, "-words", help="Number of words"),
         time: int = typer.Option(DEFAULT_TIME, "-time", help="Define time (seconds)")):
    
    if language.lower() not in ["english", "español"]:
        typer.echo("Invalid language! Please choose 'english' or 'español'.")
        raise typer.Abort()
    
    typer.echo(f"Selected language: {language}")
    typer.echo(f"Selected word count: {words}")

    if quotes:
        text, author, length = select_random_quote(f"quotes/{language}.json")
        typer.echo("Selected mode: Quotes")
        typer.echo(text)
        typer.echo(author)
        typer.echo(length)
    
    else:
        text = select_random_words(f"words/{language[0:2]}-1000", words)
        typer.echo(' '.join(text))

    clear_console()

    correct_letters = 0
    total_letters = len(text)
    word_count = 1  

    #start_time = time.time()

    # game

    #end_time = time.time()

    #wpm = calculate_wpm(start_time, end_time, word_count)
    #accuracy = calculate_accuracy(correct_letters, total_letters)

    #typer.echo(f"Your WPM: {wpm:.2f}")
    #typer.echo(f"Your accuracy: {accuracy:.2f}%")
    
@app.command()
def help():
    
    clear_console()
    help_text = pyfiglet.figlet_format("HELP", font="slant")

    typer.echo("\n")
    typer.echo(help_text)
    typer.echo("Welcome to TyPy, a terminal-based typing game developed with Python.")
    typer.echo("\nVERSION:")
    typer.echo(f"  typy {VERSION}")
    typer.echo("\nUSAGE:")
    typer.echo("  typy.exe [OPTIONS] COMMAND [ARGS]")
    typer.echo("\nOPTIONS:")
    typer.echo("  --install-completion          Install completion for the current shell.")
    typer.echo("  --show-completion             Show completion for the current shell, to copy it or customize the installation.")
    typer.echo("\nCOMMANDS:")
    typer.echo("  --lang TEXT                   Select the language of the game (e.g., 'english', 'spanish').")
    typer.echo("  --words INTEGER               Define the number of words for the game.")
    typer.echo("  --time INTEGER                Specify amount of time you want to play.")
    typer.echo("  --quotes BOOL                 Play with quotes instead of words.")
    typer.echo("  --sound BOOL                  Activate background music during the game.")
    typer.echo("\nARGS:")
    typer.echo("  <values>")
    typer.echo("\n")

    time.sleep(1.5)

if __name__ == "__main__":
    app()