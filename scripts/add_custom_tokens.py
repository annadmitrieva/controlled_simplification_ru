import argparse
import json


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def add_token_to_str(string, control_tokens_dict):
    for token, value in control_tokens_dict.items():
        string = f' <{token}_{value}> ' + string
    string = string.replace('  ', ' ')
    return string.strip()
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source')
    parser.add_argument('-t', '--target')
    parser.add_argument('-ct', '--control_tokens', nargs='*', action=ParseKwargs, help="Example: NbChars=0.95 LevSim=0.4")
    
    args = parser.parse_args()
    
    control_tokens = args.control_tokens
    
    with open(args.source, 'r') as f:
        lines = f.readlines()
        
    with open(args.target, 'w') as f:
        for line in lines:
            line = add_token_to_str(line.strip(), control_tokens)
            f.write(line)
            f.write('\n')
 
            
if __name__=='__main__':
    main()