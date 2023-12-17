import os
from datasets import load_dataset
import json
import re

class FetchData:
    def __init__(self, data_link):
        self.data_link = data_link
        self.dataset = self.download_dataset()
        self.data_folder = "data/fetch_data/job_description_data"  

        # Create the output folder if it does not exist
        os.makedirs(self.data_folder, exist_ok=True)

    def download_dataset(self):
        dataset = load_dataset(self.data_link)
        return dataset

    def job_descriptions(self):
        return self.dataset['train']['job_description']

    def position_titles(self):
        return self.dataset['train']['position_title']

    def sanitize_filename(self, filename):
        # Remove characters that are not safe in filenames
        sanitized_filename = re.sub(r'[\/:*?"<>|]', '_', filename)
        return sanitized_filename

    def save_job_desc_as_text(self):
        job_desc = self.job_descriptions()
        position_titles = self.position_titles()
        for i, desc in enumerate(job_desc):
            position_title = position_titles[i]
            sanitized_position_title = self.sanitize_filename(position_title)
            output_filename = f"{sanitized_position_title}.txt"
            output_path = os.path.join(self.data_folder, output_filename)
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(desc)

    def save_job_desc_as_json(self):
        job_desc = self.job_descriptions()
        position_titles = self.position_titles()
        for i, desc in enumerate(job_desc):
            position_title = position_titles[i]
            sanitized_position_title = self.sanitize_filename(position_title)
            output_filename = f"{sanitized_position_title}.json"
            output_path = os.path.join(self.data_folder, output_filename)
            job_desc_dict = {"job_description": desc}
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(job_desc_dict, json_file, ensure_ascii=False, indent=4)

    def print_job_desc(self):
        job_desc = self.job_descriptions()
        for i, desc in enumerate(job_desc):
            print(f"Job Description {i + 1}:")
            print("\n")
            print(desc)
            print("\n")

if __name__ == "__main__":
    data = FetchData("jacob-hugging-face/job-descriptions")
    
    # Print job descriptions
    data.print_job_desc()
    
    # Save job descriptions as text and JSON files with sanitized position titles as filenames
    data.save_job_desc_as_text()
    data.save_job_desc_as_json()



















































# import os
# from datasets import load_dataset
# import json

# class FetchData:
#     def __init__(self, data_link):
#         self.data_link = data_link
#         self.dataset = self.download_dataset()
#         self.data_folder = "processed_data/job_description_data"  # Define the folder structure

#         # Create the output folder if it does not exist
#         os.makedirs(self.data_folder, exist_ok=True)

#     def download_dataset(self):
#         dataset = load_dataset(self.data_link)
#         return dataset

#     def job_description(self):
#         job_desc = self.dataset['train']['job_description'][:]
#         return job_desc

#     def save_job_desc_as_text(self, output_filename):
#         job_desc = self.job_description()
#         output_path = os.path.join(self.data_folder, output_filename)
#         with open(output_path, 'w', encoding='utf-8') as text_file:
#             for i, desc in enumerate(job_desc, start=1):
#                 text_file.write(f"Job Description {i}:\n\n")
#                 text_file.write(desc)
#                 text_file.write("\n\n")

#     def save_job_desc_as_json(self, output_filename):
#         job_desc = self.job_description()
#         output_path = os.path.join(self.data_folder, output_filename)
#         job_desc_dict = {"job_descriptions": job_desc}
#         with open(output_path, 'w', encoding='utf-8') as json_file:
#             json.dump(job_desc_dict, json_file, ensure_ascii=False, indent=4)

#     def print_job_desc(self):
#         job_desc = self.job_description()
#         for i, desc in enumerate(job_desc):
#             print(f"Job Description {i + 1}:")
#             print("\n")
#             print(desc)
#             print("\n")

# if __name__ == "__main__":
#     data = FetchData("jacob-hugging-face/job-descriptions")
    
#     # Print job descriptions
#     data.print_job_desc()
    
#     # Save job descriptions in the specified folder
#     data.save_job_desc_as_text("job_descriptions.txt")
#     data.save_job_desc_as_json("job_descriptions.json")
