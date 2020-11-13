from os.path import dirname, realpath

from boostcfg import BoostConfigParser

SCRIPT_DIR = dirname(realpath(__file__))
FILENAME = f"{SCRIPT_DIR}/example.cfg"


def test_append_value_from_line():
    cfg = BoostConfigParser()
    cfg.append_value_from_line("  key = \t value")
    cfg.append_value_from_line("float = 3.14")
    cfg.append_value_from_line("int = -11")
    cfg.append_value_from_line("false_bool = False")
    cfg.append_value_from_line("true_bool = true")
    assert cfg["key"] == "value"
    assert cfg["float"] == float(3.14)
    assert cfg["int"] == int(-11)
    assert not cfg["false_bool"]
    assert cfg["true_bool"]
    cfg.append_value_from_line("key = value")
    cfg.append_value_from_line("TheUniverse=True")
    cfg.read_config(FILENAME, reset=False)
    assert cfg["key"] == ["value", "value"]
    assert cfg["TheUniverse"]


def test_boostcfg_init():
    cfg = BoostConfigParser(FILENAME)
    assert cfg["errLogMode"] == "trace"
    assert cfg["noOfDataEvents"] == int(7860)
    assert cfg["cmsMass"] == float(4.18)
    assert cfg["name"] == "_epem"
    assert cfg["verbose"]
    assert cfg["histMass"] == ["pion+ D0", "pion+ D-", "D0 D-"]


def test_boostcfg_read_config():
    cfg = BoostConfigParser()
    cfg.read_config(FILENAME, reset=True)
    assert cfg["productionFormalism"] == "Cano"
    cfg.read_config(FILENAME, reset=False)
    assert cfg["productionFormalism"] == ["Cano", "Cano"]
