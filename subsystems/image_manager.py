#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker  # https://github.com/docker/docker-py
from pathlib import Path
from os import path

MAIN_SCRIPT: Path = Path(path.realpath(__name__))
MAIN_FOLDER: str = str(MAIN_SCRIPT.parent.absolute())

BASE_TAG: str = "latest"
BUILD_IMAGE: str = "build_image"


def run_image() -> None:
    client = docker.from_env()
    client.containers.run(BUILD_IMAGE, command="/bin/bash")


def prepare_image() -> None:
    client = docker.from_env()
    image_name: str = f"{BUILD_IMAGE}:{BASE_TAG}"

    for image in client.images.list():
        if image_name in image.attrs["RepoTags"]:
            return

    client.images.build(path=MAIN_FOLDER, tag=BUILD_IMAGE)
