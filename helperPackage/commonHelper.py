class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQSS(style):
        # print(style)
        # with open(style, 'r') as f:
        #     read = f.read()
        #     return read
        f = open(style)
        lines = f.read()
        print(type(lines))
        f.close()
        return lines
