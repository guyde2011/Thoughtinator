from typing import Protocol, TypedDict, Generator, Iterable, Any


Rotation = TypedDict('Rotation',
                     {'x': float, 'y': float, 'z': float, 'w': float})

Translation = TypedDict('Translation',
                        {'x': float, 'y': float, 'z': float})

Pose = TypedDict('Pose',
                 {'translation': Translation, 'rotation': Rotation})

ColorImage = TypedDict('ColorImage', {
    'width': int,
    'height': int,
    'data': bytes
})

DepthImage = TypedDict('DepthImage', {
    'width': int,
    'height': int,
    'data': Iterable[float]
})

User = TypedDict('User', {
    'user_id': int,
    'username': str,
    'birthday': int,
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
    'datetime': int,
    'pose': Pose,
    'color_image': ColorImage,
    'depth_image': DepthImage,
    'feeling': Feelings
})


class ReaderDriver(Protocol):
    """
    This is a type specification for how a driver **should** look.
    It is only optional, as using python protocols doesn't enforce any
    type hierarchy, but rather allows the user to know what to expect
    from each method
    """
    user: User

    def read(self) -> Generator[Snapshot, Any, Any]:
        """Returns a generator to read snapshots
        :rtype: Generator[Snapshot]
        """
        ...
