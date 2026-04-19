import gzip
import shutil
import os

def extract_and_process_vcfs(start_chromosome, end_chromosome, output_dir):
    for chromosome_number in range(start_chromosome, end_chromosome + 1):
        input_gz_file = f'./data/1kGP_high_coverage_Illumina.chr{chromosome_number}.filtered.SNV_INDEL_SV_phased_panel.vcf.gz'
        output_file = f'{output_dir}/chr{chromosome_number}'

        # 만약 압축 해제된 파일이 이미 존재한다면 넘어갑니다.
        if os.path.exists(output_file):
            print(f'{output_file} 파일이 이미 존재합니다. 다음으로 넘어갑니다.')
            continue

        try:
            # .gz 파일 열기
            with gzip.open(input_gz_file, 'rb') as f_in:
                # 압축 해제된 데이터를 출력 파일에 쓰기
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                     
            print(f'{input_gz_file} 파일을 압축 해제하여 {output_file}에 저장했습니다.')
        except FileNotFoundError:
            # 파일이 존재하지 않으면 예외 처리
            print(f'{input_gz_file} 파일이 존재하지 않습니다. 다음으로 넘어갑니다.')


