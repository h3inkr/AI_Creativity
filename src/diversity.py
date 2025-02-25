import math
from collections import Counter
import argparse

def calculate_ttr(tokens):
    unique_tokens = set(tokens)
    return len(unique_tokens) / len(tokens) if tokens else 0

def calculate_cttr(tokens):
    unique_tokens = set(tokens)
    return len(unique_tokens) / math.sqrt(2 * len(tokens)) if tokens else 0

def calculate_rttr(tokens):
    unique_tokens = set(tokens)
    return len(unique_tokens) / math.sqrt(len(tokens)) if tokens else 0

def calculate_mattr(tokens, window_size=50):
    if len(tokens) < window_size:
        return calculate_ttr(tokens)
    
    ttr_values = [calculate_ttr(tokens[i:i + window_size]) for i in range(len(tokens) - window_size + 1)]
    return sum(ttr_values) / len(ttr_values)

def calculate_mtld(tokens, threshold=0.72):
    def mtld_forward(text):
        factor_count = 0
        current_ttr = 1
        token_count = 0
        unique_tokens = set()
        
        for token in text:
            unique_tokens.add(token)
            token_count += 1
            current_ttr = len(unique_tokens) / token_count
            if current_ttr < threshold:
                factor_count += 1
                unique_tokens = set()
                token_count = 0
        
        factor_count += 1  # 마지막 세그먼트 반영
        return len(text) / factor_count if factor_count > 0 else 0
    
    return (mtld_forward(tokens) + mtld_forward(tokens[::-1])) / 2

def calculate_hd_d(tokens, sample_size=42):
    unique_tokens = set(tokens)
    total_tokens = len(tokens)
    if total_tokens < sample_size:
        return calculate_ttr(tokens)
    
    prob_sum = sum(
        math.comb(tokens.count(word), 1) * math.comb(total_tokens - tokens.count(word), sample_size - 1) / math.comb(total_tokens, sample_size)
        for word in unique_tokens
    )
    return prob_sum

def calculate_yules_k(tokens):
    frequencies = Counter(tokens)
    M1 = sum(frequencies.values())
    M2 = sum(f**2 for f in frequencies.values())
    return (M2 - M1) / (M1 * M1) if M1 > 0 else 0

def calculate_entropy(tokens):
    frequencies = Counter(tokens)
    total_tokens = len(tokens)
    return -sum((freq / total_tokens) * math.log2(freq / total_tokens) for freq in frequencies.values() if freq > 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str)
    
    args = parser.parse_args()
    
    try:
        # 파일 읽기
        with open(args.file_name, "r", encoding="utf-8") as file:
            text = file.read()

        # 공백 기준으로 토큰화
        tokens = text.lower().split()

        # 각 지표 계산
        ttr = calculate_ttr(tokens)
        print("Complete calculate TTR!")
        cttr = calculate_cttr(tokens)
        print("Complete calculate CTTR!")
        rttr = calculate_rttr(tokens)
        print("Complete calculate RTTR!")
        mattr = calculate_mattr(tokens)
        print("Complete calculate MATTR!")
        mtld = calculate_mtld(tokens)
        print("Complete calculate MTLD!")
        hd_d = calculate_hd_d(tokens)
        print("Complete calculate HD-D!")
        yules_k = calculate_yules_k(tokens)
        print("Complete calculate Yule's K!")
        entropy = calculate_entropy(tokens)
        print("Complete calculate Shannon's Entropy!")

        # 결과 출력
        print(f"Total number of words (Tokens): {len(tokens)}")
        print(f"Total vocabulary (Types): {len(set(tokens))}")
        print(f"Type-Token Ratio (TTR): {ttr:.4f}")
        print(f"Corrected TTR (CTTR): {cttr:.4f}")
        print(f"Root TTR (RTTR): {rttr:.4f}")
        print(f"Moving-Average TTR (MATTR): {mattr:.4f}")
        print(f"Measure of Textual Lexical Diversity (MTLD): {mtld:.4f}")
        print(f"Hypergeometric Distribution Diversity (HD-D): {hd_d:.4f}")
        print(f"Yule's K: {yules_k:.4f}")
        print(f"Shannon's Entropy: {entropy:.4f}")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    except Exception as e:
        print(f"오류 발생: {e}")


