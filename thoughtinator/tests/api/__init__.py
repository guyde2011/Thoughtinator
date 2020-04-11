

USER = {
    'user_id': 1,
    'username': 'Dr Heinz Doofenshmirtz',
    'birthday': 1000,
    'gender': 0
}

POSE = {
    'rotation': {
        'x': 0.31, 'y': 0.315, 'z': 0.32, 'w': 0.325
    },
    'position': {
        'x': 0.21, 'y': 0.215, 'z': 0.22
    }
}

FEELINGS = {
    'hunger': 0.1, 'thirst': 0.15, 'exhaustion': 0.2, 'happiness': 0.25
}

COLOR_IMAGE = {
    'path': 'col_img'
}

DEPTH_IMAGE = {
    'path': 'dpt_img'
}

SNAPSHOT = {
    'user_id': 1,
    'snap_id': 2,
    'feelings': FEELINGS,
    'pose': POSE,
    'color_image': COLOR_IMAGE,
    'depth_image': DEPTH_IMAGE,
    'datetime': '1234'
}
