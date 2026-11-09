"""Export a classifier using the existing notebook's training functions."""
import ast
import json
from pathlib import Path


def main():
    import pandas as pd
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, set_seed
    from datasets import Dataset
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score
    import numpy as np

    scope = dict(locals())
    scope.update(MAX_LENGTH=256)
    notebook = json.loads(Path('takemeter.ipynb').read_text())
    wanted = {'split_dataset', 'to_ids', 'compute_metrics', 'train_model'}
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        tree = ast.parse(''.join(cell['source']))
        tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
        if tree.body:
            exec(compile(tree, 'takemeter.ipynb', 'exec'), scope)
    labels = ['experience', 'argument', 'assertion', 'chatter']
    train, val, _ = scope['split_dataset'](pd.read_csv('labels.csv'), 42)
    trainer, tokenizer = scope['train_model'](
        train, val, labels, 42, 3, 2e-5, 16, 'distilbert-base-uncased')
    destination = Path('models/takemeter')
    trainer.save_model(str(destination))
    tokenizer.save_pretrained(str(destination))
    (destination / 'run_config.json').write_text(json.dumps({'max_length': 256, 'seed': 42}))
    print(f'Exported {sum(p.stat().st_size for p in destination.iterdir() if p.is_file())} bytes to {destination}')


if __name__ == '__main__':
    main()
