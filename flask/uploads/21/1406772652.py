def guess(result):

    """
    @result : result class that contains all game log
    return : guess location coordinate as tuple (x,y)
    """

    x = 0
    y = 0
    board = result.board
    last_result = result.get_last_result()

    if "result" in last_result:
        x = last_result["guess"]["x"]
        y = last_result["guess"]["y"]

    if ("result" in last_result) and (last_result["result"] == constant.RESULT_HIT) and (x < 9) and board[y][x+1] > 0:
        x = last_result["guess"]["x"] + 1
        y = last_result["guess"]["y"]

    empty = []
    for i in range(10):
        for j in range(10):
            if result.get_board()[i][j] >= 0:
                empty.append((i,j))
    y, x = random.sample(empty,1)[0]

    #while result.get_board()[y][x] < 0:
    #    x = random.randint(0,9)
    #    y = random.randint(0,9)

    return (x,y)

    #-- to here --
