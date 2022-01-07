# 비트코인 자동매매 프로그램
- 본 프로그램은 "유튜브 조코딩 채널 (https://youtu.be/7lFbKTVzj1c)"을 참고하여 제작하였음을 밝힘
### 개발환경
- --
- Windows 11 (64bit)
- Intel i7-12700K
- DDR5 4800MHz 8 * 2GB
- nVidia RTX 3070
- Python 3.8.5 & PyCharm CE 2021.3
- Visual Studio 14+, CMake 필요

### 최초 실행 전 환경 구축
- --
1. (필요 시) 가상환경 구축 권장
2. 아나콘다 설치
3. Terminal에서 <code>pip install -r requirements.txt</code> 실행하여 기본 라이브러리 설치
4. Terminal에서 <code>conda install -c conda-forge fbprophet</code> 실행하여 페이스북 Prophet 라이브러리 설치
5. Terminal에서 <code>pip install pystan --upgrade</code> 실행하여 pystan 업데이트
6. (만약 pystan 설치에 문제가 있을 경우) <code>http://files.pythonhosted.org/packages/e3/7b/ba001a1e29e297a033c6a110ab80914bc4a2ed0a1aaec4c0224d56dfbbfe/pystan-2.19.1.1-cp38-cp38-win_amd64.whl
</code> 접속하여 whl 파일 다운로드 및 pip 설치
7. <code>static/upbit_keys.txt</code> 내 개인별 키 변경(탭문자 주의) 후 저장
8. 이후 <code>application.py</code> 파일 실행