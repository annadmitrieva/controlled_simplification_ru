import pandas as pd
import Levenshtein
import argparse
import logging


BUCKET_SIZE = 0.05


def safe_division(a, b):
    return a / b if b != 0 else 0.


def get_bucketed_ratio(value):
    return round(round(value / BUCKET_SIZE) * BUCKET_SIZE, 10)
    
    
def get_length(source, target):
    min_len = min(safe_division(len(target), len(source)), 2) 
    return {'NbChars': get_bucketed_ratio(min_len)}
    
    
def get_levenshtein_similarity(source, target):
    lev_sim = Levenshtein.ratio(source.lower(), target.lower())
    return {'LevSim': get_bucketed_ratio(lev_sim)}
    
    
PREPROCESSORS = {'NbChars': get_length, 'LevSim': get_levenshtein_similarity}

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source')
    parser.add_argument('-o', '--output')
    parser.add_argument('-p', '--processors', help='Available processors: NbChars, LevSim. Separate with comma.')
    
    args = parser.parse_args()
    
    procs = [i.strip() for i in args.processors.split(',')]
    
    with open(args.source, 'r') as f:
        source_lines = f.readlines()
        
    with open(args.output, 'r') as f:
        output_lines = f.readlines()
    
    source_lines = [i.strip() for i in source_lines]
    output_lines = [i.strip() for i in output_lines]
    
    ratios = []
    for s, t in list(zip(source_lines, output_lines)):
        d = {}
        for proc in procs:
            val = PREPROCESSORS[proc](s, t)
            d.update(val)
        ratios.append(d)
        
    ratios_df = pd.DataFrame.from_dict(ratios)
    means = ratios_df.mean()
    logging.warning(means)
    
    
if __name__ == '__main__':
    main()