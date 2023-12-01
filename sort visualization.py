from tkinter import *
from collections import UserList
import time
import random

class Block:

    def __init__(self, height: int, canvas: Canvas, index: int):
        self.height = height
        self.canvas = canvas
        self.index = index
        self.block = None

    def draw(self, x1, y, x2, color):
        if self.block:
            self.canvas.delete(self.block)

        self.block = self.canvas.create_rectangle(x1, y, x2, 330, fill=color)

class BlockList(UserList):

    def __init__(self, data, canvas):
        super().__init__(data)
        self.canvas = canvas
        self.blocks = []
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        self.blocks = []
        for i, height in enumerate(self):
            block = Block(height, self.canvas, i)
            self.blocks.append(block)
            x1, y, x2 = self.get_coordinates(block)
            block.draw(x1, y, x2, 'blue')

    def swap(self, i, j):
        self[i], self[j] = self[j], self[i]
        self.blocks[i], self.blocks[j] = self.blocks[j], self.blocks[i]
        self.draw()

    def add(self, x):
        self.append(x)
        self.draw()

    def get_coordinates(self, block: Block):
        x1 = 1080 / len(self) * block.index
        x2 = 1080 / len(self) * (block.index + 1)
        y = 330 - block.height
        return x1, y, x2

class HomePage():

    def __init__(self, home):
        self.home = home
        
        bubbleButton = Button(home, text='버블 정렬(Bubble sort)', command=lambda: SortPage('bubble'))
        bubbleButton.place(x=220, y=120, width=150, height=30)
        
        selectionButton = Button(home, text='선택 정렬(Selection sort)', command=lambda: SortPage('selection'))
        selectionButton.place(x=710, y=120, width=150, height=30)
        
        insertionButton = Button(home, text='삽입 정렬(Insertion sort)', command=lambda: SortPage('insertion'))
        insertionButton.place(x=220, y=255, width=150, height=30)
        
        quickButton = Button(home, text='퀵 정렬(Quick sort)', command=lambda: SortPage('quick'))
        quickButton.place(x=710, y=255, width=150, height=30)
        
        mergeButton = Button(home, text='병합 정렬(Merge sort)')
        mergeButton.place(x=220, y=395, width=150, height=30)
        
        radixButton = Button(home, text='기수 정렬(Radix sort)')
        radixButton.place(x=710, y=395, width=150, height=30)

class SortPage():

    def __init__(self, sort):
        sortpage = Tk()

        sortpage.title(sort + '_sort')
        sortpage.geometry('1080x540+200+200')
        sortpage.resizable(False, False)

        self.canvas = Canvas(sortpage, width=1080, height=380)
        self.canvas.pack()
        self.canvas.create_line(0, 330, 1080, 330)

        numberScale = Scale(sortpage, from_=1, to=300, orient=HORIZONTAL, label='숫자 개수', length=180, command=self.reset_array)
        speedScale = Scale(sortpage, from_=1, to=1000, orient=HORIZONTAL, label='속도 조절(ms)', length=180, command=self.set_speed)
        sortButton = Button(sortpage, text='sort', command=lambda: getattr(self, sort + '_sort')())
        homeButton = Button(sortpage, text='exit', command=lambda: sortpage.destroy())
        resetButton = Button(sortpage, text='reset', command=lambda: self.reset_array(50))
        
        numberScale.place(x=70, y=420)
        numberScale.set(50)
        speedScale.place(x=320, y=420)
        speedScale.set(50)
        sortButton.place(x=580, y=420, width=180, height=30)
        homeButton.place(x=830, y=420, width=180, height=30)
        resetButton.place(x=580, y=470, width=180, height=30)

        self.delay = 0.001

    def reset_array(self, number):
        self.arr = BlockList(random.sample(range(11, 311, 300 // int(number)), int(number)), self.canvas)
        self.canvas.delete(self.time)

    def set_speed(self, speed):
        self.delay = 0.001 * int(speed)

    def bubble_sort(self):
        start_time = time.time()
        n = len(self.arr)
        for i in range(n - 1):
            for j in range(n - i - 1):
                self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'red')
                self.arr.blocks[j + 1].draw(*self.arr.get_coordinates(self.arr.blocks[j + 1]), 'red')
                self.canvas.update()
                time.sleep(self.delay)

                if self.arr.data[j] > self.arr.data[j + 1]:
                    self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'yellow')
                    self.arr.blocks[j + 1].draw(*self.arr.get_coordinates(self.arr.blocks[j + 1]), 'yellow')
                    self.canvas.update()
                    time.sleep(self.delay)
                    self.arr.swap(j, j + 1)
                    self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'yellow')
                    self.arr.blocks[j + 1].draw(*self.arr.get_coordinates(self.arr.blocks[j + 1]), 'yellow')
                    self.canvas.update()
                    time.sleep(self.delay)
                    
                self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'blue')
                self.arr.blocks[j + 1].draw(*self.arr.get_coordinates(self.arr.blocks[j + 1]), 'blue')
        total_time = time.time() - start_time
        self.time = self.canvas.create_text(1030, 350, text='time: ' + str(total_time))
        
        for i in range(n):
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'yellow')
            self.canvas.update()
            time.sleep(0.03)
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'blue')
            self.canvas.update()

    def selection_sort(self):
        start_time = time.time()
        n = len(self.arr)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'red')
                self.arr.blocks[min_idx].draw(*self.arr.get_coordinates(self.arr.blocks[min_idx]), 'yellow')
                self.arr.canvas.update()
                time.sleep(self.delay)

                if self.arr.data[j] < self.arr.data[min_idx]:
                    self.arr.blocks[min_idx].draw(*self.arr.get_coordinates(self.arr.blocks[min_idx]), 'blue')
                    if min_idx == i:
                        self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'yellow')
                    min_idx = j

                self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'blue')
                self.arr.blocks[min_idx].draw(*self.arr.get_coordinates(self.arr.blocks[min_idx]), 'blue')

            self.arr.swap(i, min_idx)
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'yellow')
            self.arr.blocks[min_idx].draw(*self.arr.get_coordinates(self.arr.blocks[min_idx]), 'yellow')
            self.arr.canvas.update()
            time.sleep(self.delay)

            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'blue')
            self.arr.blocks[min_idx].draw(*self.arr.get_coordinates(self.arr.blocks[min_idx]), 'blue')
        
        total_time = time.time() - start_time
        self.time = self.canvas.create_text(1030, 350, text='time: ' + str(total_time))

        for i in range(n):
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'yellow')
            self.canvas.update()
            time.sleep(0.03)
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'blue')
            self.canvas.update()
    
    def insertion_sort(self):
        start_time = time.time()
        n = len(self.arr)
        for i in range(1, n):
            key = self.arr.data[i]
            j = i - 1
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'red')
            self.arr.canvas.update()
            time.sleep(self.delay)

            while j >= 0 and self.arr.data[j] > key:
                self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'red')
                self.arr.canvas.update()
                time.sleep(self.delay)

                self.arr.swap(j, j + 1)
                j -= 1

                self.arr.blocks[j + 1].draw(*self.arr.get_coordinates(self.arr.blocks[j + 1]), 'blue')
                self.arr.blocks[j].draw(*self.arr.get_coordinates(self.arr.blocks[j]), 'blue')
                self.arr.canvas.update()
                time.sleep(self.delay)

            self.arr.data[j + 1] = key

            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'blue')
            self.arr.blocks[j + 1].draw(*self.arr.get_coordinates(self.arr.blocks[j + 1]), 'blue')
            self.arr.canvas.update()
            time.sleep(self.delay)

        total_time = time.time() - start_time
        self.time = self.canvas.create_text(1030, 350, text='time: ' + str(total_time))

        for i in range(n):
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'yellow')
            self.canvas.update()
            time.sleep(0.03)
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'blue')
            self.canvas.update()

    def quick_sort(self):
        n = len(self.arr)
        start_time = time.time()
        self.quick_sort_recursion(0, n - 1)
        total_time = time.time() - start_time
        self.time = self.canvas.create_text(1030, 350, text='time: ' + str(total_time))
    
        for i in range(len(self.arr)):
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'yellow')
            self.canvas.update()
            time.sleep(0.03)
            self.arr.blocks[i].draw(*self.arr.get_coordinates(self.arr.blocks[i]), 'blue')
            self.canvas.update()
    
    def quick_sort_recursion(self, start, end):
        if start >= end:
            return

        pivot = start
        left, right = start + 1, end

        while left <= right:
            while left <= right and self.arr.data[left] <= self.arr.data[pivot]:
                self.arr.blocks[left].draw(*self.arr.get_coordinates(self.arr.blocks[left]), 'blue')
                left += 1
                self.arr.blocks[left].draw(*self.arr.get_coordinates(self.arr.blocks[left]), 'red')
                self.arr.canvas.update()
                time.sleep(self.delay)

            while left <= right and self.arr.data[right] >= self.arr.data[pivot]:
                self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'blue')
                right -= 1
                self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'red')
                self.arr.canvas.update()
                time.sleep(self.delay)

            if left < right:
                self.arr.blocks[left].draw(*self.arr.get_coordinates(self.arr.blocks[left]), 'yellow')
                self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'yellow')
                self.arr.canvas.update()
                time.sleep(self.delay)
                self.arr.swap(left, right)
                self.arr.blocks[left].draw(*self.arr.get_coordinates(self.arr.blocks[left]), 'yellow')
                self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'yellow')
                self.arr.canvas.update()
                time.sleep(self.delay)

                self.arr.blocks[left].draw(*self.arr.get_coordinates(self.arr.blocks[left]), 'blue')
                self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'blue')


        self.arr.blocks[pivot].draw(*self.arr.get_coordinates(self.arr.blocks[pivot]), 'yellow')
        self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'yellow')
        self.arr.canvas.update()
        time.sleep(self.delay)
        self.arr.swap(pivot, right)
        self.arr.blocks[pivot].draw(*self.arr.get_coordinates(self.arr.blocks[pivot]), 'yellow')
        self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'yellow')
        self.arr.canvas.update()
        time.sleep(self.delay)

        self.arr.blocks[pivot].draw(*self.arr.get_coordinates(self.arr.blocks[pivot]), 'blue')
        self.arr.blocks[right].draw(*self.arr.get_coordinates(self.arr.blocks[right]), 'blue')

        self.quick_sort_recursion(start, right - 1)
        self.quick_sort_recursion(right + 1, end)

    def merge_sort(self):
        pass

    def radix_sort(self):
        pass

home = Tk()
home.title('sort visualization')
home.geometry('1080x540+100+100')
home.resizable(False, False)

HomePage(home)

home.mainloop()