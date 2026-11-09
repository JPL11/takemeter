"""Classify JSON lines from stdin; append durable JSONL observations."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time


class Classifier:
    def __init__(self, model_path):
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
        self.model.eval()
        self.max_length = json.loads((Path(model_path) / 'run_config.json').read_text())['max_length']

    def predict(self, text):
        tokens = self.tokenizer(text, truncation=True, padding='max_length', max_length=self.max_length, return_tensors='pt')
        with self.torch.inference_mode():
            probabilities = self.model(**tokens).logits.softmax(dim=-1)[0]
        index = int(probabilities.argmax())
        return {'label': self.model.config.id2label[index], 'confidence': float(probabilities[index])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='models/takemeter')
    parser.add_argument('--log', default='logs/runs.jsonl')
    args = parser.parse_args()
    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    classifier = None
    failed = False
    with log_path.open('a', encoding='utf-8') as log:
        for line in sys.stdin:
            start, cpu = time.perf_counter(), time.process_time()
            record = {'timestamp': datetime.now(timezone.utc).isoformat(), 'input': line.rstrip('\n'), 'output': None, 'status': 'error'}
            try:
                request = json.loads(line)
                record['input'] = request
                if not isinstance(request, dict) or not isinstance(request.get('text'), str) or not request['text'].strip():
                    raise ValueError('Request must be an object with nonempty string text')
                if classifier is None:
                    classifier = Classifier(args.model)
                record['output'] = classifier.predict(request['text'])
                record['status'] = 'ok'
            except Exception as exc:
                failed = True
                record['error'] = {'type': type(exc).__name__, 'message': str(exc)}
            record['duration_ms'] = round((time.perf_counter() - start) * 1000, 3)
            record['cpu_seconds'] = round(time.process_time() - cpu, 6)
            log.write(json.dumps(record, ensure_ascii=False) + '\n')
            log.flush()
            print(json.dumps(record, ensure_ascii=False), flush=True)
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
