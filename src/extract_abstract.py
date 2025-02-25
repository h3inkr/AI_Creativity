import re
import argparse


def extract_abstracts(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 논문을 '--- Paper X ---' 기준으로 분할
    papers = re.split(r'---\s*Paper\s*\d+\s*---', text)
    abstracts = []
    
    for i, paper in enumerate(papers[1:], 1):  # 첫 번째 요소는 빈 문자열일 가능성이 높음
        match = re.search(r"Abstract\s*(.*?)\s+1\s+Introduction", paper, re.DOTALL | re.IGNORECASE)
        if match:
            abstract = re.sub(r"[\n.]", " ", match.group(1)).strip()
            abstracts.append(f"--- Paper {i} ---\n{abstract}\n")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(abstracts))
        
def take_n_tokens(input_file, output_file, n_tokens=300):
    """
    take up to n_tokens
    """
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
        
    papers = re.split(r'---\s*Paper\s*\d+\s*---', text)
    abstracts = []
    total_tokens = 0
    
    for i, paper in enumerate(papers[1:], 1):  
        match = re.search(r"Abstract\s*(.*?)\s+1\s+Introduction", paper, re.DOTALL | re.IGNORECASE)
        if match:
            abstract = re.sub(r"[\n.]", " ", match.group(1)).strip()
            tokens = abstract.split()
            total_tokens += len(tokens)
            if total_tokens < n_tokens:
                abstracts.append(f"--- Paper {i} ---\n{abstract}\n")
            else:
                break
        
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(abstracts))
                    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract abstract sections from a text file.")
    parser.add_argument("input_path", type=str, help="Path to the input text file")
    parser.add_argument("output_path", type=str, help="Path to save the extracted abstract")

    args = parser.parse_args()
    
    # extract_abstracts(args.input_path, args.output_path)
    take_n_tokens(args.input_path, args.output_path)
