from data import save_all_fund_lsjz, save_fund_list
import time


def main():
    timestamp = time.time()

    save_fund_list()

    timestamp = time.time() - timestamp
    print(timestamp)

    save_all_fund_lsjz()

    timestamp = time.time() - timestamp
    print(timestamp)


if __name__ == '__main__':
    main()
