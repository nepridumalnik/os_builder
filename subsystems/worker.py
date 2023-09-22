#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker  # https://github.com/docker/docker-py
import os


class Worker:
    __MAIN_FOLDER: str = os.getcwd()
    __IMAGE_FOLDER: str = f'{__MAIN_FOLDER}/images'

    __name: str
    __client: docker.DockerClient

    def __init__(self, dockerfile: str, name: str) -> None:
        self.__name = name

        self.__client = docker.from_env()
        image_name: str = f'{self.__name}:latest'

        for image in self.__client.images.list():
            if image_name in image.attrs['RepoTags']:
                return

        self.__client.images.build(
            path=self.__IMAGE_FOLDER,
            dockerfile=f'{self.__IMAGE_FOLDER}/{dockerfile}',
            tag=f'{self.__name}',
        )

    def run(
        self, command: str, working_dir: str = '/build', shell: bool = True
    ) -> bool:
        success: bool = False
        container = None

        try:
            command_wrapper: str

            if shell:
                command_wrapper = f'bash -c \'{command}\''
            else:
                command_wrapper = command

            container = self.__client.containers.run(
                self.__name,
                command=command_wrapper,
                volumes={self.__MAIN_FOLDER: {'bind': '/build', 'mode': 'rw'}},
                working_dir=working_dir,
                detach=True,
                stdout=True,
            )

            success = True
        except Exception as e:
            print(f'Failed with exception: {e}')
        finally:
            if container:
                logs = container.logs(stream=True)
                for line in logs:
                    print(line.strip().decode('utf-8'))

                container.wait()
                container.remove()

        return success
