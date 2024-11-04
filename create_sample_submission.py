import pandas as pd
import numpy as np

def create_sample_submission(file_path, num_rows):
    """
    Creates a sample submission file with random 0 and 1 values for 'click' column.

    Parameters:
    - file_path (str): Path to save the CSV file.
    - num_rows (int): Number of rows for the submission file, default is 8085792.

    Returns:
    - None
    """
    # ID 컬럼 생성 (0부터 num_rows까지)
    ids = range(0, num_rows + 1)
    
    # click 칼럼에 0과 1을 랜덤하게 할당
    click_values = np.random.choice([0, 1], size=num_rows+1)
    
    # 데이터프레임 생성
    sample_submission = pd.DataFrame({
        'ID': ids,
        'click': click_values
    })
    
    # 파일 저장
    sample_submission.to_csv(file_path, index=False)
    print(f"Sample submission file created at {file_path} with 'ID' and 'click' columns.")

# 사용 예시
if __name__ == "__main__":
    create_sample_submission("sample_submission.csv")
