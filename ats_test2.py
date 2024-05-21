from pypdf import PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from atspro import ATS

dirpath = r'C:\Users\manas\Dropbox\My PC (LAPTOP-OEFAVRL0)\Downloads\resume (2).pdf'
reader = PdfReader(dirpath)

# printing number of pages in pdf file 
print("Number of pages:", len(reader.pages)) 
  
# getting a specific page from the pdf file 
page = reader.pages[0] 
  
# extracting text from page 
resume = page.extract_text() 

job_description = '''Qualifications
\n
Must be able to work as a team member in a fast-paced environment
\n
Must have the ability to work well with others
\n
Must be able to read and follow instructions
\n
Must have basic math skills
\n
Able to use basic tools Able to lift up to 50 pounds on occasion
\n
Able to work independently and as part of a team
\n
Employee must be able to change water valves, set toilets, change & plumb sinks, tub drain leaks, set water lines, & change water heaters( general household plumbing & trim out experience) general construction, use power & hand tools, carpentry knowledge would be a bonus 
'''

text_arr=[resume, job_description]

# checker = ATS(resume=resume, job_description=job_description)
# checker.decide()

cv = CountVectorizer()
count_matrix = cv.fit_transform(text_arr)

sim = round(cosine_similarity(count_matrix)[0][1]*100, 2)

print("Similarity: "+str(sim)+"%")

if sim > 60:
    print("This resume fits the job role")
elif sim > 45:
    print("This resume somewhat fits the job role")
else:
    print("This resume doesn't fit the job role")