import random
import argparse
import requests

#python text-gen.py -c lorem -p 3 -w 50
#python text-gen.py -c finance -rp -p 3 -w 50

BASE_API_URL = "https://api.datamuse.com/words?ml={}"  # Dynamic API request

LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do", "eiusmod", 
    "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua", "ut", "enim", "ad", "minim", 
    "veniam", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", 
    "commodo", "consequat", "duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", 
    "esse", "cillum", "dolore", "eu", "fugiat", "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", 
    "adipiscing", "elit", "Pellentesque", "sit", "amet", "maximus", "eros", "Cras", "at", "libero", "orci", 
    "Fusce", "volutpat", "rutrum", "orci", "eget", "ultrices", "Phasellus", "blandit", "quis", "est", "in", 
    "placerat", "In", "hac", "habitasse", "platea", "dictumst", "Morbi", "eros", "nisl", "sodales", "vitae", 
    "tincidunt", "non", "sollicitudin", "sit", "amet", "sapien", "Donec", "eget", "convallis", "lectus", "Etiam", 
    "posuere", "ligula", "in", "fermentum", "luctus", "Maecenas", "ut", "velit", "elementum", "mi", "molestie", 
    "semper", "Aliquam", "sed", "velit", "ac", "sapien", "semper", "fermentum", "Nulla", "placerat", "massa", "eu", 
    "sagittis", "imperdiet", "Donec", "bibendum", "sodales", "justo", "Fusce", "facilisis", "vestibulum", "est", 
    "pulvinar", "placerat", "Sed", "fringilla", "sem", "ex", "vulputate", "sollicitudin", "velit", "ultricies", 
    "vel", "Pellentesque", "quis", "purus", "risus", "Aliquam", "erat", "volutpat", "Orci", "varius", "natoque", 
    "penatibus", "et", "magnis", "dis", "parturient", "montes", "nascetur", "ridiculus", "mus", "Maecenas", 
    "vulputate", "tortor", "ac", "mollis", "dictum", "Curabitur", "commodo", "libero", "vel", "risus", "posuere", 
    "maximus", "Praesent", "libero", "metus", "tristique", "at", "diam", "a", "sodales", "fermentum", "lectus", 
    "Mauris", "mattis", "a", "lectus", "sed", "tincidunt", "Pellentesque", "tincidunt", "vestibulum", "porttitor", 
    "Aliquam", "erat", "volutpat", "Nam", "non", "sem", "erat", "Duis", "sed", "volutpat", "felis", "Sed", 
    "viverra", "lobortis", "volutpat", "Mauris", "ut", "enim", "at", "eros", "tristique", "mattis", "Cras", 
    "tellus", "sapien", "aliquam", "ac", "nulla", "quis", "vestibulum", "placerat", "eros", "Ut", "ultricies", 
    "suscipit", "ligula", "et", "sodales", "ligula", "rutrum", "lobortis", "Aenean", "iaculis", "ligula", "sit", 
    "amet", "rhoncus", "commodo", "nunc", "metus", "tempus", "sem", "id", "fringilla", "lorem", "felis", "at", 
    "elit", "Etiam", "interdum", "vestibulum", "orci", "in", "mattis", "Proin", "sem", "nisi", "vestibulum", "vel", 
    "rutrum", "et", "varius", "ut", "urna", "Suspendisse", "potenti", "Praesent", "volutpat", "nisi", "id", 
    "condimentum", "dignissim", "Suspendisse", "ac", "dui", "risus", "Phasellus", "sit", "amet", "sodales", 
    "ligula", "Suspendisse", "aliquam", "urna", "metus", "ut", "luctus", "felis", "aliquet", "et", "In", "hac", 
    "habitasse", "platea", "dictumst", "Curabitur", "vel", "tellus", "sodales", "tincidunt", "lorem", "ac", 
    "iaculis", "mauris", "Class", "aptent", "taciti", "sociosqu", "ad", "litora", "torquent", "per", "conubia", 
    "nostra", "per", "inceptos", "himenaeos", "Class", "aptent", "taciti", "sociosqu", "ad", "litora", "torquent", 
    "per", "conubia", "nostra", "per", "inceptos", "himenaeos", "Vivamus", "mollis", "libero", "ut", "imperdiet", 
    "bibendum", "Etiam", "nec", "aliquet", "nibh", "Aenean", "ultricies", "sapien", "et"
]


def fetch_words_from_api(category, count):
    if category == "lorem":
        return [f"{LOREM_WORDS[i]} {LOREM_WORDS[i+1]}" for i in range(0, min(len(LOREM_WORDS)-1, count * 2), 2)]
    try:
        response = requests.get(BASE_API_URL.format(category))
        response.raise_for_status()
        words = [item['word'] for item in response.json()]
        random.shuffle(words)  # Shuffle to ensure different words each time
        paired_words = [f"{words[i]} {words[i+1]}" for i in range(0, min(len(words)-1, count * 2), 2)]
        return paired_words[:count]  # Return only the required number of pairs
    except requests.exceptions.RequestException:
        print("Error fetching words from API.")
    return []

def generate_words(category=None, count=1):
    """Generate random words based on category."""
    words = fetch_words_from_api(category, count)
    return words if words else ["No words available"]

def generate_randomized_paragraphs(category, num_paragraphs, words_per_paragraph):
    """Generate paragraphs where the words are randomized within the selected category."""
    paragraphs = []
    for _ in range(num_paragraphs):
        words = generate_words(category, words_per_paragraph)
        random.shuffle(words)  # Shuffle words for randomization
        if words:
            words[0] = words[0].capitalize()  # Capitalize first word
        paragraph = " ".join(words) + "."  # Add period at the end
        paragraphs.append(paragraph)
    return "\n\n".join(paragraphs)

def main():
    parser = argparse.ArgumentParser(description="Generate random words and paragraphs with optional categories.")
    parser.add_argument("-c", "--category", type=str, help="Category of words")
    parser.add_argument("-n", "--number", type=int, default=1, help="Number of word pairs to generate")
    parser.add_argument("-p", "--paragraphs", type=int, help="Number of paragraphs to generate")
    parser.add_argument("-w", "--words_per_paragraph", type=int, help="Number of words per paragraph")
    parser.add_argument("-rp", "--random_paragraphs", action="store_true", help="Generate randomized paragraphs within the chosen category")
    
    args = parser.parse_args()
    
    if args.random_paragraphs and args.paragraphs and args.words_per_paragraph:
        print(generate_randomized_paragraphs(args.category, args.paragraphs, args.words_per_paragraph))
    elif args.paragraphs and args.words_per_paragraph:
        print(generate_randomized_paragraphs(args.category, args.paragraphs, args.words_per_paragraph))
    else:
        words = generate_words(category=args.category, count=args.number)
        print("\n".join(words))

if __name__ == "__main__":
    main()


