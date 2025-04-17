import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_spop(result_path):
    """
    propごとの人気度の分布をプロットする。
    """
    print("plot_spop")
    result = pd.read_csv(result_path)
    props = result.prop.unique()
    for prop in props:
        prop_result = result[result.prop == prop].copy() # 特定のpropのみ抽出

        log_pop = np.log(prop_result["s_pop"].values)
        prop_result["log_pop"] = log_pop
        ser = log_pop
        _, bin_edges = np.histogram(ser) # 人気度の範囲
        width = 0.4*(bin_edges[1] - bin_edges[0])

        # 中間データ
        vanilla_inc = prop_result[prop_result.is_correct == 'FALSE'].copy()
        vanilla_c = prop_result[prop_result.ret_is_correct == 'TRUE'].copy()

        # 各クラスタのデータを抽出
        both_inc = vanilla_inc[vanilla_inc.ret_is_correct == 'FALSE'].copy()
        only_vanilla_c = vanilla_c[vanilla_inc.ret_is_correct == 'FALSE'].copy()
        only_ret_c = vanilla_inc[vanilla_c.ret_is_correct == 'TRUE'].copy()
        both_c = vanilla_c[vanilla_c.ret_is_correct == 'TRUE'].copy()

        hist_only_vanilla_c = np.histogram(only_vanilla_c, bins=bin_edges)
        hist_only_ret_c = np.histogram(only_ret_c, bins=bin_edges)

        # ブルーバー：vanilla 縦軸が正解率、横軸が人気度の対数
        plt.bar(bin_edges[:-1] - 0.5 * width, hist_only_vanilla_c, width=width, alpha=0.9, label="only_vanilla_correct", align='edge', hatch='//')
        plt.bar(bin_edges[:-1] - 0.5 * width, hist_only_ret_c, width=width, alpha=0.9, label="only_vanilla_correct", align='edge', hatch='//')
        plt.title(f"{prop}")
    plt.ylim([0,1.01])
    plt.xlabel("log(s_pop)")
    plt.ylabel("n")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    
    if False:
        result_path = '/results/discussion/model=EleutherAI_gpt-neox-20b-input=None-method=vanillaVSBM25-shots=15-n=2000_int8bit.csv'
        plot_spop(result_path)


if __name__ == "__main__":
    main()
