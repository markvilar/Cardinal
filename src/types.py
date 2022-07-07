from dataclasses import dataclass, field

@dataclass
class Pose():
    id: str = ""
    timestamp: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    depth: float = -1.0
    altitude: float = -1.0
    roll: float = 0.0
    pitch: float = 0.0
    heading: float = 0.0
    data: list[any] = field(default_factory=list)

    def __post__init(self) -> None:
        """ """
        pass

def main():
    pose = Pose()
    print(pose)

if __name__ == "__main__":
    main()
