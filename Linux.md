# Linux 환경 설정하기 

저번에 문서에서 했듯이 Window 운영체제에서 BlueTooth를 사용해서 PC와 EV3 본체의 신호를 서로 주고 받으려고 했지만 
Window는 bluetooth를 통한 신호 전달 기능을 지원하지 않는 관계로 WI-FI를 이용하거나 LINUX 환경을 설정해서 신호를 주고 받아야했다.

소프트웨어학부에 왔으면 언젠간 LINUX는 다뤄야할거같아서 이왕 접한 김에 미리 공부해보기로 했다.

1. 리눅스 다운하기
    CMD나 POWER SHLL을 작업 관리자 권한으로 실행한다.

    배포판 리눅스를 다운한다.

    wsl --install

    자동으로 우분투 창이 열리고 아이디와 비밀번호를 설정한다.

    sudo apt upgrade를 통해 패키지를 최신 상태로 업로드한다. 

2. WSL 환경에 필수 패키지 설치하기
    가장 중요한 부분이다. 블루투스로 신호를 주고 받기 위한 라이브러리를 설치해야한다.

    sudo apt install bluetooth libbluetooth-dev
    
    그 다음 파이썬 환경 설치 
    sudo apt install python3 python3-pip python3-venv 

    ~~파이썬 버전을 따로 정해줘야하나 싶었는데 최신버전으로 알아서 다운된다고 하길래 오류 만들기 싫어서 그냥 다운하기로 했다.~~
    *결국 tensorflow 버전 때문에 오류나서 vscode에서 사용했던 3.7.9로 다시 다운했다. 버전 호환은 항상 중요하다.*

    VSCODE에서 실행했던 가상환경파일을 리눅스에서도 다시 만들어주고 활성화 시켜야한다.

    cd /mnt/c/Users/akthq/OneDrive/Desktop/Last/

    python3 -m venv wsl_venv

    source wsl_venv/bin/activate

    가상환경을 활성화했으면 가상환경에서 pip를 통해 라이브러리를 다운해야한다.

     pip install tensorflow numpy opencv-python

    *tensorflow의 경우 330MB로 용량이 커서 다운이 너무 오래걸렸다.*

3. 파일 실행하기

    파일이 존재하는 폴더로 접근한다. 

    cd /mnt/c/Users/akthq/OneDrive/Desktop/Last

    폴더에 접근하면 파일을 실행한다. 

    python ai.py 






-사소한 부분 


    cmd나 power shell에서 붙여넣기는 마우스 우클릭이다. 

    cmd, power shell를 실수로 닫아서 리눅스 창이 꺼졌다면 wsl를 다시 치면 활성화 된다.

    md 파일을 작성하면서 느낀거지만 사용할 수록 간결하고 사용법만 적응하면 프로젝트 설명이나 코드 설명을 남기기 좋을 것 같다.