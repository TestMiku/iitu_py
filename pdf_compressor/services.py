import datetime
import mimetypes
import pathlib
import time
import uuid
import zipfile
from collections.abc import Iterable

import PIL.Image
from django.core.files.storage import Storage, default_storage
from django.core.files.uploadedfile import UploadedFile
from pypdf import PdfReader, PdfWriter


def get_absolute_path(
    path: pathlib.Path, storage: Storage = default_storage
) -> pathlib.Path:
    path = pathlib.Path(storage.path(path))
    path.mkdir(parents=True, exist_ok=True)
    return path


def compress(
    uploaded_files: Iterable[UploadedFile],
    /,
    *,
    percent: float = 0.5,
    output_path: pathlib.Path,
    storage: Storage = default_storage,
    delete_compressed_files: datetime.timedelta = datetime.timedelta(minutes=5),
) -> list[tuple[str, pathlib.Path]]:
    output_absolute_path = get_absolute_path(output_path, storage)

    for path in output_absolute_path.rglob("*"):
        if (
            path.is_file()
            and time.time() - path.stat().st_mtime >= delete_compressed_files.seconds
        ):
            path.unlink()

    paths = []
    for uploaded_file in uploaded_files:
        id_ = str(uuid.uuid4())
        path = output_absolute_path / id_ / uploaded_file.name
        (output_absolute_path / id_).mkdir()
        if uploaded_file.content_type == mimetypes.types_map[".pdf"]:
            pdf_reader = PdfReader(uploaded_file.file)
            pdf_writer = PdfWriter()
            if pdf_reader.metadata is not None:
                pdf_writer.add_metadata(pdf_reader.metadata)
            for page in pdf_reader.pages:
                page = pdf_writer.add_page(page)
                for index, image in enumerate(page.images):
                    width, height = image.image.size
                    try:
                        image = image.image.resize(
                            (int(width * percent), int(height * percent))
                        )
                        page.images[index].replace(image)
                    except ValueError:
                        pass

            pdf_writer.write(path)
        elif uploaded_file.content_type.startswith("image"):
            image = PIL.Image.open(uploaded_file.file)
            width, height = image.size
            try:
                image = image.resize((int(width * percent), int(height * percent)))
                image.save(path)
            except ValueError:
                pass
        paths.append((storage.url(output_path / id_ / uploaded_file.name), path))
    return paths


def archive(
    paths: Iterable[pathlib.Path],
    output_path: pathlib.Path,
    storage: Storage = default_storage,
) -> tuple[str, pathlib.Path]:
    name = str(uuid.uuid4()) + ".zip"
    zip_file_absolute_path = get_absolute_path(output_path, storage) / name
    with zipfile.ZipFile(zip_file_absolute_path, "w") as zip_file:
        for path in paths:
            zip_file.write(path, path.name)
    return storage.url(output_path / name), zip_file_absolute_path
