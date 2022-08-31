import argparse
import os
import requests
import shutil

import pandas as pd

from tqdm import tqdm

from squidle import Collection, Deployment, Dataset, calculate_utm_positions

def download_dataset(dataset_name, collection_path, output_path):
    """
    """
    # Load collection from file
    collection = Collection()
    collection.load_from_file(collection_path)

    # Compose dataset
    dataset = Dataset(dataset_name)
    dataset.add_deployments(collection.get_deployments())

    # TODO: For each deployment, process poses
    for deployment in dataset.get_deployments():
        deployment.set_data(calculate_utm_positions(deployment))

    print("\nAbout to download images. Continue?")
    input()

    # TODO: For each deployment, save poses and images

    # TODO: Download images
    for index, row in tqdm(collection.data.iterrows(), 
        desc="Downloading images..."):
        image_path = output_path + "/images/" + row["key"] + ".jpg"
        if not os.path.exists(image_path):
            response = requests.get(row["path_best"], stream = True)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
        else:
            continue

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')    
    parser.add_argument('name', type=str, 
        help='name of the dataset')
    parser.add_argument('collection', type=str, 
        help='path to the squidle collection')
    parser.add_argument('output', type=str, 
        help='output directory of the parsed dataset')

    args = parser.parse_args()

    download_dataset(args.name, args.collection, args.output)
        
if __name__ == "__main__":
    main()
