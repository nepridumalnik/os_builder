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
        self,
        command: str,
        working_dir: str = '/project',
        shell: bool = True,
        noexcept: bool = False,
        task_name: str = '',
    ) -> int:
        command_wrapper: str = f'bash -c \'{command}\'' if shell else command

        container = self.__client.containers.run(
            self.__name,
            command=command_wrapper,
            volumes={self.__MAIN_FOLDER: {'bind': '/project', 'mode': 'rw'}},
            working_dir=working_dir,
            detach=True,
            stdout=True,
        )

        logs = container.logs(stream=True)
        for line in logs:
            print(line.strip().decode('utf-8'))

        result = container.wait()
        container.remove()

        status_code: int = int(result['StatusCode'])

        if not noexcept and status_code:
            error_text: str

            if task_name:
                error_text = f'task {task_name} finished with error: {status_code}'
            else:
                error_text = f'task finished with error: {status_code}'

            raise Exception(error_text)

        return status_code
