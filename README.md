# IMUMotionCapture
RaspBerry Piで制御したIMU(慣性計測ユニット)を用いたモーションキャプチャー  

![XYZ](https://user-images.githubusercontent.com/116449282/229971007-50d152fa-2076-4271-8809-b475bdd12929.png)  
![Pos](https://user-images.githubusercontent.com/116449282/229970482-96e6f8eb-e3a3-4a61-a018-427c9cf4966c.png)  

IMUの加速度センサからセンサ値を取得し、ノイズ除去のフィルタ処理を施して位置推定を行った。  
カットすべき周波数の特定のために、数秒間記録したデータに対して高速フーリエ変換を用いて周波数解析を行った。  
静的解析の結果を基にリアルタイム解析の実装を行った。  

## 結果  
完全にはノイズを除去することができず、軸ずれが生じて実際の位置とずれていった。  
それでも短時間IMUの軌道を捉えることができた。

## 開発環境
PC：Windows 10 Pro、Intel Core i7-6700K  
IDE：PyCharm Professional  
IMU：BMX055  
マイコン：Raspberry Pi3 B+  
言語：Python3  
フレームワーク：pigpio
### テスト環境
開発環境と同じ

## 開発期間・人数
令和4年(2022)/9月、3人  
