from tools import *
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def turbines_sol(data):
    turbines_sol = []
    for t in data['wind_turbines']:
        turbines_sol.append(turbine(id=t['id'],
                                    substation_id=1).to_dict())
    return turbines_sol

def substation_substation_cables_sol(data):
    return []

def substations_sol(data):
    return [substation(1, 1, 1).to_dict()]

def turbines_cluster(data, n_clusters):
    idxy = pd.DataFrame().from_dict(data['wind_turbines'])
    id = idxy['id'].to_numpy()
    x = idxy[['x']].to_numpy()
    y = idxy[['y']].to_numpy()

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(y)

    cluster_centers = np.concatenate((np.mean(x) * np.ones_like(kmeans.cluster_centers_), kmeans.cluster_centers_), axis=1)
    labels = kmeans.labels_
    
    return (cluster_centers, (id, labels))