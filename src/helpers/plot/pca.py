""" File for plotting PCA
"""

from typing import Any, Iterable, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def display_factorial_planes(
    X_projected: Iterable,
    x_y: Tuple[int, int],
    pca: Optional[Any] = None,
    labels: Optional[Sequence] = None,
    clusters: Optional[Sequence] = None,
    alpha: float = 1,
    figsize: Tuple = (10, 8),
    marker: str = ".",
):
    """
    Project the individuals on the factorial plan

    Parameters
    ----------
    X_projected : np.array
        The projected individuals.
    x_y : List[int]
        The axes to be displayed.
    pca : PCA, optional
        The PCA model, by default None
    labels : List[str], optional
        The labels of the individuals, by default None
    clusters : List[str], optional
        The clusters of the individuals, by default None
    alpha : float, optional
        The transparency of the points, by default 1
    figsize : Tuple[int, int], optional
        The size of the figure, by default (10,8)
    marker : str, optional
        The marker of the points, by default "."

    Raises
    ------
    ValueError
        - If the number of axes is not 2.
        - If the axes are out of range.
    """

    X_ = np.array(X_projected)
    if len(x_y) != 2:
        raise ValueError("2 axes needed")
    if max(x_y) >= X_.shape[1]:
        raise ValueError("axis out of range")
    x, y = x_y

    _, ax = plt.subplots(1, 1, figsize=figsize)
    sns.scatterplot(
        data=None, x=X_[:, x], y=X_[:, y], hue=clusters, alpha=alpha
    )

    if pca:
        v1 = f" {round(100*pca.explained_variance_ratio_[x])} %"
        v2 = f" {round(100*pca.explained_variance_ratio_[y])} %"
    else:
        v1 = v2 = ""

    ax.set_xlabel(f"F{x+1}{v1}")
    ax.set_ylabel(f"F{y+1}{v2}")

    x_max = np.abs(X_[:, x]).max() * 1.1
    y_max = np.abs(X_[:, y]).max() * 1.1
    ax.set_xlim(left=-x_max, right=x_max)
    ax.set_ylim(bottom=-y_max, top=y_max)

    plt.plot([-x_max, x_max], [0, 0], color="grey", alpha=0.8)
    plt.plot([0, 0], [-y_max, y_max], color="grey", alpha=0.8)

    if labels is not None:
        for i, (_x, _y) in enumerate(X_[:, [x, y]]):
            plt.text(
                _x,
                _y + 0.05,
                labels[i],
                fontsize="14",
                ha="center",
                va="center",
            )
    plt.title(f"Individuals projection (on F{x+1} & F{y+1})")
    plt.show()
