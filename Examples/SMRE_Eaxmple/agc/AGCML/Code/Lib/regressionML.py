from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.metrics import r2_score
from HML_runner import HML_runner
from DMP_runner import DMP_runner
import pandas as pd
import numpy as np
import time
import json

class RegressionML():
    def __init__(self):
        pass

    def show_results(self, y_predicted, y_actual=None, ML_Alg=None, cv=5):
        if y_actual is None or len(y_actual) == 0:
            return 0

        # Score metric: R^2
        """ The coefficient R^2 is defined as (1 - u/v), where u is the residual
            sum of squares ((y_true - y_pred) ** 2).sum() and v is the total
            sum of squares ((y_true - y_true.mean()) ** 2).sum().
            The best possible score is 1.0 and it can be negative (because the
            model can be arbitrarily worse). A constant model that always
            predicts the expected value of y, disregarding the input features,
            would get a R^2 score of 0.0."""

        # Training Cross Validation Accuracy Score
        # if ML_Alg != None:
        #     val_scores = cross_val_score(ML_Alg, X_train, np.ravel(y_train), cv=cv)
        #     print(f'Training Cross Validation Score({val_scores.mean()}):', val_scores)

        # Testing Accuracy Score
        r2 = r2_score(y_actual, y_predicted)
        # if len(y_actual) > 0 and len(y_predicted) > 0:
        #     print("Testing R^2 Accuracy Score:", r2)

        return r2

    def DecisionTreeClassifier_run(self, X_train, y_train, X_test, y_actual=None):
        ml_model = self.DecisionTreeClassifier_ML(X_train, y_train)
        return self.prediction(ml_model, X_test, y_actual)

    def DecisionTreeClassifier_ML(self, X_train, y_train):
        # print("*** Decision Tree Regression ***")
        ML_Alg = DecisionTreeClassifier(max_depth=6)
        ml_model = ML_Alg.fit(X_train, y_train.ravel())
        return ml_model

    def GaussianNB_run(self, X_train, y_train, X_test, y_actual=None):
        ml_model = self.GaussianNB_ML(X_train, y_train)
        return self.prediction(ml_model, X_test, y_actual)

    def GaussianNB_ML(self, X_train, y_train):
        # print("*** Gaussian NB ***")
        ML_Alg = GaussianNB()
        ml_model = ML_Alg.fit(X_train, np.ravel(y_train))
        return ml_model

    def RandomForestRegressor_run(self, X_train, y_train, X_test, y_actual=None):
        ml_model = self.RandomForestRegressor_ML(X_train, y_train)
        return self.prediction(ml_model, X_test, np.ravel(y_actual))

    def RandomForestRegressor_ML(self, X_train, y_train):
        # print("*** Random Forest Regression ***")
        ML_Alg = RandomForestRegressor(n_estimators=100)
        ml_model = ML_Alg.fit(X_train, np.ravel(y_train))
        return ml_model


    def LinearRegressor_run(self, X_train, y_train, X_test, y_actual=None):
        ml_model = self.LinearRegressor_ML(X_train, y_train)
        return self.prediction(ml_model, X_test, y_actual)

    def LinearRegressor_ML(self, X_train, y_train):
        # print("*** Random LinearRegression Regression ***")
        ML_Alg = LinearRegression()
        ml_model = ML_Alg.fit(X_train, np.ravel(y_train))
        return ml_model


    def GradientBoostingRegressor_run(self, X_train, y_train, X_test, y_actual=None):
        ml_model = self.GradientBoostingRegressor_ML(X_train, y_train)
        return self.prediction(ml_model, X_test, y_actual)

    def GradientBoostingRegressor_ML(self, X_train, y_train):
        # print("*** Gradient Boosting Regression ***")
        ML_Alg = GradientBoostingRegressor(n_estimators=1000,
                                           learning_rate=0.1,
                                           subsample=0.5,
                                           max_depth=1,
                                           random_state=0)
        ml_model = ML_Alg.fit(X_train, np.ravel(y_train))
        return ml_model

    def GaussianProcessRegressor_run(self, X_train, y_train, X_test, y_actual=None):
        ml_model = self.GaussianProcessRegressor_ML(X_train, y_train)
        return self.prediction(ml_model, X_test, y_actual)

    def GaussianProcessRegressor_ML(self, X_train, y_train):
        # print("*** Gaussian Process Regression ***")
        kernel = DotProduct() + WhiteKernel()
        ML_Alg = GaussianProcessRegressor(kernel=kernel, random_state=0)
        ml_model = ML_Alg.fit(X_train, np.ravel(y_train))
        return ml_model

    def prediction(self, ml_model, X_test, y_actual=None):
        y_predicted = ml_model.predict(X_test)
        return y_predicted, self.show_results(y_predicted, y_actual)

    def run_with_evidence_and_check_prediction(self, dmp, model, data, y_actual):
        predicted = []
        i = 0
        for index, rows in data.iterrows():
            keys = rows.keys()
            sbn = model
            y_name = y_actual.columns[0]
            y_value = y_actual.iloc[i, 0]
            for k in keys:
                sbn += "defineEvidence({}, {});".format(k, rows.get(k))
            sbn += "run(DMP);"
            dmp.run(sbn)

            # check prediction
            # print("================ Prediction results from BN ================")
            # print(dmp.output)
            with open(dmp.output) as json_file:
                net = json.load(json_file)
                for node in net:
                    for obj, contents in node.items():
                        # print('node: ' + obj)
                        mean = None
                        for attr, values in contents.items():
                            # print(" " + attr + ': ' + str(values))
                            if attr == "marginal":
                                mean = values["MU"]

                        if obj == y_name:
                            # print("================================")
                            # print("{} : Predicted {} : Actual {}".format(y_name, mean, y_value))
                            predicted.append(float(mean))

            i += 1

        return predicted

    def ContinuousBNRegressor_run(self, name, X_train, y_train, X_test, y_actual=None, show=True):
        ssbn = self.ContinuousBNRegressor_ML(name, X_train, y_train)
        return self.ContinuousBNRegressor_prediction(name, ssbn, X_test, y_actual, show)

    def ContinuousBNRegressor_ML(self, name, X_train, y_train):
        # print("*** Continuous BN Regressor  ***")
        ###########################
        # ##
        # Make a csv data file
        csv = r'../TestData/{}_for_test.csv'.format(name)
        # csv = "E:/SW-Posco2019/DATAETL/TestData/big_data_1000000.csv"
        output = r'../Output_BN/{}_ssbn.txt'.format(name)

        df_col = pd.concat([X_train, y_train], axis=1)
        df_col.to_csv(csv, index=None)

        #############################
        # Run MEBN learning
        ts = time.time()
        hml = HML_runner()

        # Make a V-BN model
        parents = []
        child = y_train.columns[0]
        for nodeName in X_train.columns:
            parents.append(nodeName)

        hml.make_Model(child, parents)

        # Run MEBN learning
        ssbn = hml.run(csv, output)

        # print("== Mahcine learning end: Time {} ==============================".format(time.time()-ts))
        return ssbn

    def ContinuousBNRegressor_prediction(self, name, ssbn, X_test, y_actual=None, show=True):
        #############################
        # Prediction
        ts = time.time()
        output = r"../Output_BN/{}_bn_output.json".format(name)
        dmp = DMP_runner(output)

        y_predicted = self.run_with_evidence_and_check_prediction(dmp, ssbn, X_test, y_actual)

        # print("== BN was completed : Time {} ==============================".format(time.time()-ts))

        if show == True:
            return y_predicted, self.show_results(y_predicted, y_actual)
        else:
            return y_predicted, self.show_results(y_predicted, y_actual=None)



