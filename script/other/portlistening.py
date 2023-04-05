import os
import argparse
def portlistening(port):
    print("正在监听...")
    command="python3 -m http.server" + " "+ str(port)
    print(os.system(command))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    print(portlistening(args.port))