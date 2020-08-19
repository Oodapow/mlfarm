import hashlib
import argparse
import os
import json

def assert_test(x):
    assert x

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', default='dataset', type=lambda x: [assert_test(os.path.isdir(x)), x][-1])
    args = parser.parse_args()

    files = {}
    total = 0
    for r,d,f in os.walk(args.dataset):
        for file in f:
            if '.json' in file:
                continue
            fp = os.path.join(r,file)
            k = str(md5(fp))
            if k in files:
                files[k].append(fp)
            else:
                files[k] = [fp]
            total += 1
    
    with open(os.path.join(args.dataset, 'md5.json'), 'w') as f:
        json.dump(files, f, indent=2)