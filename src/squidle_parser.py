import argparse
import os
import requests
import shutil

import pandas as pd
import utm

from tqdm import tqdm

from squidle import Collection, Deployment, MultiDeploymentDataset

def process_multi_deployment_dataset(name, collection_path, output_path):
    collection = Collection(collection_path)

    # Composite multi deployment dataset
    dataset = MultiDeploymentDataset(name)
    dataset.add_deployments(collection.get_deployments())

    # Create dataset for each deployment
        # Dataset:      deployment.key
        # Image name:   key
        # Image path:   path_best


    print("\nAbout to process poses. Continue?")
    input()

    # TODO: Create pose table
    pose_data = pd.DataFrame()
    for index, row in tqdm(collection.data.iterrows(), 
        desc="Processing poses..."):
        # TODO: UTM coordinates
        u = utm.from_latlon(row["pose.lat"], row["pose.lon"])

    print("\nAbout to download images. Continue?")
    input()

    # TODO: Download images
    for index, row in tqdm(collection.data.iterrows(), 
        desc="Downloading images..."):
        image_path = output_path + "images/" + row["key"] + ".jpg"
        if not os.path.exists(image_path):
            res = requests.get(row["path_best"], stream = True)
            if res.status_code == 200:
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
        else:
            continue

    pass

def main():
    parser = argparse.ArgumentParser()

    name = "tasmania_box_36"

    path = "/home/martin/pCloudDrive/research/data/imos/squidle" \
        + "/collections/tasmania_box_36_3_revisits.csv"

    output = "/home/martin/pCloudDrive/research/data/imos/squidle" \
        + "/tasmania_box_36/"

    process_multi_deployment_dataset(name, path, output)
        
if __name__ == "__main__":
    main()
