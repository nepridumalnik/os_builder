#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main() -> None:
    import argparse
    import scenarios

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--build", "-b", help="Собрать ядро", action="store_true")

    args = parser.parse_args()

    if args.build:
        scenarios.build_kernel()


if __name__ == "__main__":
    try:
        main()
        exit(0)
    except Exception as e:
        print(f"Failed with exception: {e}")
        exit(-1)
