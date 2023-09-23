#!/usr/bin/env python
# -*- coding: utf-8 -*-


def build_kernel() -> None:
    from build_api.worker import Worker

    worker: Worker = Worker('BuildImage', 'build_image')

    worker.run('mkdir build -p', task_name='Make dir')
    worker.run('cmake .. -G Ninja', '/project/build', task_name='CMake configure')
    worker.run('cmake --build .', '/project/build', task_name='CMake build')
