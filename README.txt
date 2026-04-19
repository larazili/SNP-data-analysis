1. 제출파일 목록
(ipynb파일을 모듈(.py)로 만들어서 한 번에 실행할 수 있게 함)
[1]  코드 실행 방법 설명
  1) README.txt : 코드 실행 방법 설명

[2] 코드 파일 모듈 변경 (ipynb -> py) 
  1) data_gzip.py : 크로모좀 3202명의 snp정보가 담긴 압축 파일 해제하는 파일
  2) snp_Alzheimer.py : 알츠하이머 관련 snp 데이터 프레임 생성하는 파일
  3) snp_random.py : 랜덤 snp 데이터 프레임 생성하는 파일
  4) snp_combined.py : snp_Alzheimer.py 에서 만든 알츠하이머 관련 snp 데이터 프레임과 
                       snp_random.py 에서 만든 랜덤 snp 데이터 프레임을 합쳐서 하나의 데이터 프레임으로 만드는 파일
  5) modeling.py : snp_combined.py를 통해 만든 snp 데이터 프레임을 통해 support vector machine, ridge, decision tree, randomforest, xgboost 모델을
                   학습하고 정확도 비교 후 중요 상관변수 snp 100개를 뽑아 모델 별로 겹치는 snp 확인하는 파일
  6) map_visualization.py : support vector machine 모델의 상관관계 높은 snp 100개 중 알츠하이머 관련 snp의 지역별 비율을 확인한 후 
                            지도로 시각화하는 파일
  7) Trio.py : Trio데이터를 활용해 de novo variant 분석하는 파일

[3]데이터 폴더
  1) 1kGP_high_coverage_Illumina.chr16.filtered.SNV_INDEL_SV_phased_panel.vcf.gz : 데이터전처리 과정을 보여주기 위한 예시 파일1
  2) 1kGP_high_coverage_Illumina.chr17.filtered.SNV_INDEL_SV_phased_panel.vcf.gz : 데이터전처리 과정을 보여주기 위한 예시 파일2
  3) human_info.tsv : 사람 정보에 대한 데이터 파일
  4) parents.txt : 부모 정보에 대한 데이터 파일
  5) Region_info.tsv : 지역 정보에 대한 데이터 파일
  6) snp_20.csv : 모델링 및 분석, 예측에 사용하기 위한 정리된 파일
  7) World_Countries__Generalized_.geojson : 지도를 그리기 위해 필요한 파일

[4] 실행 파일 
1) 실행파일.ipynb : 모듈로 저장한 코드를 실행하여 결과를 확인하는 파일


2. Data 획득 방법
우리는 1000genomes에서 공개된 유전체 데이터를 사용한다.
 - http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20220422_3202_phased_SNV_INDEL_SV/
    위 사이트를 통해 파일을 모두 다운 받고 실행파일에 1~3번 과정을 통해 원하는 snp 정보를 선택해 데이터프레임 형태로 만들러 저장한다.
 - 위의 방법으로 chr1부터 chr22까지 데이터를 모두 다운로드하면 시간이 오래 걸리기 때문에, 실행파일 1~3번 과정 실행 예시로 chr16과 chr17 압축 파일을 제공하였고 실행파일 4~7번 과정 실행을 위해 chr1부터 chr22까지 1~3번 과정 처리가 다 된 데이터인 snp_20.csv 또한 제출파일에 포함한다.
 
1000genomes에서 사람 정보와 지역 정보 데이터를 사용한다.
 - https://www.internationalgenome.org/data-portal/data-collection/30x-grch38

1000genomes에서 부모 정보 데이터를 사용한다.
 - http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/1kGP.3202_samples.pedigree_info.txt 

World Countries Generalized에서 국가 경계 정보가 담긴 GeoJSON 파일 사용한다.
 - https://hub.arcgis.com/datasets/esri::world-countries-generalized/explore
 
3. 실행 필요 프로그램과 라이브러리
  1) python
  2) jupyter notebook 혹은 jupyter lab
  3) 코드 실행에 필요한 파이썬 라이브러리
    - seaborn
    - folium
    - pandas
    - numpy
    - matplotlib
    - sklearn.preprocessing
    - os
    - re
    - random
    - json
    - data_gzip
    - snp_Alzheimer
    - snp_random
    - snp_combined
    - modeling
    - map_visualization
    - Trio
  (파이썬 라이브러리들은 코드를 실행하면 설치할 수 있음(별도 설치 불필요)


4. 실행방법
제출한 데이터 파일들을 사용하는 경우(데이터 다운로드 시간이 절약됨)
  (※ 직접 모든 데이터를 다운로드할 시 전처리 과정에서 1TB 이상의 메모리가 필요하므로 snp_20.csv 데이터 사용을 권장한다.)
  1) 제출한 압축 파일의 압축을 푼다.
  2) 코드 파일(*.ipynb)과 데이터 파일들이 들어있는 'data' 폴더가 동일한 작업 폴더 안에 위치한지 확인한다.
  3) jupyter notebook을 실행하고,
      - 실행파일.ipynb
      을 차례로 실행한다.