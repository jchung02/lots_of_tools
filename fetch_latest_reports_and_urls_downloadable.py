
import pandas as pd
import dart_fss as dart

def fetch_latest_reports_and_urls(kospi_code_list):
    """
    이 함수는 KOSPI 기업 코드 리스트를 입력으로 받아, 2024년 정기보고서(rcept_no)를 가져오고,
    필요한 하위 보고서 URL들을 추출하여 데이터프레임으로 반환합니다.
    """
    latest_reports = pd.DataFrame()
    error_count = 0

    # 각 기업 코드에 대해 보고서 가져오기
    for kospi_code in kospi_code_list:
        try:
            # 2024년에 공시된 정기보고서 목록 가져오기
            reports = dart.list(corp=kospi_code, start='2024', kind='A')

            if not reports.empty:
                # 가장 최근 보고서 추출
                latest_report = reports.iloc[-1]
                latest_reports = pd.concat([latest_reports, latest_report.to_frame().T], ignore_index=True)
            else:
                print(f"No reports found for {{kospi_code}}")
        except Exception as e:
            print(f"Error processing {{kospi_code}}: {{e}}")
            error_count += 1

    # 결과를 CSV 파일로 저장
    latest_reports.to_csv('./lists_to_crawl.csv', index=False)

    # 필요한 URL들을 저장할 리스트 생성
    urls_to_crawl = []

    # 각 보고서의 하위 보고서 URL 추출
    for index, row in latest_reports.iterrows():
        try:
            rcept_no = str(row['rcept_no'])
            sub_report = dart.sub_docs(rcept_no)

            # 필요한 인덱스 및 타이틀 설정
            needed_indexes = [9, 11, 12]
            needed_titles = ['3. 연결재무제표 주석', 'XII. 상세표']
            temp_list = []

            # 인덱스로 URL 가져오기
            for i, title in zip(needed_indexes, ['1. 사업의 개요', '3. 원재료 및 생산설비', '4. 매출 및 수주현황']):
                try:
                    url = sub_report.iloc[i]['url']
                except IndexError:
                    url = ''
                temp_list.append({{'url': url, 'stock_code': row['stock_code'], 'title': title}})

            # 타이틀로 URL 가져오기
            for title in needed_titles:
                try:
                    url = sub_report[sub_report['title'] == title]['url'].values[0]
                except IndexError:
                    url = ''
                temp_list.append({{'url': url, 'stock_code': row['stock_code'], 'title': title}})

            needed_urls = pd.DataFrame(temp_list)
            urls_to_crawl.append(needed_urls)

        except Exception as e:
            print(f"Error processing {{row['corp_name']}} with rcept_no {{rcept_no}}: {{e}}")

    df_needed_urls = pd.concat(urls_to_crawl, ignore_index=True)
    return df_needed_urls
