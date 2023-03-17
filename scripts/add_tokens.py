import pandas as pd
import Levenshtein
import argparse


BUCKET_SIZE = 0.05


def safe_division(a, b):
    return a / b if b != 0 else 0.


def get_bucketed_ratio(value):
    return round(round(value / BUCKET_SIZE) * BUCKET_SIZE, 10)
    
    
def get_length(row):
    min_len = min(safe_division(len(row['target']), len(row['source'])), 2) 
    return {'NbChars': get_bucketed_ratio(min_len)}
    
    
def get_levenshtein_similarity(row):
    lev_sim = Levenshtein.ratio(row['source'].lower(), row['target'].lower())
    return {'LevSim': get_bucketed_ratio(lev_sim)}
    
    
def get_tree_depth_ratio(row):
    depth = min(safe_division(row['target_tree_depth'], row['source_tree_depth']), 2)
    return {'DepTreeDepth': get_bucketed_ratio(depth)}
    
    
def get_cefr_level(row):
    return {'CEFRgrade': row['target_level']}
    
    
PREPROCESSORS = {'NbChars': get_length, 'LevSim': get_levenshtein_similarity, 'DepTreeDepth': get_tree_depth_ratio, 'CEFRgrade': get_cefr_level}


def add_tags_to_df(df, preprocessors):
    new_rows = []
    for n, row in df.iterrows():
        new_row = {}
        for p in preprocessors:
            val = PREPROCESSORS[p](row)
            new_row.update(val)
        new_rows.append(new_row)
    rows_to_add = pd.DataFrame(new_rows)
    new_df = pd.concat([df, rows_to_add], axis=1)
    return new_df
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source')
    parser.add_argument('-o', '--output')
    parser.add_argument('-p', '--processors', help='Available processors: NbChars, LevSim, DepTreeDepth, CEFRgrade. Separate with comma.')
    
    args = parser.parse_args()
    
    procs = [i.strip() for i in args.processors.split(',')]
    
    df = pd.read_csv(args.source)
    df_aug = add_tags_to_df(df, procs)
    df_aug.to_csv(args.output, index=False)
    
    
if __name__ == '__main__':
    main()