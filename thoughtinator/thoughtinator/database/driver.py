from typing import Protocol, List, TypedDict, Optional
from datetime import datetime

Rotation = TypedDict('Rotation',
                     {'x': float, 'y': float, 'z': float, 'w': float})

Translation = TypedDict('Translation',
                        {'x': float, 'y': float, 'z': float})

Pose = TypedDict('Pose',
                 {'translation': Translation, 'rotation': Rotation})

ColorImage = TypedDict('ColorImage', {'path': str})
DepthImage = TypedDict('DepthImage', {'path': str})

User = TypedDict('User', {
        'user_id': int,
        'username': str,
        'birthday': datetime,
        'gender': int
    })

Feelings = TypedDict('Feelings', {
    'hunger': float,
    'thirst': float,
    'exhaustion': float,
    'happiness': float
})

Snapshot = TypedDict('Snapshot', {
        'user_id': int,
        'snap_id': int,
        'time': datetime,
        'pose': Pose,
        'color_image': ColorImage,
        'depth_image': DepthImage,
        'feeling': Feelings
    })


class DatabaseDriver(Protocol):
    def fetch_users(self) -> List[User]:
        pass

    def fetch_user(self, user_id: int) -> Optional[User]:
        pass

    def fetch_snapshots(self, user_id: int) -> Optional[List[Snapshot]]:
        pass

    def fetch_snapshot(self, snap_id: int) -> Optional[Snapshot]:
        pass

    def put_user(self, user: User):
        pass

    def put_snapshot(self, snapshot: Snapshot):
        pass
