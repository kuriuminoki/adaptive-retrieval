import pandas as pd


"""
自分用に結果ファイルをいじるプログラム群

実行方法
$ python load_result.py
"""

@DeprecationWarning
def calc_total_accuracy(file_path, n, start_n, end_n):
    """
    結果ファイルをUNIONする。[start_n, end_n]の範囲で結果ファイルを見る。
    param
        file_path: 結果ファイルのパス(n=の部分を{}にすること。)
        n: 何件ごとにファイルを分けているか
        start_n: 開始のn
        end_n: 終了のn
    usage
        # n={}として、後で代入する。
        file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n={}_int8bit.csv" # vanilla
        # file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=BM25-shots=15-n={}_int8bit.csv" # BM25
        calc_total_accuracy(file_path=file_path, n=100, start_n=100, end_n=1000)
    """
    print("calc_accuracy:")
    result_list = list()
    for i in range(start_n, end_n + 1, n):
        path = file_path.format(i)
        result = pd.read_csv(path)
        print("path: {}, accuracy: {}".format(path, result.is_correct.mean()))
        result_list.append(result)
    # 全ての結果ファイルをUNIONする。
    all_results = pd.concat(result_list)
    print("path: {}, accuracy: {}".format(file_path, all_results.is_correct.mean()))

    all_results_path = file_path.format("union{}-{}".format(start_n, end_n))
    print("write file : " + all_results_path)
    all_results.to_csv(all_results_path)


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
    all_results.to_csv(all_results_path)


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
    nonpa_result.to_csv(output_path)


def main():

    # nを範囲指定して結果をUNION
    if False:
        # n={}として、後で代入する。
        file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n={}_int8bit.csv" # vanilla
        # file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=BM25-shots=15-n={}_int8bit.csv" # BM25
        calc_total_accuracy(file_path=file_path, n=100, start_n=100, end_n=1000)
    
    # nを2つ指定して結果をUNION
    if False:
        file_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n={}_int8bit.csv" # vanilla
        calc_total_accuracy(file_path=file_path, n1=1400, n2=2000)

    # 考察用、検索あり・なしのJOIN
    if True:
        nonp_result_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=vanilla-shots=15-n={}_int8bit.csv" # vanilla
        para_result_path = "results/temp/model=EleutherAI_gpt-neox-20b-input=None-method=BM25-shots=15-n={}_int8bit.csv" # BM25
        output_path = "results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n={}_int8bit.csv"
        combine_nonp_para_result(nonp_result_path, para_result_path, 1000, output_path)


if __name__ == "__main__":
    main()
