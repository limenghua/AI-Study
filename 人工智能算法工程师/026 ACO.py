import random
import copy
import sys
import tkinter
import threading
import time
from functools import reduce

(ALPHA, BETA, RHO, Q) = (1, 2, 0.5, 100)
(city_num, ant_num) = (50, 50)
distance_x = []
distance_y = []
for i in range(city_num):
    distance_x.append(random.randint(100, 500))
    distance_y.append(random.randint(100, 500))

distance_graph = [[0 for col in range(city_num)] for row in range(city_num)]
print(distance_graph)
pheromone_graph = [[1 for col in range(city_num)] for row in range(city_num)]
print(pheromone_graph)

class Ant():
    def __init__(self, ID):
        self.ID = ID
        self.__clean_data()

    def __clean_data(self):
        self.path = []
        self.total_distance = 0
        self.move_count = 0
        self.current_city = -1
        self.open_table_city = [True for i in range(city_num)]
        city_index = random.randint(0, city_num-1)
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    def __choice_next_city(self):
        next_city = -1
        select_citys_prob = [0 for i in range(city_num)] # 选择城市的概率
        total_prob = 0
        # 计算选择城市的概率
        for i in range(city_num):
            if self.open_table_city[i]:
                select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * \
                                       pow(1/distance_graph[self.current_city][i], BETA)
                total_prob += select_citys_prob[i]

        # 轮盘赌选择城市
        if total_prob > 0:
            temp_prob = random.uniform(0, total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    temp_prob -= select_citys_prob[i]
                    if temp_prob <= 0:
                        next_city = i
                        break

        # 顺序选择城市
        if next_city == -1:
            for i in range(city_num):
                if self.open_table_city[i]:
                    next_city = i
                    break

        if next_city == -1:
            next_city = random.randint(0, city_num-1)
            while False == self.open_table_city[next_city]:
                next_city = random.randint(0, city_num-1)

        # 返回城市序号
        return next_city
    
    def __cal_total_distance(self):
        temp_distance = 0
        for i in range(1,city_num):
            start,end = self.path[i],self.path[i-1]
            temp_distance += distance_graph[start][end]
        end = self.path[0]
        temp_distance += distance_graph[end][start]
        self.total_distance = temp_distance
        
    def __move(self,next_city):
        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    def search_path(self):
        self.__clean_data()
        while self.move_count < city_num:
            next_city = self.__choice_next_city()
            self.__move(next_city)
        self.__cal_total_distance()

class TSP():
    def __init__(self, root, width, height, n=city_num):
        self.root = root
        self.width = width
        self.height = height
        self.n = n
        self.canvas = tkinter.Canvas(root, width=500, height=500,bg="#EBEBEB",xscrollincrement=1,yscrollincrement=1)
        self.canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.title("TSP 蚁群算法(n:初始化 e:开始搜索 s:停止搜索 q:退出程序)")
        self.__r = 5
        self.__lock = threading.RLock()
        self.__bindEvents()
        self.new()

    for i in range(city_num):
        for j in range(city_num):
            temp_distance = pow(distance_x[i] - distance_x[j], 2) + pow(distance_y[i] - distance_y[j], 2)
            temp_distance = pow(temp_distance, 0.5)
            distance_graph[i][j] = temp_distance + 1e-6

    def __bindEvents(self):
        self.root.bind("q",self.quite)
        self.root.bind("n",self.new)
        self.root.bind("e",self.search_path)
        self.root.bind("s",self.stop)

    def title(self, text):
        self.root.title(text)

    def new(self, evt=None):
        # 停止线程
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        
        self.clear()
        self.nodes = []
        self.nodes2 = []

        for i in range(len(distance_x)):
            x = distance_x[i]
            y = distance_y[i]
            self.nodes.append((x,y))
            node = self.canvas.create_oval(x-self.__r, 
                                           y-self.__r, x+self.__r, y+self.__r, 
                                           fill="#ff0000",
                                           outline="#000000", 
                                           tags="node")
            self.nodes2.append(node)
            #self.canvas.create_text(x, y-10, text="(" + str(x) + "," + str(y) + ")", fill= 'black')

        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = 1.0
        
        self.ants = [Ant(ID) for ID in range(ant_num)]
        self.best_ant = Ant(-1)
        self.best_ant.total_distance = 1 << 31
        self.iter = 1

    def line(self,order):
        self.canvas.delete("line")

        def line2(i1,i2):
            p1,p2 = self.nodes[i1],self.nodes[i2]
            self.canvas.create_line(p1,p2,fill="#000000",tags="line")
            return i2
        reduce(line2,order,order[-1])

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    def quite(self, evt=None):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.root.destroy()
        print("退出程序")
        sys.exit()

    def stop(self, evt=None):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        print("停止搜索")

    def search_path(self, evt=None):
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        last_best_distance = 1 << 31
        while self.__running:
            # 遍历每一只蚂蚁f
            for ant in self.ants:
                # 选择路径
                ant.search_path()
                if ant.total_distance < self.best_ant.total_distance:
                    self.best_ant = copy.deepcopy(ant) 
            # 更新信息素
            self.__update_pheromone_graph()
            print("迭代次数:", self.iter, "最短路径长度:", self.best_ant.total_distance)
            self.line(self.best_ant.path)
            self.title("TSP 蚁群算法(n:初始化 e:开始搜索 s:停止搜索 q:退出程序) 最短路径长度:" + str(self.best_ant.total_distance) + " 迭代次数:" + str(self.iter))
            self.canvas.update()
            self.iter += 1
            if abs(self.best_ant.total_distance - last_best_distance) > 1:
                last_best_distance = self.best_ant.total_distance
                time.sleep(1)
    
    # 更新信息素
    def __update_pheromone_graph(self):
        temp_phreomone = [[0.0 for j in range(city_num)] for i in range(city_num)]
        for ant in self.ants:
            for i in range(1,city_num):
                start,end = ant.path[i-1],ant.path[i]
                temp_phreomone[start][end] += Q/ant.total_distance
                temp_phreomone[end][start] += Q/ant.total_distance

        # 更新所有城市之间的信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_phreomone[i][j]

    def mainloop(self):
        self.root.mainloop()

    
if __name__ == '__main__':
    tsp = TSP(tkinter.Tk(), 500, 500)
    tsp.mainloop()
                    