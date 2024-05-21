from atspro import ATS, ATSModel

def run_ats(model, resume_url, job_keywords):
    # job_keywords = ['react', 'javascript', 'frontend', 'html', 'css', 'critical', 'creative', 'website', 'solving', 'design', 'development']
    ats = ATSModel(model=model)
    # resume = ATS.process_resume(r'C:\Users\manas\Dropbox\My PC (LAPTOP-OEFAVRL0)\Downloads\front-end-developer-resume-example.pdf')
    resume = ATS.process_resume_url(resume_url)

    resume_cleaned = ATS.clean_text(resume)

    # word = str(input("Enter word: "))
    # word2 = str(input("Enter word 2: "))

    sim_words = 0
    max_sim = 0
    words_are_sim = False

    for keyword in job_keywords:
        print("a ",keyword)
        for resume_word in resume_cleaned:
            if ats.is_in_vocab(keyword) and ats.is_in_vocab(resume_word) and ats.is_similar(keyword, resume_word)[0]:
                words_are_sim = True
                sim = ats.is_similar(keyword, resume_word)
                print(f"{str(sim[0])} between {keyword} and {resume_word}")
                if sim[1] > max_sim:
                    max_sim = sim[1]
                break
        if words_are_sim:
            # print("k ",keyword)
            sim_words += 1
        words_are_sim=False

    sim_percent = round((sim_words/len(job_keywords))*100, 2)
    print(sim_percent)

    if sim_percent > 65:
        return True
    else:
        return False


    


