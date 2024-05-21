from urllib import request
# from pyPdf import PdfFileWriter, PdfFileReader
import io
import requests
from PyPDF2 import PdfReader

url = "https://firebasestorage.googleapis.com/v0/b/fblaproject-e450d.appspot.com/o/resumes%2Fresume-07vx3gj?alt=media&token=e7307c18-6262-4ca4-bbcd-6b54e05d6dfc"

response = requests.get(url=url)
on_fly_mem_obj = io.BytesIO(response.content)
pdf_file = PdfReader(on_fly_mem_obj)

# getting a specific page from the pdf file 
page = pdf_file.pages[0] 
        
# extracting text from page 
resume = page.extract_text() 

print("r ",resume)

# for pageNum in xrange(pdfFile.getNumPages()):
#         currentPage = pdfFile.getPage(pageNum)
#         #currentPage.mergePage(watermark.getPage(0))