from getter import Getter
from tester import Tester

def run_getter():
    getter = Getter()
    getter.run()

def run_tester():
    tester = Tester()
    tester.run()

if __name__ == '__main__':
    run_getter()
    run_tester()