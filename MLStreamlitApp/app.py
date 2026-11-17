"""Interactive supervised machine learning portfolio app."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    f1_score,
    mean_absolute_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


st.set_page_config(page_title="ML Model Explorer", page_icon="🌳", layout="wide")
st.title("🌳 Interactive Machine Learning Explorer")
st.write("Upload a CSV or explore the Iris sample dataset, select what to predict, and train a Decision Tree.")

SAMPLE_PATH = Path(__file__).resolve().parent / "data" / "iris_openml.csv"


@st.cache_data
def load_sample():
    return pd.read_csv(SAMPLE_PATH)


source = st.radio("Choose your data source", ["Sample: Iris (OpenML)", "Upload my CSV"], horizontal=True)
if source.startswith("Sample"):
    df = load_sample()
    st.caption("Iris dataset, available as OpenML dataset 61. The CSV is included in this project for reliable offline loading.")
else:
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded is None:
        st.info("Choose a CSV file to begin, or switch to the sample dataset.")
        st.stop()
    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Could not read the CSV: {exc}")
        st.stop()

if df.empty or len(df.columns) < 2 or df.columns.duplicated().any():
    st.error("The dataset must have rows, at least two uniquely named columns, and a target to predict.")
    st.stop()

st.subheader("1. Explore your data")
st.write(f"**{len(df):,} rows · {len(df.columns)} columns**")
st.dataframe(df.head(10), use_container_width=True)

suggested = "class" if "class" in df.columns else df.columns[-1]
target = st.selectbox("Choose the target column (what the model should predict)", df.columns.tolist(), index=df.columns.get_loc(suggested))
features = df.drop(columns=[target]).copy()
y_raw = df[target]
valid = y_raw.notna()
features, y_raw = features.loc[valid], y_raw.loc[valid]

if len(features) < 10:
    st.error("At least 10 rows with a non-missing target are needed.")
    st.stop()

# IDs and free-text columns produce unhelpfully enormous one-hot encodings.
unsupported = [c for c in features if features[c].dropna().map(lambda v: isinstance(v, (list, dict))).any()]
if unsupported:
    st.error(f"Columns with list/dictionary values are unsupported: {unsupported}")
    st.stop()

numeric_target = pd.api.types.is_numeric_dtype(y_raw)
default_task = "Regression" if numeric_target and y_raw.nunique() > min(20, len(y_raw) // 5) else "Classification"
task = st.radio("Prediction type", ["Classification", "Regression"], index=0 if default_task == "Classification" else 1,
                help="Classification predicts categories; regression predicts numbers.")

if task == "Regression":
    y = pd.to_numeric(y_raw, errors="coerce")
    keep = y.notna() & np.isfinite(y)
    features, y = features.loc[keep], y.loc[keep]
    if len(y) < 10 or y.nunique() < 2:
        st.error("Regression needs at least 10 numeric targets and at least two different target values.")
        st.stop()
else:
    y = y_raw.astype(str)
    if y.nunique() < 2 or y.nunique() > min(50, len(y) // 2):
        st.error("Classification requires between 2 and 50 categories, with enough examples per category. Try Regression for continuous targets.")
        st.stop()

# Treat dates and miscellaneous values as categories; categorical missing values are imputed.
for column in features.select_dtypes(include=["datetime", "datetimetz"]).columns:
    features[column] = features[column].astype(str)
numeric_columns = features.select_dtypes(include=["number", "bool"]).columns.tolist()
categorical_columns = [c for c in features.columns if c not in numeric_columns]
for column in categorical_columns:
    features[column] = features[column].astype("string").replace({pd.NA: np.nan}).astype(object)
    features[column] = features[column].where(pd.notna(features[column]), np.nan)

transformers = []
if numeric_columns:
    transformers.append(("numeric", SimpleImputer(strategy="median", keep_empty_features=True), numeric_columns))
if categorical_columns:
    transformers.append(("categorical", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent", keep_empty_features=True)),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_columns))
preprocess = ColumnTransformer(transformers=transformers)

st.subheader("2. Configure and train")
left, middle, right = st.columns(3)
with left:
    max_depth = st.slider("Maximum tree depth", 1, 20, 5, help="How many decision levels the tree can grow. Smaller values create simpler models.")
with middle:
    min_samples_leaf = st.slider("Minimum samples per leaf", 1, 20, 2, help="Minimum training rows in each final branch. Larger values reduce overfitting.")
with right:
    test_size = st.slider("Test set percentage", 10, 40, 20, step=5)

if task == "Classification":
    counts = y.value_counts()
    can_stratify = counts.min() >= 2 and int(np.ceil(len(y) * test_size / 100)) >= y.nunique() and int(np.floor(len(y) * (100 - test_size) / 100)) >= y.nunique()
    stratify = y if can_stratify else None
    model = DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=42)
else:
    stratify = None
    model = DecisionTreeRegressor(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=42)

try:
    X_train, X_test, y_train, y_test = train_test_split(
        features, y, test_size=test_size / 100, random_state=42, stratify=stratify
    )
    pipeline = Pipeline([("preprocess", preprocess), ("model", model)])
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
except (ValueError, TypeError) as exc:
    st.error(f"This dataset could not be trained: {exc}. Check column types and missing values.")
    st.stop()

st.success(f"Model trained on {len(X_train):,} rows and evaluated on {len(X_test):,} unseen test rows. Change any setting to retrain automatically.")
st.subheader("3. Test-set results")
if task == "Classification":
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted", zero_division=0)
    a, b = st.columns(2)
    a.metric("Accuracy", f"{accuracy:.1%}")
    b.metric("Weighted F1 score", f"{f1:.3f}")
    st.info("**Accuracy** is the share of test predictions that are correct. **Weighted F1** combines precision (how often predicted categories are right) and recall (how many true examples are found), weighting each category by its size. Higher is better for both.")
    fig, ax = plt.subplots(figsize=(7, 5))
    ConfusionMatrixDisplay.from_predictions(y_test, predictions, ax=ax, xticks_rotation=45, cmap="Blues", colorbar=False)
    ax.set_title("Confusion matrix (test data)")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("The confusion matrix counts actual vs. predicted categories. Numbers on the diagonal are correct predictions; off-diagonal numbers are mistakes.")
else:
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    a, b = st.columns(2)
    a.metric("Mean Absolute Error (MAE)", f"{mae:,.3f}")
    b.metric("R² score", f"{r2:.3f}" if np.isfinite(r2) else "Undefined")
    st.info("**MAE** is the average absolute prediction mistake, measured in the target's units; lower is better. **R²** compares the model with simply guessing the average target: 1 is perfect, 0 matches the average baseline, and a negative number is worse.")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(predictions, y_test - predictions, alpha=0.65)
    ax.axhline(0, color="red", linestyle="--")
    ax.set(xlabel="Predicted value", ylabel="Actual − predicted", title="Residuals on test data")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("A residual is a prediction error. Points near the red zero line are closer to the true value; patterns can signal model problems.")

st.caption("Educational demo: performance estimates depend on the data and train/test split. Do not upload sensitive personal data.")
