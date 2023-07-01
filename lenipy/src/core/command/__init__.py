"""Commands are parse using python standard libary argparse
"""
import argparse

def init():
    parser = argparse.ArgumentParser(prog="Leni",
                                     description="Local Environment Neural Int.",
                                     epilog="by Jonas Napierski")

