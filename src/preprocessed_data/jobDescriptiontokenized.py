import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

        os.makedirs(self.output_folder, exist_ok=True)

        nltk.download('punkt')  # Download the NLTK tokenizer data
        nltk.download('stopwords')  # Download stopwords data
        nltk.download('wordnet')  # Download WordNet data

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_and_tokenize(self):
        for root, _, files in os.walk(self.input_folder):
            for file in files:
                input_path = os.path.join(root, file)

                # Read the text from the input file
                with open(input_path, 'r', encoding='utf-8') as text_file:
                    text = text_file.read()

                # Tokenize the text using NLTK
                tokens = word_tokenize(text)

                # Remove stopwords and perform lemmatization
                tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.lower() not in self.stop_words]

                # Create the output folder structure if it does not exist
                relative_path = os.path.relpath(input_path, self.input_folder)
                output_folder = os.path.join(self.output_folder, os.path.dirname(relative_path))
                os.makedirs(output_folder, exist_ok=True)

                # # Save preprocessed tokens as a JSON file
                # output_json_filename = os.path.splitext(file)[0] + "_preprocessed.json"
                # output_json_path = os.path.join(output_folder, output_json_filename)

                # # Save preprocessed tokens as a JSON file
                # preprocessed_data = {"tokens": tokens}
                # with open(output_json_path, 'w', encoding='utf-8') as json_file:
                #     json.dump(preprocessed_data, json_file, ensure_ascii=False, indent=4)

                # Save preprocessed tokens as a TXT file
                output_txt_filename = os.path.splitext(file)[0] + "_preprocessed.txt"
                output_txt_path = os.path.join(output_folder, output_txt_filename)

                # Save preprocessed tokens as a TXT file
                with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(" ".join(tokens))


if __name__ == "__main__":
    input_folder = "fetch_data/job_description_data"
    output_folder = "tokenized_data/job_description_preprocessed"

    processor = TextProcessor(input_folder, output_folder)

    # Preprocess and tokenize existing job description text files using NLTK
    processor.preprocess_and_tokenize()
