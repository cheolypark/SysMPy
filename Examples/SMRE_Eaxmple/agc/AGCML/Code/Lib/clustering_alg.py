import time
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice

class Clustering_Alg:
    def __init__(self, plot=False):
        self.datasets = []
        self.plot = plot
        self.selected_clustering_algorithms = []
        self.clustering_algorithms = {}

    def set_algs(self, algs):
        """
        :param algs: e.g., )'MiniBatchKMeans'
                            'AffinityPropagation'
                            'MeanShift'
                            'SpectralClustering'
                            'Ward'
                            'AgglomerativeClustering'
                            'DBSCAN'
                            'OPTICS'
                            'Birch'
                            'GaussianMixture'
        """
        self.selected_clustering_algorithms.append(algs)

    def set_data(self, X_data, y_data):
        new_data = (  # First data set
                        (  # X predictors [X1, X2]
                            # e.g., ) np.array([[10, 20], [20, 30], [11, 11], [11, 24], [25, 36], [12, 11], [30, 20]]),
                            X_data,
                            # Y target [Y]
                            # e.g., ) np.array([1, 0, 1, 1, 1, 0, 1])
                            y_data
                        ),
                        {  # Algorithm Parameters
                            # 'damping': 0.77, 'preference': -240,
                            # 'quantile': 0.2, 'n_clusters': 2, 'min_samples': 20, 'xi': 0.25
                        }
                    )

        self.datasets.append(new_data)
        self.set_base()

    def set_base(self, n_clusters=2):
        self.default_base = {'quantile': .3,
                             'eps': .3,
                             'damping': .9,
                             'preference': -200,
                             'n_neighbors': 10,
                             'n_clusters': n_clusters,
                             'min_samples': 10,
                             'xi': 0.05,
                             'min_cluster_size': 0.1}

    def get_clustering_alg(self):
        return self.clustering_algorithms[self.selected_clustering_algorithms[0]]

    def get_clustered_data(self, alg):
        """
        This returns clustered data according to a selected algorithm
        :param alg: a selected algorithm
        :return: clustered data
        """

        algorithm = self.clustering_algorithms[alg]
        # print(self.datasets)
        re_X_data = {}
        re_y_data = {}
        re_data = {}
        for i_dataset, (dataset, algo_params) in enumerate(self.datasets):
            X, y = dataset
            if isinstance(X, pd.DataFrame):
                for i in range(len(X.index)):
                    data_id = algorithm.labels_[i]
                    if data_id not in re_X_data:
                        re_X_data[data_id] = X.iloc[i].transpose()
                        re_y_data[data_id] = y.iloc[i]
                        re_data[data_id] = pd.concat([X.iloc[i], y.iloc[i]], axis=0)
                    else:
                        re_X_data[data_id] = pd.concat((re_X_data[data_id], X.iloc[i]), axis=1)
                        re_y_data[data_id] = pd.concat((re_y_data[data_id], y.iloc[i]), axis=1)
                        re_data[data_id] = pd.concat((re_X_data[data_id], re_y_data[data_id]), axis=0)

                for key in re_X_data:
                    re_X_data[key] = re_X_data[key].transpose()
                    re_y_data[key] = re_y_data[key].transpose()
                    re_data[key] = re_data[key].transpose()

            elif not isinstance(X, pd.DataFrame):
                for i in range(len(X)):
                    data_id = algorithm.labels_[i]
                    if data_id not in re_X_data:
                        re_X_data[data_id] = np.array([X[i]])
                        re_y_data[data_id] = np.array([y[i]])
                        re_data[data_id] = np.concatenate((re_X_data[data_id], re_y_data[data_id]), axis=1)
                    else:
                        re_X_data[data_id] = np.concatenate((re_X_data[data_id], [X[i]]), axis=0)
                        re_y_data[data_id] = np.concatenate((re_y_data[data_id], [y[i]]), axis=0)
                        re_data[data_id] = np.concatenate((re_X_data[data_id], re_y_data[data_id]), axis=1)

            return re_data, re_X_data, re_y_data

    def run(self):
        if self.plot:
            plt.figure(figsize=(9 * 2 + 3, len(self.datasets)*2))
            # plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05, hspace=.01)

        plot_num = 1
        for i_dataset, (dataset, algo_params) in enumerate(self.datasets):
            # update parameters with dataset-specific values
            params = self.default_base.copy()
            params.update(algo_params)

            X, y = dataset

            # normalize dataset for easier parameter selection
            X = StandardScaler().fit_transform(X)

            # estimate bandwidth for mean shift
            bandwidth = cluster.estimate_bandwidth(X, quantile=params['quantile'])

            # connectivity matrix for structured Ward
            connectivity = kneighbors_graph(X, n_neighbors=params['n_neighbors'], include_self=False)

            # make connectivity symmetric
            connectivity = 0.5 * (connectivity + connectivity.T)

            # ============
            # Create cluster objects
            # ============
            for alg in self.selected_clustering_algorithms:
                if alg is 'MiniBatchKMeans':
                    self.clustering_algorithms['MiniBatchKMeans'] = cluster.MiniBatchKMeans(n_clusters=params['n_clusters'])
                elif alg is 'AffinityPropagation':
                    self.clustering_algorithms['AffinityPropagation'] = cluster.AffinityPropagation(damping=params['damping'],preference=params['preference'])
                elif alg is 'MeanShift':
                    self.clustering_algorithms['MeanShift'] = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
                elif alg is 'SpectralClustering':
                    self.clustering_algorithms['SpectralClustering'] = cluster.SpectralClustering(n_clusters=params['n_clusters'], eigen_solver='arpack', affinity="nearest_neighbors")
                elif alg is 'Ward':
                    self.clustering_algorithms['Ward'] = cluster.AgglomerativeClustering(n_clusters=params['n_clusters'], linkage='ward', connectivity=connectivity)
                elif alg is 'AgglomerativeClustering':
                    self.clustering_algorithms['AgglomerativeClustering'] = cluster.AgglomerativeClustering(linkage="average", affinity="cityblock", n_clusters=params['n_clusters'], connectivity=connectivity)
                elif alg is 'DBSCAN':
                    self.clustering_algorithms['DBSCAN'] = cluster.DBSCAN(eps=params['eps'])
                elif alg is 'OPTICS':
                    self.clustering_algorithms['OPTICS'] = cluster.OPTICS(min_samples=params['min_samples'], xi=params['xi'], min_cluster_size=params['min_cluster_size'])
                elif alg is 'Birch':
                    self.clustering_algorithms['Birch'] = cluster.Birch(n_clusters=params['n_clusters'])
                elif alg is 'GaussianMixture':
                    self.clustering_algorithms['GaussianMixture'] = mixture.GaussianMixture(n_components=params['n_clusters'], covariance_type='full')

            # self.clustering_algorithms['MiniBatchKMeans'] = cluster.MiniBatchKMeans(n_clusters=params['n_clusters'])
            # self.clustering_algorithms['AffinityPropagation'] = cluster.AffinityPropagation(damping=params['damping'], preference=params['preference'])
            # self.clustering_algorithms['MeanShift'] = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
            # self.clustering_algorithms['SpectralClustering'] = cluster.SpectralClustering(n_clusters=params['n_clusters'], eigen_solver='arpack', affinity="nearest_neighbors")
            # self.clustering_algorithms['Ward'] = cluster.AgglomerativeClustering(n_clusters=params['n_clusters'], linkage='ward', connectivity=connectivity)
            # self.clustering_algorithms['AgglomerativeClustering'] = cluster.AgglomerativeClustering(linkage="average", affinity="cityblock", n_clusters=params['n_clusters'], connectivity=connectivity)
            # self.clustering_algorithms['DBSCAN'] = cluster.DBSCAN(eps=params['eps'])
            # self.clustering_algorithms['OPTICS'] = cluster.OPTICS(min_samples=params['min_samples'], xi=params['xi'], min_cluster_size=params['min_cluster_size'])
            # self.clustering_algorithms['Birch'] = cluster.Birch(n_clusters=params['n_clusters'])
            # self.clustering_algorithms['GaussianMixture'] = mixture.GaussianMixture(n_components=params['n_clusters'], covariance_type='full')

            for name, algorithm in self.clustering_algorithms.items():
                t0 = time.time()

                # catch warnings related to kneighbors_graph
                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore",
                        message="the number of connected components of the " +
                        "connectivity matrix is [0-9]{1,2}" +
                        " > 1. Completing it to avoid stopping the tree early.",
                        category=UserWarning)
                    warnings.filterwarnings(
                        "ignore",
                        message="Graph is not fully connected, spectral embedding" +
                        " may not work as expected.",
                        category=UserWarning)
                    algorithm.fit(X)

                t1 = time.time()
                if hasattr(algorithm, 'labels_'):
                    y_pred = algorithm.labels_.astype(np.int)
                else:
                    y_pred = algorithm.predict(X)
                    algorithm.labels_ = y_pred

                ################################################################
                # plot clusters
                if self.plot:
                    plt.subplot(len(self.datasets), len(self.clustering_algorithms), plot_num)
                    if i_dataset == 0:
                        plt.title(name, size=9)

                    colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
                                                         '#f781bf', '#a65628', '#984ea3',
                                                         '#999999', '#e41a1c', '#dede00']),
                                                  int(max(y_pred) + 1))))
                    # add black color for outliers (if any)
                    colors = np.append(colors, ["#000000"])
                    plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_pred])

                    plt.xlim(-2.5, 2.5)
                    plt.ylim(-2.5, 2.5)
                    plt.xticks(())
                    plt.yticks(())
                    plt.text(.99, .01, ('%.2fs' % (t1 - t0)).lstrip('0'),
                             transform=plt.gca().transAxes, size=8,
                             horizontalalignment='right')
                    plot_num += 1

        if self.plot:
            plt.show()


# # Test code
# X_data = np.array([[667. , 7],
#  [693.3, 7],
#  [732.9, 6],
#  [658.9, 1],
#  [702.8, 7],
#  [697.2, 1],
#  [658.7, 2],
#  [723.1, 1],
#  [719.5, 3],
#  [687.4, 1],
#  [704.1, 1],
#  [658.8, 4],
#  [667.8, 3],
#  [703.4, 3]])
# Y = np.array([[667. ],
#  [693.3],
#  [732.9],
#  [658.9],
#  [702.8],
#  [697.2],
#  [658.7],
#  [723.1],
#  [719.5],
#  [687.4],
#  [704.1],
#  [658.8],
#  [667.8],
#  [703.4]])
#
# cl = clusters()
# # np_X = np.concatenate((X_data, Y), axis=1)
# cl.set_data(X_data, Y)
# cl.run()
#
# data, _, _ = cl.get_clustered_data('GaussianMixture')
#
# print(data)