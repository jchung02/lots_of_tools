# %%
import pandas as pd
import OpenDartReader
import os

api_key='Your_API_KEY'

# DART Open API 키 설정
dart = OpenDartReader(api_key)

# %% [markdown]
# ### 파일 불러오기
# 아래 행부터 읽으면 원본 파일의 변수명을 못 읽는 경우 대비

# %%
import pandas as pd

def load_excel(file_path, start_row, end_row):
    # 첫 행을 포함하여 파일 전체를 읽고, 헤더가 있는 첫 번째 행만 변수로 사용
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()  # 변수명 앞뒤 공백 제거

    # 필요한 범위의 데이터만 선택
    df = df.iloc[start_row:end_row].reset_index(drop=True)  # 시작 행부터 끝 행까지 슬라이싱

    return df

input_file = '/Users/hayoun/Documents/vscode/24-2-project/governance_data/전체 표본 (2024.9.11).xlsx'

# 15749행부터 19664행까지 데이터를 읽기
df = load_excel(input_file, 15748, 19664)

# Grouping by '회사명' and '거래소코드'
grouped = df.groupby(['회사명', '거래소코드'])

# Aggregating financial years and counting entries
results = grouped.agg({
    '회계년도': ['min', 'max', 'count'],
    '설립일': 'first',
    '상장일': 'first',
    '상장폐지일': 'first'
})

# Renaming the columns for better readability
results.columns = ['시작년도', '끝년도', '기록년수', '설립일', '상장일', '상장폐지일']

# Sorting by '거래소코드' index level
results = results.sort_index(level='거래소코드')

# Display the results
results


# %%
df.to_excel('/Users/hayoun/Documents/vscode/24-2-project/governance_data/하연_RA_전체 표본.xlsx',index=False)

# %%
# index = True 여야 '회사명' 칼럼을 남길 수 있음
results.to_excel('/Users/hayoun/Documents/vscode/24-2-project/governance_data/하연_RA_회사정보.xlsx',index=True)

# %% [markdown]
# ## 회사고유코드 찾기 1차: 거래소코드로 찾기
# * '거래소코드'를 기준으로 회사고유코드를 채움
# * 거래소코드로 찾아지지 않는, NaN인 경우를 일단 파악

# %%
results=pd.read_excel('/Users/hayoun/Documents/vscode/24-2-project/governance_data/하연_RA_회사정보.xlsx')
results

# %%
dt_results = results.copy()
dt_results['시작년도'] = pd.to_datetime(results['시작년도'], format='%Y/%m').apply(lambda x: x.replace(day=1))
# +1년을 더함
dt_results['끝년도'] = pd.to_datetime(results['끝년도'], format='%Y/%m').apply(lambda x: (x + pd.DateOffset(years=1)).replace(day=1))
dt_results['거래소코드']=dt_results['거래소코드'].astype(str).str.zfill(6) #000010 형식으로 거래소코드 수복
dt_results['회사명'] = dt_results['회사명'].astype(str).str.replace(r'\(주\)', '', regex=True).str.strip() #(주)신한증권 등 (주)를 제거
# dart.find_corp_code
# '거래소코드'를 사용하여 '회사고유코드'를 채움.
dt_results['회사고유코드'] = dt_results['거래소코드'].apply(dart.find_corp_code)
dt_results[dt_results['회사고유코드'].isna()]

# %%
dt_results

# %%
dt_results.to_excel('/Users/hayoun/Documents/vscode/24-2-project/governance_data/하연_RA_고유코드정보.xlsx',index=True)

# %%



