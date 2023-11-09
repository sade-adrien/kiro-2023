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
    n_clusters = find_number_of_substations(data)
    barycentres = turbines_cluster(data, 3)[0]
    possible_sub_sites = pd.DataFrame().from_dict(data["substation_locations"])[["x", "y"]].to_numpy()
    list_substations = []
    for barycentre_number in range(len(barycentres)):
        dict_distances_sites_to_barycentre = {}
        for site_number in range(len(possible_sub_sites)):
            dict_distances_sites_to_barycentre[site_number + 1] = np.linalg.norm(barycentres[barycentre_number] - possible_sub_sites[site_number])
        

        # get the key from the min value
        key_min = min(dict_distances_sites_to_barycentre.keys(), key=(lambda k: dict_distances_sites_to_barycentre[k]))
        list_substations.append(substation(
            id= key_min,
            land_cable_type = 1,
            substation_type = 1).to_dict())
    return list_substations

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