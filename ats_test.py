from gensim.models import Word2Vec          # to access Gensim's flavor of Word2Vec 

def is_similar(phrase, phrase2):
    sum = 0
    for tuple in model.wv.most_similar(phrase, topn=10):
        sum += tuple[1]
    avg_top_sim = sum / len(model.wv.most_similar(phrase,topn=10))

    sim = model.wv.similarity(phrase, phrase2)

    # checks if difference between similarity of the two words and the similarity of the most similar words is minimal
    if abs(avg_top_sim-sim) < 0.2:
        return True
    else:
        return False
    
model = Word2Vec.load("atstweaked2.model")

# check if a word exists in our vocabulary
word = str(input("Enter word: "))
word2 = str(input("Enter word 2: "))

# if that word is in our vocabulary
if word in model.wv.key_to_index and word2 in model.wv.key_to_index:
    print("The word %s is in your model vocabulary" % word)
else:
    print("%s is not in your model vocabulary" % word)

# returns a list with the top ten words used in similar contexts to the word
print(model.wv.most_similar(word, topn=10))

# returns a cosine similarity score for the two words
print(model.wv.similarity(word, word2))
print(is_similar(word, word2))
