import re
def is_pangram(sentence):
    cleaned_sentence = re.sub(r'[^a-zA-Z]', "", sentence)
    cleaned_sentence = cleaned_sentence.lower() #make everything lowercase to not worry about casing
    letter = set(cleaned_sentence)
    abc= set("abcdefghijklmnopqrstuvwxyz")
    return abc.issubset(letter)