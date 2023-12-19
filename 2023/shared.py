def move_in_grid(x: int, y: int, direction: str) -> (int, int):
    if direction == 'N':
        return x-1, y
    if direction == 'E':
        return x, y+1
    if direction == 'S':
        return x+1, y
    if direction == 'W':
        return x, y-1
    raise ValueError(f"The direction '{direction}' is not supported.")
