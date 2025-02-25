import re
from PyPDF2 import PdfReader
import argparse


# PDF에서 Abstract부터 1 Introduction까지 추출
def extract(input_path, output_path):
    reader = PdfReader(input_path)
    full_text = ""

    # 모든 페이지에서 텍스트 추출
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n\n"

    # 끊어진 텍스트 복원
    fixed_text = fix_broken_lines(full_text)

    # Abstract ~ 1 Introduction만 추출
    abstracts = extract_section(fixed_text, output_path)
    
    return abstracts

# 끊어진 텍스트 복원 함수
def fix_broken_lines(text):
    text = re.sub(r"-\n", "", text)  # 단어가 끊긴 경우 연결
    text = re.sub(r"\n(?!\n)", " ", text)  # 문장 중간 줄바꿈 제거
    text = re.sub(r"\n{2,}", "\n\n", text)  # 문단 구분 유지
    return text.strip()

# Abstract부터 1 Introduction까지 추출
def extract_section(input_file, output_file):
    start_pattern = re.compile(r"\babstract\b", re.IGNORECASE)
    end_pattern = re.compile(r"\b1\s*Introduction\b", re.IGNORECASE)

    abstracts = []
    current_abstract = []
    in_section = False

    for line in input_file.split("\n"):
        if start_pattern.search(line) and not in_section:
            current_abstract = [line]
            in_section = True
        elif end_pattern.search(line) and in_section:
            abstracts.append("\n".join(current_abstract))
            current_abstract = []
            in_section = False
        elif in_section:
            current_abstract.append(line)

    if current_abstract:
        abstracts.append("\n".join(current_abstract))

    with open(output_file, "w", encoding="utf-8") as f:
        for idx, abstract in enumerate(abstracts, start=1):
            f.write(f"\n\n--- Paper {idx} ---\n\n")
            f.write(clean_text(abstract))
        print(f"Save file!")
    
    return abstracts

# 유효한 유니코드로 정리
def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pdf to txt")
    parser.add_argument("input_path", type=str, help="Path to the input pdf file")
    parser.add_argument("output_path", type=str, help="Path to save txt file")
    
    args = parser.parse_args()
    
    abstracts = extract(args.input_path, args.output_path)