import os

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

@dataclass
class Deployment:
    key: str
    data: pd.DataFrame = None

    def __post_init__(self):
        pass

    def __getitem__(self, item):
        return self.data[item]

@dataclass
class Collection:
    path: str
    data: pd.DataFrame = None

    def __post_init__(self):
        if self.data is None:
            self.data = pd.read_csv(self.path, index_col=0)

    def __getitem__(self, item):
        return self.data[item]

    def get_deployments(self) -> list[Deployment]:
        deployments = []
        for key in self.data["deployment.key"].unique(): 
            data = self.data[self.data["deployment.key"] == key]
            deployments.append(Deployment(key, data))
        return deployments

@dataclass
class MultiDeploymentDataset():
    key: str
    deployments: list[Deployment] = field(default_factory=list)

    def add_deployment(self, deployment: Deployment):
        deployments.append(deployment)

    def add_deployments(self, deployments: list[Deployment]):
        self.deployments.extend(deployments)

    def save_dataset(self, path: str):
        pass
