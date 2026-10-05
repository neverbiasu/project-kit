import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from ledger import export


def test_export():
    assert export([("2026-09-20", 12.5, "午饭")]) == "date,amount,note\r\n2026-09-20,12.5,午饭\r\n"


if __name__ == "__main__":
    test_export()
    print("ok")
