import matplotlib.pyplot as plt




if __name__ == '__main__':
    data = []
    for i in range(100):
        data.append((88552 - i * 100, 106097 - i * 100, 117054 - i * 100))

    draw_plot(data, "Jakiś głupi wykres", "plik.jpg")

