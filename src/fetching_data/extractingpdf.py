import spacy
from spacy.matcher import Matcher
import os
import glob
from PyPDF2 import PdfReader
import json

class ResumeParser:
    def __init__(self, pdf_folder):
        self.pdf_folder = pdf_folder
        self.nlp = spacy.load("en_core_web_lg")
        self.matcher = Matcher(self.nlp.vocab)
        self.define_matcher_patterns()  
    
    def define_matcher_patterns(self):
        # Define a list of job title keywords
        job_title_keywords = ["TUTORING", "CONSULTANT","job", "category", "role", "engineer", "developer", "analyst", 
                              "manager", "designer", "scientist", "accountant", "hr", "trainer", 
                              "accountant", "advocate", "agriculture", "apparel", "artist", "automobile", 
                              "aviation", "banking", "bpo", "call center","business development",
                              "chef", "construction", "consultant", "designer", "digital-media", 
                              "digital marketing", "engineering", "finance", "financial", "fitness", 
                              "healthcare", "human resource", "information technology", "public relations",
                              "sales", "teacher"]
        
        job_role_pattern = [{"LOWER": {"in": job_title_keywords}}, {"POS": "NOUN"}]
        self.matcher.add("job_role", [job_role_pattern])

        skills_pattern = [{"POS": {"in": ["NOUN", "PROPN"]}}]
        self.matcher.add("skills", [skills_pattern])

    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

    def extract_keywords(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)

        job_role = "Unknown"
        skills = []

        for match_id, start, end in matches:
            match_text = doc[start:end].text
            if self.nlp.vocab.strings[match_id] == "job_role":
                job_role = match_text
            elif self.nlp.vocab.strings[match_id] == "skills":
                skills.append(match_text)

        return job_role, skills

    def extract_education(self, text):
        doc = self.nlp(text)
        degree = "Unknown"
        institution = "Unknown"

        # Define keywords for education entity recognition
        education_keywords = ["bachelor's", "master's", "phd", "diploma", "degree", 
                              "institute", "university", "college"]

        for token in doc:
            if token.text.lower() in education_keywords:
                # Collect words following the education keywords as the degree
                degree = " ".join([t.text for t in token.subtree if not t.is_punct])

            if "university" in token.text.lower() or "college" in token.text.lower():
                institution = token.text

        return degree, institution

    def process_resumes(self):
        pdf_files = glob.glob(os.path.join(self.pdf_folder, "*.pdf"))
        parsed_resumes = []

        for pdf_file in pdf_files:
            resume_text = self.extract_text_from_pdf(pdf_file)
            job_role, skills = self.extract_keywords(resume_text)
            degree, institution = self.extract_education(resume_text)

            parsed_resumes.append({
                "File": os.path.basename(pdf_file),
                "Category (Job Role)": job_role,
                "Skills": skills,
                "Education": {"Degree": degree, "Institution": institution}
            })

        return parsed_resumes

if __name__ == "__main__":
    root_folder = r'dataset\data\data'  # Root folder containing subfolders with PDFs
    output_folder = "data/fetch_data/resume_parser"  # Output folder for JSON and text files
    os.makedirs(output_folder, exist_ok=True)

    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):
            resume_parser = ResumeParser(subfolder_path)
            parsed_resumes = resume_parser.process_resumes()

            # Create a subfolder for each subfolder in the output directory
            subfolder_output_folder = os.path.join(output_folder, subfolder)
            os.makedirs(subfolder_output_folder, exist_ok=True)

            for resume in parsed_resumes:
                # Save each parsed resume as a separate text file
                output_text_file = os.path.join(subfolder_output_folder, f"{resume['File']}.txt")
                with open(output_text_file, "w", encoding="utf-8") as text_file:
                    text_file.write(f"Category (Job Role): {resume['Category (Job Role)']}\n")
                    text_file.write(f"Skills: {', '.join(resume['Skills'])}\n")
                    text_file.write(f"Education: Degree - {resume['Education']['Degree']}, Institution - {resume['Education']['Institution']}\n")


















































# import spacy
# from spacy.matcher import Matcher
# import os
# import glob
# from PyPDF2 import PdfReader
# import json

# class ResumeParser:
#     def __init__(self, pdf_folder, limit=None):
#         self.pdf_folder = pdf_folder
#         self.nlp = spacy.load("en_core_web_lg")
#         self.matcher = Matcher(self.nlp.vocab)
#         self.define_matcher_patterns()  # Call the pattern definition method
#         self.limit = limit
    
#     def define_matcher_patterns(self):
#         # Define a list of job title keywords
#         job_title_keywords = ["job", "category", "role", "engineer", "developer", "analyst", 
#                               "manager", "designer", "scientist", "accountant", "hr", "trainer", 
#                               "accountant", "advocate", "agriculture", "apparel", "artist", "automobile", 
#                               "aviation", "banking", "bpo", "call center","business development",
#                               "chef", "construction", "consultant", "designer", "digital-media", 
#                               "digital marketing", "engineering", "finance", "financial", "fitness", 
#                               "healthcare", "human resource", "information technology", "public relations",
#                               "sales", "teacher"]
        
#         job_role_pattern = [{"LOWER": {"in": job_title_keywords}}, {"POS": "NOUN"}]
#         self.matcher.add("job_role", [job_role_pattern])

#         skills_pattern = [{"POS": {"in": ["NOUN", "PROPN"]}}]
#         self.matcher.add("skills", [skills_pattern])

#     def extract_text_from_pdf(self, pdf_path):
#         with open(pdf_path, "rb") as pdf_file:
#             pdf_reader = PdfReader(pdf_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
#             return text

#     def extract_keywords(self, text):
#         doc = self.nlp(text)
#         matches = self.matcher(doc)

#         job_role = "Unknown"
#         skills = []

#         for match_id, start, end in matches:
#             match_text = doc[start:end].text
#             if self.nlp.vocab.strings[match_id] == "job_role":
#                 job_role = match_text
#             elif self.nlp.vocab.strings[match_id] == "skills":
#                 skills.append(match_text)

#         return job_role, skills

#     def extract_education(self, text):
#         doc = self.nlp(text)
#         degree = "Unknown"
#         institution = "Unknown"

#         # Define keywords for education entity recognition
#         education_keywords = ["bachelor's", "master's", "phd", "diploma", "degree", 
#                               "institute", "university", "college"]

#         for token in doc:
#             if token.text.lower() in education_keywords:
#                 # Collect words following the education keywords as the degree
#                 degree = " ".join([t.text for t in token.subtree if not t.is_punct])

#             if "university" in token.text.lower() or "college" in token.text.lower():
#                 institution = token.text

#         return degree, institution

#     def process_resumes(self):
#         pdf_files = glob.glob(os.path.join(self.pdf_folder, "*.pdf"))
#         parsed_resumes = []

#         for pdf_file in pdf_files[:self.limit]:
#             resume_text = self.extract_text_from_pdf(pdf_file)
#             job_role, skills = self.extract_keywords(resume_text)
#             degree, institution = self.extract_education(resume_text)

#             parsed_resumes.append({
#                 "File": os.path.basename(pdf_file),
#                 "Category (Job Role)": job_role,
#                 "Skills": skills,
#                 "Education": {"Degree": degree, "Institution": institution}
#             })

#         return parsed_resumes

# if __name__ == "__main__":
#     root_folder = r'data\data\data'  # Root folder containing subfolders with PDFs
#     output_folder = "processed_data/resume_parser"  # Output folder for JSON and text files
#     os.makedirs(output_folder, exist_ok=True)
    
#     resume_limit = 15  # Set your desired limit here, or set to None to process all resumes

#     for subfolder in os.listdir(root_folder):
#         subfolder_path = os.path.join(root_folder, subfolder)
#         if os.path.isdir(subfolder_path):
#             resume_parser = ResumeParser(subfolder_path, limit=resume_limit)
#             parsed_resumes = resume_parser.process_resumes()

#             # Create a subfolder for each subfolder in the output directory
#             subfolder_output_folder = os.path.join(output_folder, subfolder)
#             os.makedirs(subfolder_output_folder, exist_ok=True)
            
#             for resume in parsed_resumes:
#                 # Save each parsed resume as a separate text file
#                 output_text_file = os.path.join(subfolder_output_folder, f"{resume['File']}.txt")
#                 with open(output_text_file, "w", encoding="utf-8") as text_file:
#                     # text_file.write(f"File: {resume['File']}\n")
#                     text_file.write(f"Category (Job Role): {resume['Category (Job Role)']}\n")
#                     text_file.write(f"Skills: {', '.join(resume['Skills'])}\n")
#                     text_file.write(f"Education: Degree - {resume['Education']['Degree']}, Institution - {resume['Education']['Institution']}\n")
#                     # text_file.write("=" * 80 + "\n")






































# from PyPDF2 import PdfReader
# import os
# import glob

# class PDFTextExtractor:
#     def __init__(self, pdf_path):
#         self.pdf_path = pdf_path

#     def extract_text(self):
#         with open(self.pdf_path, "rb") as pdf_file:
#             reader = PdfReader(pdf_file)
#             results = []
#             for page in reader.pages:
#                 text = page.extract_text()
#                 results.append(text)
#             return ' '.join(results)

# def main():
#     resume_folder = "data\\data\\data\\ACCOUNTANT\\"
#     pdf_files = glob.glob(os.path.join(resume_folder, "*.pdf"))

#     # Sort the PDF files by modification time in descending order to get the most recent ones
#     pdf_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

#     # Select the 10 most recent PDF files or all PDF files if there are fewer than 10
#     selected_pdfs = pdf_files[:10]

#     for i, pdf_file in enumerate(selected_pdfs, start=1):
#         pdf_extractor = PDFTextExtractor(pdf_file)
#         extracted_text = pdf_extractor.extract_text()
#         print(f" \n Resume {i}: {pdf_file} \n")
#         print("\n")
#         print(extracted_text)
#         print("\n")
#         print("=" * 80)
#         print("\n")

# if __name__ == "__main__":
#     main()






# import spacy
# from spacy.matcher import Matcher
# import os
# import glob
# from PyPDF2 import PdfReader
# import json

# class ResumeParser:
#     def __init__(self, pdf_folder, limit=15):
#         self.pdf_folder = pdf_folder
#         self.nlp = spacy.load("en_core_web_lg")
#         self.matcher = Matcher(self.nlp.vocab)
#         self.define_matcher_patterns()
#         self.limit = limit
    
#     def define_matcher_patterns(self):
#         # Define a list of job title keywords
#         job_title_keywords = ["job", "category", "role", "engineer", "developer", "analyst", 
#                               "manager", "designer", "scientist", "accountant", "hr", "trainer", 
#                               "accountant", "advocate", "agriculture", "apparel", "artist", "automobile", 
#                               "aviation", "banking", "bpo", "call center","business development",
#                               "chef", "construction", "consultant", "designer", "digital-media", 
#                               "digital marketing", "engineering", "finance", "financial", "fitness", 
#                               "healthcare", "human resource", "information technology", "public relations",
#                               "sales", "teacher"]
        
#         job_role_pattern = [{"LOWER": {"in": job_title_keywords}}, {"POS": "NOUN"}]
#         self.matcher.add("job_role", [job_role_pattern])

#         skills_pattern = [{"POS": {"in": ["NOUN", "PROPN"]}}]
#         self.matcher.add("skills", [skills_pattern])

#     def extract_text_from_pdf(self, pdf_path):
#         with open(pdf_path, "rb") as pdf_file:
#             pdf_reader = PdfReader(pdf_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
#             return text

#     def extract_keywords(self, text):
#         doc = self.nlp(text)
#         matches = self.matcher(doc)

#         job_role = "Unknown"
#         skills = []

#         for match_id, start, end in matches:
#             match_text = doc[start:end].text
#             if self.nlp.vocab.strings[match_id] == "job_role":
#                 job_role = match_text
#             elif self.nlp.vocab.strings[match_id] == "skills":
#                 skills.append(match_text)

#         return job_role, skills

#     def extract_education(self, text):
#         doc = self.nlp(text)
#         degree = "Unknown"
#         institution = "Unknown"

#         # Define keywords for education entity recognition
#         education_keywords = ["bachelor's", "master's", "phd", "diploma", "degree", 
#                               "institute", "university", "college"]

#         for token in doc:
#             if token.text.lower() in education_keywords:
#                 # Collect words following the education keywords as the degree
#                 degree = " ".join([t.text for t in token.subtree if not t.is_punct])

#             if "university" in token.text.lower() or "college" in token.text.lower():
#                 institution = token.text

#         return degree, institution

#     def process_resumes(self):
#         pdf_files = glob.glob(os.path.join(self.pdf_folder, "*.pdf"))
#         parsed_resumes = []

#         for pdf_file in pdf_files[:self.limit]:
#             resume_text = self.extract_text_from_pdf(pdf_file)
#             job_role, skills = self.extract_keywords(resume_text)
#             degree, institution = self.extract_education(resume_text)

#             parsed_resumes.append({
#                 "File": os.path.basename(pdf_file),
#                 "Category (Job Role)": job_role,
#                 "Skills": skills,
#                 "Education": {"Degree": degree, "Institution": institution}
#             })

#         return parsed_resumes

# if __name__ == "__main__":
#     resume_folder = r"data\data\data"  # Update the path to your resume folder
#     resume_parser = ResumeParser(resume_folder)
#     parsed_resumes = resume_parser.process_resumes()

#     # Print the parsed resumes
#     for resume in parsed_resumes:
#         # print("File:", resume["File"])
#         print("Category (Job Role):", resume["Category (Job Role)"])
#         print("Skills:", resume["Skills"])
#         print("Education:", resume["Education"])
#         print("=" * 80)

#     # Save parsed resumes in JSON format
#     output_folder = "processed_data/resume_data"
#     os.makedirs(output_folder, exist_ok=True)
#     output_file = os.path.join(output_folder, "parsed_resumes.json")
#     with open(output_file, "w", encoding="utf-8") as json_file:
#         json.dump(parsed_resumes, json_file, ensure_ascii=False, indent=4)
        
    
#     # Save parsed resumes in text format
#     output_text_file = os.path.join(output_folder, "parsed_resumes.txt")
#     with open(output_text_file, "w", encoding="utf-8") as text_file:
#         for resume in parsed_resumes:
#             text_file.write(f"File: {resume['File']}\n")
#             text_file.write(f"Category (Job Role): {resume['Category (Job Role)']}\n")
#             text_file.write(f"Skills: {', '.join(resume['Skills'])}\n")
#             text_file.write(f"Education: Degree - {resume['Education']['Degree']}, Institution - {resume['Education']['Institution']}\n")
#             text_file.write("=" * 80 + "\n")

