from autonavsim2d.utils.utils import BLACK
import json

def load_map(grid, file_path):
    '''
    Loads a predefined map from a json file. See below for an example file:
    {
        "obstacles": [
            {
                "type": "rectangle",
                "top_left": [1, 1],
                "bottom_right": [3, 3]
            },
            {
                "type": "circle",
                "center": [5, 5],
                "radius": 2
            },
            {
                "type": "triangle",
                "vertices": [
                    [7, 7],
                    [9, 7],
                    [8, 9]
                ]
            }
        ]
    }
    '''
    if file_path is None:
        return grid
    
    def draw_rectangle(top_left, bottom_right):
        for x in range(top_left[0], bottom_right[0] + 1):
            for y in range(top_left[1], bottom_right[1] + 1):
                grid[x][y][1] = BLACK

    def draw_circle(center, radius):
        cx, cy = center
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    grid[x][y][1] = BLACK

    def draw_triangle(vertices):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        v1, v2, v3 = vertices
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                p = (x, y)
                d1 = sign(p, v1, v2)
                d2 = sign(p, v2, v3)
                d3 = sign(p, v3, v1)
                has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
                has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
                if not (has_neg and has_pos):
                    grid[x][y][1] = BLACK

    with open(file_path, 'r') as file:
        data = json.load(file)

    for obstacle in data['obstacles']:
        if obstacle['type'] == 'rectangle':
            draw_rectangle(obstacle['top_left'], obstacle['bottom_right'])
        elif obstacle['type'] == 'circle':
            draw_circle(obstacle['center'], obstacle['radius'])
        elif obstacle['type'] == 'triangle':
            draw_triangle(obstacle['vertices'])
    
    return grid