from argparse import ArgumentParser


def register(parser: ArgumentParser):
    if parser is None:
        return

    parser.add_argument("--logfile", action="store_true", dest="log_to_file_b")
    parser.add_argument("--logpath", action="store_const", dest="log_path_s")
    parser.add_argument("--setlevel", choices=["INFO","DEBUG","ERROR"], dest="log_setlevel_s")

