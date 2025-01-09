import random

true_value = random.randint(1, 100)
print("숫자를 맞춰보세요(1~100)")
input_value = "9999"

while true_value != input_value:
    input_value = int(input())
    
    if input_value > true_value: # 사용자의 입력값이 true_value보다 클 때
        print("숫자가 너무 큽니다.")
    else: # 사용자의 입력값이 true_value보다 직을 때
        print("숫자가 너무 작습니다")
        
print(f"정답입니다. 입력한 숫자는 {true_value}")
