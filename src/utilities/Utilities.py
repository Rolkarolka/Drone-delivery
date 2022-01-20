import math
import matplotlib.pyplot as plt


class Utilities:
    @staticmethod
    def calc_distance(coord_a, coord_b):
        return math.sqrt((coord_a[0] - coord_b[0]) ** 2 + (coord_a[1] - coord_b[1]) ** 2)

    @staticmethod
    def draw_plot(data: list[tuple[int, int, int]], title: str = None, filename: str = None):
        min_values = [data_tuple[0] for data_tuple in data]
        avg_values = [data_tuple[1] for data_tuple in data]
        max_values = [data_tuple[2] for data_tuple in data]

        plt.plot(min_values, marker='o', label='Min score')
        plt.plot(avg_values, marker='o', label='Avg score')
        plt.plot(max_values, marker='o', label='Max score')
        if title is not None:
            plt.title(title)
        plt.xlabel("Generation")
        plt.ylabel("Score")
        plt.legend()
        plt.subplots_adjust(left=0.15)
        if filename is not None:
            plt.savefig(filename)
        plt.show()
