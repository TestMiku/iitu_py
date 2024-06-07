def tcp_key(x: str) -> tuple[int, int]:
    return tuple[int, int](map(int, x.split(".")))
