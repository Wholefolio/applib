#!/usr/bin/env python
"""This script will generate a random 50-character string suitable for use as a SECRET_KEY."""
import random


def generate(length=50):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)'
    secure_random = random.SystemRandom()
    return ''.join(secure_random.sample(charset, length))


if __name__ == "__main__":
    print(generate())
