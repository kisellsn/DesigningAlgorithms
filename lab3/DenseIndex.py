import fileinput
import os

class DenseIndex:
    def __init__(self, data_file, index_file):
        self.data_file = data_file
        self.index_file = index_file

    def build_index(self):
        mas=[]
        with open(self.index_file, 'w') as i_file:
            with open(self.data_file, 'r') as d_file:
                d_file.seek(0)
                i_file.seek(0)
                i_file.truncate()
                current_offset = 0
                for line in d_file:
                    search_key, data = line.strip().split(',')
                    search_key = int(search_key)

                    index_entry = f"{search_key}, {current_offset}\n"
                    current_offset += len(line) + 1
                    mas.append(index_entry)
                mas.sort(key=lambda x: int(x.split(',')[0]))
                for i in mas: i_file.write(i)

                i_file.flush()

    def binary_search(self, search_key):
        with open(self.index_file, 'r') as i_file:
            i_file.seek(0)
            mas=i_file.readlines()
            left = 0
            right = len(mas)-1

        while left <= right:
            mid = (right + left)// 2

            current_line = mas[mid]
            key, offset = current_line.split(',')

            key = int(key)
            offset = int(offset)

            print(f"current pointer at", offset)
            print(f"our key is", key)

            if key == search_key:
                return offset

            elif key > search_key:
                right = mid-1

            else:
                left = mid+1
        return None

    def search(self, search_key):
        offset = self.binary_search(search_key)

        with open(self.data_file, 'r') as d_file:
            if offset is not None:
                d_file.seek(offset)
                return d_file.readline()
            else:
                return None

    def insert(self, record):
        search_key, data = record.strip().split(',')
        search_key = int(search_key)
        offset = self.binary_search(search_key)

        if offset is None:
            with open(self.data_file, 'r') as d_file:
                d_file.seek(0, 2)
                offset = d_file.tell()

            with open(self.data_file, 'a') as d_file_w:
                with open(self.index_file, 'a') as i_file_w:
                    d_file_w.write(record+'\n')
                    i_file_w.seek(0, 2)

                    index_entry = f"{search_key},{offset}\n"
                    i_file_w.write(index_entry)
                    i_file_w.flush()
            return 1
        else:
            print(f"Record with key {search_key} is exist.")
            return 0

    def delete(self, search_key):
        offset = self.binary_search(search_key)
        if offset is not None:
            with open(self.data_file, 'r+') as d_file:
                d_file.seek(offset)
                del_line = d_file.readline()
            with fileinput.FileInput(self.data_file, inplace=True, backup='.bak') as d_file:
                for line in d_file:
                    if line != del_line:
                        print(line, end='')
            os.unlink(self.data_file + '.bak')
            return 1
        else:
            print(f"Record with key {search_key} not found.")
            return 0


    def update(self, search_key, new_data):
        offset = self.binary_search(search_key)
        if offset is not None:
            with open(self.data_file, 'r+') as d_file:
                d_file.seek(offset)
                old_line = d_file.readline()
                key, data = old_line.strip().split(',')
                new_line = f"{key}, {new_data}\n"
            with fileinput.FileInput(self.data_file, inplace=True, backup='.bak') as d_file:
                for line in d_file:
                    if line == old_line:
                        print(new_line, end='')
                    else:
                        print(line, end='')
            os.unlink(self.data_file + '.bak')
            return 1
        else:
            print(f"Record with key {search_key} not found.")
            return 0


if __name__ == '__main__':
    data_file = "data.txt"
    index_file = "index.txt"

    di = DenseIndex(data_file, index_file)
    di.build_index()

    result = di.search(10)
    print(result)