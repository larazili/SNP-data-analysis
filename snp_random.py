import os
import random
import re
import pandas as pd
import pandas as pd

# 랜덤으로 데이터 뽑기
def find_snp_by_positions(input_file, num_snp_to_find):
    found_snp_info = []

    with open(input_file, 'r') as f:
        lines = f.readlines()

        random_positions = random.sample(range(len(lines)), num_snp_to_find)

        for line_number in random_positions:
            line = lines[line_number].strip()
            columns = line.split('\t')
            if len(columns) >= 3:
                chrom = columns[0]
                position = columns[1]
                snp_info = columns[2]
                found_snp_info.append((line_number + 1, chrom, position, snp_info, columns))
    
    return found_snp_info

# 범주별로 적당한 수치로 변환
def convert_genotype(genotype):
    if genotype == '0|0':
        return 0
    elif genotype == '0|1' or genotype == '1|0':
        return 0.5
    elif genotype == '1|1':
        return 1

# 뽑은 데이터의 컬럼명 지정 및 데이터 프레임으로 데이터 저장
def create_dataframe(result, start_idx):
    data = {}
    num_snps = len(result)
    
    for idx, (_, _, position, _, columns) in enumerate(result, start=start_idx):
        snp_name = f'snp_{position}'  # 컬럼명을 포지션으로 설정
        genotype_values = [convert_genotype(genotype) for genotype in columns[9:]]
        
        data[snp_name] = genotype_values

    df = pd.DataFrame(data)
    return df

def process_chromosome(chromosome_number, num_files=10):
    # 디렉토리 생성 (이미 존재하면 무시됨)
    output_dir = f'./data/snp_{chromosome_number}/'
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, num_files + 1):
        # 사용 예시
        input_file = f'./data/chr{chromosome_number}'  # 실제 파일 경로로 변경하세요.
        num_snp_to_find = 1000
        result = find_snp_by_positions(input_file, num_snp_to_find)

        # 데이터프레임 생성
        snp_i = create_dataframe(result, start_idx=1)

        # 파일 저장
        output_file = f'{output_dir}snp_{chromosome_number}_{i}.csv'
        snp_i.to_csv(output_file, index=False)

def merge_snp_data(chromosome_number, num_files=10):
    # 빈 데이터프레임 생성하여 합친 데이터 초기화
    merged_snp_data = pd.DataFrame()

    for i in range(1, num_files + 1):
        file_name = f'./data/snp_{chromosome_number}/snp_{chromosome_number}_{i}.csv'
        df = pd.read_csv(file_name)
        merged_snp_data = pd.concat([merged_snp_data, df], axis = 1)
    merged_snp_data.to_csv(f'./data/snp_{chromosome_number}_10000.csv')

