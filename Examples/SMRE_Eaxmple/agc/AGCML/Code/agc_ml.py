import numpy as np
from regressionML import RegressionML
from saveResults import SaveResults
import pandas as pd
from sklearn.model_selection import train_test_split


##################################
# 1. Generate Data

training_data = r'../Data/training_data.csv'
validation_data = r'../Data/validation_data.csv'

df_training = pd.read_csv(training_data)
df_validation = pd.read_csv(validation_data)

X_train = []
y_train= []
X_test= []
y_test= []



# Excel Start
excel = SaveResults(r'../Output/prediction_result_ph2_Roll_Force.xlsx')

excel.insert("Actual", np.append(y_test.values.ravel(), 0.0))

yPredicted, r2 = RegressionML().GradientBoostingRegressor_run(X_train, y_train, X_test, y_test)
excel.insert("Gradient Boosting", np.append(yPredicted, r2))
yPredicted, r2 = RegressionML().RandomForestRegressor_run(X_train, y_train, X_test, y_test)
excel.insert("Random Forest", np.append(yPredicted, r2))
yPredicted, r2 = RegressionML().GaussianProcessRegressor_run(X_train, y_train, X_test, y_test)
excel.insert("Gaussian Process", np.append(yPredicted, r2))
yPredicted, r2 = RegressionML().ContinuousBNRegressor_run("Roll_Force", X_train, y_train, X_test, y_test)
excel.insert("Continuous BN", np.append(yPredicted, r2))

# Excel End
excel.save()
