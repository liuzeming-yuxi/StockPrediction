import numpy as np
import math

def get_length(p1, p2):
    x, y = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    return (x*x + y*y)**0.5

def get_slope(p1, p2):
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

def get_cos(p1, p2):
    return np.sum(p1*p2)/np.sqrt(np.sum(p1**2))/np.sqrt(np.sum(p2**2))

def parallel(p1, p2, k):
    return get_cos(p1, p2) >= k

def perpindicular(p1, p2, k):
    return get_cos(p1, p2) <= k

def check_w(k1, k2, p):
    if len(p) != 5:
        raise 'The size of point is illegal'
    if p[2][1] > p[0][1] or p[2][1] > p[4][1]:
        return False
    p1p2 = p[3] - p[1]
    q1q2 = p[2] - p[0]
    p1q1 = p[0] - p[1]
    p2q2 = p[2] - p[3]
    p1q2 = p[2] - p[1]
    p2q3 = p[4] - p[3]
    oq2 = p[2] - (p[1] + p[3]) / 2
    if parallel(p1p2, q1q2, k1) == False or parallel(p1q1, p2q2, k1) == False or parallel(p1q2, p2q3, k1) == False\
        or perpindicular(oq2, p1p2, k2) == False:
        return False
    return True

def check_m(k1, k2, p):#p1q1p2q2p3
    if len(p) != 5:
        raise 'The size of point is illegal'
    if p[2][1] > p[0][1] or p[2][1] > p[4][1]:
        return False
    q1q2 = p[3] - p[1]
    p1p3 = p[4] - p[0]
    p1q1 = p[1] - p[0]
    p2q2 = p[3] - p[2]
    p2q1 = p[1] - p[2]
    p3q2 = p[3] - p[4]
    op2 = p[2] - (p[2] + p[4]) / 2
    if parallel(q1q2, p1p3, k1) == False or parallel(p1q1, p2q2, k1) == False or parallel(p2q1, p3q2, k1) == False\
        or perpindicular(op2, q1q2, k2) == False:
        return False
    return True

def checkk(p1,p2, k):
    p3 = p2 * k - p1
    return np.sum(np.abs(p3))


def get_k(p1, p2):
    l, r = 0.0, 0.0
    for i in range(0,4):
        r = max(r, np.max(p1/p2))
    while r - l > 1e-4:
        lmid, rmid = l+(r-l)/3, r-(r-l)/3
        if checkk(p1, p2, lmid)<=checkk(p1, p2, rmid):
            r=rmid
        else:
            l=lmid
    return (lmid + rmid) / 2

class ModeMatch:
    sum_W_L = 0
    sum_W_S = 0
    sum_M_L = 0
    sum_M_S = 0
    sum_W = 0
    sum_M = 0
    W = None
    W_L = None
    W_S = None
    M = None
    M_L = None
    M_S = None

    def __init__(self, k1, k2):
        self.k1 = k1
        self.k2 = k2
        return

    def fit(self, extreme):
        n = len(extreme)
        L = []
        S = []
        for i in range(0, n - 1):
            L.append(get_length(extreme[i], extreme[i+1]))
            S.append(get_slope(extreme[i], extreme[i+1]))

        n = n - 1
        for i in range(0, n - 4):
            p = np.array([extreme[i], extreme[i+1], extreme[i+2], extreme[i+3], extreme[i+4]])
            l = np.array([L[i], L[i+1], L[i+2], L[i+3]])
            s = np.array([S[i], S[i+1], S[i+2], S[i+3]])

            if S[i] < 0:
                if check_w(self.k1, self.k2, p) == False:
                    continue
                print('W')
                kl, ks = 1.0, 1.0
                if self.W is None:
                    self.W = p
                    self.W_L = l
                    self.W_S = s
                else:
                    kl, ks = get_k(self.W_L, l), get_k(self.W_S, s)
                self.sum_W += 1
                self.sum_W_L += kl * L[i + 4]
                self.sum_W_S += ks * S[i + 4]
            else:
                if check_m(self.k1, self.k2, p) == False:
                    continue
                print('M')
                kl, ks = 1.0, 1.0
                if self.M is None:
                    self.M = p
                    self.M_L = l
                    self.M_S = s
                else:
                    kl, ks = get_k(self.M_L, l), get_k(self.M_S, s)
                self.sum_M += 1
                self.sum_M_L += kl * L[i + 4]
                self.sum_M_S += ks * S[i + 4]
        return

    def predict_m(self):
        if (self.sum_M == 0):
            return 0, 0
        return self.sum_M_L / self.sum_M, self.sum_M_S / self.sum_M

    def predict_w(self):
        if(self.sum_W == 0):
            return 0 ,0
        return self.sum_W_L / self.sum_W, self.sum_W_S / self.sum_W