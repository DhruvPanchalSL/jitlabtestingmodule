import os
import re


repository_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

flutter_build_gradle = os.path.join(
    repository_root,
    ".android",
    "Flutter",
    "build.gradle",
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

with open(flutter_build_gradle, "r", encoding="utf-8") as source_file:
    gradle_text = source_file.read()

gradle_text, group_replacements = re.subn(
    r'^group\s*=\s*["\'][^"\']+["\']\s*$',
    'group = "{}"'.format(published_group),
    gradle_text,
    count=1,
    flags=re.MULTILINE,
)

gradle_text, version_replacements = re.subn(
    r'^version\s*=\s*["\'][^"\']+["\']\s*$',
    'version = "{}"'.format(release_version),
    gradle_text,
    count=1,
    flags=re.MULTILINE,
)

if group_replacements != 1 or version_replacements != 1:
    raise RuntimeError(
        "Could not configure Maven group/version in {}".format(
            flutter_build_gradle,
        )
    )

with open(flutter_build_gradle, "w", encoding="utf-8") as destination_file:
    destination_file.write(gradle_text)

print("Configured Flutter AARs as {}:*:{}".format(
    published_group,
    release_version,
))
