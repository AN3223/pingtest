from multiping import MultiPing
from pandas import DataFrame, read_pickle, datetime
from time import sleep

IPS = ["8.8.8.8", "1.1.1.1", "127.0.0.1", "192.168.1.1"]
PICKLE_PATH = "ping_stats.pkl.zip"
TIMEOUT = 10
INTERVAL_SECONDS = 1
try:
    df = read_pickle(PICKLE_PATH)
except FileNotFoundError:
    df = DataFrame({k: [] for k in IPS})


def ping(ips, timeout):
    mp = MultiPing(ips)
    mp.send()
    return mp.receive(timeout)


while True:
    success, fail = ping(IPS, TIMEOUT)
    pingdata = DataFrame(
            {k: [v] for k, v in success.items()},
            index=[datetime.now()]
    )
    print(pingdata)
    df = df.append(pingdata, sort=True)
    df.to_pickle(PICKLE_PATH)
    sleep(INTERVAL_SECONDS)
