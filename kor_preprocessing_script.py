
import re
from soynlp.normalizer import repeat_normalize

# 시스템 문구 삭제 함수
def remove_system_phrases(text):
    system_phrases = [
        r'#@시스템#동영상#', r'#@시스템#사진#', r'#@이모티콘#', r'#@기타#', r'#@시스템#기타#'
    ]
    for phrase in system_phrases:
        text = re.sub(phrase, '', text)
    return text

# 이모티콘 삭제 함수
def remove_emoticons(text):
    emoticon_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # 이모티콘
        u"\U0001F300-\U0001F5FF"  # 기호 & 픽토그램
        u"\U0001F680-\U0001F6FF"  # 교통 & 지도 기호
        u"\U0001F1E0-\U0001F1FF"  # 깃발 (iOS)
        u"\U00002700-\U000027BF"  # 기타 기호
        u"\U0001F900-\U0001F9FF"  # 추가 기호
        "]+", flags=re.UNICODE)
    return emoticon_pattern.sub(r'', text)

# 인명 가명, 주소 처리 함수
def replace_names(text):
    text = re.sub(r'#@이름#', '<이름>', text)
    text = re.sub(r'#@주소#', '<주소>', text)
    return text

# 초성 처리 함수
def handle_consonants(text):
    # 초성이 4개 이상 반복되는 경우 4개까지만 남기기
    text = repeat_normalize(text, num_repeats=4)

    # 1~3개 반복되는 초성이 초성이 아닌 것들 사이에 있을 때 삭제
    text = re.sub(r'([^ㄱ-ㅎ]|^)([ㄱ-ㅎ]{1,3})([^ㄱ-ㅎ]|$)', r'\1\3', text)

    return text

# 전체 전처리 함수
def preprocess_text(text):
    text = remove_system_phrases(text)
    text = remove_emoticons(text)
    text = replace_names(text)
    text = handle_consonants(text)
    return text
