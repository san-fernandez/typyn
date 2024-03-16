'''

def select_random_words(path, count):

    with open(path, "r", encoding="utf-8") as file:
        word_list = file.read().splitlines()

    try:
        random_words = random.sample(word_list, count)
        return random_words
    except ValueError:
        print("there are not so many words bro calm down")

def select_random_quote(path):
    with open(file_path, "r", encoding="utf-8") as file:
        quotes = json.load(file)
    
    random_quote = random.choice(quotes)
    quote_text = random_quote["quote"]
    author = random_quote["author"]
    quote_length = random_quote["length"]
    
    return quote_text, author, quote_length

def calculate_wpm(words_written, time_elapsed):

    time_elapsed_minutes = time_elapsed / 60.0

    wpm = words_written / time_elapsed_minutes
    
    return wpm

def calculate_accuracy(total_key_presses, correct_key_presses):
    if total_key_presses == 0:
        return 0.0, 0
    
    accuracy = (correct_key_presses / total_key_presses) * 100.0
    return accuracy

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

'''