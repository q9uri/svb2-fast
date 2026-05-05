---
language:
- ja
license: apache-2.0
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:15098874
- loss:MatryoshkaLoss
- loss:MultipleNegativesRankingLoss
pipeline_tag: sentence-similarity
library_name: sentence-transformers
metrics:
- cosine_accuracy@1
- cosine_accuracy@3
- cosine_accuracy@5
- cosine_accuracy@10
- cosine_precision@1
- cosine_precision@3
- cosine_precision@5
- cosine_precision@10
- cosine_recall@1
- cosine_recall@3
- cosine_recall@5
- cosine_recall@10
- cosine_ndcg@10
- cosine_mrr@10
- cosine_map@100
model-index:
- name: SSE Retrieval MRL
  results:
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoClimateFEVER
      type: NanoClimateFEVER
    metrics:
    - type: cosine_accuracy@1
      value: 0.28
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.5
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.6
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.72
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.28
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.17999999999999997
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.14
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.096
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.11566666666666667
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.259
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.309
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.38366666666666666
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.31101912464080167
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.42077777777777775
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.23472725032298258
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoDBPedia
      type: NanoDBPedia
    metrics:
    - type: cosine_accuracy@1
      value: 0.64
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.9
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.92
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.98
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.64
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.5866666666666667
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.516
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.458
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.06160341544840008
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.16190481698320675
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.2178662941767401
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.3311868598508409
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.5596322526310974
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.7651904761904761
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.39996237625484127
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoFEVER
      type: NanoFEVER
    metrics:
    - type: cosine_accuracy@1
      value: 0.34
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.6
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.68
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.82
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.34
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.2
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.14
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.08599999999999998
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.33
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.5566666666666668
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.6466666666666667
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.7866666666666667
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.5611230907066518
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.5003333333333334
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.49227582231970923
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoFiQA2018
      type: NanoFiQA2018
    metrics:
    - type: cosine_accuracy@1
      value: 0.28
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.4
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.48
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.64
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.28
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.16666666666666663
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.12400000000000003
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.088
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.17600000000000002
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.2701904761904762
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.30707936507936506
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.4077460317460318
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.32472050466088326
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.37310317460317455
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.26922263832673005
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoHotpotQA
      type: NanoHotpotQA
    metrics:
    - type: cosine_accuracy@1
      value: 0.52
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.6
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.64
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.72
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.52
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.26
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.17199999999999996
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.10800000000000001
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.26
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.39
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.43
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.54
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.4795069124741789
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.5758333333333333
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.41822608557151697
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoMSMARCO
      type: NanoMSMARCO
    metrics:
    - type: cosine_accuracy@1
      value: 0.22
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.36
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.44
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.6
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.22
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.11999999999999998
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.08800000000000002
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.06000000000000001
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.22
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.36
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.44
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.6
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.3845438350481858
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.3190793650793651
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.3335241736823179
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoNFCorpus
      type: NanoNFCorpus
    metrics:
    - type: cosine_accuracy@1
      value: 0.38
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.54
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.54
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.62
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.38
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.32666666666666666
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.26
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.214
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.021377385454146837
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.07632083549405319
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.08294525764762037
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.12132329911306272
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.2736049434105412
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.4543809523809523
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.10136232337644312
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoNQ
      type: NanoNQ
    metrics:
    - type: cosine_accuracy@1
      value: 0.24
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.4
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.56
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.68
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.24
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.13333333333333333
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.11200000000000002
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.07200000000000001
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.22
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.37
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.51
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.65
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.42175811202298474
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.3658015873015873
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.35721440136770855
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoQuoraRetrieval
      type: NanoQuoraRetrieval
    metrics:
    - type: cosine_accuracy@1
      value: 0.68
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.88
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.9
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.9
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.68
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.3399999999999999
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.21999999999999997
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.11599999999999998
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.5806666666666667
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.8140000000000001
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.8453333333333333
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.866
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.7785953864009594
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.775
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.7428386778628464
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoSCIDOCS
      type: NanoSCIDOCS
    metrics:
    - type: cosine_accuracy@1
      value: 0.36
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.56
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.7
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.74
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.36
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.26
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.21599999999999997
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.154
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.07466666666666667
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.16266666666666665
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.22266666666666665
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.31566666666666665
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.30260137759921313
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.4850238095238095
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.2192397003809301
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoArguAna
      type: NanoArguAna
    metrics:
    - type: cosine_accuracy@1
      value: 0.12
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.38
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.46
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.62
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.12
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.12666666666666665
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.09200000000000001
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.06200000000000001
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.12
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.38
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.46
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.62
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.35208645349040213
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.26857936507936503
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.2793008453049682
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoSciFact
      type: NanoSciFact
    metrics:
    - type: cosine_accuracy@1
      value: 0.52
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.66
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.74
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.78
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.52
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.23333333333333336
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.16
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.08599999999999998
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.485
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.635
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.725
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.76
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.6372055531156149
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.6100238095238094
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.5990326492390428
      name: Cosine Map@100
  - task:
      type: information-retrieval
      name: Information Retrieval
    dataset:
      name: NanoTouche2020
      type: NanoTouche2020
    metrics:
    - type: cosine_accuracy@1
      value: 0.5102040816326531
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.9183673469387755
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.9387755102040817
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.9795918367346939
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.5102040816326531
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.5306122448979591
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.5142857142857142
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.4448979591836735
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.02749427230935509
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.09510475496599126
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.15543797830995626
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.26176487754214656
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.4730551485884738
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.7036281179138323
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.35719386134567377
      name: Cosine Map@100
  - task:
      type: nano-beir
      name: Nano BEIR
    dataset:
      name: NanoBEIR mean
      type: NanoBEIR_mean
    metrics:
    - type: cosine_accuracy@1
      value: 0.39155416012558875
      name: Cosine Accuracy@1
    - type: cosine_accuracy@3
      value: 0.592182103610675
      name: Cosine Accuracy@3
    - type: cosine_accuracy@5
      value: 0.6614442700156987
      name: Cosine Accuracy@5
    - type: cosine_accuracy@10
      value: 0.7538147566718995
      name: Cosine Accuracy@10
    - type: cosine_precision@1
      value: 0.39155416012558875
      name: Cosine Precision@1
    - type: cosine_precision@3
      value: 0.26645735217163785
      name: Cosine Precision@3
    - type: cosine_precision@5
      value: 0.2118681318681319
      name: Cosine Precision@5
    - type: cosine_precision@10
      value: 0.15729984301412875
      name: Cosine Precision@10
    - type: cosine_recall@1
      value: 0.20711346717014628
      name: Cosine Recall@1
    - type: cosine_recall@3
      value: 0.3485272474590046
      name: Cosine Recall@3
    - type: cosine_recall@5
      value: 0.41169196629848837
      name: Cosine Recall@5
    - type: cosine_recall@10
      value: 0.5110785437116987
      name: Cosine Recall@10
    - type: cosine_ndcg@10
      value: 0.4507271303684606
      name: Cosine Ndcg@10
    - type: cosine_mrr@10
      value: 0.5089811616954475
      name: Cosine Mrr@10
    - type: cosine_map@100
      value: 0.36954775425813163
      name: Cosine Map@100
datasets:
- tomaarsen/NanoBEIR-ja
- hotchpotch/sentence_transformer_japanese
---

![SSE](assets/SSE_Logo.png)

If you would like to know more details:

**[SSE Technical Article](https://huggingface.co/blog/RikkaBotan/stable-static-embedding-technical-report)**


![SSE](assets/SSE_comp_ja.png)

(a) Retrieval performance (nDCG@10) across NanoBEIR Japanese tasks. (b) Mean nDCG@10 vs. inference speed (QPS: queries per second) measured on Miracl using an Intel® Core™ Ultra 7 265K (3.90 GHz) with batch size 32.


# 🩵 SSE: Stable Static Embedding for Retrieval MRL 日本語バージョン 🩵  
### **軽量、高速かつ強力な埋め込みモデル**

**パフォーマンスの簡易解説**  
このモデルは NanoBEIR_ja（日本語文書検索タスク） において **NDCG@10 = 0.4507** を達成しました。
このスコアは他の静的埋め込みモデル（ [`static-embedding-japanese`](https://huggingface.co/hotchpotch/static-embedding-japanese) (0.4487)など ）を上回るパフォーマンスです。
さらに、**次元数を半分**（512 vs 1024）に抑えています。
次元数の削減と、**Separable Dynamic Tanh** により、環境によっては検索速度は **約２倍高速** になっています。

| モデル | NanoBEIR NDCG@10 | 次元数 | パラメータ数 | 速度の優位性 | ライセンス |
|-------|------------------|------------|------------|-----------------|---------|
| **SSE Retrieval MRL Japanese** | **0.4507** ✨ | **512** | **~17M** 🪽 | **検索が約２倍高速** (超効率的) | Apache 2.0 |
| `static-embedding-japanese` | 0.4487 | 1024 | ~34M | ベースライン | MIT |

---

## 🩵 **SSE Retrieval MRL を選ぶ理由** 🩵  

✅ **パラメータ数の小さなモデル (<35M パラメータ) の中では高い性能（NDCG@10）**  

✅ **約17M のパラメータのみ** ：軽量モデルである[ruri-v3-30m](cl-nagoya/ruri-v3-30m) より約43% 小さい。 

✅ **次元数512の出力** — 次元数1024のモデルよりも豊かな表現力を持ち、[`static-embedding-japanese`](https://huggingface.co/hotchpotch/static-embedding-japanese) の **半分サイズ**  

✅ **Matryoshka 対応** — 256/128/64/32 に簡単に切り替えられ、性能の緩やかな低下を実現  

✅ **Apache 2.0 ライセンス** — 商用・個人利用ともに可能

✅ **CPU 最適化** — エッジデバイスや限られたハードウェアでも高速に動作

---

## 🩵 モデル詳細 🩵

| プロパティ | 値 |
|----------|-------|
| **モデルタイプ** | Sentence Transformer (SSE アーキテクチャ) |
| **最大シーケンス長** | 無制限 |
| **出力次元** | 512 (Matryoshka により 次元数32 まで削減可能!) |
| **類似度関数** | コサイン類似度 |
| **言語** | 日本語 |
| **ライセンス** | Apache 2.0 |

tokenizerは下記を使用させていただきました。

[hotchpotch/xlm-roberta-japanese-tokenizer](https://huggingface.co/hotchpotch/xlm-roberta-japanese-tokenizer)

```python
SentenceTransformer(
  (0): SSE(
    (embedding): EmbeddingBag(32768, 512, mode='mean')
    (dyt): SeparableDyT()
  )
)
```

![Architecture](assets/SSE_Architecture.png)

---

## 🩵 数学的背景 🩵

このモデルは静的埋め込みモデルの汎化性能を向上させるために、オリジナルのアーキテクチャである、**SSE: Stable Static Embedding**を採用しています。
SSEは、EmbeddingBagとSeparable Tanh Normalizationから構成されます。
Dynamic Tanh Normalization (DyT) は、静的埋め込みにおいて、強度適応型勾配流を可能にします。入力次元 x に対して、DyT は以下のように計算されます。

$$ 
y_k = c_k \tanh(a_k x_k + b_k) 
$$ 

ここで、a, b, c は学習可能なパラメータです。
すると、x の勾配は以下の通りになります。

$$
\frac{\partial y_k}{\partial x_k} = c_k a_k \, \mathrm{sech}^2(a_k x_k + b_k).
$$

飽和した次元 |x| > 1 の場合

$$
|a_i x_i + b_i| \gg 1 
$$ 

は指数関数的な減衰をもたらします。

$$ 
\mathrm{sech}^2(z) \sim 4e^{-2|z|} 
$$

これにより勾配が抑制され、

$$ 
\partial y_i / \partial x_i \to 0 
$$

となります。

対して、非飽和の次元 |x| << 1 の場合、

$$ 
\mathrm{sech}^2(z) \approx 1 
$$ 

ほぼ一定の勾配を維持します。

$$ 
\partial y_j / \partial x_j \approx c_j a_j 
$$

この強度依存型のゲートは、ノイズが多く大きな成分を持つ次元からの学習信号を減衰させつつ、安定した情報を有する次元については勾配流を維持します。これは明示的なハイパーパラメータなしで、表現空間の汎化性能を高める暗黙的な正則化を可能にします。

---

## 🩵 評価結果 (NanoBEIR_ja) 🩵

| データセット | NDCG@10 | MRR@10 | MAP@100 |
|---------|---------|--------|---------|
| **NanoBEIR Mean** | **0.4507**✨ | **0.5090** | **0.3695** |
| NanoClimateFEVER | 0.3110 | 0.4208 | 0.2347 |
| NanoDBPedia | 0.5596 | 0.7652 | 0.4000 |
| NanoFEVER | 0.5611 | 0.5003 | 0.4923 |
| NanoFiQA2018 | 0.3247 | 0.3731 | 0.2692 |
| NanoHotpotQA | 0.4795 | 0.5758 | 0.4182 |
| NanoMSMARCO | 0.3845 | 0.3191 | 0.3335 |
| NanoNFCorpus | 0.2736 | 0.4544 | 0.1014 |
| NanoNQ | 0.4218 | 0.3658 | 0.3572 |
| NanoQuoraRetrieval | **0.7786**✨ | **0.7750** | **0.7428** |
| NanoSCIDOCS | 0.3026 | 0.4850 | 0.2192 |
| NanoArguAna | 0.3521 | 0.2686 | 0.2793 |
| NanoSciFact | 0.6372 | 0.6100 | 0.5990 |
| NanoTouche2020 | 0.4731 | 0.7036 | 0.3572 |

---

## 🩵 使い方 🩵

```python
import torch
from sentence_transformers import SentenceTransformer

# モデルのロード（リモートコードは有効化）
model = SentenceTransformer(
    "RikkaBotan/stable-static-embedding-fast-retrieval-mrl-ja",
    trust_remote_code=True,
    device="cuda" if torch.cuda.is_available() else "cpu",
)

# 対象の文章
sentences = [
    "大規模言語モデルは学習により、高い推論能力を獲得することが可能である。",
    "静的埋め込みモデルは、簡素なアーキテクチャにより、表現空間を高速に生成可能である。"
]

with torch.no_grad():
    embeddings = model.encode(
        sentences,
        convert_to_tensor=True,
        normalize_embeddings=True,
        batch_size=32
    )

# コサイン類似度
# cosine_sim = embeddings[0] @ embeddings[1].T
cosine_sim = model.similarity(embeddings, embeddings)

print("embeddings shape:", embeddings.shape)
print("cosine similarity matrix:")
print(cosine_sim)
```
---

## 🩵 検索用使用例 🩵

```python
import torch
from sentence_transformers import SentenceTransformer

# モデルのロード（リモートコードは有効化）
model = SentenceTransformer(
    "RikkaBotan/stable-static-embedding-fast-retrieval-mrl-ja",
    trust_remote_code=True,
    device="cuda" if torch.cuda.is_available() else "cpu",
)

# 推論
query = "安定性静的埋め込みモデルとは何ですか？"
sentences = [
    "安定性静的埋め込みモデルは自己注意機構を必要としません。",
    "安定性静的埋め込みモデルは高速に高精度な埋め込み表現を生成するためのモデルです。",
    "自己注意機構はトークン間の関係性をスコア化する仕組みのことです",
    "昨夜はアイドルの曲を聴きながらお菓子作りをしていました。",
    "言語モデルは一般的に、次時刻のトークンを予測するという学習が行われます。",
    "お気に入りのヘアアクセサリーを身に着けると、とてもテンションが上がるよね。",
]


with torch.no_grad():
    embeddings = model.encode(
        [query] + sentences,
        convert_to_tensor=True,
        normalize_embeddings=True,
        batch_size=32
    )

print("embeddings shape:", embeddings.shape)

# コサイン類似度
similarities = model.similarity(embeddings[0], embeddings[1:])
for i, similarity in enumerate(similarities[0].tolist()):
    print(f"{similarity:.05f}: {sentences[i]}")
```

---

## 🩵 学習時のハイパーパラメータ 🩵

#### デフォルトと異なる設定

- `eval_strategy`: steps
- `per_device_train_batch_size`: 3072
- `gradient_accumulation_steps`: 10
- `learning_rate`: 0.1
- `adam_epsilon`: 1e-10
- `num_train_epochs`: 2
- `lr_scheduler_type`: cosine
- `warmup_ratio`: 0.02
- `bf16`: True
- `dataloader_num_workers`: 4
- `batch_sampler`: no_duplicates

---

## 🩵 学習データセット 🩵

下記の**14個のデータセット**を使用しました。

| Dataset |
|---------|
| `hpprc_emb__auto-wiki-nli-triplet` |
| `hpprc_emb__jqara` |
| `hpprc_emb__jagovfaqs` |
| `hpprc_emb__jsquad` |
| `hpprc_emb__jaquad` |
| `hpprc_emb__mkqa-triplet` |
| `hpprc_llmjp-kaken` |
| `hpprc_msmarco_ja` |
| `hpprc_emb__auto-wiki-qa-nemotron` |
| `mldr_ja` |
| `mrtydi_ja` |
| `miracl_ja` |
| `mmarco_ja` |
| `mmarco_ja_hard` |

**MatryoshkaLoss**を用いて学習を行っています。

## 🩵 学習結果 🩵

![loss](assets/SSE_loss.png)

![ndcg](assets/SSE_ndcg.png)

## 🩵 作成者：六花牡丹（りっかぼたん） 🩵

おっとりで甘えん坊な研究者見習い。
言語モデルに関するものが主な研究分野です。
お仕事のご依頼・登壇依頼・執筆依頼に関しては、下記までご連絡ください。

X(Twitter):
https://twitter.com/peony__snow

![Logo](assets/RikkaBotan_Logo.png)

## 🩵 謝辞 🩵

このモデルの学習のための計算リソースの一部は、Saldraさん、Witnessさん、Lumina Logic Minds社から提供いただきました。貴重なサポートに感謝いたします。

sentence-transformers、python、pytorchを使用させていただきました。
作成・メンテンナンスしてくださっている皆様に感謝いたします。

何よりも、このモデルにご興味を持ってくださりありがとうございます。

## 🩵 引用 🩵

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MatryoshkaLoss
```bibtex
@misc{kusupati2024matryoshka,
    title={Matryoshka Representation Learning},
    author={Aditya Kusupati and Gantavya Bhatt and Aniket Rege and Matthew Wallingford and Aditya Sinha and Vivek Ramanujan and William Howard-Snyder and Kaifeng Chen and Sham Kakade and Prateek Jain and Ali Farhadi},
    year={2024},
    eprint={2205.13147},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{henderson2017efficient,
    title={Efficient Natural Language Response Suggestion for Smart Reply},
    author={Matthew Henderson and Rami Al-Rfou and Brian Strope and Yun-hsuan Sung and Laszlo Lukacs and Ruiqi Guo and Sanjiv Kumar and Balint Miklos and Ray Kurzweil},
    year={2017},
    eprint={1705.00652},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```