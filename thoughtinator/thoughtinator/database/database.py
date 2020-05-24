from functools import cached_property

from typing import Optional, Iterable, overload, List, Union, cast

from . import DatabaseDriver, User, Snapshot


class Database:
    """
    A wrapper for the access to the database via drivers
    For more info see Database.users and Database.snapshots
    """
    def __init__(self, driver: DatabaseDriver):
        """ Creates a new database driver wrapper
        :type driver: DatabaseDriver
        :param driver: the driver to wrap
        """
        self._driver: DatabaseDriver = driver

    @cached_property
    def users(self):
        """
        The users in the database
        Use iter(database.users) to get all users.
        Use database.users[user_id] to get a specific user
        """
        class UsersProxy:
            def __iadd__(_, user: User):
                self._driver.put_user(user)

            def __getitem__(_, user_id: int) -> Optional[User]:
                return self._driver.fetch_user(user_id)

            def __contains__(_, user_id: int):
                return user_id in self._driver.fetch_users()

            def __iter__(_) -> Iterable[User]:
                return iter(self._driver.fetch_users())
        return UsersProxy()

    @cached_property
    def snapshots(self):
        class SnapshotsProxy:
            """
            The snapshots in the database
            Use database.snapshots[user] to get all snapshots of a user
            Use database.snapshots[snapshot_id] to get a specific snapshot
            """
            @overload
            def __getitem__(_, snap_id: int) -> Optional[Snapshot]: ...  # noqa: F811, E501

            @overload
            def __getitem__(_, user: User) -> List[Snapshot]: ...  # noqa: F811

            def __getitem__(_, index) -> Union[List[Snapshot], Optional[Snapshot]]:  # noqa: F811, E501
                if isinstance(index, int):
                    return self._driver.fetch_snapshot(cast(int, index))
                else:
                    return self._driver.fetch_snapshots(
                        cast(User, index)['user_id'])

        return SnapshotsProxy()

    @property
    def savers(self):
        return self._driver.savers
