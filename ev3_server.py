#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import socket
# Wi-Fi 통신이므로 PyBluez가 필요 없습니다.
# 모터 제어는 일단 주석 처리된 상태를 유지합니다.

# -----------------
# 1. TCP/IP 설정
# -----------------
EV3_IP = '0.0.0.0'  # 모든 네트워크 인터페이스에서 연결 수신 대기
PORT = 8080         # 통신 포트 번호 (클라이언트와 동일해야 함)

# -----------------
# 2. 소켓 설정 및 연결 대기
# -----------------
try:
    # TCP/IP 소켓 생성 (socket.AF_INET 사용)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((EV3_IP, PORT))
    server_socket.listen(1) # 하나의 연결만 허용

    print("EV3 Server waiting via Wi-Fi. Port: {}".format(PORT)) 
    
    # PC 클라이언트 연결 수락
    conn, addr = server_socket.accept() 
    # IP 주소가 출력되므로, 한글 출력 오류를 피하기 위해 영어로 출력합니다.
    print("PC Client connected from: {}".format(addr[0])) 

    # -----------------
    # 3. 데이터 수신 루프
    # -----------------
    while True:
        data = conn.recv(1024).decode('utf-8').strip() 
        
        if not data:
            print("PC Client disconnected.")
            break 
            
        print("--- Received Signal ---")
        print("Signal: {}".format(data))
        
        # 신호에 따른 모터 제어 로직은 여기에 위치합니다.
        # if data == "1":
        #     ...

except Exception as e:
    print("ERROR occurred: {}".format(e))
    
finally:
    if 'conn' in locals():
        conn.close()
    if 'server_socket' in locals():
        server_socket.close()
    print("Socket connection terminated.")