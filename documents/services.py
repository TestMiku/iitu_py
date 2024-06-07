import pathlib

from django.core.files.storage import Storage, default_storage


def get_path(user: str, /, *args: str) -> pathlib.Path:
    return pathlib.Path(f"p1/documents/{user}", *args)


def get_absolute_path(user: str, /, *args: str, storage: Storage = default_storage) -> pathlib.Path:
    return pathlib.Path(storage.path(get_path(user, *args)))


def set_path(instance) -> None:
    instance.path = instance.get_real_name() if instance.parent is None else str(
        (pathlib.Path(instance.parent.path) / instance.get_real_name()).as_posix())
