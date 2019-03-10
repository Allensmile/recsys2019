from recsys.transformers import (
    FeatureEng,
    PandasToNpArray,
    PandasToRecords,
    RankFeatures,
)
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import KBinsDiscretizer, StandardScaler

numerical_features = [
    "rank",
    "price",
    "price_vs_max_price",
    "price_vs_mean_price",
    "item_similarity_to_last_clicked_item",
    "last_poi_item_clicks",
    "last_poi_item_impressions",
    "last_poi_item_ctr",
    "user_item_ctr",
    "last_item_index",
    "clickout_user_item_clicks",
    "clickout_item_clicks",
    "clickout_item_impressions",
    "was_interaction_img",
    "interaction_img_freq",
    "was_interaction_deal",
    "interaction_deal_freq",
    "was_interaction_info",
    "interaction_info_freq",
    "was_item_searched",
    "interaction_img_diff_ts",
]
numerical_features_for_ranking = [
    "price",
    "item_similarity_to_last_clicked_item",
    "last_poi_item_clicks",
    "last_poi_item_impressions",
    "last_poi_item_ctr",
    "user_item_ctr",
    "clickout_user_item_clicks",
    "clickout_item_clicks",
    "clickout_item_impressions",
    "interaction_img_freq",
    "interaction_deal_freq",
    "interaction_info_freq",
    # "interaction_img_diff_ts",
]
categorical_features = [
    "device",
    "platform",
    "last_sort_order",
    "last_filter_selection",
]

features_eng = FeatureEng()


def make_vectorizer_1():
    return make_pipeline(
        features_eng,
        ColumnTransformer(
            [
                (
                    "numerical",
                    make_pipeline(
                        PandasToNpArray(),
                        SimpleImputer(strategy="mean"),
                        StandardScaler(),
                    ),
                    numerical_features,
                ),
                (
                    "categorical",
                    make_pipeline(PandasToRecords(), DictVectorizer()),
                    categorical_features,
                ),
                (
                    "numerical_ranking",
                    RankFeatures(),
                    numerical_features_for_ranking + ["clickout_id"],
                ),
                # (
                #     "properties",
                #     CountVectorizer(
                #         preprocessor=lambda x: "UNK" if x != x else x,
                #         tokenizer=lambda x: x.split("|"),
                #         min_df=5,
                #     ),
                #     "properties",
                # ),
                (
                    "last_10_actions",
                    CountVectorizer(ngram_range=(1, 5), tokenizer=list, min_df=5),
                    "last_10_actions",
                ),
                ("last_event_ts", DictVectorizer(), "last_event_ts"),
            ]
        ),
    )


def make_vectorizer_2():
    return make_pipeline(
        features_eng,
        ColumnTransformer(
            [
                (
                    "numerical",
                    make_pipeline(
                        PandasToNpArray(),
                        SimpleImputer(strategy="mean"),
                        KBinsDiscretizer(),
                    ),
                    numerical_features,
                ),
                (
                    "categorical",
                    make_pipeline(PandasToRecords(), DictVectorizer()),
                    categorical_features,
                ),
                (
                    "numerical_ranking",
                    make_pipeline(RankFeatures(), StandardScaler()),
                    numerical_features_for_ranking + ["clickout_id"],
                ),
                # (
                #     "properties",
                #     CountVectorizer(
                #         preprocessor=lambda x: "UNK" if x != x else x,
                #         tokenizer=lambda x: x.split("|"),
                #         min_df=5,
                #     ),
                #     "properties",
                # ),
                (
                    "last_10_actions",
                    CountVectorizer(ngram_range=(1, 5), tokenizer=list, min_df=5),
                    "last_10_actions",
                ),
                ("last_event_ts", DictVectorizer(), "last_event_ts"),
            ]
        ),
    )
