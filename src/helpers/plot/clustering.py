import time
import warnings
from itertools import cycle, islice
from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from numpy.random import default_rng
from sklearn import cluster, datasets, mixture
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def sklearn_comparison(
    algorithms_to_take: List[Union[str, bool]],
    datasets_to_take: Optional[List[bool]] = None,
    figsize=(26, 13),
):
    """
    Compare the different clustering algorithms on the sklearn datasets.

    Parameters
    ----------
    clustering_algorithms : dict
        The clustering algorithms to be compared.
    datasets_to_take : list
        The datasets to be used.
    """

    if datasets_to_take is None:
        datasets_to_take = [
            True,
        ] * 6

    np.random.seed(0)

    # ============
    # Generate datasets. We choose the size big enough to see the scalability
    # of the algorithms, but not too big to avoid too long running times
    # ============
    n_samples = 500
    noisy_circles = datasets.make_circles(
        n_samples=n_samples, factor=0.5, noise=0.05
    )
    noisy_moons = datasets.make_moons(n_samples=n_samples, noise=0.05)
    blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
    no_structure = np.random.rand(n_samples, 2), None

    # Anisotropicly distributed data
    random_state = 170
    X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
    transformation = [[0.6, -0.6], [-0.4, 0.8]]
    X_aniso = np.dot(X, transformation)
    aniso = (X_aniso, y)

    # blobs with varied variances
    varied = datasets.make_blobs(
        n_samples=n_samples,
        cluster_std=[1.0, 2.5, 0.5],
        random_state=random_state,
    )

    # ============
    # Set up cluster parameters
    # ============
    plt.figure(figsize=figsize)
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.95, wspace=0.05, hspace=0.01
    )

    plot_num = 1

    default_base = {
        "quantile": 0.3,
        "eps": 0.3,
        "damping": 0.9,
        "preference": -200,
        "n_neighbors": 3,
        "n_clusters": 3,
        "min_samples": 7,
        "xi": 0.05,
        "min_cluster_size": 0.1,
    }

    final_datasets = [
        (
            noisy_circles,
            {
                "damping": 0.77,
                "preference": -240,
                "quantile": 0.2,
                "n_clusters": 2,
                "min_samples": 7,
                "xi": 0.08,
            },
        ),
        (
            noisy_moons,
            {
                "damping": 0.75,
                "preference": -220,
                "n_clusters": 2,
                "min_samples": 7,
                "xi": 0.1,
            },
        ),
        (
            varied,
            {
                "eps": 0.18,
                "n_neighbors": 2,
                "min_samples": 7,
                "xi": 0.01,
                "min_cluster_size": 0.2,
            },
        ),
        (
            aniso,
            {
                "eps": 0.15,
                "n_neighbors": 2,
                "min_samples": 7,
                "xi": 0.1,
                "min_cluster_size": 0.2,
            },
        ),
        (blobs, {"min_samples": 7, "xi": 0.1, "min_cluster_size": 0.2}),
        (no_structure, {}),
    ]

    final_datasets = [
        ds for ds, take in zip(final_datasets, datasets_to_take) if take
    ]

    for i_dataset, (dataset, algo_params) in enumerate(final_datasets):
        # update parameters with dataset-specific values
        params = default_base.copy()  # type: ignore
        params.update(algo_params)  # type: ignore

        X, y = dataset

        # normalize dataset for easier parameter selection
        X = StandardScaler().fit_transform(X)

        # estimate bandwidth for mean shift
        bandwidth = cluster.estimate_bandwidth(X, quantile=params["quantile"])

        # connectivity matrix for structured Ward
        connectivity = kneighbors_graph(
            X, n_neighbors=params["n_neighbors"], include_self=False
        )
        # make connectivity symmetric
        connectivity = 0.5 * (connectivity + connectivity.T)

        # ============
        # Create cluster objects
        # ============
        ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
        kmeans = cluster.KMeans(n_clusters=params["n_clusters"], n_init="auto")
        biscecting_kmeans = cluster.BisectingKMeans(
            n_clusters=params["n_clusters"]
        )
        two_means = cluster.MiniBatchKMeans(
            n_clusters=params["n_clusters"], n_init="auto"
        )
        ward = cluster.AgglomerativeClustering(
            n_clusters=params["n_clusters"],
            linkage="ward",
            connectivity=connectivity,
        )
        spectral = cluster.SpectralClustering(
            n_clusters=params["n_clusters"],
            eigen_solver="arpack",
            affinity="nearest_neighbors",
        )
        dbscan = cluster.DBSCAN(eps=params["eps"])
        optics = cluster.OPTICS(
            min_samples=params["min_samples"],
            xi=params["xi"],
            min_cluster_size=params["min_cluster_size"],
        )
        affinity_propagation = cluster.AffinityPropagation(
            damping=params["damping"],
            preference=params["preference"],
            random_state=0,
        )
        average_linkage = cluster.AgglomerativeClustering(
            linkage="average",
            metric="cityblock",
            n_clusters=params["n_clusters"],
            connectivity=connectivity,
        )
        birch = cluster.Birch(n_clusters=params["n_clusters"])
        gmm = mixture.GaussianMixture(
            n_components=params["n_clusters"], covariance_type="full"
        )

        clustering_algorithms = [
            ("KMeans", kmeans),
            ("MiniBatch\nKMeans", two_means),
            ("Bisecting\nKMeans", biscecting_kmeans),
            ("Affinity\nPropagation", affinity_propagation),
            ("MeanShift", ms),
            ("Spectral\nClustering", spectral),
            ("Ward", ward),
            ("Agglomerative\nClustering", average_linkage),
            ("DBSCAN", dbscan),
            ("OPTICS", optics),
            ("BIRCH", birch),
            ("Gaussian\nMixture", gmm),
        ]

        if isinstance(algorithms_to_take[0], str):
            clustering_algorithms = [
                ca
                for ca in clustering_algorithms
                if ca[0] in algorithms_to_take
            ]
        else:
            clustering_algorithms = [
                ca
                for ca, take in zip(clustering_algorithms, algorithms_to_take)
                if take
            ]

        for name, algorithm in clustering_algorithms:
            if isinstance(algorithms_to_take[0], str):
                if name not in algorithms_to_take:
                    continue
            else:
                if not algorithms_to_take[i_dataset]:
                    continue
            t0 = time.time()

            # catch warnings related to kneighbors_graph
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="the number of connected components of the "
                    + "connectivity matrix is [0-9]{1,2}"
                    + " > 1. Completing it to avoid stopping the tree early.",
                    category=UserWarning,
                )
                warnings.filterwarnings(
                    "ignore",
                    message="Graph is not fully connected, spectral embedding"
                    + " may not work as expected.",
                    category=UserWarning,
                )
                algorithm.fit(X)

            t1 = time.time()
            if hasattr(algorithm, "labels_"):
                y_pred = algorithm.labels_.astype(int)
            else:
                y_pred = algorithm.predict(X)

            plt.subplot(
                len(final_datasets), len(clustering_algorithms), plot_num
            )
            if i_dataset == 0:
                plt.title(name, size=18)

            colors = np.array(
                list(
                    islice(
                        cycle(
                            [
                                "#377eb8",
                                "#ff7f00",
                                "#4daf4a",
                                "#f781bf",
                                "#a65628",
                                "#984ea3",
                                "#999999",
                                "#e41a1c",
                                "#dede00",
                            ]
                        ),
                        int(max(y_pred) + 1),
                    )
                )
            )
            # add black color for outliers (if any)
            colors = np.append(colors, ["#000000"])
            plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_pred])

            plt.xlim(-2.5, 2.5)
            plt.ylim(-2.5, 2.5)
            plt.xticks(())
            plt.yticks(())
            plt.text(
                0.99,
                0.01,
                ("%.2fs" % (t1 - t0)).lstrip("0"),
                transform=plt.gca().transAxes,
                size=15,
                horizontalalignment="right",
            )
            plot_num += 1

    plt.show()


def cluster_analysis(data, model, n_c, cols, frac=None, seed_frac=42):
    """
    Analyse the clusters of a clustering model.

    Parameters
    ----------
    data : array-like
        The data to cluster.
    model : object
        The clustering model.
    n_c : int
        The number of clusters.
    cols : list
        The columns of the data.
    frac : float, optional
        The fraction of the data to use for the analysis. The default is None.
    seed_frac : int, optional
        The seed for the random number generator. The default is 42.
    """
    y = model.fit_predict(data)

    if frac is None:
        numbers = np.arange(data.shape[0])
    else:
        rng = default_rng(seed=seed_frac)
        numbers = rng.choice(
            data.shape[0], size=int(frac * data.shape[0]), replace=False
        )

    if isinstance(data, pd.DataFrame):
        df_seg = data.iloc[numbers]
    else:
        df_seg = pd.DataFrame(data[numbers], columns=cols)
    df_seg["cluster"] = y[numbers]
    values = df_seg["cluster"].value_counts()

    sns.pairplot(df_seg, hue="cluster").fig.suptitle(
        " - ".join(
            [f"C{i}({values[i]/sum(values)*100:.1f}%)" for i in range(n_c)]
        ),
        y=1.05,
    )
    plt.show()

    minmaxsc = ColumnTransformer(
        [
            ("tr", MinMaxScaler(), cols),
        ],
        remainder="passthrough",
    )
    df_seg_sc = pd.DataFrame(
        minmaxsc.fit_transform(df_seg), columns=df_seg.columns
    )
    df_seg_sc["cluster"] = df_seg_sc["cluster"].astype(int)
    df_long_sc = pd.melt(
        df_seg_sc, "cluster", var_name="column", value_name="value"
    )
    sns.boxplot(
        x="column", hue="cluster", y="value", data=df_long_sc
    ).set_title(
        " - ".join(
            [f"C{i}({values[i]/sum(values)*100:.1f}%)" for i in range(n_c)]
        )
    )
    plt.show()
