import os

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

import utm

@dataclass
class Deployment:
    key: str
    data: pd.DataFrame = None

    def __getitem__(self, item):
        return self.data[item]

    def get_data(self):
        return self.data

    def set_data(self, data: pd.DataFrame):
        self.data = data

def calculate_utm_position(row):
    (easting, northing, zone, band) \
        = utm.from_latlon(row["pose.lat"], row["pose.lon"])
    return pd.Series([easting, northing, zone, band], index=["pose.easting", 
        "pose.northing", "pose.utm_zone", "pose.utm_band"])

def calculate_utm_positions(deployment: Deployment) -> Deployment:
    data = deployment.get_data()
    utm_positions = data.apply(calculate_utm_position, axis = 1, 
        result_type="expand")
    return data.join(utm_positions)

@dataclass
class Collection:
    data: pd.DataFrame = None

    def __getitem__(self, item):
        return self.data[item]

    def load_from_file(self, path: str):
         if self.data is None:
            self.data = pd.read_csv(path, index_col=0)

    def get_deployments(self) -> list[Deployment]:
        deployments = []
        for key in self.data["deployment.key"].unique(): 
            data = self.data[self.data["deployment.key"] == key]
            deployments.append(Deployment(key, data))
        return deployments

@dataclass
class Dataset():
    key: str
    deployments: list[Deployment] = field(default_factory=list)

    def add_deployment(self, deployment: Deployment):
        deployments.append(deployment)

    def add_deployments(self, deployments: list[Deployment]):
        self.deployments.extend(deployments)

    def get_deployments(self) -> list[Deployment]:
        return self.deployments
