import pandas as pd
from textblob import TextBlob
import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def analyze_text(file_path):
    # Read text from file
    with open(file_path, 'r') as f:
        text = f.read()

    # Create a TextBlob object
    blob = TextBlob(text)

    # Generate sentiment scores
    positive_score = blob.sentiment.polarity
    negative_score = 1- positive_score
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity

    # Generate average sentence length
    avg_sentence_length = sum(len(sentence.words) for sentence in blob.sentences) / len(blob.sentences)
    
    # Tokenize the text
    words = word_tokenize(text)

    # Generate complex word count
    d = cmudict.dict()
    def nsyl(word):
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
        except KeyError:
            # Handle the case where the word is not in the dictionary
            return 0
    
    complex_word_count = sum(1 for word in words if nsyl(word) >= 3)
    
     # Generate FOG index
    def fog_index(words):
        complex_words = 0
        for word in words:
            if len(word) >= 3:
                if any(c.isalpha() and c.isupper() for c in word):
                    complex_words += 1
        return 0.4 * ( (len(words) / len(nltk.sent_tokenize(text))) + (100 * (complex_words / len(words))) )

    fog = fog_index(words)
    
    # Generate average number of words per sentence
    avg_num_words_per_sentence = len(words) / len(nltk.sent_tokenize(text))
    
    # Generate word count
    word_count = len(words)
    
    # Generate syllable per word
    syllable_per_word = sum(nsyl(word) for word in words) / word_count
    
    # Generate personal pronouns
    personal_pronouns = sum(1 for word, pos in pos_tag(words) if pos == 'PRP')
    
    # Generate average word length
    avg_word_length = sum(len(word) for word in words) / word_count
    
    #Generate percentage of complex words
    per_complex_words = round(((complex_word_count/word_count)*100),2)
    
    # Create a dataframe to store the scores
    scores = pd.DataFrame({'POSITIVE SCORE' : [positive_score],
                           'NEGATIVE SCORE' : [negative_score],
                           'POLARITY SCORE' : [polarity_score],
                           'SUBJECTIVITY SCORE' : [subjectivity_score],
                           'AVG SENTENCE LENGTH' : [avg_sentence_length],
                           'PERCENTAGE OF COMPLEX WORDS' : [per_complex_words],
                           'FOG INDEX' : [fog],
                           'AVG NUMBER OF WORDS PER SENTENCE' : [avg_num_words_per_sentence],
                           'COMPLEX WORD COUNT' : [complex_word_count],
                           'WORD COUNT' : [word_count],
                           'SYLLABLE PER WORD' : [syllable_per_word],
                           'PERSONAL PRONOUNS' : [personal_pronouns],
                           'AVG WORD LENGTH' : [avg_word_length]})

    return scores

print(analyze_text("extract\\130.txt"))

    
    
