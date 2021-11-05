from typing import Union
from fibsem_metadata.models.index import Index
from fibsem_metadata.utils import materialize_element
import click
from pathlib import Path
from fibsem_metadata.models.manifest import DatasetManifest
from fibsem_metadata.models.metadata import DatasetMetadata
from fibsem_metadata.models.views import DatasetViews
from fibsem_metadata.models.sources import VolumeSource


def validate_tree(root: str) -> None:
    """
    root must be a string naming a directory tree that contains a
    directory called "datasets" populated with directories with variable
    names, which contain a subdirectory called "sources"
    """
    datasets_path = Path(root) / "metadata"
    if not (datasets_path.exists() and datasets_path.is_dir()):
        raise OSError(f"Metadata directory {str(datasets_path)} is invalid.")

    for subpath in datasets_path.glob("*"):
        manifest_file = subpath / "manifest.json"
        if not (manifest_file.exists() and manifest_file.is_file()):
            raise FileNotFoundError(f"Could not find {str(manifest_file)}")


def build_manifest(dataset_path: Union[Path, str]) -> int:
    root = Path(dataset_path)
    manifest_path = root / "manifest.json"
    source_paths = (root / "sources").glob("*.json")
    metadata_path = root / "metadata.json"
    views_path = root / "views.json"
    name = root.parts[-1]

    volumes = [materialize_element(path, VolumeSource) for path in source_paths]
    views = materialize_element(views_path, DatasetViews)
    metadata = materialize_element(metadata_path, DatasetMetadata)
    manifest = DatasetManifest(
        name=name, metadata=metadata, volumes=volumes, views=views.views
    )
    manifest_path.write_text(manifest.json(indent=2))
    return 0


@click.command()
@click.argument("root", type=click.Path(exists=True, file_okay=False))
def main(root: str) -> int:
    paths = tuple(filter(lambda v: v.is_dir(), Path(root).glob("*")))
    # generate the manifest
    [build_manifest(path) for path in paths]
    # generate the index
    index = Index(datasets=tuple(map(str, paths)))
    with open(Path(root) / "index.json", mode="w") as fh:
        fh.write(index.json())
    return 0


if __name__ == "__main__":
    main()
