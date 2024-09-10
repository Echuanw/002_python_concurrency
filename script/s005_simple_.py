import socket
from urllib.parse import urlparse

def get_url_normal(url):
    """通过 socket 请求 html"""
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"


    # 建立 socket 连接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 80))

    client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))
    
    # 接受数据
    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    html_data = data.split("\r\n\r\n")[1]
    print(html_data)

    client.close()

def main():
    # get_url_normal("https://www.baidu.com/")

if __name__ == '__main__':
    main()