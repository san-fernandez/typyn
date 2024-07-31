import typer
import random
import curses
import time
import os
import json
import pkg_resources
import toml
import pyfiglet
import asciichartpy
from asciimatics.screen import Screen
from typyn.resources.intro_animation import intro

VERSION = '1.0.17'
ALL_LANGUAGES = [{"name": "English", "flag": "🇬🇧"}, {"name": "Spanish", "flag": "🇪🇸"}]

DEFAULT_LANGUAGE = 'english'
DEFAULT_WORDS = 15
DEFAULT_TIME = 40
DEFAULT_QUOTES = False
DEFAULT_SAVE = True

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

def calculate_stats(text, text_input, start_time, end_time):

	word_count = 0
	correct_letters = 0
	total_letters = len(text)
	current_streak = 0
	max_streak = 0
		
	# all this crap to transform the text
	text_list = text.split()
	joined_text_input = ''.join(text_input)
	words_text_input = joined_text_input.split()

	for original_word, user_word in zip(text_list, words_text_input):
		if original_word == user_word:
			word_count += 1

	wpm = calculate_wpm(start_time, end_time, word_count)

	for i in range(min(len(text), len(text_input))):
		if text[i] == text_input[i]:
			correct_letters += 1
			current_streak += 1
			if current_streak > max_streak:
				max_streak = current_streak
		else:
			current_streak = 0

	accuracy = calculate_accuracy(correct_letters, total_letters)
	incorrect_letters = total_letters - correct_letters

	return wpm, accuracy, total_letters, correct_letters, incorrect_letters, max_streak

def clear_console():

	if os.name == "posix":
		_ = os.system("clear")
	else:
		_ = os.system("cls")

def display_text(stdscr, target, current, wpm=0):

	stdscr.addstr(target)

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)

def save_game_data(wpm, accuracy):

	if DEFAULT_SAVE:
		local_time = time.localtime()
	
		game_data = {
			"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", local_time),
			"wpm": wpm,
			"accuracy": accuracy
		}

		user_path = pkg_resources.resource_filename(__name__, f"user_data/player_data.json") 
		with open(user_path, 'a') as json_file:
			json.dump(game_data, json_file)
			json_file.write('\n')

def print_game_statistics(wpm, accuracy, total_chars, correct_chars, incorrect_chars, max_streak):

	title = pyfiglet.figlet_format("Game Statistics")

	print(title)

	time.sleep(0.4)

	print("-" * 56)

	time.sleep(0.4)

	print("WPM:                {:<10}".format(round(wpm, 1)))
	time.sleep(0.2)
	print("Accuracy:           {:<3}%".format(round(accuracy, 1)))
	time.sleep(0.2)
	print("Total Char:         {:<10}".format(total_chars))
	time.sleep(0.2)
	print("Correct Char:       {:<10}".format(correct_chars))
	time.sleep(0.2)
	print("Incorrect Char:     {:<10}".format(incorrect_chars))
	time.sleep(0.2)
	print("Max Streak:         {:<10}".format(max_streak))

	time.sleep(0.4)

	print("-" * 56)

def plot_statistics():

	timestamps = []
	wpms = []
	accuracies = []

	user_path = pkg_resources.resource_filename(__name__, f"user_data/player_data.json") 

	with open(user_path, 'r') as json_file:
		for line in json_file:
			game_data = json.loads(line)
			timestamps.append(game_data["timestamp"])
			wpms.append(game_data["wpm"])
			accuracies.append(game_data["accuracy"])

	time.sleep(0.7)		

	print("\nWPM (historical data):")
	print(asciichartpy.plot(wpms, {'height': 10}))

	time.sleep(0.7)

	print("\nAccuracy (historical data):")
	print(asciichartpy.plot(accuracies, {'height': 10}))	

	print("-" * 56)

def game(stdscr, text):

	curses.curs_set(0)
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) 

	target_text = text
	current_text = []

	start_time = time.time()

	while True:

		stdscr.clear()
		display_text(stdscr, target_text, current_text)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 10:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)
		else:
			stdscr.clear()
			break

	return current_text

@app.command()
def run(language: str = typer.Option(DEFAULT_LANGUAGE, "--lang", help="Language to use"),
		 words: int = typer.Option(DEFAULT_WORDS, "--words", help="Number of words"),
		 timer: int = typer.Option(DEFAULT_TIME, "--time", help="Define time (seconds)"),
		 quotes: bool = typer.Option(DEFAULT_QUOTES, "--quotes", help="Select quotes instead of words"),
		 save: bool = typer.Option(DEFAULT_SAVE, "--save", help="Choose if you want to save your stats")):
	
	if language.lower() not in ["english", "español"]:
		typer.echo("Invalid language! Please choose 'english' or 'español'.")
		raise typer.Abort()

	if quotes:
		data_path = pkg_resources.resource_filename(__name__, f"data/quotes/{language}.json")
		text, author, length = select_random_quote(data_path)

	else:
		data_path = pkg_resources.resource_filename(__name__, f"data/words/{language[0:2]}-1000.txt")
		text = select_random_words(data_path, words)
		text = ' '.join(text)

	clear_console()

	Screen.wrapper(intro)

	start_time = time.time()
	text_input = curses.wrapper(game, text)
	end_time = time.time()

	wpm, accuracy, total_letters, correct_letters, incorrect_letters, max_streak = calculate_stats(text, text_input, start_time, end_time)

	save_game_data(wpm, accuracy)

	time.sleep(0.5)

	print_game_statistics(wpm, accuracy, total_letters, correct_letters, incorrect_letters, max_streak)
	plot_statistics()

	typer.echo("\nThe game has finished. Press 'q' to quit or 'r' to restart")
	while True:
		key = typer.getchar()
		if key == "q":
			break
		elif key == "r":
			clear_console()
			start_time = time.time()
			text_input = []
			text_input = curses.wrapper(game, text)
			end_time = time.time()
			wpm, accuracy, total_letters, correct_letters, incorrect_letters, max_streak = calculate_stats(text, text_input, start_time, end_time)
			save_game_data(wpm, accuracy)
			print_game_statistics(wpm, accuracy, total_letters, correct_letters, incorrect_letters, max_streak)
			plot_statistics()
			typer.echo("\nThe game has finished. Press 'q' to quit or 'r' to restart")
		else:
			typer.echo("Invalid key. Press 'q' to quit or 'r' to restart.")

@app.command()
def help():
	
	clear_console()
	help_text = pyfiglet.figlet_format("HELP", font="slant")

	typer.echo("\n")
	typer.echo(help_text)
	typer.echo(f"Welcome to TyPyn, a terminal-based typing game developed with Python.")
	typer.echo("\nUSAGE:")
	typer.echo("    typyn [OPTIONS] COMMAND [ARGS]")
	typer.echo("\nOPTIONS:")
	typer.echo("    run                         Run the game.")
	typer.echo("    version                     Check current version of TyPyn.")
	typer.echo("    show-languages              Show all the available languages.")
	typer.echo("    delete-saves                Delete all your saves.")
	typer.echo("  --install-completion          Install completion for the current shell.")
	typer.echo("  --show-completion             Show completion for the current shell, to copy it or customize the installation.")
	typer.echo("\nCOMMANDS:")
	typer.echo("  --lang TEXT                   Select the language of the game (e.g., 'english', 'spanish').")
	typer.echo("  --words INTEGER               Define the number of words for the game.")
	typer.echo("  --timer INTEGER               Specify amount of time you want to play.")
	typer.echo("  --quotes BOOL                 Play with quotes instead of words.")
	typer.echo("  --save BOOL                   Choose if you want to save your statistics locally in your computer.")
	typer.echo("\nARGS:")
	typer.echo("  <values>")
	typer.echo("\n")

	time.sleep(1.5)

@app.command()
def version(version : bool = typer.Option(None, "--version", "--v", help="Check current version")):

	clear_console()
	typy_text = pyfiglet.figlet_format(f"TyPyn {VERSION}", font="larry3d")

	typer.echo(f"{typy_text}")

	time.sleep(1.5)

@app.command()
def show_languages(show_languages: bool = typer.Option(None, "--show-languages", "--showl", help="Show all the available languages")):

	clear_console()
	typer.echo("╔════════════════════════════════════╗")
	typer.echo("║        Available Languages         ║")
	typer.echo("╚════════════════════════════════════╝")

	for language in ALL_LANGUAGES:
		time.sleep(0.7)
		typer.echo(f"║  {language['flag']} {language['name'].ljust(16)}" + " "*(20 - len(language['name'])) + "║")

	typer.echo(' ' + "═"*36)
	
@app.command()
def delete_saves():
	
	try:
		confirmation = input("Are you sure you want to delete all your historical data? (yes/no): ").lower()
		if confirmation == "yes":
				# Open the JSON file in write mode to truncate the content
				user_path = pkg_resources.resource_filename(__name__, f"user_data/player_data.json") 
				with open(user_path, 'w') as json_file:
					json_file.truncate(0)  # Truncate the file content
				print("All historical data has been deleted.")
		else:
			print("Operation canceled. No data was deleted.")

	except FileNotFoundError:
		print("The historical data file does not exist.")

if __name__ == "__main__":
	app()