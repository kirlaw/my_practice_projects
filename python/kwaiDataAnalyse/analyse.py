# -*- coding: utf-8 -*-
import os, re, math, platform, unicodedata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# ===================== 基础参数 =====================
INPUT_FILE = "data.xlsx"       # 待分析文件
TEXT_COLS  = ["cleaned","内容", "text", "review"]   # 自动探测文本列优先级
RATING_COLS = ["评级","评分","rating","stars","score"]  # 自动探测评级列
DATE_COLS   = ["发表时间","日期","date","time","timestamp","datetime"]  # 自动探测日期列
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

LEMMA_EXCLUDE = {"kwai","tiktok","iphone","google","nba"}

# 词云字体 —— 自动选择常见系统字体，避免葡语字符乱码
def get_default_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/arial.ttf"
    elif system == "Darwin":
        return "/System/Library/Fonts/Supplemental/Arial.ttf"
    else:
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_PATH = get_default_font()
from wordcloud import WordCloud

# ===================== 停用词与噪声词 =====================
# 覆盖：代词/冠词/介词/连词/副词/疑问词/常见助动词 + 口语与网络词 + 补充
PT_STOP = {
    # 冠词/代词/介词/连词/副词（节选+扩展）
    "o","a","os","as","um","uma","uns","umas","de","do","da","dos","das","no","na","nos","nas","em","por","para","com","sem",
    "sobre","entre","até","pelo","pela","pelos","pelas","e","mas","ou","se","porque","que","nem","como","quando","onde","qual","quais","quanto","porquê","porque",
    "eu","tu","ele","ela","nós","vos","vós","eles","elas","você","vocês","meu","minha","meus","minhas","teu","tua","teus","tuas","seu","sua","seus","suas",
    "isto","isso","aquilo","este","esta","estes","estas","esse","essa","esses","essas","aquele","aquela","aqueles","aquelas","aqui","aí","ali","lá",
    "não","sim","muito","pouco","agora","hoje","ontem","amanhã","também","só","já","há","era","foi","são","ser","está","estão","estar","tenho","tem","ter","haver",
    # 口语/无意义高频
    "pra","pro","tá","né","kk","kkk","kkkk","pq","eh","ah","vc","vcs","tipo","mto","mt","q","oq","rs","ok","obg","vlw",
    "nao","não","lr",
}

# 额外要硬过滤掉的“无意义/品牌符号/噪声”集合（词频完全不计）
HARD_BAN = {"nao","não","lr","rt","tbt","http","https","www"}

# 正则与工具
RE_WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", re.UNICODE)

def normalize_lower(text: str) -> str:
    """统一小写；保留重音（葡语重要）"""
    return text.lower()

def strip_non_text(text: str) -> str:
    """去非字母数字字符（保留空格），用于清理判定"""
    return re.sub(r"[^0-9A-Za-zÀ-ÖØ-öø-ÿ\s]+", " ", text)

def has_too_many_noise_chars(raw: str) -> bool:
    """若原文中非字母数字/符号太多，则视为噪声评论"""
    if not raw: return True
    text = strip_non_text(raw)
    letters = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]", text)
    return len(letters) < 3  # 过短、几乎无文本

# ===================== 轻量词形还原（离线） =====================
# 名词复数 -> 单数（保守规则）
def noun_to_singular(token: str) -> str:
    # ões -> ão ; ães -> ão ; is / os / as 结尾的一般复数；éis->el；óis->ol；ais->al
    if token.endswith("ões"): return token[:-3] + "ão"
    if token.endswith("ães"): return token[:-3] + "ão"
    if token.endswith("éis"): return token[:-3] + "el"
    if token.endswith("óis"): return token[:-3] + "ol"
    if token.endswith("ais"): return token[:-3] + "al"
    # 通用去 s（避免过度：长度>3 且不是结尾 'us' 这类外来名词）
    if token.endswith("s") and len(token) > 3:
        return token[:-1]
    return token

# 动词变形 -> 原形（非常轻量的启发式：只覆盖最常见）
def verb_to_infinitive(token: str) -> str:
    # 常见进行时/动名词
    if token.endswith("ando"): return token[:-4] + "ar"
    if token.endswith("endo"): return token[:-4] + "er"
    if token.endswith("indo"): return token[:-4] + "ir"
    # 常见过去式/现在式（极简启发，避免过拟合）
    for suf, inf in [
        ("ei","ar"),("ou","ar"),("amos","ar"),("aram","ar"),
        ("i","er"),("eu","er"),("emos","er"),("eram","er"),
        ("i","ir"),("iu","ir"),("imos","ir"),("iram","ir"),
    ]:
        if token.endswith(suf) and len(token) > len(suf)+1:
            # 仅当去掉词尾后合理时才替换
            base = token[:-len(suf)]
            if len(base) >= 2:
                return base + inf
    return token

def adjective_to_masculine(token: str) -> str:
    """
    将常见形容词阴性变为阳性：
    - a 结尾 -> o
    - ista/ante/ente 结尾不变（中性或不规则）
    """
    # 排除特殊词或外来词
    if token in LEMMA_EXCLUDE:
        return token

    # 常见阴性 -> 阳性
    if token.endswith("a") and len(token) > 2:
        if token.endswith(("ista","ante","ente")):  # 不规则中性形
            return token
        return token[:-1] + "o"
    return token


def is_likely_portuguese_word(token):
    # 只保留至少有一个元音 + 字母组成的单词，且不是全大写（避免缩写）
    return bool(re.search(r"[aeiouáéíóúãõàè]", token, re.IGNORECASE))

def lemmatize_token(token: str) -> str:
    """
    1. 名词复数 -> 单数
    2. 动词变形 -> 原形
    3. 形容词阴性 -> 阳性
    """
    if not is_likely_portuguese_word(token) or token in LEMMA_EXCLUDE:
        return token

    t = noun_to_singular(token)
    t = verb_to_infinitive(t)
    t = adjective_to_masculine(t)
    return t

def tokenize_and_clean(text: str):
    toks = [t for t in RE_WORD.findall(text)]
    out = []
    for t in toks:
        # t = normalize_lower(t)
        # if any(ch.isdigit() for ch in t):  # 含数字的过滤掉
        #     continue
        # if t in HARD_BAN:  # 硬过滤
        #     continue
        # if t in PT_STOP:   # 停用词过滤
        #     continue
        # t = lemmatize_token(t)
        # if t in PT_STOP or t in HARD_BAN:
        #     continue
        # if len(t) < 2:     # 太短的 token
        #     continue
        out.append(t)
    return out

# ===================== 读取数据 + 严格清洗 =====================
df = pd.read_excel(INPUT_FILE)

# 自动探测列
def pick_col(candidates, cols):
    for c in candidates:
        if c in cols: return c
    return None

text_col = pick_col(TEXT_COLS, df.columns)
rating_col = pick_col(RATING_COLS, df.columns)
date_col   = pick_col(DATE_COLS, df.columns)

if not text_col:
    raise ValueError(f"找不到文本列，尝试列名之一：{TEXT_COLS}")

# 清理：去空、去重复、去极短/噪声
df = df.copy()
df[text_col] = df[text_col].astype(str).str.strip()
df = df[df[text_col].notna() & (df[text_col] != "")]

# 去重复
df = df.drop_duplicates(subset=[text_col])

# 去噪声评论（无字母、无有效文本）
mask_noise = df[text_col].apply(has_too_many_noise_chars)
df = df[~mask_noise]

# 统一小写（仅用于分词；保留原文另存一列可选）
texts = df[text_col].astype(str).tolist()

# 解析评分（1~5）
def parse_rating(x):
    if pd.isna(x): return np.nan
    s = str(x)
    m = re.search(r"([1-5])", s)
    return float(m.group(1)) if m else np.nan
if rating_col:
    df["rating_norm"] = df[rating_col].apply(parse_rating)

# 解析日期（到月）
if date_col:
    df["date_parsed"] = pd.to_datetime(df[date_col], errors="coerce")
    df["month"] = df["date_parsed"].dt.to_period("M").astype(str)

# 分词 & 词形规范
tokens_by_doc = [tokenize_and_clean(t) for t in texts]

df["clean_tokens"] = tokens_by_doc
df["clean_text"] = df["clean_tokens"].apply(lambda x: " ".join(x))
df.to_csv(f"{OUT_DIR}/dataset_cleaned.csv", index=False, encoding="utf-8-sig")

# 去“过短评论”（分词后少于3个 token）
len_mask = [len(x) >= 0 for x in tokens_by_doc]
df = df[len_mask].reset_index(drop=True)
tokens_by_doc = [t for t in tokens_by_doc if len(t) >= 0]

# ===================== 词频 & 词云 =====================
def make_wordcloud(freq_dict, path, title=None):
    if not freq_dict: return
    wc = WordCloud(width=1600, height=900, background_color="white", font_path=FONT_PATH, collocations=False)
    wc.generate_from_frequencies(freq_dict)
    plt.figure(figsize=(12,7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if title: plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

# 总体词频
all_tokens = [tok for doc in tokens_by_doc for tok in doc]
freq_all = Counter(all_tokens)
pd.DataFrame(freq_all.most_common(), columns=["word","count"]).to_csv(f"{OUT_DIR}/word_frequency_overall.csv", index=False)
make_wordcloud(dict(freq_all.most_common(1000)), f"{OUT_DIR}/wordcloud_overall.png", "Word Cloud (Overall)")

# 按 1~5 星词云
if "rating_norm" in df.columns:
    for star in [1,2,3,4,5]:
        idx = (df["rating_norm"] == star)
        toks = [tok for doc, flag in zip(tokens_by_doc, idx) if flag for tok in doc]
        if not toks: continue
        freq_s = Counter(toks)
        pd.DataFrame(freq_s.most_common(), columns=["word","count"]).to_csv(f"{OUT_DIR}/word_frequency_{star}star.csv", index=False)
        make_wordcloud(dict(freq_s.most_common(1000)), f"{OUT_DIR}/wordcloud_{star}star.png", f"Word Cloud ({star}★)")

# ===================== 情感分析（离线词典法） =====================
# 轻量葡语情感词典（可根据语料扩充；已含常见评价词）
POS_LEX = {
    "bom","boa","ótimo","otimo","ótima","otima","excelente","maravilhoso","maravilhosa","adoro","adorei","gostei",
    "incrível","incrivel","perfeito","perfeita","recomendo","funciona","rápido","rapido","feliz","satisfeito","satisfeita",
    "agradável","agradavel","qualidade","eficiente","lindo","linda","barato","barata","vale","útil","util","confiável",
    "confiavel","amável","amavel","atencioso","atenciosa","fantástico","fantastica","fantástica","top","impecável","impecavel",
    "maravilha","recomendável","recomendavel"
}
NEG_LEX = {
    "ruim","pior","péssimo","pessimo","péssima","pessima","horrível","horrivel","odiei","odioso","defeito","quebrado",
    "lento","demorado","atraso","atrasou","triste","insatisfeito","insatisfeita","terrível","terrivel","inexistente",
    "enganoso","enganação","enganacao","caro","cara","fraco","fraca","falha","erro","cancelar","cancelado","demora",
    "demorou","tarde","péssima","pessima","suporte","péssimos","pessimos","decepcionado","decepcionada","decepcionante",
    "horrível","horrivel","péssimo","pessimo"
}

def sentiment_score(tokens):
    score = 0
    for t in tokens:
        score += 1 if t in POS_LEX else 0
        score -= 1 if t in NEG_LEX else 0
    return score

labels, scores = [], []
for doc in tokens_by_doc:
    s = sentiment_score(doc)
    scores.append(s)
    if s > 0: labels.append("POS")
    elif s < 0: labels.append("NEG")
    else: labels.append("NEU")

df["sentiment"] = labels
df["sentiment_score"] = scores
df.to_csv(f"{OUT_DIR}/dataset_with_sentiment.csv", index=False)

# 情感总体比例图
plt.figure(figsize=(7,5))
order = ["NEG","NEU","POS"]
vals = [ (df["sentiment"]==o).mean() for o in order ]
plt.bar(order, vals)
plt.title("Sentiment Proportions (Overall)")
plt.ylabel("Proportion")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/sentiment_proportions_overall.png", dpi=200)
plt.close()

# 三类情感词云
for lab in ["POS","NEU","NEG"]:
    toks = [tok for doc, y in zip(tokens_by_doc, labels) if y == lab for tok in doc]
    freq = Counter(toks)
    pd.DataFrame(freq.most_common(), columns=["word","count"]).to_csv(f"{OUT_DIR}/word_frequency_{lab}.csv", index=False)
    make_wordcloud(dict(freq.most_common(1000)), f"{OUT_DIR}/wordcloud_{lab}.png", f"Word Cloud ({lab})")

# 评分与情感的关系（每星级三类情感比例）
if "rating_norm" in df.columns:
    piv = (df
           .assign(cnt=1)
           .pivot_table(index="rating_norm", columns="sentiment", values="cnt", aggfunc="sum", fill_value=0)
           .apply(lambda x: x/x.sum(), axis=1))
    piv = piv.reindex([1,2,3,4,5])
    plt.figure(figsize=(8,5))
    piv.plot(kind="bar", stacked=True)
    plt.title("Sentiment vs Rating")
    plt.ylabel("Proportion")
    plt.xlabel("Rating (Stars)")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/sentiment_vs_rating.png", dpi=200)
    plt.close()

# 情感随时间的变化（按月）
if "month" in df.columns:
    trend = (df.groupby(["month","sentiment"]).size()
             .groupby(level=0).apply(lambda s: s/s.sum())
             .unstack(fill_value=0)
             .sort_index())
    plt.figure(figsize=(10,5))
    for lab in ["NEG","NEU","POS"]:
        if lab in trend.columns:
            plt.plot(trend.index, trend[lab], marker="o", label=lab)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.title("Sentiment Trend Over Time (Monthly)")
    plt.ylabel("Proportion")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/sentiment_trend_monthly.png", dpi=200)
    plt.close()

# ===================== 语义网络（简洁清晰） =====================
# 共现窗口=2，统计边权
edges = Counter()
for doc in tokens_by_doc:
    for i in range(len(doc)-1):
        a, b = sorted((doc[i], doc[i+1]))
        if a != b:
            edges[(a,b)] += 1

# 取前 N 条最强边，构子图（避免一大坨）
TOP_EDGES = 300
edge_items = edges.most_common(TOP_EDGES)
G = nx.Graph()
for (a,b), w in edge_items:
    G.add_edge(a,b, weight=w)

# 只取度数 Top 节点子图（再次收敛）
deg_series = dict(G.degree())
top_nodes = sorted(deg_series, key=deg_series.get, reverse=True)[:200]
H = G.subgraph(top_nodes).copy()

# 导出网络表
edge_df = pd.DataFrame([(u,v,d["weight"]) for u,v,d in H.edges(data=True)], columns=["source","target","weight"])
edge_df.to_csv(f"{OUT_DIR}/semantic_network_edges.csv", index=False)
deg_df  = pd.DataFrame(H.degree(), columns=["node","degree"]).sort_values("degree", ascending=False)
deg_df.to_csv(f"{OUT_DIR}/semantic_network_degree.csv", index=False)

# 绘图（简洁）
plt.figure(figsize=(12,10))
pos_layout = nx.spring_layout(H, k=0.5, seed=42)
nx.draw_networkx_nodes(H, pos_layout, node_size=80, alpha=0.9)
nx.draw_networkx_edges(H, pos_layout, width=[0.4 + d['weight']*0.05 for _,_,d in H.edges(data=True)], alpha=0.6)
# 仅给度数Top 40打标签，避免拥挤
label_nodes = set(sorted(deg_series, key=deg_series.get, reverse=True)[:40])
nx.draw_networkx_labels(H, pos_layout, labels={n:n for n in H.nodes if n in label_nodes}, font_size=8)
plt.axis("off")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/semantic_network.png", dpi=220)
plt.close()

# ===================== LDA 主题分析 + 自动选主题数 + 气泡图 + 趋势图 =====================
from gensim import corpora, models
from sklearn.decomposition import LatentDirichletAllocation

docs_joined = [" ".join(doc) for doc in tokens_by_doc]
if len(docs_joined) >= 5:
    vectorizer = CountVectorizer(min_df=3, max_df=0.9)
    X = vectorizer.fit_transform(docs_joined)
    terms = vectorizer.get_feature_names_out()

    if X.shape[1] > 0:
        # ===================== 自动选主题数 =====================
        min_topics, max_topics = 5, min(15, X.shape[0]//5)
        perplexities = []
        coherences = []

        # gensim dictionary & corpus
        dictionary = corpora.Dictionary(tokens_by_doc)
        corpus = [dictionary.doc2bow(doc) for doc in tokens_by_doc]

        for n_topics in range(min_topics, max_topics+1):
            # sklearn LDA -> perplexity
            lda_skl = LatentDirichletAllocation(n_components=n_topics, random_state=42)
            lda_skl.fit(X)
            perplexities.append(lda_skl.perplexity(X))

            # gensim LDA -> coherence
            lda_gensim = models.LdaModel(corpus=corpus,
                                         id2word=dictionary,
                                         num_topics=n_topics,
                                         random_state=42,
                                         passes=10)
            coherence_model = models.CoherenceModel(model=lda_gensim,
                                                    texts=tokens_by_doc,
                                                    dictionary=dictionary,
                                                    coherence='c_v',
                                                    processes=1)
            coherences.append(coherence_model.get_coherence())
            print(f"Topics={n_topics} | Perplexity={perplexities[-1]:.2f} | Coherence={coherences[-1]:.3f}")

        # ===================== 绘制困惑度与一致性趋势图 =====================
        plt.figure(figsize=(10,5))
        plt.plot(range(min_topics, max_topics+1), perplexities, marker='o', label='Perplexity')
        plt.xlabel("Number of Topics")
        plt.ylabel("Perplexity")
        plt.title("LDA Perplexity vs Number of Topics")
        plt.xticks(range(min_topics, max_topics+1))
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/lda_perplexity_trend.png", dpi=220)
        plt.close()

        plt.figure(figsize=(10,5))
        plt.plot(range(min_topics, max_topics+1), coherences, marker='o', color='green', label='Coherence')
        plt.xlabel("Number of Topics")
        plt.ylabel("Coherence (c_v)")
        plt.title("LDA Coherence vs Number of Topics")
        plt.xticks(range(min_topics, max_topics+1))
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/lda_coherence_trend.png", dpi=220)
        plt.close()

        # 最佳主题数：一致性最高
        best_idx = np.argmax(coherences)
        n_topics = min_topics + best_idx
        print(f"✅ 选择最佳主题数: {n_topics}")

        # ===================== 用最佳主题数训练最终 LDA =====================
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(X)

        # 主题-关键词表
        topics = []
        for i, comp in enumerate(lda.components_):
            top_idx = np.argsort(comp)[::-1][:12]
            top_terms = [terms[j] for j in top_idx]
            topics.append({"topic": i, "top_words": ", ".join(top_terms)})
        topics_df = pd.DataFrame(topics)
        topics_df.to_csv(f"{OUT_DIR}/lda_topics.csv", index=False)

        # 文档-主题分布
        doc_topic = lda.transform(X)
        pd.DataFrame(doc_topic, columns=[f"topic_{i}" for i in range(n_topics)]).to_csv(
            f"{OUT_DIR}/lda_doc_topic_distribution.csv", index=False
        )

        # 主题占比（气泡图）
        topic_props = doc_topic.mean(axis=0)
        plt.figure(figsize=(10,6))
        xs = np.arange(n_topics)
        ys = topic_props
        sizes = 4000 * (topic_props / topic_props.max() if topic_props.max()>0 else topic_props+1e-6)
        plt.scatter(xs, ys, s=sizes, alpha=0.5)
        for i, prop in enumerate(topic_props):
            top3 = topics_df.loc[topics_df["topic"]==i, "top_words"].values[0].split(", ")[:3]
            label = f"T{i}: " + ", ".join(top3)
            plt.text(i, prop+0.01, label, ha="center", va="bottom", fontsize=8)
        plt.xticks(xs, [f"T{i}" for i in xs])
        plt.xlabel("Topics")
        plt.ylabel("Average Proportion")
        plt.title("LDA Topic Proportions (Bubble Chart)")
        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/lda_topic_bubbles.png", dpi=220)
        plt.close()
    else:
        open(f"{OUT_DIR}/lda_skipped.txt","w",encoding="utf-8").write("LDA 跳过：清洗后无足够特征（X.shape[1]==0）")
else:
    open(f"{OUT_DIR}/lda_skipped.txt","w",encoding="utf-8").write("LDA 跳过：有效文档数不足 (<5)")

print("✅ 全部分析完成，结果在 outputs/ 文件夹。")
