class DataReader:
    """Class to read data"""

    def __init__(self,attr_file,train_file,test_file,real=False):
        self.attr_file = attr_file
        self.train_file = train_file
        self.test_file = test_file
        self.attributes = []
        self.train_data = []
        self.test_data = []
        self.bitstring_train_data = []
        self.bitstring_test_data = []
        self.bitstring_length = 0

    def read_attr_file(self):
        with open("data/" + self.attr_file) as f:
            for line in f:
                if not line.isspace():
                    attr = line.strip().split(' ')[0]
                    values = line.strip().split(' ')[1:]
                    self.attributes.append({'attr':attr,'values':values})
                    self.bitstring_length += len(values)

    def read_train_file(self):
        with open("data/" + self.train_file) as f:
            for line in f:
                if not line.isspace():
                    self.train_data.append(line.strip().split(' '))
        for data in self.train_data:
            self.bitstring_train_data.append(self.data_to_bitstring(data))

    def read_test_file(self):
        with open("data/" + self.test_file) as f:
            for line in f:
                if not line.isspace():
                    self.test_data.append(line.strip().split(' '))
        for data in self.test_data:
            self.bitstring_test_data.append(self.data_to_bitstring(data))

    def data_to_bitstring(self,data):
        bitstring=''
        for i in range(len(data)):
            for value in self.attributes[i]['values']:
                if data[i] == value:
                    bitstring +='1'
                else:
                    bitstring +='0'
        return bitstring


if __name__ == '__main__':
    t = DataReader('tennis-attr.txt','tennis-train.txt','tennis-test.txt')
    t.read_attr_file()
    t.read_train_file()
    t.read_test_file()
    print(t.train_data)
    print(t.bitstring_train_data)
    print(t.test_data)
    print(t.bitstring_test_data)
    print(t.bitstring_length)