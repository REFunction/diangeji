class IndexQueue:
    # data: [[index1, data1],[index2,data2],……]
    # index 下标从1开始
    # 新插入的index会被临时设为len+1
    data = []
    def put(self, item):
        self.data.append([len(self.data)+1,item])
        self.update()

    def get(self):
        # 判断是否为空
        if len(self.data)!=0:
            return_item = self.data[0][1]
            self.data.pop(0)
            self.update()
            return return_item
        else:
            return False

    def exchange_by_index(self, index1, index2):
        if index1<=len(self.data) and index2<=len(self.data):
            self.data[index1][0] = index2
            self.data[index2][0] = index1
            self.update()
        else:
            print('超出队列长度')

    def update(self):
        # 根据index排序
        self.data.sort(key=lambda x:x[0])
        temp = [[index + 1, item[1]]for index, item in enumerate(self.data)]
        self.data = temp

    def isEmpty(self):
        if len(self.data)==0:
            return True
        else:
            return False

if __name__ == '__main__':
    queue = IndexQueue()
    queue.put('a')
    queue.put('b')
    for i in range(5):
        queue.put(i)
    print(queue.data)
    print(queue.get())
    print(queue.data)
    queue.exchange_by_index(2,4)
    print(queue.data)
