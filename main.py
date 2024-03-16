import typer
import random
import yaspin
import inquirer

app = typer.Typer()

def select_random_words(path, count):

    with open(path, "r", encoding="utf-8") as file:
        word_list = file.read().splitlines()

    random_words = random.sample(word_list, count)
    return random_words


@app.command()
def welcome():
    
    questions = [inquirer.List('language', message="choose language:", choices=["english", "español"]),
    inquirer.Text("word_count", message="Enter number of words", validate=lambda _, x: int(x) > 0),]

    answers = inquirer.prompt(questions)

    language = answers["language"]

    word_count = int(answers["word_count"])
    words = select_random_words(f"words/{language[0:2].lower()}-1000", word_count)

    typer.echo(" ".join(words))

if __name__ == "__main__":
    app()