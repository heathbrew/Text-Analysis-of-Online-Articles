import pandas as pd
from textblob import TextBlob
import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import os
import csv
def analyze_text(file_path):
    # Read text from file
    with open(file_path, 'r') as f:
        text = f.read()

    # Create a TextBlob object
    blob = TextBlob(text)

    # Generate sentiment scores
    positive_score = round(blob.sentiment.polarity,2)
    negative_score = round(1- positive_score,2)
    polarity_score = round(blob.sentiment.polarity,2)
    subjectivity_score = round(blob.sentiment.subjectivity,2)

    # Generate average sentence length
    try :
        avg_sentence_length = round(sum(len(sentence.words) for sentence in blob.sentences) / len(blob.sentences),2)
    except ZeroDivisionError:
        avg_sentence_length = 0
    
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
        try :
            return round(0.4 * ( (len(words) / len(nltk.sent_tokenize(text))) + (100 * (complex_words / len(words))) ),2)
        except ZeroDivisionError:
            return 0


    fog = fog_index(words)
    
    # Generate average number of words per sentence
    try:
        avg_num_words_per_sentence = round(len(words) / len(nltk.sent_tokenize(text)),2)
    except ZeroDivisionError:
            avg_num_words_per_sentence = 0  
    
    # Generate word count
    word_count = len(words)
    
    # Generate syllable per word
    try :
        syllable_per_word = round(sum(nsyl(word) for word in words) / word_count,2)
    except ZeroDivisionError:
        syllable_per_word = 0
    
    # Generate personal pronouns
    personal_pronouns = sum(1 for word, pos in pos_tag(words) if pos == 'PRP')
    
    # Generate average word length
    try:
        avg_word_length = round(sum(len(word) for word in words) / word_count,2)
    except ZeroDivisionError:
        avg_word_length = 0
    
    #Generate percentage of complex words
    try:
        per_complex_words = round(((complex_word_count/word_count)*100),2)
    except ZeroDivisionError:
        per_complex_words = 0
    
    # Create a dataframe to store the scores
    # scores = pd.DataFrame({'POSITIVE SCORE' : [positive_score],
    #                        'NEGATIVE SCORE' : [negative_score],
    #                        'POLARITY SCORE' : [polarity_score],
    #                        'SUBJECTIVITY SCORE' : [subjectivity_score],
    #                        'AVG SENTENCE LENGTH' : [avg_sentence_length],
    #                        'PERCENTAGE OF COMPLEX WORDS' : [per_complex_words],
    #                        'FOG INDEX' : [fog],
    #                        'AVG NUMBER OF WORDS PER SENTENCE' : [avg_num_words_per_sentence],
    #                        'COMPLEX WORD COUNT' : [complex_word_count],
    #                        'WORD COUNT' : [word_count],
    #                        'SYLLABLE PER WORD' : [syllable_per_word],
    #                        'PERSONAL PRONOUNS' : [personal_pronouns],
    #                        'AVG WORD LENGTH' : [avg_word_length]})
    scores = {'POSITIVE SCORE' : positive_score,
                           'NEGATIVE SCORE' : negative_score,
                           'POLARITY SCORE' : polarity_score,
                           'SUBJECTIVITY SCORE' : subjectivity_score,
                           'AVG SENTENCE LENGTH' : avg_sentence_length,
                           'PERCENTAGE OF COMPLEX WORDS' : per_complex_words,
                           'FOG INDEX' : fog,
                           'AVG NUMBER OF WORDS PER SENTENCE' : avg_num_words_per_sentence,
                           'COMPLEX WORD COUNT' : complex_word_count,
                           'WORD COUNT' : word_count,
                           'SYLLABLE PER WORD' : syllable_per_word,
                           'PERSONAL PRONOUNS' : personal_pronouns,
                           'AVG WORD LENGTH' : avg_word_length}
    return scores

# Create an empty dataframe
scores = pd.DataFrame(columns=['POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE',
                               'SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS',
                               'FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT', 'WORD COUNT',
                               'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])

def get_text_files(directory):
    text_files = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            text_files.append(file)
    text_files_list = text_files[51:144] + text_files[0:51]
    return text_files_list
# print(get_text_files("extract"))

# print(f'extract/{get_text_files("extract")[0]}')
# print(f'extract/{get_text_files("extract")[0]}.txt')

for i in range(len(get_text_files("extract"))):
    path = f'extract/{get_text_files("extract")[i]}'
    with open(path, 'r') as f:
        analysis = analyze_text(path)
        # print(analysis)
        scores = scores.append(analysis, ignore_index=True)
        print(scores)


scores.to_excel("scores.xlsx", sheet_name='Sheet1')
# Read the existing Excel file
existing_df = pd.read_excel('Output Data.xlsx')

# Concatenate the existing dataframe with the new one containing the scores
result_df = pd.concat([existing_df, scores], axis=1)

# Save the resulting dataframe to an Excel file
result_df.to_excel('Output Data Structure.xlsx', index=False)

    
    
