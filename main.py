import re                                   # for regular expressions
import os                                   # to look up operating system-based info
import string                               # to do fancy things with strings
import glob                                 # to locate a specific file type
from pathlib import Path                    # to access files in other directories
import gensim                               # to access Word2Vec
from gensim.models import Word2Vec          # to access Gensim's flavor of Word2Vec
import pandas as pd   

dirpath = r'C:\Users\manas\Dropbox\My PC (LAPTOP-OEFAVRL0)\Downloads\ViralTexts-nineteenth-century-recipes-plaintext'
file_type = ".txt"
filenames = []
data = []

# this for loop will run through folders and subfolders looking for a specific file type
for root, dirs, files in os.walk(dirpath, topdown=False):
   # look through all the files in the given directory
   for name in files:
       if (root + os.sep + name).endswith(file_type):
           filenames.append(os.path.join(root, name))
   # look through all the directories
   for name in dirs:
       if (root + os.sep + name).endswith(file_type):
           filenames.append(os.path.join(root, name))

# this for loop then goes through the list of files, reads them, and then adds the text to a list
for filename in filenames:
    with open(filename) as afile:
        # print(filename)
        data.append(afile.read()) # read the file and then add it to the list
        afile.close() # close the file when you're done

print("d ", data[0:5])
        
def clean_text(text):
    # make text lowercase
    tokens = text.split()
    tokens = [t.lower() for t in tokens]

    # remove punctuation
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    tokens = [re_punc.sub('', token) for token in tokens]

    # remove numbers
    tokens = [token for token in tokens if token.isalpha()]
    return tokens

data_clean = []
for x in data:
    data_clean.append(clean_text(x))

# Confirm that number of clean texts is the same as original texts
print(len(data))
print(len(data_clean))

# Confirm the first cleaned text is the same as the first original text
print(data[0].split()[0])
print(data_clean[0][0])

# Confirm the last cleaned text is the same as the last original text
print(data[0].split()[-1])
print(data_clean[0][-1])

# print(data_clean[0:10])

model = Word2Vec(sentences=data_clean, window=5, min_count=3, epochs=5, sg=1)
model.save("atsbase.model")

# check if a word exists in our vocabulary
word = str(input("Enter word: "))

# if that word is in our vocabulary
if word in model.wv.key_to_index:
    print("The word %s is in your model vocabulary" % word)
else:
    print("%s is not in your model vocabulary" % word)

# returns a list with the top ten words used in similar contexts to the word "milk"
print(model.wv.most_similar(word, topn=10))