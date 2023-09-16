#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker  # https://github.com/docker/docker-py
from pathlib import Path
from os import path

MAIN_SCRIPT: Path = Path(path.realpath(__file__))
MAIN_FOLDER: str = str(MAIN_SCRIPT.parent.absolute())

BASE_TAG: str = "latest"
BUILD_IMAGE: str = "build_image"


def prepare_image(client: docker.DockerClient) -> None:
    image_name: str = f"{BUILD_IMAGE}:{BASE_TAG}"

    for image in client.images.list():
        if image_name in image.attrs["RepoTags"]:
            return

    client.images.build(path=MAIN_FOLDER, tag=BUILD_IMAGE)
