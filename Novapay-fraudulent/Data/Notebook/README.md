Fraud Detection Using Machine Learning

Project Overview

This project develops and evaluates machine learning models to detect fraudulent financial transactions. The objective is to build an accurate classification model capable of distinguishing fraudulent transactions from legitimate ones while minimizing false positives and false negatives.

Project Workflow

The project was completed using the following workflow:

1. Import Libraries

The required Python libraries were imported, including Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, and other supporting packages for data preprocessing, visualization, and machine learning.

2. Load Dataset

The fraud detection dataset was loaded into a Pandas DataFrame for analysis.

3. Data Inspection

The dataset was explored to understand its structure by examining:

Dataset dimensions
Data types
Missing values
Duplicate records
Summary statistics
Class distribution
4. Data Cleaning

Data preprocessing included:

Handling missing values
Removing duplicate records
Correcting inconsistent data
Converting variables to appropriate data types
Preparing the dataset for modelling
5. Exploratory Data Analysis (EDA)

EDA was performed to identify trends and relationships within the data using:

Histograms
Boxplots
Correlation heatmaps
Count plots
Distribution plots
Fraud versus non-fraud comparisons

Key insights from the exploratory analysis helped identify important variables associated with fraudulent transactions.

6. Feature Engineering

Feature engineering involved:

Encoding categorical variables
Scaling numerical variables where appropriate
Creating new features
Selecting relevant predictors
Splitting the dataset into training and testing sets
7. Machine Learning Model Development

Two supervised classification algorithms were developed and evaluated:

Logistic Regression
Random Forest Classifier

Each model was trained using the training dataset and evaluated on the test dataset.

Model Performance Comparison

Model Performance Comparison
Model	Accuracy	Precision (Fraud)	Recall (Fraud)	F1-score (Fraud)
Logistic Regression	95%	70%	83%	76%
Random Forest	98%	99%	80%	89%

Interpretation

The Logistic Regression model achieved an overall accuracy of 95%. It demonstrated the highest recall (83%), indicating that it detected slightly more fraudulent transactions than the Random Forest model. However, its lower precision (70%) suggests that it generated a larger number of false fraud alerts.

The Random Forest model achieved an accuracy of 98%, with an outstanding precision of 99% and an F1-score of 89%. These results indicate that the model produced highly reliable fraud predictions while maintaining strong overall classification performance.

Key Insights
Fraudulent transactions represented a much smaller proportion of the dataset, indicating class imbalance.
Data preprocessing and feature engineering significantly improved model performance.
Random Forest captured complex, non-linear relationships within the data better than Logistic Regression.
Logistic Regression identified slightly more fraud cases, but at the expense of more false positives.
Random Forest provided a better balance between correctly identifying fraud and minimizing unnecessary fraud alerts.

Conclusion

Both machine learning models performed well in detecting fraudulent transactions. However, Random Forest demonstrated superior overall performance by achieving the highest accuracy (98%), precision (99%), and F1-score (89%).

Although Logistic Regression produced a slightly higher recall (83%), the overall balance of performance metrics favours the Random Forest model. Therefore, Random Forest is recommended as the preferred model for deployment in a fraud detection system.

Future work may include hyperparameter tuning, threshold optimization, feature selection, SMOTE for handling class imbalance, and testing additional ensemble learning techniques such as XGBoost or LightGBM.