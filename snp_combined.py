import pandas as pd

def combine_snp_data(start, end):
    snp = pd.DataFrame()

    # 파일을 순회하며 데이터 합치기
    for i in range(start, end+1):
        file_name = f'./data/snp_{i}_10000.csv'
        df = pd.read_csv(file_name)
        df = df.add_prefix(f'chr{i}_') 
        snp = pd.concat([snp, df], axis=1)

    return snp

def del_col(data, start, end):
    for i in range(start, end+1):
        data = data.drop(columns=f'chr{i}_Unnamed: 0')
        
    return data

