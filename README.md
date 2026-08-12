💳 Explainable Fraud Detection System
Machine Learning · SHAP · FastAPI · Docker

An end-to-end machine learning solution for detecting fraudulent digital money-transfer transactions, explaining model decisions, and serving predictions through a containerised REST API.

The project demonstrates the complete ML lifecycle—from data preparation and model development to hyperparameter optimisation, explainable AI, API development, and Docker containerisation.

📌 Project Overview

Fraud detection presents a significant challenge for digital payment and money-transfer platforms because fraudulent transactions typically represent only a small proportion of overall transaction volume.

The objective of this project was to develop a scalable and explainable machine-learning system capable of identifying potentially fraudulent transactions while minimising unnecessary false fraud alerts.

The project addresses three key questions:

Can fraudulent transactions be identified accurately using machine learning?
Which transaction and behavioural characteristics drive fraud predictions?
Can the trained model be converted into a deployable application rather than remaining only in a notebook?

To address these questions, Logistic Regression and Random Forest models were evaluated, followed by RandomizedSearchCV, GridSearchCV, decision-threshold optimisation, SHAP explainability, FastAPI deployment, and Docker containerisation.

🎯 Final Model Performance

The optimised Random Forest classifier achieved:

Metric	Performance
Accuracy	98.24%
Fraud Precision	100.00%
Fraud Recall	79.90%
Fraud F1-score	88.83%
Decision Threshold	0.55

The selected threshold prioritises very high precision while maintaining approximately 80% fraud recall.

This means transactions classified as fraudulent have a very low false-positive rate, although further work could focus on identifying a greater proportion of fraudulent transactions.

🧠 Machine Learning Workflow
Raw Transaction Data
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Feature Engineering
        │
        ▼
Encoding & Preprocessing
        │
        ▼
Stratified Train/Test Split
        │
        ▼
Baseline Models
 ┌──────────────┬───────────────┐
 │   Logistic   │ Random Forest │
 │  Regression  │               │
 └──────────────┴───────────────┘
        │
        ▼
RandomizedSearchCV
        │
        ▼
GridSearchCV
        │
        ▼
Threshold Optimisation
        │
        ▼
Final Random Forest
        │
        ▼
SHAP Explainability
        │
        ▼
FastAPI REST API
        │
        ▼
Docker Container
📊 Dataset

The final modelling dataset contained:

11,335 transactions
52 predictive features
Binary target: is_fraud
9,068 training observations
2,267 test observations
Training Class Distribution
Transaction Class	Observations
Legitimate	8,272
Fraudulent	796

The class distribution demonstrates the imbalance commonly encountered in real-world fraud detection.

To account for this imbalance, stratified sampling and class weighting were incorporated into model development.

🔧 Data Preparation

The preprocessing workflow included:

Missing-value assessment and treatment
Duplicate identification
Data-type correction
Timestamp processing
Categorical encoding
Feature engineering
Numeric preprocessing
Stratified train/test splitting
Class-imbalance handling

The final machine-learning feature matrix contained 52 numerical predictors.

🤖 Model Development

Two primary classification algorithms were initially compared.

Logistic Regression

Logistic Regression provided a useful interpretable baseline.

Its fraud-class performance was approximately:

Metric	Result
Precision	70%
Recall	83%
F1-score	76%
Accuracy	95%

Although Logistic Regression detected a slightly larger proportion of fraudulent transactions, its lower precision resulted in considerably more false-positive fraud alerts.

Random Forest

The baseline Random Forest substantially improved overall fraud classification.

Metric	Result
Precision	99%
Recall	80%
F1-score	89%
Accuracy	98%

Random Forest therefore provided a substantially stronger balance between fraud detection and false-positive control.

⚙️ Hyperparameter Optimisation
RandomizedSearchCV

RandomizedSearchCV was used to explore a broad Random Forest hyperparameter space using 5-fold cross-validation.

The best configuration identified included:

RandomForestClassifier(
    class_weight="balanced",
    criterion="entropy",
    max_depth=20,
    min_samples_leaf=2,
    min_samples_split=6,
    n_estimators=379,
    n_jobs=-1,
    random_state=42
)
Performance
Metric	Result
Accuracy	0.9819
Precision	0.9938
Recall	0.7990
F1-score	0.8858

Confusion matrix:

[[2067,    1],
 [  40,  159]]

Only one legitimate transaction was incorrectly classified as fraudulent.

🔍 GridSearchCV

A more focused GridSearchCV was subsequently performed around the promising parameter region identified by RandomizedSearchCV.

The best estimator was:

RandomForestClassifier(
    class_weight="balanced",
    criterion="entropy",
    max_depth=20,
    max_features="log2",
    min_samples_split=4,
    n_estimators=425,
    n_jobs=-1,
    random_state=42
)
GridSearchCV Performance
Metric	Result
Accuracy	0.9819
Precision	0.9938
Recall	0.7990
F1-score	0.8858

Both optimisation strategies therefore produced highly consistent test-set performance.

🎚️ Decision-Threshold Optimisation

Fraud detection involves an important trade-off between:

False positives: legitimate customers incorrectly flagged as fraudulent.
False negatives: fraudulent transactions that remain undetected.

Different probability thresholds were therefore evaluated.

Threshold	Accuracy	Precision	Recall	F1
0.20	0.9718	0.8571	0.8141	0.8351
0.30	0.9797	0.9636	0.7990	0.8736
0.40	0.9819	0.9938	0.7990	0.8858
0.50	0.9819	0.9938	0.7990	0.8858
0.55	0.9824	1.0000	0.7990	0.8883
0.60	0.9824	1.0000	0.7990	0.8883
0.80	0.9806	1.0000	0.7789	0.8757

A probability threshold of 0.55 was selected.

This produced the strongest F1-score while achieving 100% fraud precision on the evaluation set.

🔎 Explainable AI with SHAP

High predictive performance alone is insufficient for many financial risk applications. Analysts also need to understand why a transaction has been classified as suspicious.

SHAP (SHapley Additive exPlanations) was therefore incorporated to provide both:

Global model explainability
Transaction-level explainability
Global Feature Importance




The strongest model drivers included:

txn_velocity_24h
txn_velocity_1h
ip_risk_score
risk_score_internal
account_age_days
device_trust_score
chargeback_history_count
location_mismatch
amount_src
amount_usd

Transaction behaviour and risk characteristics were therefore generally more influential than transaction amount alone.

SHAP Beeswarm Analysis




The SHAP summary analysis demonstrates both the magnitude and direction of feature contributions.

Key patterns include:

High transaction velocity tends to increase fraud risk.
Higher IP risk contributes positively to fraud predictions.
Elevated internal risk scores increase predicted fraud risk.
Previous chargeback activity contributes to suspicious classifications.
Location mismatch increases fraud risk.
Greater account maturity generally reduces fraud risk.
Higher device trust generally reduces fraud risk.
🔬 Individual Transaction Explanation




SHAP was also used to explain individual model predictions.

For the investigated fraudulent transaction, major contributors included:

Feature	SHAP Contribution
txn_velocity_24h	0.104369
txn_velocity_1h	0.088656
ip_risk_score	0.067026
risk_score_internal	0.055049
account_age_days	0.043033
device_trust_score	0.035274
chargeback_history_count	0.034299
location_mismatch	0.028711

This demonstrates that the model's fraud decision is based on the combined influence of several behavioural and risk indicators rather than a single variable.

💡 Business Insights

The analysis suggests several operationally relevant fraud indicators.

1. Transaction velocity is highly informative

txn_velocity_24h and txn_velocity_1h were the strongest predictors.

Rapid transaction activity may therefore provide an important early-warning signal for suspicious behaviour.

2. Network risk matters

ip_risk_score was one of the strongest model drivers, demonstrating the potential value of network and IP intelligence in transaction monitoring.

3. Account maturity provides useful context

Newer accounts were associated with greater fraud risk, suggesting that account age can support risk-based transaction screening.

4. Device information adds predictive value

Lower device trust was associated with increased fraud risk.

Device intelligence can therefore complement conventional transaction monitoring.

5. Historical behaviour matters

Chargeback history contributed meaningfully to predictions, supporting the inclusion of historical customer behaviour in fraud-risk assessment.

6. Transaction amount alone is insufficient

Although transaction amounts contributed to the model, behavioural and risk indicators were substantially more influential.

A robust fraud strategy should therefore combine monetary, behavioural, device, geographic and network characteristics.

🚀 FastAPI Deployment

The trained model was converted from a notebook-based machine-learning experiment into a REST API using FastAPI.

The API provides:

Model health checking
Fraud classification
Fraud probability
Configurable decision threshold
SHAP-based explanation output
Health Endpoint
GET /health

Example response:

{
    "status": "healthy",
    "model_loaded": true,
    "model": "Tuned Random Forest",
    "threshold": 0.55,
    "number_of_features": 52
}
Prediction Endpoint
POST /predict

Example output:

{
    "prediction": 1,
    "classification": "Fraudulent",
    "fraud_probability": 1.0,
    "decision_threshold": 0.55,
    "top_explanations": [
        {
            "feature": "txn_velocity_24h",
            "shap_value": 0.104369,
            "direction": "increases fraud risk"
        },
        {
            "feature": "txn_velocity_1h",
            "shap_value": 0.088656,
            "direction": "increases fraud risk"
        },
        {
            "feature": "ip_risk_score",
            "shap_value": 0.067026,
            "direction": "increases fraud risk"
        }
    ]
}

Interactive FastAPI documentation is available locally through:

http://127.0.0.1:8000/docs
🐳 Docker Containerisation

The FastAPI application was containerised using Docker to provide a portable and reproducible runtime environment.

Build the Docker Image

From the project root:

docker build -t fraud-detection-api .
Run the Container
docker run -p 8000:8000 fraud-detection-api

The application can then be accessed locally through port 8000.

Health Check
http://127.0.0.1:8000/health

Successful Docker health response:

{
    "status": "healthy",
    "model_loaded": true,
    "model": "Tuned Random Forest",
    "threshold": 0.55,
    "number_of_features": 52
}

This confirms that the trained Random Forest model can be successfully loaded and served from inside the Docker container.

📁 Repository Structure
Novapay-fraudulent/
│
├── api/
│   └── main.py
│
├── Figures/
│   ├── shap_feature_importance.png
│   ├── shap_summary_beeswarm.png
│   └── shap_individual_fraud_waterfall.png
│
├── Models/
│   ├── fraud_detection_model.pkl
│   └── feature_names.pkl
│
├── Dockerfile
├── Requirements-docker.txt
├── README.md
└── .gitignore
🛠️ Technology Stack
Area	Technologies
Programming	Python
Data Manipulation	Pandas, NumPy
Machine Learning	Scikit-learn
Explainable AI	SHAP
Visualisation	Matplotlib
API	FastAPI, Uvicorn
Validation	Pydantic
Model Persistence	Joblib
Containerisation	Docker
Version Control	Git, GitHub
Development	VS Code, Jupyter Notebook
⚠️ Model Limitations

Although the final model achieved very high precision, approximately 20% of fraudulent transactions remained undetected.

In a real financial environment, the cost associated with false negatives may justify selecting a lower operating threshold or introducing additional fraud-review layers.

The model should therefore be considered a demonstration of an end-to-end fraud detection architecture rather than a production banking fraud system.

Real-world deployment would additionally require:

Continuous model monitoring
Data-drift detection
Security and authentication
Model governance
Bias and fairness assessment
Regulatory review
Automated retraining
Human fraud-investigation workflows
🔮 Future Development

Potential improvements include:

Optimising specifically for fraud recall and financial cost
Cost-sensitive learning
XGBoost or LightGBM benchmarking
Automated preprocessing of raw API inputs
Model and data-drift monitoring
API authentication
Automated testing
CI/CD integration
Cloud deployment
Real-time transaction streaming
Analyst-facing fraud monitoring dashboard
🏁 Conclusion

This project demonstrates an end-to-end machine-learning approach to fraud detection.

A tuned Random Forest classifier achieved strong fraud classification performance, while SHAP provided transparent global and transaction-level explanations.

The project was subsequently extended beyond model development by exposing predictions through FastAPI and containerising the application with Docker.

The completed workflow demonstrates practical capabilities across:

Data preparation → Machine learning → Hyperparameter optimisation → Model evaluation → Explainable AI → API development → Containerisation → Version control

👤 Author

Leonard Mgbeahuruike

Data Analytics · Machine Learning · Environmental & Sustainability Analytics

🔗 Repository

This repository contains the machine-learning model, SHAP explainability outputs, FastAPI application, and Docker configuration required to reproduce the deployment architecture.