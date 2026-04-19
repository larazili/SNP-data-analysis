import pandas as pd

# 각 행별로 NaN이 아닌 값을 보여주는 함수
def nonnan_values(row):
        return row[~pd.isna(row)]

def find_nonzero_child_snp_for_father(snp_data, filtered_fatherID):
    # 전체 데이터에서 아빠만 있는 데이터에서 아빠인 행 찾기
    father_id = snp_data[snp_data.index.isin(filtered_fatherID['fatherID'])]
    
    # SNP 정보만 선택
    father_snp = father_id[father_id.columns[:-6]]

    # 0인 SNP 열 찾기
    father_id_zero = father_snp[father_snp == 0]
    father_id_zero_columns = father_id_zero.columns[father_id_zero.notna().any()]
    
    # 찾은 0인 SNP 중 자식은 0이 아닌 SNP 찾기
    filtered_fatherID_snp = filtered_fatherID[filtered_fatherID.columns[:-6]]
    filtered_fatherID_snp = filtered_fatherID_snp[father_id_zero_columns]
    filtered_fatherID_nonzero = filtered_fatherID_snp[filtered_fatherID_snp != 0]
    true_columns = filtered_fatherID_nonzero.columns[filtered_fatherID_nonzero.notna().any()]
    filtered_fatherID_nonzero = filtered_fatherID_nonzero[true_columns]
    filtered_fatherID_nonzero
    
    #자식은 0이 아닌 SNP 중 모두 값이 있는 열 찾기
    true_columns = filtered_fatherID_nonzero.columns[filtered_fatherID_nonzero.notna().any()]
    filtered_fatherID_nonzero = filtered_fatherID_nonzero[true_columns]
    
    return father_id_zero, filtered_fatherID_nonzero

def find_nonzero_child_snp_for_mother(snp_data, filtered_motherID):
    # 전체 데이터에서 엄마만 있는 데이터에서 엄마인 행 찾기
    mother_id = snp_data[snp_data.index.isin(filtered_motherID['motherID'])]
    
    # SNP 정보만 선택
    mother_snp = mother_id[mother_id.columns[:-6]]

    # 0인 SNP 열 찾기
    mother_id_zero = mother_snp[mother_snp == 0]
    mother_id_zero_columns = mother_id_zero.columns[mother_id_zero.notna().any()]
    
    # 찾은 0인 SNP 중 자식은 0이 아닌 SNP 찾기
    filtered_motherID_snp = filtered_motherID[filtered_motherID.columns[:-6]]
    filtered_motherID_snp = filtered_motherID_snp[mother_id_zero_columns]
    filtered_motherID_nonzero = filtered_motherID_snp[filtered_motherID_snp != 0]
    true_columns = filtered_motherID_nonzero.columns[filtered_motherID_nonzero.notna().any()]
    filtered_motherID_nonzero = filtered_motherID_nonzero[true_columns]
    
    # 자식은 0이 아닌 SNP 중 모두 값이 있는 열 찾기
    true_columns = filtered_motherID_nonzero.columns[filtered_motherID_nonzero.notna().any()]
    filtered_motherID_nonzero = filtered_motherID_nonzero[true_columns]
    
    return mother_id_zero, filtered_motherID_nonzero

