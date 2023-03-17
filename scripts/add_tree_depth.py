from deeppavlov import build_model, configs
from conllu import parse_tree_incr
import networkx as nx
from nltk.parse import DependencyGraph
from networkx.algorithms.dag import dag_longest_path_length
import pandas as pd
import datetime
from razdel import sentenize

model = build_model("ru_syntagrus_joint_parsing")


def get_sentences(text):
    sents = list(sentenize(text))
    return [_.text for _ in sents]


def get_conllu(sentence):
  text = '# text = ' + sentence
  parsed = model([sentence])
  return '\n'.join([text, parsed[0]])
  
  
def get_synt_tree(conllu_sent):
  tree = [line for line in conllu_sent.split('\n') if line and line[0] != '#']
  return '\n'.join(tree)
  
  
def write_tree(tree, file):
    with open(file, 'a') as f:
        f.write(tree)
        f.write('\n\n')
  
  
def get_tree_depth(text):
    try:
        paths = 0
        sentences = get_sentences(text)
        for sentence in sentences:
            parsed = get_conllu(sentence)
            tree = get_synt_tree(parsed)
            d = DependencyGraph(tree)
            # optional if you want to keep the trees
            write_tree(tree, file)
            path_len = dag_longest_path_length(d.nx_graph())
            paths += path_len
        return paths/len(sentences) if len(sentences) > 0 else 0
    except Exception as e:
        print(str(e))
        print(sentence)
        return None
    