import matplotlib.pyplot as plt


# X軸データを指定しない，ただプロットするだけの関数
def standardPlotValue(plotY, color='Red', title='None'):
    plt.title(title)
    plt.plot(plotY, color=color)
    plt.grid(True)
    plt.show()


# X軸を時間とした標準的な時系列プロット。1つの図に1のデータを描画する一般的な使い方
def simplePlotValue(plotX, plotY, color='Red', title='None'):
    plt.title(title)
    plt.plot(plotX, plotY, color=color)
    plt.grid(True)
    plt.show()


# X軸を時間とした標準的な時系列プロット。1つの図に複数のデータを描画するように設定してある
def somePlotValues(plotX, plotYs, title='None', save=False):
    colors = ['r', 'g', 'k', 'b', 'c', 'm', 'y', 'w']
    plt.title(title)
    for i, plotY in enumerate(plotYs):
        plt.plot(plotX, plotY, color=colors[i])
    plt.grid(True)
    plt.legend(['X', 'Y', 'Z'])
    plt.show()


# 原点を中心とした十字軸のプロット。X軸にX方向，Y軸にY方向の値を指定することで，センサの平面での動作をプロットするのに使う
def crossPlotValue(plotX, plotY, color="Black", title='None'):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(title)

    # 下軸と左軸をそれぞれ中央へもってくる
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))

    # 上軸と右軸を表示しない
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.plot(plotX, plotY, color=color, linestyle='None', marker='o')
    plt.plot(plotX[0], plotY[0], color='Red', linestyle='None', marker='o')
    plt.plot(plotX[-1], plotY[-1], color='Green', linestyle='None', marker='o')
    plt.grid(True)
    plt.show()


def ampPlot(plotX, plotAmp, plotAmp2, figsize=(6, 8)):
    axis = ['X', 'Y', 'Z']
    ffig, ax = plt.subplots(3, 2, figsize=figsize, tight_layout=True)
    N = int(len(plotX[0]) / 2)
    # N = 100
    for i in range(3):
        ax[i, 0].plot(plotX[i][:N], plotAmp[i][:N])
        ax[i, 1].plot(plotX[i][:N], plotAmp2[i][:N])
        ax[i, 0].set_xlabel('freqency(Hz)', fontsize=14)
        ax[i, 1].set_xlabel('freqency(Hz)', fontsize=14)
        ax[i, 0].set_ylabel('amplitude {}'.format(axis[i]), fontsize=14)
        ax[i, 0].grid(True)
        ax[i, 1].grid(True)
    plt.show()


def wavePlot(plotX, plotYs1, plotYs2):
    axis = ['X', 'Y', 'Z']
    fig, ax = plt.subplots(3, 1, figsize=(6, 8), tight_layout=True)
    for i in range(3):
        ax[i].plot(plotX, plotYs1[i], label='original')
        ax[i].plot(plotX, plotYs2[i], c="r", label='IFFT')  # IFFT（逆変換）
        ax[i].set_xlabel('time(sec)', fontsize=14)
        ax[i].set_ylabel('signal', fontsize=14)
        ax[i].set_title(axis[i])
        ax[i].legend()
        ax[i].grid(True)
    plt.show()


def aspPlot(plotX, plotAcc, plotSpeed, plotDisp):
    title = ['Accel [m/s^2]', 'Speed [m/s]', 'Displacement [m]']
    label = ['X', 'Y', 'Z']
    fig, ax = plt.subplots(3, 3, figsize=(12, 8), tight_layout=True)
    for i in range(3):
        ax[i, 0].plot(plotX, plotAcc[i])
        ax[i, 1].plot(plotX, plotSpeed[i])
        ax[i, 2].plot(plotX, plotDisp[i])
        ax[i, 0].set_ylabel(label[i])
        ax[0, i].set_title(title[i])
        ax[0, i].grid(True)
        ax[1, i].grid(True)
        ax[2, i].grid(True)
    plt.show()
