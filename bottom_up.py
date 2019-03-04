from matplotlib import pyplot
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering


def make_dendrogram(dataframe):
    pyplot.figure()
    pyplot.title("Dendrogram")
    dendrogram(linkage(dataframe, 'ward'))


def learn_clusters(dataframe):
    cluster = AgglomerativeClustering(affinity='euclidean', linkage='ward')
    cluster.fit_predict(dataframe)
    pyplot.figure()
    pyplot.title("Learned Clusters with Hierarchical Bottom-Up Approach")
    pyplot.scatter(dataframe.x, dataframe.y, c=cluster.labels_, cmap='rainbow')


def bottom_up_clustering(dataframe):
    make_dendrogram(dataframe)
    learn_clusters(dataframe)

