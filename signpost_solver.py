import os

FROM_STATS = 'from'
TO_STATS = 'to'
ID_STATS = 'id'
VAL_DIR_DELIMITER = ';'


def read_board(path):
    f = open(path, 'r')
    lines = f.read().splitlines()
    board = [l.split() for l in lines]

    lengthy = set([len(r) for r in board])
    assert len(lengthy) == 1

    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = board[i][j].split(VAL_DIR_DELIMITER)

    stats = dict()
    stats[TO_STATS] = [[None] * len(board) for _ in range(len(board[0]))]
    stats[FROM_STATS] = [[None] * len(board) for _ in range(len(board[0]))]
    stats[ID_STATS] = dict()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j][0] != '':
                stats[ID_STATS][int(board[i][j][0])] = (i, j)

    board, stats = set_signposts_by_numbers(board, stats)

    return board, stats


def set_signposts_by_numbers(board, stats):
    ks = sorted(stats[ID_STATS].keys())
    for i in range(len(ks) - 1):
        if ks[i] + 1 == ks[i + 1]:
            set_signpost(board, stats, stats[ID_STATS][ks[i]][0], stats[ID_STATS][ks[i]][1],
                         stats[ID_STATS][ks[i + 1]][0],
                         stats[ID_STATS][ks[i + 1]][1])
    return board, stats


def get_to_opts(board, stats, i, j):
    if stats[TO_STATS][i][j]:
        return [stats[TO_STATS][i][j]]
    towards = board[i][j][1]
    if towards == 'E':
        return []
    elif towards == 'U':
        return [(x, j) for x in range(i) if stats[FROM_STATS][x][j] is None and (
                board[i][j][0] == '' or board[x][j][0] == '' or int(board[i][j][0]) + 1 == int(board[x][j][0]))]
    elif towards == 'UR':
        return [(i - x, j + x) for x in range(1, min(i + 1, len(board[0]) - j)) if
                stats[FROM_STATS][i - x][j + x] is None and (
                        board[i][j][0] == '' or board[i - x][j + x][0] == '' or int(board[i][j][0]) + 1 == int(
                    board[i - x][j + x][0]))]
    elif towards == 'R':
        return [(i, x) for x in range(len(board) - 1, j, -1) if stats[FROM_STATS][i][x] is None and (
                board[i][j][0] == '' or board[i][x][0] == '' or int(board[i][j][0]) + 1 == int(board[i][x][0]))]
    elif towards == 'DR':
        return [(i + x, j + x) for x in range(1, min(len(board) - i, len(board[0]) - j)) if
                stats[FROM_STATS][i + x][j + x] is None and (
                        board[i][j][0] == '' or board[i + x][j + x][0] == '' or int(board[i][j][0]) + 1 == int(
                    board[i + x][j + x][0]))]
    elif towards == 'D':
        return [(x, j) for x in range(len(board) - 1, i, -1) if stats[FROM_STATS][x][j] is None and (
                board[i][j][0] == '' or board[x][j][0] == '' or int(board[i][j][0]) + 1 == int(board[x][j][0]))]
    elif towards == 'DL':
        return [(i + x, j - x) for x in range(1, min(j + 1, len(board) - i)) if
                stats[FROM_STATS][i + x][j - x] is None and (
                        board[i][j][0] == '' or board[i + x][j - x][0] == '' or int(board[i][j][0]) + 1 == int(
                    board[i + x][j - x][0]))]
    elif towards == 'L':
        return [(i, x) for x in range(j) if stats[FROM_STATS][i][x] is None and (
                board[i][j][0] == '' or board[i][x][0] == '' or int(board[i][j][0]) + 1 == int(board[i][x][0]))]
    elif towards == 'UL':
        return [(i - x, j - x) for x in range(1, min(i, j) + 1) if stats[FROM_STATS][i - x][j - x] is None and (
                board[i][j][0] == '' or board[i - x][j - x][0] == '' or int(board[i][j][0]) + 1 == int(
            board[i - x][j - x][0]))]


def get_from_opts(board, stats, i, j):
    if stats[FROM_STATS][i][j]:
        return [stats[FROM_STATS][i][j]]
    opts = []
    opts.extend([(x, j) for x in range(i) if stats[TO_STATS][x][j] is None and board[x][j][1] == 'D'])
    opts.extend([(i - x, j + x) for x in range(1, min(i + 1, len(board[0]) - j)) if
                 stats[TO_STATS][i - x][j + x] is None and board[i - x][j + x][1] == 'DL'])
    opts.extend([(i, x) for x in range(len(board[0]) - 1, j, -1) if
                 stats[TO_STATS][i][x] is None and board[i][x][1] == 'L'])
    opts.extend([(i + x, j + x) for x in range(1, min(len(board) - i, len(board[0]) - j)) if
                 stats[TO_STATS][i + x][j + x] is None and board[i + x][j + x][1] == 'UL'])
    opts.extend(
        [(x, j) for x in range(len(board) - 1, i, -1) if stats[TO_STATS][x][j] is None and board[x][j][1] == 'U'])
    opts.extend([(i + x, j - x) for x in range(1, min(len(board) - i, j + 1)) if
                 stats[TO_STATS][i + x][j - x] is None and board[i + x][j - x][1] == 'UR'])
    opts.extend([(i, x) for x in range(j) if stats[TO_STATS][i][x] is None and board[i][x][1] == 'R'])
    opts.extend(
        [(i - x, j - x) for x in range(1, min(i, j) + 1) if
         stats[TO_STATS][i - x][j - x] is None and board[i - x][j - x][1] == 'DR'])
    return opts


def set_signpost(board, stats, i, j, toi, toj):
    stats[TO_STATS][i][j] = (toi, toj)
    stats[FROM_STATS][toi][toj] = (i, j)
    if board[i][j][0] != '' and board[toi][toj][0] == '':
        board[toi][toj][0] = str(int(board[i][j][0]) + 1)
        stats[ID_STATS][int(board[i][j][0]) + 1] = (toi, toj)
    if board[i][j][0] == '' and board[toi][toj][0] != '':
        board[i][j][0] = str(int(board[toi][toj][0]) - 1)
        stats[ID_STATS][int(board[toi][toj][0]) - 1] = (i, j)
    return board, stats


def set_counts(board, stats):
    keep_on = True
    while keep_on:
        keep_on = False
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j][0] != '':
                    if stats[TO_STATS][i][j]:
                        toi = stats[TO_STATS][i][j][0]
                        toj = stats[TO_STATS][i][j][1]
                        if board[toi][toj][0] == '':
                            keep_on = True
                            board[toi][toj][0] = str(int(board[i][j][0]) + 1)
                            stats[ID_STATS][int(board[i][j][0]) + 1] = (toi, toj)
                    if stats[FROM_STATS][i][j]:
                        fromi = stats[FROM_STATS][i][j][0]
                        fromj = stats[FROM_STATS][i][j][1]
                        if board[fromi][fromj][0] == '':
                            keep_on = True
                            board[fromi][fromj][0] = str(int(board[i][j][0]) - 1)
                            stats[ID_STATS][int(board[i][j][0]) - 1] = (fromi, fromj)
    return board, stats


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            s = board[i][j][0] + ';' + board[i][j][1]
            if len(s) < 5:
                s += ' ' * (5 - len(s))
            print(s, end=' ')
        print()
    print()


def skip_logic_1(board, stats):
    keep_on = False
    ks = sorted(stats[ID_STATS].keys())
    for t in range(len(ks) - 1):
        if ks[t] + 2 == ks[t + 1]:
            i1 = stats[ID_STATS][ks[t]][0]
            j1 = stats[ID_STATS][ks[t]][1]
            i3 = stats[ID_STATS][ks[t + 1]][0]
            j3 = stats[ID_STATS][ks[t + 1]][1]
            opts = list(set(get_to_opts(board, stats, i1, j1)) & set(get_from_opts(board, stats, i3, j3)))
            if len(opts) == 1:
                keep_on = True
                set_signpost(board, stats, i1, j1, opts[0][0], opts[0][1])
                set_signpost(board, stats, opts[0][0], opts[0][1], i3, j3)
    return keep_on, board, stats


def skip_logic(board, stats):
    # print("IN SKIP LOGIC")
    ks = sorted(stats[ID_STATS].keys())
    for n in range(2, 5):
        for i in range(len(ks) - 1):
            if ks[i] + n == ks[i + 1]:
                i1 = stats[ID_STATS][ks[i]][0]
                j1 = stats[ID_STATS][ks[i]][1]
                iend = stats[ID_STATS][ks[i + 1]][0]
                jend = stats[ID_STATS][ks[i + 1]][1]
                opts = get_to_opts(board, stats, i1, j1)
                hops = list()
                hops.append(opts)
                tracks = [[opt] for opt in opts]
                while len(hops) < n:
                    hops.append([])
                    for hop in hops[-2]:
                        newhops = get_to_opts(board, stats, hop[0], hop[1])
                        hops[-1].extend(newhops)
                        oldtracks = [t for t in tracks if t[-1] == hop and len(t) == len(hops) - 1]
                        newtracks = []
                        for t in oldtracks:
                            for nh in newhops:
                                nt = [h for h in t]
                                nt.append(nh)
                                newtracks.append(nt)
                        tracks.extend(newtracks)
                    tracks = [t for t in tracks if len(t) == len(hops)]
                # print('tracks:')
                # for track in tracks:
                #     print(track)
                track = [t for t in tracks if t[-1] == (iend, jend)]
                if hops[-1].count((iend, jend)) == 1 and len(track) == 1:
                    # print('FOUND')
                    track = track[0]
                    # print(track)
                    for hop in range(len(track) - 1):
                        set_signpost(board, stats, track[hop][0], track[hop][1], track[hop + 1][0], track[hop + 1][1])
                    print_board(board)
                    return True, board, stats
    return False, board, stats


def solve(board, stats):
    keep_on = True
    while keep_on:
        keep_on = False
        board, stats = set_counts(board, stats)
        board, stats = set_signposts_by_numbers(board, stats)
        for i in range(len(board)):
            for j in range(len(board[0])):
                if not stats[TO_STATS][i][j] and board[i][j][0] != str(len(board) * len(board[0])):
                    opts = get_to_opts(board, stats, i, j)
                    # if len(opts) > 0:
                    #     print(i, j, TO_STATS, opts)
                    if len(opts) == 1:
                        keep_on = True
                        board, stats = set_signpost(board, stats, i, j, opts[0][0], opts[0][1])
                        print_board(board)
                if not stats[FROM_STATS][i][j] and board[i][j][0] != '1':
                    opts = get_from_opts(board, stats, i, j)
                    # if len(opts) > 0:
                    #     print(i, j, FROM_STATS, opts)
                    if len(opts) == 1:
                        keep_on = True
                        board, stats = set_signpost(board, stats, opts[0][0], opts[0][1], i, j)
                        print_board(board)
        if not keep_on:
            keep_on, board, stats = skip_logic(board, stats)
    return board, stats


def backtrack(board, stats):
    tos = dict()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if not stats[TO_STATS][i][j]:
                tos[(i, j)] = get_to_opts(board, stats, i, j)
    ks = sorted(tos.keys(), key=(lambda x: len(tos[x])))
    current = ks.pop()
    k = 0
    while current:
        currentopt = tos[current].pop()
        while currentopt:
            print('try no', k)
            print('connecting', current, TO_STATS, currentopt)
            k += 1
            board1, stats1 = set_signpost(board, stats, current[0], current[1], currentopt[0], currentopt[1])
            board1, stats1 = solve(board1, stats1)
            if is_solved(board1, stats1):
                print('SOLVED!')
                print_board(board1)
                return board1, stats1
            currentopt = tos[current].pop()
        current = ks.pop()
    print('FAIL')
    return board, stats


def is_solved(board, stats):
    current = None
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j][0] == '1':
                current = (i, j)
    while current and board[current[0]][current[1]][0] != str(len(board) * len(board[0])):
        current = stats[TO_STATS][current[0]][current[1]]
    if not current:
        return False
    return True
    # if board[current[0]][current[1]][0] == str(len(board) * len(board[0])):
    #     return True
    # return False


if __name__ == '__main__':
    # board, stats = read_board(os.path.join(os.getcwd(), 'easy_board'))
    board, stats = read_board(os.path.join(os.getcwd(), 'hard_board'))
    print_board(board)
    print(stats)

    # print(get_from_opts(board, stats, 5, 5))

    sb, ss = solve(board, stats)
    print_board(sb)
    print(ss[TO_STATS])
    print(ss[FROM_STATS])
    print(ss[ID_STATS])
    if is_solved(sb, ss):
        print('SOLVED!')
