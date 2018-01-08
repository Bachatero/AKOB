#!/usr/bin/env python

def countdown(n):
    "Count down from n, print only even numbers, stop at 0."

    while True:
        if n%2 == 0:
            print(n)
        n = n - 1
        if n == 0:
            break


countdown(12)
