import re
from datetime import datetime

# -------------------------
# Word Maps
# -------------------------
NUM_WORDS = {
    "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,
    "ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,
    "sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,
    "twenty":20,"thirty":30,"forty":40,"fifty":50
}

ORDINALS = {
    "first":1,"second":2,"third":3,"fourth":4,"fifth":5,"sixth":6,"seventh":7,
    "eighth":8,"ninth":9,"tenth":10,"eleventh":11,"twelfth":12,"thirteenth":13,
    "fourteenth":14,"fifteenth":15,"sixteenth":16,"seventeenth":17,"eighteenth":18,
    "nineteenth":19,"twentieth":20,"thirtieth":30
}

MONTHS = {
    "january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
    "july":7,"august":8,"september":9,"october":10,"november":11,"december":12
}

def words_to_digits(words):
    digits = []
    for w in words:
        if w in NUM_WORDS and NUM_WORDS[w] < 10:
            digits.append(str(NUM_WORDS[w]))
    return int("".join(digits)) if digits else None


def extract_year(text):
    match = re.search(r"twenty\s+twenty(?:\s+\w+)?", text)
    if not match:
        return None

    parts = match.group().split()

    if len(parts) == 2:
        return 2020

    last_word = parts[-1]
    if last_word in NUM_WORDS:
        return 2000 + 20 + NUM_WORDS[last_word]

    return None

def extract_date(text):
    month_word = next((m for m in MONTHS if m in text), None)
    if not month_word:
        return None

    day = None
    for word, num in ORDINALS.items():
        if word in text:
            day = num
            break

    year = extract_year(text)

    if month_word and day and year:
        return datetime(year, MONTHS[month_word], day).strftime("%Y-%m-%d")

    return None


def extract_location(text):
    text = text.lower()
    match = re.search(r"(?:location\s+)?pantry\s+([a-z]+)", text)
    if not match:
        return None

    word = match.group(1) 
    if word in NUM_WORDS:
        return f"pantry {NUM_WORDS[word]}"
    return f"pantry {word}"


def extract_quantity_and_item(chunk):
    words = chunk.lower().split()

    if "expires" not in words:
        return None, None

    exp_index = words.index("expires")

    qty_index = None
    for i in range(exp_index - 1, -1, -1):
        if words[i] in NUM_WORDS:
            qty_index = i
            break

    if qty_index is None:
        return None, None

    quantity = NUM_WORDS[words[qty_index]]

    item_words = words[qty_index + 1:exp_index]

    noise = {"uh", "a", "the", "okay", "gonna", "know", "it's"}
    item_words = [w for w in item_words if w not in noise]

    item = " ".join(item_words).strip()
    return quantity, item if item else None


def parse_pantry_speech(text):
    text = text.lower()
    text = text.replace("apple's", "apples").replace("banana's", "bananas")

    results = []

    # split by expire, all items have this... skips first entry idk why 
    chunks = re.split(r"\bexpires?\b", text)

    for chunk in chunks:
        if not chunk.strip():
            continue

        
        quantity, item = extract_quantity_and_item(chunk + " expires")

        date = extract_date(chunk + " expires")  # expires
        location = extract_location(chunk + " location")  # location 

        if quantity and item and date and location:
            results.append({
                "quantity": quantity,
                "item": item,
                "date": date,
                "location": location
            })

    return results


# testing 
if __name__ == "__main__":
    speech = """
    five bananas expires february fifth twenty twenty six location pantry six
    two apples expires february twenty fifth twenty twenty six location pantry nine
    one milk expires february fifth twenty twenty nine location pantry one
    """

    from pprint import pprint
    pprint(parse_pantry_speech(speech))