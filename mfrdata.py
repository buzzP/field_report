import os
import datetime


class MFRdata:
    script_dir = os.path.dirname(__file__)

    def __init__(self):
        self.filename = None
        self.items = None    # was 'users'
        self.file = None

    def create_folder(self, path, name, record, dist):
        try:
            if os.path.isdir(path):
                print("Error: The Directory you're trying to create already exists")
            else:
                os.makedirs(path)
                with open(os.path.join(path, '{0}_{1}.txt'.format(path, 'MFR')), "a") as ip_file:
                    # could print project information to these first rows
                    ip_file.write('Project: ' + '\t' + str(name) + '\n')
                    ip_file.write('Project Number: ' + '\t' + str(path) + '\n')
                    ip_file.write('Engineer of Record: ' + '\t' + str(record) + '\n')
                    ip_file.write('Distribution: ' + '\t' + str(dist) + '\n')

        except IOError as exception:
            raise IOError('%s: %s' % (path, exception.strerror))
        return None

    def create_file(self, fl):
        self.file = open(os.path.join(fl, '{0}_{1}.txt'.format(fl, 'MFR')), 'wb')
        self.file.close()

    def number_of_items(self, n):
        self.file = open(os.path.join(self.script_dir, n, '{0}_{1}.txt'.format(n, 'MFR')), "r")
        num = 0
        for line in self.file:
            num = num + 1
            print(f'number of lines in file is {num}')
        return num

    def get_last_item(self, n):
        # get last field report item number, to keep ordering sequentially
        self.file = open(os.path.join(self.script_dir, n, '{0}_{1}.txt'.format(n, 'MFR')), "r")

        count = 0
        for line in self.file:
            # this may be wrong and need to be updated for this function to work
            num = line[0]
            print(f' type of first object is {str(type(num))}')
            date = line[5]
            if num.isnumeric():
                print(f' first value is {num}')
                number, location, description, photo, action, dt = line.strip().split("\t")
                print(f' number {number}, location {location}, description {description}, photo {photo}, action {action}, date {dt}')
                count = int(number) + 1
        # check if the text file has any 'items'; if not a number then return 0
        return count

    def save_item(self, p, n, l, d, a, pic):
        # write data into the text file
        with open(os.path.join(self.script_dir, p, '{0}_{1}.txt'.format(p, 'MFR')), 'a') as f:  # a is used to append to file, instead of 'w'
            f.write(str(n) + '\t')
            f.write(str(l) + '\t')
            f.write(str(d) + '\t')
            f.write(str(pic) + '.png' + '\t')
            f.write(str(a) + '\t')
            f.write(str(datetime.datetime.today()) + '\t')
            f.write('\n')
