#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker
from images.image_manager import prepare_image


def main() -> None:
    client = docker.from_env()
    prepare_image(client=client)

    print("Done!")


if __name__ == "__main__":
    main()
