#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker  # https://github.com/docker/docker-py
import os


class Worker:
    __MAIN_FOLDER: str = os.getcwd()
    __IMAGE_FOLDER: str = f"{__MAIN_FOLDER}/{'images'}"

    __name: str

    def __init__(self, dockerfile: str, name: str) -> None:
        self.__name = name

        client = docker.from_env()
        image_name: str = f"{self.__name}:latest"

        for image in client.images.list():
            if image_name in image.attrs["RepoTags"]:
                return

        client.images.build(
            path=self.__IMAGE_FOLDER,
            dockerfile=f"{self.__IMAGE_FOLDER}/{dockerfile}",
            tag=f"{self.__name}",
        )

    def run_image(self, command: str, working_dir: str = "/build") -> None:
        client = docker.from_env()
        container = None

        try:
            container = client.containers.run(
                self.__name,
                command=command,
                volumes={self.__MAIN_FOLDER: {"bind": "/build", "mode": "rw"}},
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
