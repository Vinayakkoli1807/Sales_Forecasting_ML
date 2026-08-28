# 📊 Sales Forecasting System

> A Machine Learning-powered sales forecasting application that predicts sales from order, customer, product, geographic, and financial attributes through an interactive Streamlit dashboard.
> 🔗 Live Demo: https://salesforecasting-ml-1807.streamlit.app/

## 🚀 Project Overview

The **Sales Forecasting System** is an end-to-end Machine Learning project built to estimate sales for a given order configuration.

The project includes:

- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Correlation and outlier analysis
- Statistical hypothesis testing
- Multiple regression model experiments
- Model comparison and evaluation
- Random Forest hyperparameter tuning
- Model serialization with Joblib
- An interactive Streamlit prediction dashboard
- Interactive business visualizations and insights

The final application allows users to enter order details and generate a predicted sales value along with supporting metrics, charts, and business insights.

---

## ✨ Key Features

### 🤖 Machine Learning Prediction
The application loads a trained Random Forest regression model and uses the saved feature-column structure to generate predictions.

### 📝 Interactive Order Inputs
Users can provide:

- Ship Mode
- Customer Segment
- Region
- Product Category
- Sub-Category
- City
- State
- Quantity
- Discount
- Profit

### 📈 Interactive Dashboard
After generating a forecast, the dashboard displays:

- Predicted Sales
- Quantity
- Discount
- Profit
- Profit Margin
- Predicted-sales gauge
- Revenue breakdown
- Discount-impact simulation
- Business insights
- Complete input summary

### 💡 Business Insights
The dashboard categorizes predicted sales into Low, Medium, and High levels and provides contextual insights about discounting, profitability, shipping mode, and customer segment.

---

## 🧠 Machine Learning Workflow

```text
Raw Sales Data
      ↓
Data Cleaning
      ↓
Duplicate & Unnecessary Column Removal
      ↓
Exploratory Data Analysis
      ↓
Outlier Analysis / Winsorization
      ↓
Categorical Encoding
      ↓
Train-Test Split
      ↓
Multiple Regression Models
      ↓
Model Evaluation
      ↓
Random Forest Hyperparameter Tuning
      ↓
Best Model
      ↓
Joblib Model Serialization
      ↓
Streamlit Dashboard
      ↓
Sales Prediction + Business Insights
```

---

## 📂 Dataset

The project uses a sales dataset containing **2,121 records and 21 columns**.

### Main Dataset Columns

| Category | Columns |
|---|---|
| Order Information | Row ID, Order ID, Order Date, Ship Date |
| Customer Information | Customer ID, Customer Name, Segment |
| Location | Country, City, State, Postal Code, Region |
| Product Information | Product ID, Category, Sub-Category, Product Name |
| Business Metrics | Sales, Quantity, Discount, Profit |

The modeling workflow removes identifiers and other columns that were considered unnecessary for the selected modeling stage, then applies one-hot encoding to categorical variables.

> **Note:** The final saved `feature_columns.pkl` contains the exact feature structure expected by the trained model.

---

## 🔎 Exploratory Data Analysis

The notebook includes analysis of:

- Missing values
- Duplicate records
- Unique values
- Numerical distributions
- Correlation between business metrics
- Outlier detection
- Winsorization
- Categorical feature distributions
- Region distribution
- Sub-category distribution
- Region vs. Segment distribution
- Sales distribution
- Profit distribution across segments
- Top products by total sales
- Total sales by sub-category
- Sales vs. profit by sub-category
- Feature importance

### Important Correlation Findings

The analysis identified:

- **Sales vs Quantity:** approximately `0.44` positive correlation
- **Discount vs Profit:** approximately `-0.48` negative correlation
- **Sales vs Profit:** approximately `0.17` positive correlation
- **Discount vs Sales:** approximately `-0.03`, indicating very weak linear association
- **Quantity vs Profit:** approximately `0.06`
- **Quantity vs Discount:** approximately `-0.02`

These findings indicate that quantity has a moderate positive relationship with sales, while higher discounts are associated with lower profit in the analyzed data.

---

## 🧪 Statistical Analysis

The notebook also performs hypothesis testing using statistical methods including:

- One-way ANOVA
- Pearson correlation

The analysis examines whether sales differ significantly across:

- Regions
- Customer segments
- Cities

It also evaluates the relationship between discount and sales.

---

## 🤖 Models Evaluated

Several regression approaches were experimented with.

| Model | R² Score | MAE | RMSE |
|---|---:|---:|---:|
| Linear Regression | -1061161.65% | 42,424.95 | 57,025.61 |
| Random Forest | 81.79% | 80.06 | 153.37 |
| Decision Tree | 76.41% | 102.89 | 174.56 |
| SVR | -8.08% | 289.31 | 575.48 |
| Gradient Boosting | 84.02% | 88.60 | 143.65 |
| XGBoost | **85.16%** | **75.49** | **138.43** |

### Model Selection

The notebook evaluates multiple models and then performs **RandomizedSearchCV** on Random Forest.

The tuned Random Forest configuration selected by the search was:

```text
n_estimators = 200
max_depth = 20
min_samples_split = 5
min_samples_leaf = 2
```

The serialized model used by the application is the tuned **Random Forest Regressor**.

### Tuned Random Forest Evaluation

The saved-model training workflow reports:

- **R²:** `0.8190`
- **MAE:** `85.66`
- **RMSE:** `152.87`

> The model comparison table above contains the individual model experiment results from the notebook. The tuned Random Forest is the model saved for the Streamlit application.

---

## 🖥️ Streamlit Application

The application is implemented in `app.py` using Streamlit.

The app loads:

```python
model = joblib.load("sales_forecasting_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")
```

The prediction interface prepares an input DataFrame using the saved feature-column structure and applies the selected categorical values before passing the data to the trained model.

---

## 📊 Dashboard Visualizations

The application provides three main analytical areas:

### 1. Visualizations

- Predicted Sales Gauge
- Revenue Breakdown
- Discount Impact Simulation

### 2. Business Insights

- Sales level
- Discount assessment
- Profit margin interpretation
- Shipping-mode insight
- Customer-segment insight

### 3. Input Summary

Displays the complete set of order parameters entered by the user and reports categorical-feature matching information.

---

## 🛠️ Tech Stack

### Programming & Data Science

- Python
- Pandas
- NumPy
- Scikit-learn
- SciPy
- Joblib

### Machine Learning

- Linear Regression
- Random Forest Regressor
- Decision Tree Regressor
- Support Vector Regression
- Gradient Boosting Regressor
- XGBoost
- Ridge Regression
- Voting Regressor
- RandomizedSearchCV

### Visualization

- Matplotlib
- Seaborn
- Plotly

### Web Application

- Streamlit

### Development Environment

- Jupyter Notebook
- VS Code
- Git
- GitHub

---

## 📁 Project Structure

```text
sales-forecasting-system/
│
├── app.py
├── sales_forecasting_model.pkl
├── feature_columns.pkl
├── sales_forecasting.ipynb
├── stores_sales_forecasting.csv
├── requirements.txt
├── .gitignore
└── README.md
```

### File Description

| File | Description |
|---|---|
| `app.py` | Streamlit application and prediction interface |
| `sales_forecasting_model.pkl` | Serialized trained Random Forest model |
| `feature_columns.pkl` | Saved feature-column structure used during prediction |
| `sales_forecasting.ipynb` | Data analysis, preprocessing, modeling, evaluation, and tuning notebook |
| `stores_sales_forecasting.csv` | Dataset used for the project |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files and folders excluded from Git |
| `README.md` | Project documentation |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📌 Example Prediction Workflow

1. Open the Sales Forecasting dashboard.
2. Select the shipping mode.
3. Select the customer segment.
4. Select the region.
5. Select the product category.
6. Enter the sub-category, city, and state.
7. Enter quantity, discount, and profit.
8. Click **Generate Forecast**.
9. Review the predicted sales.
10. Explore the visualizations and business insights.

---

## ⚠️ Model Scope & Limitations

This model was trained using historical **U.S. sales data**.

Therefore:

- Predictions should be interpreted within the context of the analyzed U.S. sales data.
- Predictions may not generalize to other markets or regions.
- Model performance depends on the quality and distribution of the input data.
- Historical relationships may not remain constant in future business conditions.
- The dashboard provides model-based estimates rather than guaranteed future sales.

---

## 🔮 Future Improvements

Potential improvements include:

- Add time-series forecasting using historical order dates
- Add monthly/quarterly sales forecasting
- Compare additional ensemble models
- Improve categorical encoding and preprocessing consistency
- Add model explainability using SHAP
- Add confidence/prediction intervals
- Add historical sales dashboards
- Add downloadable prediction reports
- Add automated model retraining
- Add cloud deployment
- Add database integration for live sales data
- Add user authentication and role-based access

---

## 🎯 Project Objective

The primary objective of this project is to demonstrate an end-to-end Machine Learning workflow — from raw sales data and exploratory analysis to model training, evaluation, hyperparameter tuning, model serialization, and deployment through an interactive web application.

---

## 👨‍💻 Author

**Vinayak Koli**

Data Science & Machine Learning Enthusiast

---

## ⭐ If You Find This Project Useful

If this project helped you or you found it interesting, consider giving the repository a ⭐ on GitHub.
