#!/usr/bin/env python
# -*- coding: utf-8 -*-


def build_kernel() -> None:
    from subsystems.worker import Worker

    worker: Worker = Worker("BuildImage", "build_image")

    worker.run("mkdir build -p")
    worker.run("cmake ..", "/build/build")
    worker.run("cmake --build .", "/build/build")
