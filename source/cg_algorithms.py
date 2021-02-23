#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0, x1, y1 = round(p_list[0][0]), round(p_list[0][1]), round(p_list[1][0]), round(p_list[1][1])
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, round(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        dx = x1 - x0
        dy = y1 - y0
        xk, yk = x0, y0
        if dx == 0:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        elif dy == 0:
            for x in range(x0, x1 + 1):
                result.append((x, y0))
        elif abs(dy) <= abs(dx):
            m = dy / dx
            for x in range(abs(dx)+1):
                result.append((xk, round(yk)))
                xk += 1
                yk += m
        else:
            s = 1 if y0 < y1 else -1
            m = dx / dy
            for y in range(abs(dy)+1):
                result.append((round(xk), yk))
                xk += s * m
                yk += s
    elif algorithm == 'Bresenham':
        s = 1 if y0 < y1 else -1
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        xk, yk = x0, y0
        if dy < dx:
            p = 2*dy - dx
            for x in range(dx + 1):
                result.append((xk, yk))
                if p >= 0:
                    yk += s
                    p -= 2*dx
                xk += 1
                p += 2*dy
        else:
            p = 2*dx - dy
            for y in range(dy + 1):
                result.append((xk, yk))
                if p >= 0:
                    xk += 1
                    p -= 2*dy
                yk += s
                p += 2*dx

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    rx = abs(p_list[1][0] - p_list[0][0]) / 2
    ry = abs(p_list[1][1] - p_list[0][1]) / 2
    xc = round((p_list[1][0] + p_list[0][0]) / 2)
    yc = round((p_list[1][1] + p_list[0][1]) / 2)
    pk = ry ** 2 - rx ** 2 * (ry + 1 / 4)
    result = []
    if rx == 0 or ry == 0:
        return draw_line(p_list, 'DDA')
    xk, yk = 0, round(ry)
    while xk * ry ** 2 < yk * rx ** 2:
        result.append((xk + xc, yk + yc))
        result.append((xk + xc, -yk + yc))
        result.append((-xk + xc, yk + yc))
        result.append((-xk + xc, -yk + yc))
        if pk >= 0:
            pk += 2 * rx ** 2 - 2 * rx ** 2 * yk
            yk -= 1
        xk += 1
        pk += 2 * ry ** 2 * xk + 3 * ry ** 2
    pk = ry ** 2 * (xk + 1/2) ** 2 + rx ** 2 * (yk - 1) ** 2 - rx ** 2 * ry ** 2
    while yk >= 0:
        result.append((xk + xc, yk + yc))
        result.append((xk + xc, -yk + yc))
        result.append((-xk + xc, yk + yc))
        result.append((-xk + xc, -yk + yc))
        if pk <= 0:
            pk += 2 * ry ** 2 + 2 * ry ** 2 * xk
            xk += 1
        yk -= 1
        pk += 3 * rx ** 2 - 2 * rx ** 2 * yk
    return result


def get_lambda(i, r, t, u):
    if abs(u[i + 4 - r] - u[i]) < 1e-7:
        return 0
    else:
        return (t - u[i]) / (u[i + 4 - r] - u[i])


def deBoor_Cox(i, r, t, p_list, u, w):
    if r == 0:
        return p_list[i][0] if w == 'x' else p_list[i][1]
    else:
        l = get_lambda(i, r, t, u)
        return l * deBoor_Cox(i, r - 1, t, p_list, u, w) + (1 - l) * deBoor_Cox(i - 1, r - 1, t, p_list, u, w)


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':
        n = len(p_list)
        tmpX = [0 for _ in range(n)]
        tmpY = [0 for _ in range(n)]
        result.append((round(p_list[0][0]), round(p_list[0][1])))
        for tt in range(0, 1000 * n + 1):
            t = tt / 1000 / n
            for j in range(0, n - 1):
                tmpX[j] = p_list[j][0] * (1 - t) + p_list[j + 1][0] * t
                tmpY[j] = p_list[j][1] * (1 - t) + p_list[j + 1][1] * t
            for i in range(2, n):
                for j in range(0, n - i):
                    tmpX[j] = tmpX[j] * (1 - t) + tmpX[j + 1] * t
                    tmpY[j] = tmpY[j] * (1 - t) + tmpY[j + 1] * t
            x, y = tmpX[0], tmpY[0]
            result.append((round(x), round(y)))
    elif algorithm == 'B-spline':
        k = 4
        n = len(p_list) - 1
        u = [i for i in range(n + k + 2)]
        step = 0.001
        for i in range(k - 1, n + 1):
            t = u[i]
            while t <= u[i + 1]:
                x = deBoor_Cox(i, k - 1, t, p_list, u, 'x')
                y = deBoor_Cox(i, k - 1, t, p_list, u, 'y')
                result.append((round(x), round(y)))
                t = t + step

    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int()) 水平方向平移量
    :param dy: (int()) 垂直方向平移量
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    return [[t[0] + dx, t[1] + dy] for t in p_list]


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int()) 旋转中心x坐标
    :param y: (int()) 旋转中心y坐标
    :param r: (int()) 顺时针旋转角度（°）
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    theta = r * math.pi / 180
    for i in range(len(p_list)):
        x1 = (p_list[i][0] - x) * math.cos(theta) - (p_list[i][1] - y) * math.sin(theta) + x
        y1 = (p_list[i][0] - x) * math.sin(theta) + (p_list[i][1] - y) * math.cos(theta) + y
        p_list[i] = [x1, y1]
    return p_list


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int()) 缩放中心x坐标
    :param y: (int()) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in range(len(p_list)):
        x1 = (p_list[i][0] - x) * s + x
        y1 = (p_list[i][1] - y) * s + y
        p_list[i] = [x1, y1]
    return p_list


def compute_outcode(x_min, y_min, x_max, y_max, x, y):
    code = 0
    if x < x_min:
        code |= 1
    elif x > x_max:
        code |= 2
    if y < y_min:
        code |= 4
    elif y > y_max:
        code |= 8
    return code


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int(): [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int(): [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if algorithm == 'Cohen-Sutherland':
        outcode0 = compute_outcode(x_min, y_min, x_max, y_max, x0, y0)
        outcode1 = compute_outcode(x_min, y_min, x_max, y_max, x1, y1)
        while True:
            if not outcode0 | outcode1:
                return [[x0, y0], [x1, y1]]
            elif outcode0 & outcode1:
                return [[0, 0], [0, 0]]
            else:
                outcodeOut = outcode0 if outcode0 else outcode1
                x, y = x0, y0
                if outcodeOut & 8:
                    x = round(x0 + (x1 - x0) * (y_max - y0) / (y1 - y0))
                    y = y_max
                elif outcodeOut & 4:
                    x = round(x0 + (x1 - x0) * (y_min - y0) / (y1 - y0))
                    y = y_min
                elif outcodeOut & 2:
                    y = round(y0 + (y1 - y0) * (x_max - x0) / (x1 - x0))
                    x = x_max
                elif outcodeOut & 1:
                    y = round(y0 + (y1 - y0) * (x_min - x0) / (x1 - x0))
                    x = x_min
                if outcodeOut == outcode0:
                    x0 = x
                    y0 = y
                    outcode0 = compute_outcode(x_min, y_min, x_max, y_max, x0, y0)
                else:
                    x1 = x
                    y1 = y
                    outcode1 = compute_outcode(x_min, y_min, x_max, y_max, x1, y1)

    elif algorithm == 'Liang-Barsky':
        flag = False
        u1, u2 = 0.0, 1.0
        p, q = [], []
        p.append(x0 - x1)
        p.append(x1 - x0)
        p.append(y0 - y1)
        p.append(y1 - y0)

        q.append(x0 - x_min)
        q.append(x_max - x0)
        q.append(y0 - y_min)
        q.append(y_max - y0)

        for i in range(4):
            if p[i] < 0:
                r = q[i]/p[i]
                u1 = max(u1, r)
                if u1 > u2:
                    flag = True
            elif p[i] > 0:
                r = q[i]/p[i]
                u2 = min(u2, r)
                if u1 > u2:
                    flag = True
            elif p[i] == 0 and q[i] < 0:
                flag = True

        if flag:
            return [[0, 0], [0, 0]]
        new_x0 = round(x0 + u1 * (x1 - x0))
        new_y0 = round(y0 + u1 * (y1 - y0))
        new_x1 = round(x0 + u2 * (x1 - x0))
        new_y1 = round(y0 + u2 * (y1 - y0))
        return [[new_x0, new_y0], [new_x1, new_y1]]



