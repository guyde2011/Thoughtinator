from typing import Protocol, List, TypedDict, Optional, Dict, Callable


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
        'snap_id': int,
        'datetime': int,
        'pose': Pose,
        'color_image': ColorImage,
        'depth_image': DepthImage,
        'feeling': Feelings
    })


class DatabaseDriver(Protocol):
    """
    This is a type specification for how a driver **should** look.
    It is only optional, as using python protocols doesn't enforce any
    type hierarchy, but rather allows the user to know what to expect
    from each method
    """

    savers: Dict[str, Callable]

    def fetch_users(self) -> List[User]:
        """ Returns all users in the database

        :rtype: List[User]
        """
        ...

    def fetch_user(self, user_id: int) -> Optional[User]:
        """ Fetches a user with a given user id (or None if it doesn't exist)
        :type user_id: int
        :param user_id: the user id to fetch

        :rtype: User or None
        """
        ...

    def fetch_snapshots(self, user_id: int) -> Optional[List[Snapshot]]:
        """ Fetches the snapshots of a given user (or None if they don't exist)
        :type user_id: int
        :param user_id: the user's id

        :rtype: List[Snapshot] or None
        """
        ...

    def fetch_snapshot(self, snap_id: int) -> Optional[Snapshot]:
        """ Fetches a snapshot with a given id (or None if it doesn't exist)
        :type snap_id: int
        :param snap_id: the snapshots's id

        :rtype: Snapshot or None
        """
        ...

    def put_user(self, user: User):
        """ Puts a user in the database
        :type user: User
        :param user: the user to put
        """
        ...

    def put_snapshot(self, snapshot: Snapshot):
        """ Puts a snapshot in the database
        :type snapshot: Snapshot
        :param snapshot: the snapshot to put
        """
        ...
