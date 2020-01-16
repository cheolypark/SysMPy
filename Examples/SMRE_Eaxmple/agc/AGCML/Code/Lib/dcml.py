from regressionML import RegressionML
import pandas as pd
from sklearn.model_selection import train_test_split
from clustering_alg import Clustering_Alg
import threading
from statistics import mean
import math
import warnings
from sklearn.metrics import r2_score


class DataClusterBasedMachineLearning:
    """
    Data Cluster based Machine Learning
    """
    def __init__(self, data_x,  data_y, clustering_algs, prediction_algs, max_clusters):
        """
        :param data: A training data set D
        :param clustering_alg: A set of clustering algorithms C
        :param prediction_alg: A set of prediction algorithms P
        :param max_clusterss: A maximum number of clusters m
        """
        self.data_x = data_x
        self.data_y = data_y
        self.clustering_algs = clustering_algs
        self.prediction_algs = prediction_algs
        self.max_clusters = max_clusters

        self.ml_models = {}
        self.high_scored_dcml_model = None

        # For experiment
        self.ml_data = {}
        self.is_experiment = True

    def do_machine_learning(self, cbn_name, prediction_alg, x_train, y_train):
        if prediction_alg is 'GradientBoosting':
            model = RegressionML().GradientBoostingRegressor_ML(x_train, y_train)
        elif prediction_alg is 'RandomForest':
            model = RegressionML().RandomForestRegressor_ML(x_train, y_train)
        elif prediction_alg is 'GaussianProcess':
            model = RegressionML().GaussianProcessRegressor_ML(x_train, y_train)
        elif prediction_alg is 'ContinuousBN':
            model = RegressionML().ContinuousBNRegressor_ML(cbn_name, x_train, y_train)
        return model

    def do_prediction(self, cbn_name, prediction_alg, model, x_test, y_test=None):
        if prediction_alg is 'GradientBoosting':
            yPredicted, r2 = RegressionML().prediction(model, x_test, y_test)
        elif prediction_alg is 'RandomForest':
            yPredicted, r2 = RegressionML().prediction(model, x_test, y_test)
        elif prediction_alg is 'GaussianProcess':
            yPredicted, r2 = RegressionML().prediction(model, x_test, y_test)
        elif prediction_alg is 'ContinuousBN':
            yPredicted, r2 = RegressionML().ContinuousBNRegressor_prediction(cbn_name, model, x_test, y_test)
        return yPredicted, r2

    def perform_machine_learning_alg(self, cl_alg, num_clusters, cur_cluster, prediction_alg, x_train, x_test, y_train, y_test):
        # temporary name for CBN
        cbn_name = f'{cl_alg}_{num_clusters}_{cur_cluster}'

        # perform ML
        model = self.do_machine_learning(cbn_name, prediction_alg, x_train, y_train)

        # perform prediction
        yPredicted, r2 = self.do_prediction(cbn_name, prediction_alg, model, x_test, y_test)

        # print(cl_alg, num_clusters, cur_cluster, prediction_alg, yPredicted, r2)

        # store results
        if math.isnan(r2):
            # In some cases, the training data has the size of 1, then R2 becomes NaN.
            warnings.warn(f'{cl_alg}.{num_clusters}.{cur_cluster}.{prediction_alg}: The prediction result was NaN.')
            self.ml_models[cl_alg][num_clusters][cur_cluster][prediction_alg]['R2'] = -10
        else:
            self.ml_models[cl_alg][num_clusters][cur_cluster][prediction_alg]['R2'] = r2

        self.ml_models[cl_alg][num_clusters][cur_cluster][prediction_alg]['ML_MODEL'] = model

    def perform_machine_learning(self, cl_alg, num_clusters, cur_cluster, x_train, x_test, y_train, y_test):

        thread = []
        for prediction_alg in self.prediction_algs:
            self.ml_models[cl_alg][num_clusters][cur_cluster][prediction_alg] = {}
            print(f'[Thread] {cl_alg}.{num_clusters}.{cur_cluster} -> ML alg {prediction_alg}')
            t = threading.Thread(target=self.perform_machine_learning_alg, args=([cl_alg, num_clusters, cur_cluster, prediction_alg, x_train, x_test, y_train, y_test]))
            t.setDaemon(True)
            thread.append(t)

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        # select a best prediction alg and remove all low-scored algorithms
        alg_high = None
        r2_high = -10000
        for prediction_alg in self.prediction_algs:
            print(f'Check R2 for {cl_alg}.{num_clusters}.{cur_cluster}.{prediction_alg}')
            r2 = self.ml_models[cl_alg][num_clusters][cur_cluster][prediction_alg]['R2']
            print(f'R2 {cl_alg}.{num_clusters}.{cur_cluster}.{prediction_alg} = {r2}')
            r2_high = max(r2_high, r2)
            if r2 is r2_high:
                if alg_high is not None:
                    del self.ml_models[cl_alg][num_clusters][cur_cluster][alg_high]
                alg_high = prediction_alg
            else:
                del self.ml_models[cl_alg][num_clusters][cur_cluster][prediction_alg]

    def perform_clustering_alg_with_clusters(self, cl_alg, num_clusters):
        print(f'perform_prediction_alg {cl_alg} with the cluster {num_clusters}')

        cl = Clustering_Alg()
        cl.set_algs(cl_alg)
        cl.set_base(n_clusters=num_clusters)
        cl.set_data(self.data_x, self.data_y)
        cl.run()

        # Note that the clustering algorithm can change the number of clusters
        # e.g., ) The default n_clusters = 3 changes to n_clusters = 2 according to the clustering result

        self.ml_models[cl_alg]['CL_MODEL'] = cl

        data, data_x, data_y = cl.get_clustered_data(cl_alg)

        thread = []
        test_size = 0.2

        for cur_cluster, datum in data_x.items():

            self.ml_models[cl_alg][num_clusters][cur_cluster] = {}
            print(f'data split for {cl_alg}.{num_clusters}.{cur_cluster}')

            # split data for machine learning
            x_train, x_test, y_train, y_test = train_test_split(data_x[cur_cluster], data_y[cur_cluster], test_size=test_size)

            if self.is_experiment:

                if cl_alg not in self.ml_data:
                    self.ml_data[cl_alg] = {}
                if num_clusters not in self.ml_data[cl_alg]:
                    self.ml_data[cl_alg][num_clusters] = {}
                if cur_cluster not in self.ml_data[cl_alg][num_clusters]:
                    self.ml_data[cl_alg][num_clusters][cur_cluster] = {}

                self.ml_data[cl_alg][num_clusters][cur_cluster]['x_train'] = x_train
                self.ml_data[cl_alg][num_clusters][cur_cluster]['x_test'] = x_test
                self.ml_data[cl_alg][num_clusters][cur_cluster]['y_train'] = y_train
                self.ml_data[cl_alg][num_clusters][cur_cluster]['y_test'] = y_test

            t = threading.Thread(target=self.perform_machine_learning, args=([cl_alg, num_clusters, cur_cluster, x_train, x_test, y_train, y_test]))
            t.setDaemon(True)
            thread.append(t)

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        # calculate the average R2 and store it to 'ml_models.cl_alg.num_clusters.avg_r2'
        avg_r2 = []
        for cur_cluster, ml_alg_r2 in self.ml_models[cl_alg][num_clusters].items():
            try:
                r2 = list(ml_alg_r2.values())[0]['R2']
            except IndexError:
                print('list index out of range')
            avg_r2.append(r2)

        self.ml_models[cl_alg][num_clusters]['avg_r2'] = mean(avg_r2)

    def perform_clustering(self, cl_alg):
        thread = []
        for num_clusters in range(2, self.max_clusters + 1):
            self.ml_models[cl_alg][num_clusters] = {}
            print(f'[Thread] clustering alg {cl_alg} with the cluster number {num_clusters} start')
            t = threading.Thread(target=self.perform_clustering_alg_with_clusters, args=([cl_alg, num_clusters]))
            t.setDaemon(True)
            thread.append(t)

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        # select a best number of clusters and remove all low-scored models
        cl_num_high = None
        avg_r2_high = -10000
        # keys = list(self.ml_models[cl_alg].keys())
        # for num_clusters in keys:
        for num_clusters in range(2, self.max_clusters + 1):
            avg_r2 = self.ml_models[cl_alg][num_clusters]['avg_r2']
            avg_r2_high = max(avg_r2_high, avg_r2)
            if avg_r2 is avg_r2_high:
                if cl_num_high is not None:
                    del self.ml_models[cl_alg][cl_num_high]
                    del self.ml_data[cl_alg][cl_num_high]
                cl_num_high = num_clusters
            else:
                del self.ml_models[cl_alg][num_clusters]
                del self.ml_data[cl_alg][num_clusters]

        self.ml_models[cl_alg]['avg_r2'] = avg_r2_high

    def run(self):
        thread = []
        for cl_alg in self.clustering_algs:
            self.ml_models[cl_alg] = {}
            print(f'[Thread] {cl_alg} start')
            t = threading.Thread(target=self.perform_clustering, args=([cl_alg]))
            t.setDaemon(True)
            thread.append(t)

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        # select a high-scored model
        avg_r2_high = -10000
        for cl_alg in self.clustering_algs:
            avg_r2 = self.ml_models[cl_alg]['avg_r2']
            avg_r2_high = max(avg_r2_high, avg_r2)
            if avg_r2 is avg_r2_high:
                # if cl_high is not None:
                #     del self.ml_models[cl_high]
                self.high_scored_dcml_model = cl_alg
            else:
                pass
                # del self.ml_models[cl_alg]

        print('Learned DC-ML Model:')
        for ml in self.ml_models:
            print(ml, self.ml_models[ml]['avg_r2'])

        print('High-Scored DC-ML Model:', self.high_scored_dcml_model)

        return self.ml_models[self.high_scored_dcml_model]

    def perform_prediction(self, ml_family, x_test, y_test):
        # cl = Clustering_Alg()
        # data, data_x, data_y = cl.get_clustered_data(cl_alg)
        cl_model = ml_family['CL_MODEL']
        cl_alg = cl_model.get_clustering_alg()
        y_label = cl_alg.fit_predict(x_test)

        index = 0
        yPredicted = []

        for ml in y_label:
            ml_models = list(ml_family.values())[0][ml]
            ml_name = list(ml_models.keys())[0]
            ml_model = list(ml_models.values())[0]['ML_MODEL']

            # perform prediction
            yPre, r2 = self.do_prediction('Temp', ml_name, ml_model, x_test.iloc[[index]])
            yPredicted.append(yPre)
            print(f'{ml_name} predicted {yPre}.')
            index += 1

        yPredicted = pd.DataFrame(yPredicted)
        r2 = r2_score(y_test, yPredicted)
        return yPredicted, r2

    ##########################################################
    # Get Result Information
    def get_high_scored_clustered_data(self):
        _, v = next(iter(self.ml_data.items()))
        _, clusters = next(iter(v.items()))
        return clusters

    def get_high_scored_cl_model(self):
        return self.high_scored_dcml_model

    def get_high_scored_ml_models(self):
        _, v = next(iter(self.ml_models.items()))
        _, clusters = next(iter(v.items()))
        result = {}
        for c, d in clusters.items():
            if isinstance(d, dict):
                result[c] = d

        return result

    def get_high_scored_avg_r2(self):
        _, v = next(iter(self.ml_models.items()))
        avg_r2 = '{:.9}'.format(v['avg_r2'])
        return avg_r2
