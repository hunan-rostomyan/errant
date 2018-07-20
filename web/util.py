import json
import os

SENTENCE, ANNOTATION = 'S', 'A'

def Empty(line):
    return (line.strip()) == ''

def get_kind(line):
    return line[0]

def get_sentence(line):
    return line[1:].strip()

def get_annotation(line, sep='|||'):
    prefix, etype, edits, required, comment, anid = line.split(sep)
    _, start, end = prefix.split()
    edits = edits.split('||')
    return {
        'start': int(start),
        'end': int(end),
        'error': etype,
        'edits': edits,
        'annotator': int(anid)
    }

def m2_to_json(path, pretty=True):
    try:
        with open(path) as fp:
            gold = {}
            sent, sid = '', 0
            for line in fp:
                if not Empty(line):
                    if get_kind(line) == SENTENCE:
                        sent = get_sentence(line)
                        sid += 1
                    else:
                        if sid not in gold:
                            gold[sid] = {'sentence': sent, 'annotations': []}
                        annotation = get_annotation(line)
                        gold[sid]['annotations'].append(annotation)

        # prepare output
        output = json.dumps(gold, indent=2) if pretty else json.dumps(gold)

        with open(path + '.json', 'w') as fp:
            fp.write(output)

        return gold
    except FileNotFoundError as e:
        print('Unable to write to: {}'.format(path))