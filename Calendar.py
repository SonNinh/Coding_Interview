


'''
[9:00 10:30] [12:00 13:00]
[9:00                                   20:00]

[10:00 11:30] [12:30 14:30]
[10:00                                   18:30]

------------------------
[11:30 12:00]

[9:00 10:00 10:30 11:30] [12:00 12:30 13:00 14:30]

9:00    9:30    10:00    10:30    11:00    11:30    12:00    12:30  13:00   13:30    14:00  14:30
<<-------------------------->>                      <<----------------->>
                                  <<++++++++++>>             <<++++++++++++++++++++++++++++++++>>
                                                OOOO
1                           0     1            0    1        2          1                       0

0 -> 1
'''

class MySolution:

    def flatten(self, X, bound_X):
        res = [i for part in X for i in part]
        return bound_X[:1] + res + bound_X[-1:]

    def merge(self, A, B, bound_A, bound_B):
        A_flat = self.flatten(A, bound_A)
        B_flat = self.flatten(B, bound_B)

        time_axis = []
        flag = []
        count_A = 0
        count_B = 0
        num_A = len(A_flat)
        num_B = len(B_flat)
        while count_A < num_A and count_B < num_B:
            if A_flat[count_A] < B_flat[count_B]:
                time_axis.append(A_flat[count_A])
                flag.append(count_A%2==0)
                count_A += 1
            else:
                time_axis.append(B_flat[count_B])
                flag.append(count_B%2==0)
                count_B += 1
        for i in range(count_A, num_A):
            flag.append(i%2==0)
        for i in range(count_B, num_B):
            flag.append(i%2==0)
        
        time_axis += A_flat[count_A:] + B_flat[count_B:]
        return time_axis, flag

    def solve(self, A, B, bound_A, bound_B):
        res = []
        time_axis, flag = self.merge(A, B, bound_A, bound_B)

        cur = 2
        part = []
        pre = 1
        pre_t = None
        for t, f in zip(time_axis, flag):
            cur += -1 if f else 1
            if cur == 1 and pre == 0:
                if pre_t != t:
                    res.append([pre_t, t])
            pre = cur
            pre_t = t

        return res


class ClementSolution:
    def flatten(self, X):
        res = [i for part in X for i in part]
        return res
    
    def argsort(self, seq):
        return sorted(range(len(seq)), key=seq.__getitem__)

    def solve(self, A, B, bound_A, bound_B):

        big_time = A + B + [[0, bound_A[0]], [bound_A[1],24], [0, bound_B[0]], [bound_B[1],24]]
        flag = [True, False] * len(big_time)
        big_time.sort(key=lambda x: x[0])
        big_time = self.flatten(big_time)
        idx = self.argsort(big_time)
        
        res = []
        for pre, cur in zip(idx[:-1], idx[1:]):
            if not flag[pre] and flag[cur]:
                pre_time = big_time[pre]
                cur_time = big_time[cur]
                if pre_time != cur_time:
                    res.append([pre_time, cur_time])
        
        return res


'''
[9:00 10:30] [12:00 13:00]

[10:00 11:30] [12:30 14:30]
'''

if __name__ == "__main__":
    
    A = [[9, 10.5], [12, 13], [16, 18]]
    bound_A = [8, 20]
    B = [[10, 11.5], [12.5, 14.5], [14.5, 15], [16, 17]]
    bound_B = [8.5, 18.5]

    task = ClementSolution()
    print(task.solve(A, B, bound_A, bound_B))
    task = MySolution()
    print(task.solve(A, B, bound_A, bound_B))
    