import pickle
import sys
import vgdl
import time


def main():
    args = sys.argv[1:]
    assert (args[0])
    path = args[0]

    pickle_in = open(path, 'rb')
    data = pickle.load(pickle_in)

    observations = data['observations']
    rewards = data['rewards']
    actions = data['actions']

    # for i in range(len(data['observations'])):
    #     if actions[i] != vgdl.ACTION.NOOP:
    #         o = observations[i]
    #         print(o)
    #         x_coord = o['position'][0]
    #         y_coord = o['position'][1]
    #         speed = o['speed']
    #         # Index of distances based on SpriteSet order

    # print([observations[0]])
    print(observations[0]['otherAgents'])
    # translate_to_ilasp([observations[0]])
    # translate_to_ilasp(observations)
    print(len(observations))


def translate_to_ilasp(observations):
    # Using string concatting here, can make more efficient later
    # Currently the example name is hardcoded, but can pass it in as parameter
    ilasp = '#pos(example1, {}, {}, {\n'
    ilasp += ('time(1..' + str(len(observations)) + ').\n')
    ilasp += get_sprites_in_context(observations[0]['sprites'])

    for i in range(len(observations)):
        o = observations[i]
        points = o['otherAgents']
        for p in points:
            ilasp += translate_point_to_ilasp(p, i + 1)
        ilasp += '\n'
    ilasp += '}).'
    print(ilasp)
    filename = "ilasp/" + time.strftime("%Y-%m-%d-%H-%M") + ".las"
    f = open(filename, "w")
    f.write(ilasp)


def get_sprites_in_context(sprites):
    ilasp = ''
    for s in sprites:
        ilasp += get_sprite_id(s) + '(' + s + ').\n'
    return ilasp


def translate_point_to_ilasp(p, time):
    tmp = ''
    point_id = 'p_' + p['name'] + '_' + str(time)
    tmp += 'point(' + point_id + ', "' + str(p['position'][0]) + '", "' + str(p['position'][1]) + '").\n'
    tmp += 'pos(' + p['name'] + ', ' + str(time) + ', ' + point_id + ').\n'
    return tmp


def get_sprite_id(name):
    if name.startswith('wall'):
        return 'block'
    if name.startswith('chased'):
        return 'block'
    if name.startswith('goal'):
        return 'goal'
    return 'agent'


if __name__ == "__main__":
    main()
