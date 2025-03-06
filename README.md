# LEAF

​	This is the code for the LEAF method presented in the paper **Small and Medium-Sized Enterprise Funding Guarantee Assessment via Feature Augmentation with Local Interpretable Model–Agnostic  Explanations**

[中文文档](./README-zh.md)

## **Framework of the proposed model**

​	In this study, we effectively expanded the existing feature set by generating a new augmented feature set (AFS) via LIME. Simultaneously, to fully leverage the prediction results from the original data, we trained a model using the original feature set (OFS), obtaining the corresponding out-of-fold (OOF) prediction probabilities. Two second-stage models were subsequently trained for OFS and AFS. We acquired the filtered sample database and the filtered LIME data (LIME') through feature filtering, which led to the construction of feature-screened datasets, namely, the improved original feature set (OFS') and the enhanced augmented feature set (AFS'). Finally, we merged OFS' and AFS' to construct the final feature set (FFS) and trained the third-stage model. In the prediction stage, we averaged the outputs of the first- and third-stage models to enhance the generalizability, ultimately obtaining the final prediction result.

​	The algorithm employs multiple models for prediction, enhancing both the method's generalizability and its capacity to capture comprehensive information. This approach contributes to the improved performance and stability of the predictive model.

![LIME流程图最新](./LIME流程图最新.png)





## Datasets:

​	If your dataset is a binary dataset, store it in csv format in the binary folder, if it is a multicategorical dataset, store it in the muti_class folder. Here we have taken the dichotomous dataset as an example, which has been stored into a binary file, where the ‘评估资产’ column is the dichotomous label, 1 means pass and 0 means fail.



## RUN code:

python main.py --task=**binary or multi** --model_name=**xgb or lgbm or random_forest** --seed=**A number of your choice, we used 42**   For instance: python main.py  --task=binary --model_name=xgb --seed=42

[./README-zh.md]: 