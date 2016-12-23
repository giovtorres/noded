import sys
sys.path.insert(0, "bin")

import noded

testjob = {
    "uid": 35375,
    "jobid": 17753113,
    "memusage": 152219648,
    "memlimit": 42949672960,
    "cpusetcpus": [9,11,15,25,27,31],
    "proclist": set(["36840", "36844", "36873", "36877"]),
    "num_running_children": 6,
    "cpu_and_procs": {
        9: [["blastn", "R"]],
        11: [["blastn", "R"]],
        15: [["blastn", "R"]],
        25: [["blastn", "R"]],
        27: [["blastn", "R"]],
        31: [["blastn", "R"]]
    },
    "overloaded": False
}

def test_expand_cpuset():
    """Test cpuset expansion."""
    assert noded.expand_cpuset("0-3") == [0, 1, 2, 3]
    assert noded.expand_cpuset("8-11,24-27") == [8, 9, 10, 11, 24, 25, 26, 27]


def test_get_sys_info():
    """Test system info gathering."""
    sys_info = noded.get_sys_info()
    assert isinstance(sys_info["nodename"], str)
    assert isinstance(sys_info["total_logical_cpus"], int)


def test_parse_config():
    """Test noded.conf parsing."""
    config = noded.parse_config("conf/noded.conf")
    assert config.get("defaults", "redis_host") == "localhost"
    assert config.getint("defaults", "redis_port") == 6379
    assert config.getint("defaults", "redis_db") == 0
    assert config.getint("defaults", "redis_timeout") == 1
    assert config.getint("defaults", "sleep_time") == 30
    assert config.getint("defaults", "expire_time") == 300
    assert config.getint("defaults", "rb_maxlen") == 4


def test_lineup_children():
    """Test lineup_children function."""
    num_running_children, cpu_and_procs, job_overloaded = noded.lineup_children(
        [9, 11, 15, 25, 27, 31],
        set(['36844', '36877', '36840', '36873']),
        "tests/mockroot/proc"
    )
    assert num_running_children == 6
    assert cpu_and_procs == {
        9: [["blastn", "R"]],
        11: [["blastn", "R"]],
        15: [["blastn", "R"]],
        25: [["blastn", "R"]],
        27: [["blastn", "R"]],
        31: [["blastn", "R"]]
    }
    assert job_overloaded is False


def test_get_running_threads():
    """Test get_running_threads function."""
    running_threads = noded.get_running_threads("36877", "tests/mockroot/proc")
    assert running_threads == {
    '9': [['blastn', 'R', '36878']],
    '11': [['blastn', 'R', '36883']],
    '15': [['blastn', 'R', '36882']],
    '25': [['blastn', 'R', '36879']],
    '27': [['blastn', 'R', '36881']],
    '31': [['blastn', 'R', '36880']]
    }
