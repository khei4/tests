import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# open v-cmp.csv by pandas and plot and show by seaborn
df = pd.read_csv("v-cmp.csv")
print(df)
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
# sns.histplot(df, x="after-vecmut-AVX512SLPInstructionsCnt", color="orange")
# sns.histplot(df, x="after-vecmut-SVESLPInstructionsCnt", color="blue")
sns.histplot(
    df,
    x="after-vecmut-AVX512LVVectorizedCnt",
    color="red",
    alpha=0.3,
)
sns.histplot(
    df,
    x="after-vecmut-SVELVVectorizedCnt",
    color="blue",
    alpha=0.3,
)
# sns.histplot(df, x="after-vecmut-SVELVVectorizedCnt", color="blue")
# sns.histplot(df, x="pre-vecmut-AVX512SLPInstructionsCnt", color="orange")
# sns.histplot(df, x="pre-vecmut-AVX512SLPInstructionsCnt", color="orange")
# sns.scatterplot(x="Age", y="Fare", hue="Survived", data=df)
plt.show()
