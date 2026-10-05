import csv, io, sys


def export(rows):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["date", "amount", "note"])
    w.writerows(rows)
    return buf.getvalue()


if __name__ == "__main__" and sys.argv[1:2] == ["export"]:
    print(export([("2026-09-20", 12.5, "午饭")]), end="")
