#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg
import numpy as np
from PIL import Image


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    item_dict = {}
    pen_color = np.zeros(3, np.uint8)
    width = 0
    height = 0

    with open(input_file, 'r') as fp:
        line = fp.readline()
        while line:
            line = line.strip().split(' ')
            if line[0] == 'resetCanvas':
                width = int(line[1])
                height = int(line[2])
                item_dict = {}
            elif line[0] == 'saveCanvas':
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)
                canvas.fill(255)
                for item_type, p_list, algorithm, color in item_dict.values():
                    pixels = []
                    if item_type == 'line':
                        pixels = alg.draw_line(p_list, algorithm)
                    elif item_type == 'polygon':
                        pixels = alg.draw_polygon(p_list, algorithm)
                    elif item_type == 'ellipse':
                        pixels = alg.draw_ellipse(p_list)
                    elif item_type == 'curve':
                        pixels = alg.draw_curve(p_list, algorithm)
                    for x, y in pixels:
                        canvas[y, x] = color
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                pen_color[0] = int(line[1])
                pen_color[1] = int(line[2])
                pen_color[2] = int(line[3])
            elif line[0] in ['drawLine', 'drawEllipse', 'clip']:
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                if line[0] == 'drawLine':
                    algorithm = line[6]
                    item_dict[item_id] = ['line', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
                elif line[0] == 'drawEllipse':
                    algorithm = ''
                    item_dict[item_id] = ['ellipse', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
                else:
                    algorithm = line[6]
                    p_list = alg.clip(item_dict[item_id][1], x0, y0, x1, y1, algorithm)
                    if p_list[0][0] == p_list[1][0] and p_list[0][1] == p_list[1][1]:
                        del item_dict[item_id]
                    else:
                        item_dict[item_id][1] = p_list
            elif line[0] in ['drawPolygon', 'drawCurve']:
                item_id = line[1]
                dot = []
                for d in [line[i:i+2] for i in range(2, len(line)-1, 2)]:
                    dot.append(list(map(int, d)))
                algorithm = line[-1]
                temp = 'polygon' if line[0] == 'drawPolygon' else 'curve'
                item_dict[item_id] = [temp, dot, algorithm, np.array(pen_color)]
            elif line[0] == 'translate':
                item_id = line[1]
                dx = int(line[2])
                dy = int(line[3])
                item_dict[item_id][1] = alg.translate(item_dict[item_id][1], dx, dy)
            elif line[0] in ['rotate', 'scale']:
                item_id = line[1]
                x = int(line[2])
                y = int(line[3])
                if line[0] == 'rotate':
                    if item_dict[item_id][0] != 'ellipse':
                        r = int(line[4])
                        item_dict[item_id][1] = alg.rotate(item_dict[item_id][1], x, y, r)
                else:
                    s = float(line[4])
                    item_dict[item_id][1] = alg.scale(item_dict[item_id][1], x, y, s)

            line = fp.readline()
