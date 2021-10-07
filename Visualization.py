from vpython import *
 
import json 

# Map keypresses to corresponding face colors and rotation axes.
faces = {'r': (color.red, (1, 0, 0)),
         'l': (color.orange, (-1, 0, 0)),
         'u': (color.white, (0, 1, 0)),
         'd': (color.yellow, (0, -1, 0)),
         'f': (color.green, (0, 0, 1)),
         'b': (color.blue, (0, 0, -1))}
 
stickers = []
for face_color, axis in faces.values():
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            sticker = box(color=face_color, pos=vec(x, y, 1.5),
                          length=0.98, height=0.98, width=0.05)
            cos_angle = dot(vec(0, 0, 1), vec(*axis))
            pivot = (cross(vec(0, 0, 1), vec(*axis))
                     if cos_angle == 0 else vec(1, 0, 0))
            sticker.rotate(angle=acos(cos_angle), axis=pivot, origin=vec(0, 0, 0))
            stickers.append(sticker)
    scene.lights.append(distant_light(direction=vec(*axis),color=color.gray(0.3)))


def expand(movements):
    empty = []
    for move in movements:
        if len(move) > 1:
            if move[1] == '2':
                empty.append(move[0].lower())
                empty.append(move[0].lower())
            else:
                empty.append(move[0])
        else:
            empty.append(move.lower())

    print(empty)
    return empty

fps = 24

f = open ('movements.json', "r")
 
movements = json.loads(f.read())
scramble = expand(movements["scramble"])
solution = expand(movements["solution"])



for move in scramble + solution:
    key = move
    if key.lower() in faces:
        face_color, axis = faces[key.lower()]
        angle = ((pi / 2) if key.islower() else -pi / 2)
        for r in arange(0, angle, angle / fps):
            rate(fps)
            for sticker in stickers:
                if dot(sticker.pos, vec(*axis)) > 0.5:
                    sticker.rotate(angle=angle / fps, axis=vec(*axis), origin=vec(0, 0, 0))



exit()