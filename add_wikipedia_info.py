"""
  Wikipediaの情報をresultファイル(csv)にカラムとして追加する。
"""
import pandas as pd

from get_wikipedia import get_page_history_counts

import time


def add_page_history_counts(input_path, output_path):

    count_type = "edits"

    result = pd.read_csv(input_path)

    page_history_counts = list()
    titles = result.s_wiki_title

    for title in titles:
        fix_title = title.replace(' ', '_')
        page_history_counts.append(get_page_history_counts(fix_title, count_type))
        time.sleep(0.01)

    result["page_history_counts"] = page_history_counts
    result.to_csv(output_path, index=False)


def main():
    input_path = "results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n=2000_spop_int8bit.csv"
    output_path = "results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n=2000_spop_int8bit_phc.csv"
    add_page_history_counts(input_path, output_path)


if __name__ == "__main__":
    main()
