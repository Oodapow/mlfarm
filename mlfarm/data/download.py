from bing_image_downloader import downloader
import argparse
import os

def assert_test(x):
    assert x

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default=os.path.abspath(os.path.join(__file__, '..', 'keywords.list')), type=lambda x: [assert_test(os.path.isfile(x)), x][-1])
    parser.add_argument('-l', '--limit', default=100, type= lambda x: [int(x), assert_test(x>0), x][-1])
    parser.add_argument('-d', '--dataset', default='dataset', type=lambda x: [assert_test(not os.path.isdir(x)), x][-1])
    parser.add_argument('-t', '--timeout', default=60, type= lambda x: [int(x), assert_test(x>0), x][-1])
    args = parser.parse_args()

    print(args)
    
    with open(args.file, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    for line in lines:
        downloader.download(line, limit=args.limit,  output_dir=args.dataset, adult_filter_off=True, force_replace=False, timeout=args.timeout)