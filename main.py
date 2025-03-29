import speedtest
import datetime
import plotext as plt
import os

# upload and download in Mbit
# format: download,upload,ping,date,server_name,server_id
home_path = os.path.expanduser("~") + '/'
file = home_path + "data.csv"


def toMbit(d: float):
    """
    :return d / 2**20
    """
    return d / 2**20


def plot_data(server_id_=None):
    """
    :param server_id_: 
    """
    with open(file, "r") as f:
        x_data = []
        y_data = []
        for line in f.readlines():
            split = line.split(",")
            download, upload, ping, date, server_name, server_id = split
            download = float(download)
            upload = float(upload)
            ping = float(ping)
            date = datetime.datetime.fromisoformat(date)
            server_id = int(server_id)

            # print(date, download, upload, ping, server_name, server_id, server_id_)
            if server_id_ is not None and server_id_ == server_id:
                x_data.append(date)
                y_data.append(toMbit(download))

        # 2025-03-29 16:08:49
        plt.date_form("d/m/Y H:M:S")
        x_data = plt.datetimes_to_string(x_data)
        plt.plot(x_data, y_data)
        plt.show()


def get_data():
    """
    :return true/false on success/error
    """
    # If you want to test against a specific server
    # servers = [1234]
    servers = []
    
    # If you want to use a single threaded test
    # threads = 1
    threads = None
    
    d = datetime.datetime.now().isoformat()
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()
    
    # {
    #    'download': 85803322.07903455, 
    #    'upload': 38158177.68618681, 
    #    'ping': 94.873, 
    #    'server': {
    #        'url': 'http://fra-eq5-tptest1.31173.se:8080/speedtest/upload.php',
    #        'lat': '50.1109',
    #        'lon': '8.6821',
    #        'name': 'Frankfurt',
    #        'country': 'Germany',
    #        'cc': 'DE',
    #        'sponsor': '31173 Services AB',
    #        'id': '23095',
    #        'host': 'fra-eq5-tptest1.31173.se:8080',
    #        'd': 0.892336482937424,
    #        'latency': 94.873
    #    }, 
    #    'timestamp': '2025-03-29T14:46:22.228927Z',
    #    'bytes_sent': 48357376,
    #    'bytes_received': 108111248,
    #    'share': 'http://www.speedtest.net/result/17550269379.png',
    #    'client': {
    #        'ip': '138.199.38.154',
    #        'lat': '50.1188',
    #        'lon': '8.6843',
    #        'isp': 'Datacamp',
    #        'isprating': '3.7',
    #        'rating': '0',
    #        'ispdlavg': '0',
    #        'ispulavg': '0',
    #        'loggedin': '0',
    #        'country': 'DE'
    #    }
    # }
    r = s.results.dict()
    e = r["server"]
    data = str(r["download"]) + "," + str(r["upload"]) + "," + str(r["ping"]) \
            + "," + d + "," + e["name"] + "," + e["id"] + "\n"
    
    with open(file, "a") as f:
        f.write(data)
        return True 


if __name__ == '__main__':
    get_data()
    plot_data(server_id_= 8040)
