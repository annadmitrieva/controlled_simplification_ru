import pandas as pd
import argparse


def get_token_names(df):
    control_tokens = []
    for t in ['NbChars', 'LevSim', 'DepTreeDepth', 'CEFRgrade']:
        if t in df.columns:
            control_tokens.append(t)
    return control_tokens
           
            
def add_tag(tag, value, string):
    string = f' <{tag}_{value}> ' + string
    string = string.replace('  ', ' ')
    return string.strip()
    
    
def get_strings_from_df(df, token_names):
    sources = []
    targets = []
    
    for n, row in df.iterrows():
        source = row['source']
        for token in token_names:
            source = add_tag(token, row[token], source)
        sources.append(source)
        targets.append(row['target'])
    
    return sources, targets
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-s', '--source')
    parser.add_argument('-t', '--target')
    
    args = parser.parse_args()
    
    df = pd.read_csv(args.file)
    token_names = get_token_names(df)
    
    sources, targets = get_strings_from_df(df, token_names)
    
    with open(args.source, 'w') as f:
        for line in sources:
            f.write(line)
            f.write('\n')
            
    with open(args.target, 'w') as f:
        for line in targets:
            f.write(line)
            f.write('\n')
            
            
if __name__=='__main__':
    main()