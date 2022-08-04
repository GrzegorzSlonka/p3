import json
import csv
import time
import sys
import pickle
from abc import ABC, abstractmethod


class Dr(ABC):
    def __init__(self, path):
        self.path = path
        self.main()

    @staticmethod
    def check_time(f):
        def meas(*args, **kwargs):
            start = time.time()
            c = f(*args, **kwargs)
            end = time.time()
            print()
            print("We've found a car for you in", round(end - start, 7), "s")
            return c

        return meas

    @check_time
    def get_data(self, av=None):
        try:
            with open(self.path, 'r') as data:
                if '.json' in self.path:
                    rdr = json.load(data)
                elif '.csv' in self.path:
                    rdr = csv.DictReader(data, delimiter=';')

                if av is not None:
                    cars = [r for r in rdr if r['available'] == 'yes']
                else:
                    cars = [r for r in rdr]
            return sorted(cars, key=lambda d: float(d['price']))[:3]
        except FileNotFoundError:
            print("Entered file doesn't exist!")
            sys.exit(1)

    @abstractmethod
    def main(self):
        pass


class Main(Dr):
    def __init__(self, path='cars.csv'):
        super().__init__(path)
        self.cars = []

    def main(self):
        self.unpickle_cars()
        print()
        ic = input('Do you want to find the cheapest car? (y - yes, other key - exit the program)')
        if str(ic).lower() == 'y':
            ic = input('Search for currently available cars only? (y/n)')
            if str(ic).lower() == 'y':
                self.cars = self.get_data(av=True)
            elif str(ic).lower() == 'n':
                self.cars = self.get_data()
            for c in self.cars:
                print(c)
            print()
            ic = input('Do you want to pickle your choice? (y/n)')
            if str(ic).lower() == 'y':
                self.pickle_cars()
        else:
            sys.exit()
        self.main()

    def pickle_cars(self):
        p_out = open("cars.pkl", "wb")
        pickle.dump(self.cars, p_out)

    def unpickle_cars(self):
        try:
            p_in = open("cars.pkl", "rb")
            self.cars = pickle.load(p_in)
            print('Your pickled cars:')
            for c in self.cars:
                print(c)
        except FileNotFoundError:
            print("You don't have any pickled cars!")




