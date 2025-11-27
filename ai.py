#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import cv2
import tensorflow.keras
import numpy as np
import socket
import time

# ===================================================
# 1. EV3 통신 및 AI 모델 설정 (필수 수정)
# ===================================================

# 🚨 중요: 여기에 EV3 브릭의 현재 IP 주소를 입력하세요!
EV3_IP = "192.168.X.XXX" # <-- 실제 EV3 IP 주소로 변경
PORT = 8080
client_socket = None

# 학습된 모델 불러오기
# 🚨 중요: 실제 파일 경로로 변경하세요.
model_filename = 'C:/Users/akthq/OneDrive/Desktop/converted_keras (7)/keras_model.h5' 
model = tensorflow.keras.models.load_model(model_filename)

# EV3로 전송할 신호 코드 정의
SIGNAL_WAKE = "0" # 올바른 자세 (모터 멈춤 신호)
SIGNAL_FORWARD_HEAD = "1" # 거북목 상태 (모터 작동 신호)

# ===================================================
# 2. 함수 정의 및 TCP/IP 연결
# ===================================================

## 이미지 전처리
def preprocessing(frame):
    # 사이즈 조정 및 정규화
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    
    # 이미지 차원 재조정
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    return frame_reshaped

## 신호 전송 함수 (Wi-Fi/TCP 버전)
def send_correction_signal(signal_code):
    global client_socket
    if client_socket:
        try:
            message = (signal_code + '\n').encode('utf-8') 
            client_socket.sendall(message)
            # print(f"Client sent signal: {signal_code}") # 디버깅용
        except Exception as e:
            # 통신 에러 발생 시 소켓 연결 종료
            print(f"ERROR: Data transmission failed. Disconnecting. {e}")
            client_socket.close()
            client_socket = None

# TCP/IP 연결 시도
print("Attempting to connect to EV3dev via Wi-Fi...")
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((EV3_IP, PORT))
    print("EV3dev Connection SUCCESS via Wi-Fi!")
except Exception as e:
    print(f"EV3dev Connection FAILED. AI will run without motor correction. Error: {e}")
    client_socket = None

# ===================================================
# 3. 메인 루프 (AI 추론 및 통신)
# ===================================================

# 카메라 캡쳐 객체, 0=내장 카메라
capture = cv2.VideoCapture(0)

# 캡쳐 프레임 사이즈 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

forward_head_cnt = 0 # 거북목 상태가 지속된 루프 횟수 (0으로 초기화)
THRESHOLD_COUNT = 30 # 30회 감지 (cv2.waitKey(200) 기준으로 약 6초) 후 신호 전송

print("\nStarting AI Detection Loop...")
while True:
    ret, frame = capture.read()
    if not ret: 
        print("Failed to read frame!")
        time.sleep(0.1)
        continue 

    # 이미지 뒤집기 및 출력
    frame_fliped = cv2.flip(frame, 1)
    cv2.imshow("VideoFrame", frame_fliped)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(200) & 0xFF == ord('q'): # 루프 당 200ms 대기 (0.2초)
        break
    
    # 데이터 전처리
    preprocessed = preprocessing(frame_fliped)

    # 예측
    prediction = model.predict(preprocessed)
    
    # 예측 결과 해석 및 신호 결정
    prob_wake = prediction[0, 0]
    prob_forward_head = prediction[0, 1]
    
    is_forward_head = prob_wake < prob_forward_head # 거북목 확률이 더 높을 경우 True

    if is_forward_head:
        forward_head_cnt += 1
        print(f'[거북목 상태 감지]')
        
    else:
        # 올바른 자세일 경우 카운트 초기화
        print(f'[올바른 자세]')
        forward_head_cnt = 0
    
    
    # --- 모터 신호 전송 로직 ---
    if forward_head_cnt >= THRESHOLD_COUNT:
        # 30회 이상 지속: 모터 작동 신호를 연속적으로 보냄
        current_signal = SIGNAL_FORWARD_HEAD
        if forward_head_cnt == THRESHOLD_COUNT: # 최초 30회 도달 시에만 메시지 출력
             print(f'--- {THRESHOLD_COUNT}회 지속! EV3로 모터 작동 신호 전송 ---')
    else:
        # 30회 미만 또는 올바른 자세: 모터 멈춤 신호를 보냄
        current_signal = SIGNAL_WAKE 

    # EV3로 최종 신호 전송
    send_correction_signal(current_signal)
    
# 카메라 객체 반환 및 종료
capture.release() 
cv2.destroyAllWindows()
if client_socket:
    client_socket.close()
    print("Socket connection closed.")