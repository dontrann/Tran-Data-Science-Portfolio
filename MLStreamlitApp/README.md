# Interactive Machine Learning Explorer

## 1. Project Overview

This project is an interactive machine learning application built with Python and Streamlit.

Users can:

- Upload their own CSV dataset or use the Iris dataset from OpenML.
- Select a target column to predict.
- Choose between classification and regression.
- Train a supervised machine learning model.
- Adjust model hyperparameters.
- View performance metrics and visualizations.

## 2. Live App

**Streamlit App:** Link will be added after deployment.

### 3. How to Run Locally

**Step 1:** Download or clone the GitHub repository.

**Step 2:** Open the downloaded repository folder in VS Code.

**Step 3:** Open the terminal and install the required libraries:

```bash
python -m pip install -r MLStreamlitApp/requirements.txt
```

**Step 4:** Run the application:

```bash
python -m streamlit run MLStreamlitApp/app.py
```

**Step 5:** Open `http://localhost:8501` in your browser.

## 4. Required Libraries

The following libraries are listed in `requirements.txt`:

| Library | Version |
|---|---|
| Streamlit | >=1.35, <2.0 |
| pandas | >=2.0, <3.0 |
| NumPy | >=1.24, <3.0 |
| scikit-learn | >=1.3, <2.0 |
| Matplotlib | >=3.7, <4.0 |

## 5. Machine Learning Models and Hyperparameters

The application uses two supervised machine learning models:

- **Decision Tree Classifier:** Predicts categories and displays accuracy, weighted F1 score, and a confusion matrix.
- **Decision Tree Regressor:** Predicts numerical values and displays mean absolute error (MAE), R² score, and a residual plot.

Users can adjust the following settings using Streamlit sliders:

| Setting | Description |
|---|---|
| Maximum Tree Depth | Controls how deep the decision tree can grow. |
| Minimum Samples per Leaf | Sets the minimum number of samples in each leaf. |
| Test Set Percentage | Controls how much data is used for testing. |

The model automatically retrains and updates its results whenever a setting changes.

## 6. References

1. [Streamlit Documentation](https://docs.streamlit.io/get-started) - Guide to building and running Streamlit applications.
2. [Scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html) - Documentation for Decision Tree models and hyperparameters.
3. [OpenML Iris Dataset](https://www.openml.org/d/61) - Source of the sample dataset.