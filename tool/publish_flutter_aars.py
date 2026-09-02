import glob
import os
import shutil
import xml.etree.ElementTree as ET


repository_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

source_repository = os.path.join(
    repository_root,
    "build",
    "host",
    "outputs",
    "repo",
    "com",
    "example",
    "jitlabtestingmodule",
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

published_group = "{}.{}".format(
    github_group,
    repository_name,
)

maven_repository_root = os.environ.get(
    "MAVEN_LOCAL_REPOSITORY",
    os.path.join(os.path.expanduser("~"), ".m2", "repository"),
)

maven_local = os.path.join(
    maven_repository_root,
    *published_group.split(".")
)

maven_namespace = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", maven_namespace)

for artifact_name in ("flutter_debug", "flutter_release"):
    artifact_root = os.path.join(source_repository, artifact_name)
    aar_files = glob.glob(os.path.join(artifact_root, "*", "*.aar"))

    if len(aar_files) != 1:
        raise RuntimeError(
            "Expected exactly one AAR for {}, found {}".format(
                artifact_name,
                len(aar_files),
            )
        )

    source_aar = aar_files[0]
    source_pom = os.path.splitext(source_aar)[0] + ".pom"

    if not os.path.isfile(source_pom):
        raise IOError("Missing POM: {}".format(source_pom))

    destination = os.path.join(
        maven_local,
        artifact_name,
        release_version,
    )

    if not os.path.isdir(destination):
        os.makedirs(destination)

    destination_aar = os.path.join(
        destination,
        "{}-{}.aar".format(artifact_name, release_version),
    )

    destination_pom = os.path.join(
        destination,
        "{}-{}.pom".format(artifact_name, release_version),
    )

    shutil.copy2(source_aar, destination_aar)

    pom_tree = ET.parse(source_pom)
    pom_root = pom_tree.getroot()

    pom_root.find(
        "{" + maven_namespace + "}groupId"
    ).text = published_group

    pom_root.find(
        "{" + maven_namespace + "}artifactId"
    ).text = artifact_name

    pom_root.find(
        "{" + maven_namespace + "}version"
    ).text = release_version

    pom_tree.write(
        destination_pom,
        encoding="utf-8",
        xml_declaration=True,
    )

    print(
        "Published {}:{}:{}".format(
            published_group,
            artifact_name,
            release_version,
        )
    )
