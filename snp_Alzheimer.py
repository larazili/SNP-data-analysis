import random
import re
import pandas as pd

def find_snp_by_positions(input_file, desired_positions):
    found_snp_info = []

    with open(input_file, 'r') as f:
        line_number = 0
        for line in f:
            line_number += 1
            columns = line.strip().split('\t')
            if len(columns) >= 3:
                chrom = columns[0]
                position = columns[1]
                snp_info = columns[2]
                
                if position in desired_positions:
                    found_snp_info.append((line_number, chrom, position, snp_info, columns))
    
    return found_snp_info

