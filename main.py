#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subsystems.worker import Worker


def main() -> None:
    worker: Worker = Worker("BuildImage", "build_image")

    worker.run("mkdir build -p")
    worker.run("cmake ..", "/build/build")
    worker.run("cmake --build .", "/build/build")

    print("Done!")


if __name__ == "__main__":
    main()
