from tools import *
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def turbines_sol(data, substation_list, turbine_cluster):
    turbine_id, turbine_cluster =  turbine_cluster
    turbines_sol = []
    for t in range(len(data['wind_turbines'])):
        turbines_sol.append(
                            turbine(id=int(turbine_id[t]),
                                    substation_id=int(substation_list[turbine_cluster[t]]["id"])
                                    ).to_dict()

                                )   
    return turbines_sol

def substation_substation_cables_sol(data, substation_list):
    substation_substation_cables = []
    # sort sub_sub_cable_types_price by price
    sub_sub_cable_types_price = sub_sub_cable_types_price.sort_values(by="price")
    sub_sub_cable_types_id = int(sub_sub_cable_types_price.iloc[0]["id"])

    substation_list_with_coordinates = pd.DataFrame(substation_list)[["id"]].merge(pd.DataFrame().from_dict(data["substation_locations"]), left_on="id", right_on="id")
    while len(substation_list_with_coordinates) > 1:
        distances = substation_list_with_coordinates.copy()
        id_sub = distances.iloc[0]["id"]
        distances["distance"] = distances.apply(lambda x: (x['x'] - distances.iloc[0]['x'])**2 + (x['y'] - distances.iloc[0]['y'])**2, axis=1)
        distances = distances.sort_values(by="distance")

        substation_substation_cables.append(substation_substation_cable(int(id_sub), int(distances.iloc[1]["id"]), sub_sub_cable_types_id).to_dict())
        # delete first row of dataframe
        substation_list_with_coordinates = substation_list_with_coordinates.iloc[1:]

        # delete row with id equal to distances.iloc[1]["id"]
        substation_list_with_coordinates = substation_list_with_coordinates[substation_list_with_coordinates.id != distances.iloc[1]["id"]]

    return substation_substation_cables

def substations_sol(data, turbine_cluster):
    barycentres, turbine_cluster =  turbine_cluster

    possible_sub_sites = pd.DataFrame().from_dict(data["substation_locations"])[["x", "y"]].to_numpy()
    list_substations = []

    list_substations = []
    selected_substation_id = []
    for barycentre_number in range(len(barycentres)):
        dict_distances_sites_to_barycentre = {}
        for site_number in range(len(possible_sub_sites)):
            dict_distances_sites_to_barycentre[site_number + 1] = np.linalg.norm(barycentres[barycentre_number] - possible_sub_sites[site_number])
        
        # sort the dict_distances_sites_to_barycentre by value
        
        list_distances = [(k,v) for k,v in dict_distances_sites_to_barycentre.items()]
        list_distances.sort(key=lambda x: x[1])
        while list_distances[0][0] in selected_substation_id:
            list_distances.pop(0)
        key_min = list_distances[0][0]
        selected_substation_id.append(key_min)

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
