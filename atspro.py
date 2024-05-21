from pypdf import PdfReader
from PyPDF2 import PdfReader as PR
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec 
from gensim.parsing.preprocessing import remove_stopwords
import re
import string
import requests
import io

# used with no models
class ATS:
    def __init__(self, resume, job_description):
        self.resume = resume
        self.job_description = job_description
    
    def decide(self, log=False):
        """
        Uses the sklearn library to determine whether the resume fits the job description and logs the final decision

        self (ATS): The current ATS instance
        log (bool): Logs the decision process
        """
        text_arr=[self.resume, self.job_description]

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text_arr)

        sim = round(cosine_similarity(count_matrix)[0][1]*100, 2)
        if log:
            print("Similarity: "+str(sim)+"%")

        if sim > 60:
            print("This resume fits the job role")
        elif sim > 45:
            print("This resume somewhat fits the job role")
        else:
            print("This resume doesn't fit the job role")
    
    def process_resume(path, page=0, log=False):
        """
        Takes the path to the pdf of a resume and returns a string version of the resume

        path (str): The path of the resume to be processed
        page (int): The page to be processed
        log (bool): Logs the scanning process
        """
        reader = PdfReader(path)

        # printing number of pages in pdf file 
        if log:
            print("Number of pages:", len(reader.pages)) 
        
        # getting a specific page from the pdf file 
        page = reader.pages[0] 
        
        # extracting text from page 
        resume = page.extract_text() 

        return resume
    
    def process_resume_url(url, page=0, log=False):
        """
        Takes the url of a resume and returns a string version of the resume

        url (str): The url of the resume to be processed
        page (int): The page to be processed
        log (bool): Logs the scanning process
        """
        response = requests.get(url=url)
        on_fly_mem_obj = io.BytesIO(response.content)

        reader = PR(on_fly_mem_obj)

        # printing number of pages in pdf file 
        if log:
            print("Number of pages:", len(reader.pages)) 
        
        # getting a specific page from the pdf file 
        page = reader.pages[0] 
        
        # extracting text from page 
        resume = page.extract_text() 

        return resume

    def clean_text(text):
        """
        Takes a string of text and cleans it by removing stopwords and number

        text (str): The string of text to be cleaned
        """
        # make text lowercase
        tokens = text.split()
        tokens = [t.lower() for t in tokens]

        # remove punctuation
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        tokens = [re_punc.sub('', token) for token in tokens]

        # remove numbers
        tokens = [token for token in tokens if token.isalpha()]

        filtered_tokens = remove_stopwords(" ".join(tokens))
        return filtered_tokens.split()

# used with pre trained models  
class ATSModel:
    def __init__(self, model):
        # self.model_path = model_path
        # self.model = Word2Vec.load(model_path)
        self.model = model
    
    def is_in_vocab(self, phrase):
        """
        Checks if the phrase is in the model vocabulary and returns a boolean value

        self (ATSModel): The current ATSModel instance
        phrase (str): The phrase to be checked
        """

        return phrase in self.model.wv.key_to_index
    
    def is_similar(self, phrase, phrase2):
        """
        Uses a Word2Vec model to determine whether two phrases are similar and returns a tuple value containing the decision and the similarity percentage

        self (ATSModel): The current ATSModel instance
        phrase (str): The first phrase
        phrase2 (str): The second phrase
        """
        sum = 0
        for tuple in self.model.wv.most_similar(phrase, topn=10):
            sum += tuple[1]
        avg_top_sim = sum / len(self.model.wv.most_similar(phrase,topn=10))

        sim = self.model.wv.similarity(phrase, phrase2)
        sim_percentage = round((sim/avg_top_sim)*100, 2)

        # checks if difference between similarity of the two words and the similarity of the most similar words is minimal
        if abs(avg_top_sim-sim) < 0.15:
            return (True, sim_percentage)
        else:
            return (False, sim_percentage)
