import re
import nltk
import argparse
import urllib.request
from typing import List
from bs4 import BeautifulSoup
from newspaper import Article
from collections import Counter


# Constants
MALE = "male"
FEMALE = "female"
UNKNOWN = "unknown"
BOTH = "both"

# Male Word Bank
MALE_WORDS = set(
    [
        "guy",
        "spokesman",
        "hero",
        "chairman",
        "men",
        "him",
        "he",
        "his",
        "boy",
        "boyfriend",
        "father",
        "brother",
        "brothers",
        "dad",
        "fiance",
        "dads",
        "fathers",
        "son",
        "sons",
        "uncle",
        "uncles",
        "waiter",
        "actor",
        "priest",
        "prince",
        "king",
        "widower",
        "gentleman",
        "gentlemen",
        "nephew",
        "grandfather",
        "husband",
        "boy",
        "boys",
        "man",
        "mr",
        "male",
    ]
)

# Female Word Bank
FEMALE_WORDS = set(
    [
        "girl",
        "spokeswoman",
        "heroine",
        "chairwoman",
        "her",
        "she",
        "hers",
        "lady",
        "girlfriend",
        "mother",
        "sister",
        "sisters",
        "mom",
        "fiancee",
        "moms",
        "mothers",
        "daughter",
        "daughters",
        "aunt",
        "aunts",
        "actress",
        "ladies",
        "princess",
        "queen",
        "widow",
        "wife",
        "wives",
        "mrs",
        "ms",
        "neice",
        "grandmother",
        "granddaughter",
        "grandma",
        "female",
        "woman",
    ]
)


def genderize(sentence: List[str]) -> str:
    """This function returns the gender association for a sentence."""
    mwlen = len(MALE_WORDS.intersection(sentence))
    fwlen = len(FEMALE_WORDS.intersection(sentence))
    result = UNKNOWN
    if mwlen > 0 and fwlen == 0:
        result = MALE
    elif mwlen == 0 and fwlen > 0:
        result = FEMALE
    elif mwlen > 0 and fwlen > 0:
        result = BOTH

    return result


def count_gender(sentences: List[List[str]]):
    """This function returns the gender association stats for a sentence."""
    sents = Counter()
    words = Counter()
    for sentence in sentences:
        gender = genderize(sentence)
        sents[gender] += 1
        words[gender] += len(sentence)

    return sents, words


def parse_gender(text: List[str]) -> None:
    """This function prints gender statistics to the terminal."""
    sentences = [
        [word.lower() for word in nltk.word_tokenize(sentence)] for sentence in text
    ]
    sents, words = count_gender(sentences)
    total = sum(words.values())
    for gender, count in words.items():
        pcent = 100 * count / total
        nsents = sents[gender]
        print("{0:.3f}% {1} ({2} sentences)".format(pcent, gender, nsents))

    return None


def clean_text(text: str) -> List[str]:
    """This function cleans a block of text extracted from BeautifulSoup."""
    regex = r"[^\w+\.\?\!\"]"
    text = re.sub(regex, " ", text)
    text = nltk.tokenize.sent_tokenize(text, "english")

    return text


def parse_article(url: str) -> None:
    """This function parses a url and computes the gender statistics."""
    # parse article: BeautifulSoup
    print("BeautifulSoup Results:")
    print("----------------------")
    fp = urllib.request.urlopen(url)
    mbytes = fp.read()
    html = mbytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(html, "lxml")
    text = clean_text(soup.text)
    parse_gender(text)

    # parse article: Article
    print("\nNewspaper3k Results:")
    print("--------------------")
    article = Article(args.url)
    article.download()
    article.parse()
    text = article.text
    text = clean_text(text)
    parse_gender(text)

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process article.")
    parser.add_argument("--url", type=str, help="Article URL.")
    args = parser.parse_args()
    parse_article(args.url)
