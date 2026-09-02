import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

repository_root = Path(__file__).resolve().parent.parent

source_repository = (
    repository_root
    / "build"
    / "host"
    / "outputs"
    / "repo"
    / "com"
    / "example"
    / "jitlabtestingmodule"
)

github_group = os.environ.get(
    "GROUP",
    "com.github.DhruvPanchalSL",
)

repository_name = os.environ.get(
    "ARTIFACT",
    "jitlabtestingmodule",
)

release_version = os.environ.get(
    "VERSION",
    "1.0.0",
)

published_group = f"{github_group}.{repository_name}"

maven_local = (
    Path.home()
    / ".m2"
    / "repository"
    / Path(*published_group.split("."))
)

maven_namespace = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", maven_namespace)

for artifact_name in ("flutter_debug", "flutter_release"):
    artifact_root = source_repository / artifact_name

    aar_files = list(artifact_root.glob("*/*.aar"))

    if len(aar_files) != 1:
        raise RuntimeError(
            f"Expected exactly one AAR for {artifact_name}, "
            f"found {len(aar_files)}"
        )

    source_aar = aar_files[0]
    source_pom = source_aar.with_suffix(".pom")

    if not source_pom.exists():
        raise FileNotFoundError(source_pom)

    destination = (
        maven_local
        / artifact_name
        / release_version
    )

    destination.mkdir(parents=True, exist_ok=True)

    destination_aar = (
        destination
        / f"{artifact_name}-{release_version}.aar"
    )

    destination_pom = (
        destination
        / f"{artifact_name}-{release_version}.pom"
    )

    shutil.copy2(source_aar, destination_aar)

    pom_tree = ET.parse(source_pom)
    pom_root = pom_tree.getroot()

    pom_root.find(
        f"{{{maven_namespace}}}groupId"
    ).text = published_group

    pom_root.find(
        f"{{{maven_namespace}}}artifactId"
    ).text = artifact_name

    pom_root.find(
        f"{{{maven_namespace}}}version"
    ).text = release_version

    pom_tree.write(
        destination_pom,
        encoding="utf-8",
        xml_declaration=True,
    )

    print(
        f"Published "
        f"{published_group}:{artifact_name}:{release_version}"
    )