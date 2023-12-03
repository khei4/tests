import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# open v-cmp.csv by pandas and plot and show by seaborn
df = pd.read_csv("v-mut.csv")
# pre-vecmut-AVX512LVAnalyzedCnt,
# pre-vecmut-AVX512LVVectorizedCnt,
# pre-vecmut-AVX512EPVectorizedCnt,
# pre-vecmut-AVX512SLPInstructionsCnt,
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

# plot the differences  of analyzed loops by LoopVectorizer
# mode = "LV Loop Num"
# plot the differences of vectorized loops by LoopVectorizer
# mode = "LV Analyzed Num"
# # plot the differences of vectorized instructions by SLPVectorizer
mode = "SLP"
# # plot the differences of EP vectorized by LoopVectorizer
# mode = "LV EP"


pre_label = "pre-vecmut-AVX512" + StatsDic[mode]
after_label = "after-vecmut-AVX512" + StatsDic[mode]
filtered_df = df[df[pre_label] < df[after_label]]
print(len(filtered_df))

sns.histplot(
    filtered_df,
    x=pre_label,
    color="blue",
    alpha=0.3,
)
sns.histplot(
    filtered_df,
    x=after_label,
    color="red",
    alpha=0.3,
)
# set title as popop
plt.title("1000 times generation and mutation")
# set x-axis label as popop
plt.xlabel("The number of instructions SLP Vectorizer vectorized")
# set y-axis label as popop
plt.ylabel("The number of test cases")
plt.legend(labels=["Before VecMut", "After VecMut"])
# save as png
plt.savefig("v-cmp.png")
plt.show()
