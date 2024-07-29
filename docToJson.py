import json
import os
from docx import Document
def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def clean_text(text):
    # Remove any line that contains "Oferta pentru firma"
    lines = text.splitlines()
    cleaned_lines = [line for line in lines if "Oferta pentru firma" not in line]
    return "\n".join(cleaned_lines).strip()


def clean_prompt(text):
    cleaned_text = clean_text(text)
    return cleaned_text.replace("Solicitarea client:", "").strip()


def clean_completion(text):
    return clean_text(text)


def extract_sections(text):
    sections = {"prompt": "", "input": "", "completion": ""}
    lines = text.splitlines()

    prompt_and_input = []
    completion = []
    in_completion_section = False

    for line in lines:
        if "Scopul documentului" in line:
            in_completion_section = True
        if in_completion_section:
            completion.append(line)
        else:
            prompt_and_input.append(line)

    # Join the prompt_and_input lines back into a single string
    prompt_and_input_text = "\n".join(prompt_and_input).strip()
    # Split prompt_and_input_text at "NOTA:"
    if "NOTA:" in prompt_and_input_text:
        prompt_part, input_part = prompt_and_input_text.split("NOTA:", 1)
        sections["prompt"] = clean_prompt(prompt_part)
        sections["input"] = input_part.strip()
    else:
        sections["prompt"] = clean_prompt(prompt_and_input_text)

    # Join the completion lines back into a single string
    remaining_text = "\n".join(completion).strip()
    # Clean the completion text
    sections["completion"] = clean_completion(remaining_text)

    return sections


def process_files(input_dir, output_file):
    data = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".docx"):
            file_path = os.path.join(input_dir, filename)
            text = read_docx(file_path)
            sections = extract_sections(text)
            data.append(sections)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


input_dir = "Vezif/Oferte test"  # Change this to the path of your .docx files
output_file = "training_data.json"

process_files(input_dir, output_file)
