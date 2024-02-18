#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items
from rpy2 import robjects
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

# R의 metaSEM 패키지 설치 및 라이브러리 로드
robjects.r('if(!requireNamespace("metaSEM", quietly = TRUE)) install.packages("metaSEM")')
robjects.r('library("metaSEM")')

# Streamlit 앱 구성
st.sidebar.title('Meta-Analysis')
st.sidebar.write('개발-이학박사 김우진, 현재 인공지능 개발자로 재직중')
st.sidebar.write('통계강의문의 mystatsolve@gmail.com')
st.sidebar.write('강의 및 컨설팅분야-구조방정식 모형분석')
tab1, tab2 = st.tabs(['OR-RE', 'Tab B'])

# Tab A 내용 가상환경 py39
with tab1:
    st.title("Odds ratio : Random Effect model")

    # 사용자로부터 데이터 프레임 입력 받기
    uploaded_file = st.file_uploader("CSV 파일 업로드", type=['csv'])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        # 입력 데이터 프레임 확인
        st.write("#데이터 프레임에는 효과크기(log of the odds ratio)와 샘플링 분산이 포함되어야 함")
        st.write("#효과크기는 yi, 샘플링 분산은 vi로 표기되어야 함")
        st.write("입력 데이터 프레임:")
        st.write(data)

        # pandas 데이터프레임을 R 데이터프레임으로 변환
        with localconverter(robjects.default_converter + pandas2ri.converter):
            r_data = robjects.conversion.py2rpy(data)
        
        # R 환경에 데이터 할당
        robjects.globalenv['r_data'] = r_data
        
        # R 코드 실행
        mak1 = robjects.r('mak1<-meta(y=yi, v=vi,data=r_data)')
        summary2 = robjects.r('summary(mak1)')
        summary3 = str(summary2)
        
        # 결과 출력
        st.write("R 코드 실행 결과:")
        st.text_area("R summary", summary3, height=300)
        

# Tab B 내용
with tab2:
    st.write('진행중')
