import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# open v-cmp.csv by pandas and plot and show by seaborn
df = pd.read_csv("v-cmp-10000.csv")
# pre-vecmut-SVELVAnalyzedCnt,
# pre-vecmut-SVELVVectorizedCnt,
# pre-vecmut-SVEEPVectorizedCnt,
# pre-vecmut-SVESLPInstructionsCnt,
# pre-vecmut-AVX512LVAnalyzedCnt,
# pre-vecmut-AVX512LVVectorizedCnt,
# pre-vecmut-AVX512EPVectorizedCnt,
# pre-vecmut-AVX512SLPInstructionsCnt,
# after-vecmut-SVELVAnalyzedCnt,
# after-vecmut-SVELVVectorizedCnt,
# after-vecmut-SVEEPVectorizedCnt,
# after-vecmut-SVESLPInstructionsCnt,
# after-vecmut-AVX512LVAnalyzedCnt,
# after-vecmut-AVX512LVVectorizedCnt,
# after-vecmut-AVX512EPVectorizedCnt,
# after-vecmut-AVX512SLPInstructionsCnt
StatsDic = {
    "SLP": "SLPInstructionsCnt",
    "LV Loop Num": "LVVectorizedCnt",
    "LV Analyzed Num": "LVAnalyzedCnt",
    "LV EP": "EPVectorizedCnt",
}
Descriptions = {
    "SLP": "Instructions vectorized by SLPVectorizer",
    "LV Loop Num": "Loops vectorized by LoopVectorize",
    "LV Analyzed Num": "Loops analyzed by LoopVectorize",
    "LV EP": "Epilogue Loops vectorized by LoopVectorize",
}

FileNames = {
    "SLP": "v-mut-slp-instructions-histogram.png",
    "LV Loop Num": "v-mut-lv-vectorized-histogram.png",
    "LV Analyzed Num": "v-mut-lv-analyzed-histogram.png",
    "LV EP": "v-mut-lv-epilogue-vectorized-histogram.png",
}
# plot the differences of analyzed loops by LoopVectorizer
# mode = "LV Analyzed Num"
# # plot the differences of EP vectorized by LoopVectorizer
# mode = "LV EP"

# plot the differences  of vectorized loops by LoopVectorizer
# mode = "LV Loop Num"
# # plot the differences of vectorized instructions by SLPVectorizer
mode = "SLP"

print("mode = ", mode)


# SLPVectorizer difference between avx512 ans sve for pre and after
pre_sve_label = "pre-vecmut-SVE" + StatsDic[mode]
after_sve_label = "after-vecmut-SVE" + StatsDic[mode]
pre_avx512_label = "pre-vecmut-AVX512" + StatsDic[mode]
after_avx512_label = "after-vecmut-AVX512" + StatsDic[mode]

pre_sve_more_vectorized_df = df[df[pre_avx512_label] < df[pre_sve_label]]
pre_avx512_more_vectorized_df = df[df[pre_avx512_label] > df[pre_sve_label]]

after_sve_more_vectorized_df = df[df[after_avx512_label] < df[after_sve_label]]
after_avx512_more_vectorized_df = df[df[after_avx512_label] > df[after_sve_label]]

only_pre_df = df[
    (df[pre_avx512_label] != df[pre_sve_label])
    & (df[after_avx512_label] == df[after_sve_label])
]
only_after_df = df[
    (df[pre_avx512_label] == df[pre_sve_label])
    & (df[after_avx512_label] != df[after_sve_label])
]
# print(
#     only_pre_df[[pre_avx512_label, pre_sve_label, after_avx512_label, after_sve_label]]
# )
# print(
#     only_after_df[
#         [pre_avx512_label, pre_sve_label, after_avx512_label, after_sve_label]
#     ]
# )

print(
    "before vecmut total diff num: ",
    len(pre_sve_more_vectorized_df) + len(pre_avx512_more_vectorized_df),
)
print("before vecmut num sve wins: ", len(pre_sve_more_vectorized_df))
print("before vecmut num avx512 wins: ", len(pre_avx512_more_vectorized_df))

print(
    "after vecmut total diff num: ",
    len(after_sve_more_vectorized_df) + len(after_avx512_more_vectorized_df),
)
print("after vecmut num sve wins: ", len(after_sve_more_vectorized_df))
print("after vecmut num avx512 wins: ", len(after_avx512_more_vectorized_df))

print("diff lost by vecmut: ", len(only_pre_df))
print("diff found only if vecmut: ", len(only_after_df))

# sns.histplot(
#     df,
#     x=pre_label,
#     color="blue",
#     alpha=0.3,
#     binwidth=1,
#     # bins=200,
#     # stat="density",
# )
# sns.histplot(
#     df,
#     x=after_label,
#     color="red",
#     alpha=0.3,
#     binwidth=1,
#     # bins=200,
#     # stat="density",
# )

# XLims = {
#     "SLP": 15,
#     "LV Loop Num": 20,
#     "LV Analyzed Num": 60,
#     "LV EP": 60,
# }
# plt.xlim(0, XLims[mode])
# YLims = {
#     "SLP": 10000,
#     "LV Loop Num": 10000,
#     "LV Analyzed Num": 700,
#     "LV EP": 10000,
# }
# plt.ylim(0, YLims[mode])
# # set title as
# plt.title("10000 times generation and mutation")
# # set x-axis label as
# plt.xlabel(Descriptions[mode])
# # put the average value of df[pre_label] amd df[after_label]on the graph
# plt.axvline(df[pre_label].mean(), color="blue", linestyle="dashed", linewidth=1)
# plt.axvline(
#     df[after_label].mean(),
#     color="red",
#     linestyle="dashed",
#     linewidth=1,
# )
# # set y-axis label as
# plt.ylabel("The number of test cases(normalized)")
# plt.legend(
#     labels=[
#         "Mean Before Mutation",
#         "Mean After Mutation",
#         "Before VecMut",
#         "After VecMut",
#     ]
# )
# # save as png
# # from matplotlib.ticker import MaxNLocator
# plt.xticks(range(0, XLims[mode], 5))

# # ax = plt.figure().gca()
# # ax.yaxis.set_major_locator(MaxNLocator(integer=True))
# plt.savefig(FileNames[mode])
# plt.show()
