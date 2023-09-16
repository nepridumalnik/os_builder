#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subsystems.image_manager import prepare_image, run_image


def main() -> None:
    prepare_image()
    run_image()

    print("Done!")


if __name__ == "__main__":
    main()
