#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='date_from', required=True)
    parser.add_argument('--to', dest='date_to', required=True)
    args = parser.parse_args()
    print(f'Backfill range: {args.date_from} to {args.date_to}')


if __name__ == '__main__':
    main()
