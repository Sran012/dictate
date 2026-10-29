# entrypoint. the whole product is: install the bits, get talking, type what
# you said. for now it just prints a menu.
import argparse


def main():
    p = argparse.ArgumentParser(prog="bolo")
    sub = p.add_subparsers(dest="cmd")

    for name, help_text in [
        ("install", "one command, whole pipeline"),
        ("setup", "repair if something died"),
        ("test", "say something, show me the words"),
        ("uninstall", "clean the service and the permission"),
    ]:
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("--dry-run", action="store_true")

    args = p.parse_args()
    print(f"bolo {args.cmd} — wiring this up next")


if __name__ == "__main__":
    main()
