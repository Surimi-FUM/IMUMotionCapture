"""
周波数解析
・高速フーリエ変換を駆使して，有効波形を取り出す
https://momonoki2017.blogspot.com/2018/03/pythonfft-4.html
"""

import numpy as np
from Ploter import *
import pandas as pd


def main():
    """csvデータロード"""
    filename = 'OffAngle_csv/accel_data.csv'
    acc_data = pd.read_csv(filename, header=None, dtype=float)
    acc_data = np.array(acc_data)

    """計算用"""
    F_abs_amp = [[], [], []]
    F2_abs_amp = [[], [], []]
    fq = [[], [], []]
    dt = 0.01  # [s]
    v = [0, 0, 0]
    x = [0, 0, 0]
    acc_filter = [[], [], []]
    resultant_acc = []

    """プロット用"""
    plot_acc = [[], [], []]
    plot_v = [[], [], []]
    plot_x = [[], [], []]
    plot_time = np.arange(0, len(acc_data[0]) * dt, dt)

    """FFT＆IFFT処理"""
    for i, acc in enumerate(acc_data):
        N = len(acc)
        # 高速フーリエ変換(FFT)
        acc_fft = np.fft.fft(acc)

        # FFTの複素数結果を絶対に変換
        F_abs = np.abs(acc_fft)
        # 振幅をもとの信号に揃える
        F_abs_amp[i] = F_abs / N * 2  # 交流成分はデータ数で割って2倍

        # 周波数軸のデータ作成
        fq[i] = np.linspace(0, 1.0 / dt, N)  # 周波数軸　linspace(開始,終了,分割数)

        """フィルタ処理"""
        acc_fft2 = np.copy(acc_fft)

        # カットオフ周波数設定
        fc_L = 0
        fc_H = 0
        if i == 0:
            # X-axis
            fc_L = 0.2
            fc_H = 1.0
        elif i == 1:
            # Y-axis
            fc_L = 0.2
            fc_H = 1.0
        else:
            # Z-axis
            fc_L = 0.1
            fc_H = 1.0
        acc_fft2[(fq[i] < fc_L)] = 0
        acc_fft2[(fq[i] > fc_H)] = 0

        """フィルタリング処理したFFT結果の確認"""
        # FFTの複素数結果を絶対値に変換
        F2_abs = np.abs(acc_fft2)
        # 振幅をもとの信号に揃える
        F2_abs_amp[i] = F2_abs / N * 2  # 交流成分はデータ数で割って2倍

        """波形に戻す"""
        F_ifft = np.fft.ifft(acc_fft2)  # 逆フーリエ変換(IFFT)
        acc_filter[i] = F_ifft.real

    """合成加速度の算出"""
    for i in range(len(acc_filter[0])):
        m = acc_filter[0][i] ** 2 + acc_filter[1][i] ** 2 + acc_filter[2][i] ** 2
        resultant_acc.append(np.sqrt(m))

    """移動距離算出"""
    for i, datas in enumerate(acc_filter):
        datas *= 9.81
        for j, acc in enumerate(datas):
            if resultant_acc[j] < 0.01:
                acc = 0
            v[i] += acc * dt
            x[i] += (acc * dt * dt) / 2 + v[i] * dt

            plot_acc[i].append(acc / 9.81)
            plot_v[i].append(v[i])
            plot_x[i].append(x[i])

    """プロット処理"""
    # AMPの表示
    ampPlot(plotX=fq, plotAmp=F_abs_amp, plotAmp2=F2_abs_amp)
    # 波形データの表示
    wavePlot(plotX=plot_time, plotYs1=acc_data, plotYs2=acc_filter)
    # 積分結果の表示
    aspPlot(plotX=plot_time, plotAcc=plot_acc, plotSpeed=plot_v, plotDisp=plot_x)
    # X軸とY軸の移動距離をマッピング
    crossPlotValue(plotX=plot_x[0], plotY=plot_x[1], title='Position X-Y')

    print("Fin.")


if __name__ == '__main__':
    main()
