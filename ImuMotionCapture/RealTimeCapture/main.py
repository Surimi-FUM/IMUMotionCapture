import numpy as np
import time
from BMX055Class import BMX055
from Ploter import *

def main():
    """準備"""
    sensor = BMX055()
    sensor.setup()

    # 計算用
    start = time.perf_counter()
    start_dt = time.perf_counter()
    stop_time = 20.0   # 計測を終了する時間
    lowpass_acc = [0, 0, 1]
    highpass_acc = [0, 0, 0]
    v = [0, 0, 0]
    x = [0, 0, 0]

    # プロット用
    plot_acc = [[], [], []]
    plot_highacc = [[], [], []]
    plot_v = [[], [], []]
    plot_x = [[], [], []]
    plot_time = []
    fftanalysis_dt = []

    """
    ローパスの初期化
    ・初期化することで，ハイパスフィルタ値の初期値がきれいに調整される
    """
    acc = sensor.getAccel()
    acc_data = np.array(acc)
    for i in range(3):
        lowpass_acc[i] = acc_data[i]

    """計測"""
    while True:
        keikaTime = time.perf_counter() - start
        if keikaTime >= stop_time:
            break

        # センサ値の取得
        gyro = sensor.getGyro()
        acc = sensor.getAccel()
        acc_data = np.array(acc)
        gyro_data = np.array(gyro)

        dt = time.perf_counter() - start_dt
        start_dt = time.perf_counter()
        fftanalysis_dt.append(dt)

        """
        ローパス＆ハイパスフィルタ
        ・ローパスフィルタで重力成分を取り出し，それを元データから差し引く
        """
        fc = 0.2  # カットオフ周波数
        c = 2 * np.pi * fc
        K = (1 / c) / ((1 / c) + dt)
        for i, data in enumerate(acc_data):
            lowpass_acc[i] = K * lowpass_acc[i] + (1 - K) * data
            highpass_acc[i] = data - lowpass_acc[i]

        """
        合成加速度
        ・軸成分を排除した加速度データ。手振れなどの微小な揺れによるノイズを除去する
        """
        m = highpass_acc[0] ** 2 + highpass_acc[1] ** 2 + highpass_acc[2] ** 2
        resultant_acc = np.sqrt(m)

        if resultant_acc < 0.01:
            for i in range(3):
                highpass_acc[i] = 0

        """移動距離算出"""
        for i, acc in enumerate(highpass_acc):
            acc *= 9.81
            v[i] += acc * dt
            x[i] += (acc * dt * dt) / 2 + v[i] * dt

        plot_time.append(keikaTime)
        for i in range(3):
            plot_acc[i].append(acc_data[i])
            plot_highacc[i].append(highpass_acc[i])
            plot_v[i].append(v[i])
            plot_x[i].append(x[i])
        print("\r{} / {} : {}".format(keikaTime, stop_time, 0), end="")

    """描画処理"""
    wavePlot(plotX=plot_time, plotYs1=plot_acc, plotYs2=plot_highacc)
    # 積分結果の表示
    aspPlot(plotX=plot_time, plotAcc=plot_highacc, plotSpeed=plot_v, plotDisp=plot_x)
    # X軸とY軸の移動距離をマッピング
    crossPlotValue(plotX=plot_x[0], plotY=plot_x[1], title='Position X-Y')
    # X軸とY軸の移動距離をマッピング
    crossPlotValue(plotX=plot_x[0], plotY=plot_x[2], title='Position X-Z')
    # X軸とY軸の移動距離をマッピング
    crossPlotValue(plotX=plot_x[1], plotY=plot_x[2], title='Position Y-Z')

    """
    FFT解析
    ・右側の波形の始点が0になっていたら直流成分(重力成分)を除去できている
    ・このプログラムではY軸，Z軸へのカット周波数を調整する必要がある
    """
    F_abs_amp = [[], [], []]
    fq = [[], [], []]
    dt = np.sum(fftanalysis_dt) / len(fftanalysis_dt)
    for i, acc in enumerate(plot_acc):
        N = len(acc)
        # 高速フーリエ変換(FFT)
        acc_fft = np.fft.fft(acc)

        # FFTの複素数結果を絶対に変換
        F_abs = np.abs(acc_fft)
        # 振幅をもとの信号に揃える
        F_abs_amp[i] = F_abs / N * 2  # 交流成分はデータ数で割って2倍

        # 周波数軸のデータ作成
        fq[i] = np.linspace(0, 1.0 / dt, N)  # 周波数軸　linspace(開始,終了,分割数)

    F2_abs_amp = [[], [], []]
    for i, acc in enumerate(plot_highacc):
        N = len(acc)
        # 高速フーリエ変換(FFT)
        acc_fft = np.fft.fft(acc)

        # FFTの複素数結果を絶対に変換
        F_abs = np.abs(acc_fft)
        # 振幅をもとの信号に揃える
        F2_abs_amp[i] = F_abs / N * 2  # 交流成分はデータ数で割って2倍

        # 周波数軸のデータ作成
        fq[i] = np.linspace(0, 1.0 / dt, N)  # 周波数軸　linspace(開始,終了,分割数)
    # AMPの表示
    ampPlot(plotX=fq, plotAmp=F_abs_amp, plotAmp2=F2_abs_amp)
    print("\nFin.")


if __name__ == '__main__':
    main()
