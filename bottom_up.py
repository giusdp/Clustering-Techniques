from sklearn.datasets.samples_generator import make_blobs
from matplotlib import pyplot
from pandas import DataFrame
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering


def create_blob_dataset(n_samples, n_clusters):
    X, y = make_blobs(n_samples=n_samples, centers=n_clusters, n_features=2) # generate 2d dataset
    df = DataFrame(dict(x=X[:,0], y=X[:,1], label=y))
    return df    

def make_dendogram(dataframe):
    # max 16 colors to identify clusters. So DO NOT set more than 16 clusters at a time. Otherwise error with colors[key] below
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna', 'khaki', 'fuchsia']
    _, ax = pyplot.subplots()
    grouped = dataframe.groupby('label')
    pyplot.title("Created Clusters")  
    for key, group in grouped:
        group.plot(ax=ax, kind='scatter', x='x', y='y', label=key, color=colors[key])

    pyplot.figure(figsize=dataframe.shape)  
    pyplot.title("Cluster Dendogram")  
    shc.dendrogram(shc.linkage(dataframe, method='ward'))

def learn_clusters(dataframe, n_clusters):
    cluster = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')  
    cluster.fit_predict(dataframe) 

    pyplot.figure(figsize=dataframe.shape)  
    pyplot.title("Learned Clusters with Hierarchical Bottom-Up Approach")
    pyplot.scatter(dataframe.x, dataframe.y, c=cluster.labels_, cmap='rainbow')  

def bottom_up_clustering(n_samples, n_clusters, n_clusters_to_learn):
    dataframe = create_blob_dataset(n_samples, n_clusters)
    make_dendogram(dataframe)
    learn_clusters(dataframe, n_clusters_to_learn)

if __name__ == '__main__':
    n_samples = 100
    n_clusters = 100
    n_clusters_to_learn = 2
    bottom_up_clustering(n_samples, n_clusters, n_clusters_to_learn)
    pyplot.show()