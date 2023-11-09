from tools import *
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def turbines_sol(data, substation_list, turbine_cluster):
    turbine_id, turbine_cluster =  turbine_cluster
    turbines_sol = []
    for t in range(len(data['wind_turbines'])):
        turbines_sol.append(
                            turbine(id=turbine_id[t],
                                    substation_id=substation_list[turbine_cluster[t]]
                                    ).to_dict()

                                )   
    return turbines_sol

def substation_substation_cables_sol(data):
    return []

def substations_sol(data, turbine_cluster):
    barycentres, turbine_cluster =  turbine_cluster

    n_clusters = find_number_of_substations(data)
    possible_sub_sites = pd.DataFrame().from_dict(data["substation_locations"])[["x", "y"]].to_numpy()
    list_substations = []
    for barycentre_number in range(len(barycentres)):
        dict_distances_sites_to_barycentre = {}
        for site_number in range(len(possible_sub_sites)):
            dict_distances_sites_to_barycentre[site_number + 1] = np.linalg.norm(barycentres[barycentre_number] - possible_sub_sites[site_number])
        

        # get the key from the min value
        key_min = min(dict_distances_sites_to_barycentre.keys(), key=(lambda k: dict_distances_sites_to_barycentre[k]))
        
        sub_type = get_substation_type(data)
        land_cable_type = get_cable_land_type(data, sub_type)
        
        list_substations.append(substation(
            id= key_min,
            land_cable_type = land_cable_type['id'],
            substation_type = sub_type['id']
            ).to_dict())
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

def get_substation_type(data):
    min_rating = 1e6
    min_cost = 1e6
    eligible_types = []
    selected_type = None
    for substation_type in data['substation_types']:
        if min_rating > substation_type['rating']:
            min_rating = substation_type['rating']
            eligible_types = [substation_type]
        elif min_rating == substation_type['rating']:
            eligible_types.append(substation_type)

    for e in eligible_types:
        if min_cost > e['cost']:
            min_cost = e['cost']
            selected_type = e
    
    return selected_type

def get_cable_land_type(data, sub_type):
    eligible_land_cables = []
    for cable_type in data['land_substation_cable_types']:
        if cable_type['rating'] >= sub_type['rating']:
            eligible_land_cables.append(cable_type)

    min_cost = 1e6
    p = []
    for c in eligible_land_cables:
        if min_cost >= 25*c['variable_cost'] + c['fixed_cost']:
            p = [c]
        elif min_cost == 25*c['variable_cost'] + c['fixed_cost']:
            p.append(c)

    minval = min(p, key=lambda x: x['probability_of_failure'])
    p = [d for d in p if d['probability_of_failure'] == minval['probability_of_failure']]
    selected_type = max(p, key=lambda x: x['rating'])
    return selected_type
