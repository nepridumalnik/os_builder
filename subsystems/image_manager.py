#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker  # https://github.com/docker/docker-py
import os

MAIN_FOLDER: str = os.getcwd()

BASE_TAG: str = "latest"
BUILD_IMAGE: str = "build_image"


def run_image(command: str, working_dir: str = "/build") -> None:
    client = docker.from_env()
    container = None

    try:
        container = client.containers.run(
            BUILD_IMAGE,
            command=command,
            volumes={MAIN_FOLDER: {"bind": "/build", "mode": "rw"}},
            working_dir=working_dir,
            detach=True,
        )
    except Exception as e:
        print(f"Failed with exception: {e}")
    finally:
        if container:
            logs = container.logs()
            print(logs.decode("utf-8"))

            container.wait()
            container.remove()


def prepare_image() -> None:
    client = docker.from_env()
    image_name: str = f"{BUILD_IMAGE}:{BASE_TAG}"

    for image in client.images.list():
        if image_name in image.attrs["RepoTags"]:
            return

    client.images.build(path=MAIN_FOLDER, tag=BUILD_IMAGE)
