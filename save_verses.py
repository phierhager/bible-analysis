from nltk.stem import PorterStemmer
import os
import re

# Abbreviations for the books of the Bible
abbreviations = {
    "Gen": "Genesis",
    "Exod": "Exodus",
    "Lev": "Leviticus",
}

# Initialize stemmer
stemmer = PorterStemmer()


def read_bible(file_path="bible-esv.txt"):
    with open(file_path, "r") as f:
        return f.read()


# Save all verses containing the stemmed word
def save_verses(bible: str, word: str):
    # Ensure the output directory exists
    os.makedirs("verses", exist_ok=True)
    stemmed_word = stemmer.stem(word.lower())  # Stem the input word
    verses = []

    for verse in bible.split("\n"):
        verse_lower = verse.strip().lower()
        stemmed_verse = " ".join(
            stemmer.stem(w) for w in verse_lower.split()
        )  # Stem each word in the verse
        if (
            stemmed_word in stemmed_verse
        ):  # Check if the stemmed word is in the stemmed verse
            verses.append(verse)

    with open(f"verses/{word}.txt", "w") as f:
        f.write("\n".join(verses))


def reformat_bible():
    # if it does not have the pattern number:number in the line,
    # then it is a continuation of the previous verse
    # and we should append it to the previous verse
    with open("bible-esv.txt", "r") as f:
        lines = f.readlines()

    # lines = [
    #     "Deu 7:8 but it is because the LORD loves you and is keeping the oath that he swore to your fathers, that the",
    #     "LORD has brought you out with a mighty hand and redeemed you from the house of slavery, from the hand of",
    #     "Pharaoh king of Egypt.",
    #     "Deu 7:9 Know therefore that the LORD your God is God, the faithful God who keeps covenant and steadfast",
    #     "love with those who love him and keep his commandments, to a thousand generations,",
    #     "Deu 7:10 and repays to their face those who hate him, by destroying them. He will not be slack with one who",
    #     "hates him. He will repay him to his face.",
    # ]
    verses = []
    current_verse = ""
    for line in lines[2:]:
        if line.strip() == "":
            continue
        if re.search(r"\d+:\d+", line):  # New verse starts with number:number pattern
            if current_verse:
                verses.append(current_verse.strip())  # Save the previous verse
            current_verse = line.strip()
        else:
            current_verse += " " + line.strip()  # Continue the current verse

    if current_verse:
        verses.append(current_verse.strip())  # Add the last verse

    print(f"Reformatted {len(verses)} verses")
    with open("bible-esv-format.txt", "w") as f:
        f.write("\n".join(verses))


def txt_to_md(file_path):
    pass


if __name__ == "__main__":
    # reformat_bible()

    lines = open("bible-esv-format.txt").readlines()
    beginnings = [line[:3] for line in lines]
    beginnings.sort(key=lambda x: counts[x], reverse=True)
    number_of_books = 66
    print(beginnings[:number_of_books])

    # bible = read_bible("bible-esv-formatted.txt")
    # words = [
    #     "God",
    #     "Jesus",
    #     "love",
    #     "faith",
    #     "hope",
    #     "sin",
    #     "forgive",
    #     "salvation",
    #     "heaven",
    #     "hell",
    #     "bless",
    #     "prayer",
    #     "worship",
    #     "holy",
    #     "spirit",
    #     "baptize",
    #     "repent",
    #     "believe",
    # ]
    # for word in words:
    #     save_verses(bible, word)
