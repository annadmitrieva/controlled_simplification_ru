# controlled_simplification_ru

This repository contains code and supplementary materials for the paper ["Automatic text simplification of Russian texts using control tokens"](https://aclanthology.org/2023.bsnlp-1.9/).

Best mBART model checkpoints can be downloaded from here: https://disk.yandex.com/d/cubPTzFsIFtvxg. 

In the /data folder, you can find lists of ids of sentence pairs from various datasets mentioned in the paper. Using these ids and the information about whether the source and target sentences were swapped (the reversed order), it is possible to construct a dataset identical to the one used in the paper.

The /scripts folder contains the scripts used to add control tokens. The finetuning process for all models was pretty generic. mBART models were finetuned with RuSimpleSentEval's basic solution scripts: https://github.com/dialogue-evaluation/RuSimpleSentEval. T5 models were finetuned similarly to the currently unaccessible scripts for T5 finetuning (https://gist.github.com/avidale/4de1454bf41822dc862fddbd779d4cc6), which are similar to the example solution from this post: https://habr.com/ru/post/564916/, and the inference process was similar to this demo: https://gist.github.com/avidale/dd74f81bbb7e3b57de474b5fb4ca4bd7.
