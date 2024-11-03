import pandas as pd

def blank_target_column(file_path, target_column):
    """
    Reads a CSV file, blanks out the specified target column, and saves the modified file.
    
    Parameters:
    - file_path (str): The path to the CSV file.
    - target_column (str): The name of the column to blank out.
    
    Returns:
    - None
    """
    # 데이터 불러오기
    df = pd.read_csv(file_path)
    
    # 타겟 칼럼 비우기
    if target_column in df.columns:
        df[target_column] = None  # 또는 df[target_column] = '' 빈 문자열로 설정 가능
        print(f"'{target_column}' column has been blanked out.")
    else:
        print(f"Column '{target_column}' not found in the dataset.")
        return

    # 수정된 데이터 저장
    df.to_csv(file_path, index=False)
    print(f"Modified file saved to: {file_path}")

# 사용 예시
if __name__ == "__main__":
    file_path = 'test.csv'
    target_column = 'target_column_name'  # 비워야 하는 타겟 칼럼명으로 변경
    blank_target_column(file_path, target_column)
