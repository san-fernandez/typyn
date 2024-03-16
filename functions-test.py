import random
import pyfiglet
import json

#############################################

def select_random_words(path, count):

    with open(path, "r", encoding="utf-8") as file:
        word_list = file.read().splitlines()

    try:
        random_words = random.sample(word_list, count)
        return random_words
    except ValueError:
        print("there are not so many words bro calm down")

path = "words/en-1000"
count = 50
selected_words = select_random_words(path, count)

print(selected_words)

path = "words/es-1000"
count = 1001
selected_words = select_random_words(path, count)

print(selected_words)

#############################################

def select_random_quote(path):
    with open(file_path, "r", encoding="utf-8") as file:
        quotes = json.load(file)
    
    random_quote = random.choice(quotes)
    quote_text = random_quote["quote"]
    author = random_quote["author"]
    quote_length = random_quote["length"]
    
    return quote_text, author, quote_length

# Example usage:
file_path = "quotes/english.json"
quote, author, length = select_random_quote(file_path)
print("Quote:", quote)
print("Author:", author)
print("Length:", length)

#############################################

def display_player_stats_ascii(stats):
    """
    Displays the player's statistics in ASCII art style using PyFiglet.
    
    Args:
    stats (dict): Dictionary containing the player's statistics.
    """
    # Convert statistics into ASCII art
    WPM_ascii = pyfiglet.figlet_format(str(stats["WPM"]), font="slant")
    accuracy_ascii = pyfiglet.figlet_format(str(stats["accuracy"]) + "%", font="slant")
    total_score_ascii = pyfiglet.figlet_format(str(stats["total_score"]), font="slant")
    
    # Display the statistics
    print("Words Per Minute (WPM):")
    print(WPM_ascii)
    print("Accuracy:")
    print(accuracy_ascii)
    print("Total Score:")
    print(total_score_ascii)

# Example usage:
player_stats = {
    "WPM": 55,
    "accuracy": 90,
    "total_score": 1500
}
display_player_stats_ascii(player_stats)

#############################################

def calculate_wpm(words_written, time_elapsed):

    time_elapsed_minutes = time_elapsed / 60.0

    wpm = words_written / time_elapsed_minutes
    
    return wpm

# Ejemplo de uso:
words_written = 10  # Por ejemplo, la cantidad de palabras escritas por el usuario
time_elapsed = 10  # Por ejemplo, el tiempo transcurrido en segundos
wpm = calculate_wpm(words_written, time_elapsed)
print("Words per minute (WPM):", wpm)

#############################################

def calculate_accuracy(total_key_presses, correct_key_presses):
    if total_key_presses == 0:
        return 0.0, 0
    
    accuracy = (correct_key_presses / total_key_presses) * 100.0
    return accuracy

# Example usage:
total_key_presses = 100  # For example, total number of key presses
correct_key_presses = 25  # For example, number of correct key presses
incorrect_key_presses = total_key_presses - correct_key_presses # For example, number of incorrect key presses
accuracy = calculate_accuracy(total_key_presses, correct_key_presses)
print("Accuracy:", accuracy, "%")
print("Correct Presses:", correct_key_presses)
print("Incorrect Presses:", incorrect_key_presses)

#############################################