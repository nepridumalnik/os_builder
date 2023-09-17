#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def build_kernel() -> None:
    from subsystems.worker import Worker

    worker: Worker = Worker("BuildImage", "build_image")

    worker.run("mkdir build -p")
    worker.run("cmake ..", "/build/build")
    worker.run("cmake --build .", "/build/build")


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--build", "-b", help="Собрать ядро", action="store_true")

    args = parser.parse_args()

    if args.build:
        build_kernel()


if __name__ == "__main__":
    try:
        main()
        exit(0)
    except Exception as e:
        print(f"Failed with exception: {e}")
        exit(-1)
