import pandas as pd
import numpy as np


"""
自分用に結果ファイルをいじるプログラム群

実行方法
$ python load_result.py
"""


def calc_total_accuracy(file_path, n1, n2):
    """
    2つの結果ファイルをUNIONする。
    param
        file_path: 結果ファイルのパス(n=の部分を{}にすること。)
        n1:
        n2:
    usage
        file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n={}_int8bit.csv"
        calc_total_accuracy(file_path=file_path, 1000, 2000)
    """
    print("calc_accuracy:")
    result_list = list()

    # n1
    result1 = pd.read_csv(file_path.format(n1))
    print("path: {}, accuracy: {}".format(file_path.format(n1), result1.is_correct.mean()))
    result_list.append(result1)
    
    # n2
    result2 = pd.read_csv(file_path.format(n2))
    print("path: {}, accuracy: {}".format(file_path.format(n2), result2.is_correct.mean()))
    result_list.append(result2)

    # 全ての結果ファイルをUNIONする。
    all_results = pd.concat(result_list)
    print("total accuracy: {}".format(all_results.is_correct.mean()))

    all_results_path = file_path.format("union{}and{}".format(n1, n2))
    print("write file : " + all_results_path)
    all_results = all_results.reset_index(drop=True)
    all_results.to_csv(all_results_path, index=False)


def combine_nonp_para_result(nonparametric_path, parametric_path, n, output_path):
    """
    検索なし・ありの結果をJOINして1つにまとめる。
    param
        nonparametric_path: 検索なしの結果ファイルのパス
        parametric_path: 検索ありの結果ファイルのパス
        n: n=?
        output_path: 出力先
    usage
    """
    print("combine_nonp_para_result")
    nonparametric_path = nonparametric_path.format(n)
    parametric_path = parametric_path.format(n)

    nonpa_result = pd.read_csv(nonparametric_path)
    para_result = pd.read_csv(parametric_path)

    nonpa_result["ret_pred"] = para_result["pred"]
    nonpa_result["ret_prompt"] = para_result["prompt"]
    nonpa_result["ret_generation"] = para_result["generation"]
    nonpa_result["ret_is_correct"] = para_result["is_correct"]
    if "has_answer" in para_result.columns:
        nonpa_result["has_answer"] = para_result["has_answer"]
    if "retrieval_id" in para_result.columns:
        nonpa_result["retrieval_id"] = para_result["retrieval_id"]
    
    output_path = output_path.format(n)
    print("write file : " + output_path)
    nonpa_result = nonpa_result.reset_index(drop=True)
    nonpa_result.to_csv(output_path, index=False)


def extract_only_correct(input_path, output_path):
    """
    vanilla, retの結果が違うデータのみでフィルタリングする。
    input_path: 入力ファイル
    output_path: 抽出結果（フィルタリング結果）の書き込み先
    """
    result = pd.read_csv(input_path)
    extracted_result_list = list()

    extracted_result1 = result.copy()
    extracted_result1 = extracted_result1[extracted_result1.is_correct == True]
    extracted_result1 = extracted_result1[extracted_result1.ret_is_correct == False]
    extracted_result_list.append(extracted_result1)

    extracted_result2 = result.copy()
    extracted_result2 = extracted_result2[extracted_result2.is_correct == False]
    extracted_result2 = extracted_result2[extracted_result2.ret_is_correct == True]
    extracted_result_list.append(extracted_result2)

    pd.concat(extracted_result_list).to_csv(output_path, index=False)


def add_log_pop_column(input_path, summary_path, output_path):
    """
    s_popの対数を計算し、そのカラムを追加する。
    また、s_popが閾値より値が大きいかを判定したカラムと閾値のカラムも追加する。
    """
    result = pd.read_csv(input_path)
    log_pop = np.log(result["s_pop"].values)
    result["log_pop"] = log_pop

    result_list = list()
    summary = pd.read_csv(summary_path)
    summary = summary.set_index('prop')
    props = result.prop.unique()
    for prop in props:
        prop_result = result[result.prop == prop].copy()
        threshold = summary.at[prop, "thresnold"]
        prop_result["use_ret"] = prop_result.log_pop < threshold
        prop_result["thresnold"] = threshold
        result_list.append(prop_result)
    
    pd.concat(result_list).to_csv(output_path, index=False)


def main():
    
    # nを2つ指定して結果をUNION
    if False:
        file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n={}_int8bit.csv" # vanilla
        calc_total_accuracy(file_path=file_path, n1=1400, n2=2000)
        file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=BM25-shots=15-n={}_int8bit.csv" # BM25
        calc_total_accuracy(file_path=file_path, n1=1000, n2=2000)

    # 考察用、検索あり・なしのJOIN
    if False:
        # nonp_result_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n={}_int8bit.csv" # vanilla
        # para_result_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=BM25-shots=15-n={}_int8bit.csv" # BM25
        nonp_result_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n=union1400and{}_int8bit.csv" # vanilla
        para_result_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=BM25-shots=15-n=union1000and{}_int8bit.csv" # BM25
        output_path = "results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n={}_int8bit.csv"
        combine_nonp_para_result(nonp_result_path, para_result_path, 2000, output_path)
    
    # 正解状況でフィルタリング
    if False:
        n = 2000
        input_path = f"results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n={n}_int8bit.csv"
        output_path = f"results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n={n}_filter_int8bit.csv"
        print("output_file: {}".format(output_path))
        extract_only_correct(input_path, output_path)
    
    # s_popの対数を計算し、そのカラムを追加する。
    if True:
        n = 2000
        input_path = f"results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n=2000_int8bit.csv"
        summary_path = f"results/discussion/model=EleutherAI_gpt-neox-20b-input=None-shots=15-n=union1400and2000_int8bit-ar_summary.csv"
        output_path = f"results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n=2000_spop_int8bit.csv"
        add_log_pop_column(input_path, summary_path, output_path)


if __name__ == "__main__":
    main()
