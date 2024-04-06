from src.picscanner import PicScanner
from og_log import LOG
from src.task import solve_multithread,solve_monothread


# Get a screenshot of your screen and use it as input for the puzzle
# !!! All tiles must be discovered to be valid input


if __name__ == "__main__":
    LOG.start()

    scanner = PicScanner("./img/pic000.jpg")     #  ~ 1080 x 2400 picture 
    mapping = scanner.get_mapping()

    solve_multithread(mapping)

