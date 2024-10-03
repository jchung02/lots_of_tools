import requests
from tqdm import tqdm

# 좌표 -> 행정동 변환 함수
def get_legal_dong(lat, lon):
    url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={lon}&y={lat}"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # 행정동 코드가 있는 영역만 반환
            for region_info in data['documents']:
                if region_info['region_type'] == 'H':  # 행정동명으로 
                    return region_info['region_3depth_name']  # 행정동 반환
        return None
    except Exception as e:
        print(f"Error fetching legal dong for lat: {lat}, lon: {lon} - {e}")
        return None

# 행정동 컬럼 추가 함수
def add_legal_dong_column(df):
    # '행정동' 칼럼 추가 및 값 채우기
    df['행정동'] = df.apply(lambda row: get_legal_dong(row['Latitude'], row['Longitude']), axis=1)
    return df

# tqdm를 활용하여 진행상황 표시
def process_with_progress(df):
    tqdm.pandas()
    df['행정동'] = df.progress_apply(lambda row: get_legal_dong(row['Latitude'], row['Longitude']), axis=1)
    return df
