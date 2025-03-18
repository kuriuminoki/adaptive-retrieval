import argparse
import pandas as pd
from tqdm import tqdm
import multiprocessing


def func(args, parallel):
    print('args={}, parallel={}'.format(args, parallel))

def main():
    for i in range(1, 10):
        for i in range(11, 20):
            print(i)


if __name__ == "__main__":
    main()

