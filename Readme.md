# 動画比較およびクリーンアップツール

このプロジェクトは、音声トラックに基づいて動画ファイルを比較するためのPythonスクリプトとライブラリを提供します。このツールは、ディレクトリ内の重複動画を特定し、自動的に別のディレクトリに移動するために使用できます。

## 機能

- **動画比較**: Mel-Frequency Cepstral Coefficients (MFCC) と Dynamic Time Warping (DTW) アルゴリズムを使用して、音声トラックに基づいて2つの動画ファイルを比較します。
- **重複クリーンアップ**: 重複する動画ファイルと、それに対応する `.vtt` 字幕ファイルを自動的に特定し、`duplicate` ディレクトリに移動します。
- **柔軟な設定**: 比較対象の数と、動画を重複とみなすための閾値を設定できます。

## ファイル概要

- `lib/compare_and_cleanup.py`: 
  - 動画の比較、クリーンアップ、およびキャッシュ管理を行うPythonライブラリです。動画ファイルの比較、キャッシュファイルの管理、重複動画のクリーンアップ機能を提供します。
  
- `lib/video_comparison.py`: 
  - 動画の比較を行うためのPythonライブラリで、音声の抽出、MFCCの生成、DTW距離の計算を行います。このライブラリは、比較のコアロジックを担当します。

- `apply_compare_and_cleanup_to_all.py`: 
  - 指定されたルートディレクトリ以下のすべてのサブディレクトリに対して、動画比較とクリーンアップのプロセスを適用するコマンドラインスクリプトです。キャッシュファイルを管理し、キャッシュファイルの数が指定された制限を超えないようにします。

- `run_compare_and_cleanup.py`: 
  - 単一のディレクトリ内で重複動画を比較してクリーンアップするコマンドラインスクリプトです。必要な操作を実行するために、`lib/compare_and_cleanup.py` ライブラリを使用します。

- `run_compare.py`: 
  - 2つの動画ファイルを比較し、DTW距離を計算して結果を出力するコマンドラインスクリプトです。

## インストール

スクリプトを使用する前に、必要なPythonライブラリがインストールされていることを確認してください。以下のコマンドでインストールできます。

```bash
pip install numpy scipy librosa pydub
```

さらに、システムに `ffmpeg` がインストールされている必要があります。以下の手順で `ffmpeg` をインストールしてください。

### Ubuntu/Linux

```bash
sudo apt-get install ffmpeg
```

### MacOS

```bash
brew install ffmpeg
```

### Windows

```bash
choco install ffmpeg
```

## 使用方法

### 1. 動画比較

`run_compare.py` スクリプトを使用して、2つの動画ファイルを比較し、音声トラック間のDTW距離を出力します。

```bash
python run_compare.py <video_file1> <video_file2>
```

例:

```bash
python run_compare.py video1.mp4 video2.mp4
```

### 2. 単一ディレクトリのクリーンアップ

`run_compare_and_cleanup.py` スクリプトを使用して、指定されたディレクトリ内の重複動画ファイルを特定して移動します。このスクリプトは、対応する `.vtt` 字幕ファイルも移動します。

```bash
python run_compare_and_cleanup.py <dir> [-N 10] [-T 200000] [-v]
```

- `<dir>`: 比較対象となる動画ファイルが含まれるディレクトリ。
- `-N/--compare-target-num`: 各ファイルに対して比較するファイルペアの最大数（デフォルトは10）。
- `-T/--threshold`: 動画を重複とみなすためのDTW距離の閾値（デフォルトは200000）。
- `-v/--verbose`: 処理の詳細な手順を表示します。

例:

```bash
python run_compare_and_cleanup.py /path/to/videos -N 5 -T 150000 -v
```

### 3. 複数ディレクトリのクリーンアップ

`apply_compare_and_cleanup_to_all.py` スクリプトを使用して、指定されたルートディレクトリ以下のすべてのサブディレクトリに対して、比較とクリーンアップのプロセスを適用します。

```bash
python apply_compare_and_cleanup_to_all.py <root_dir> [-N 10] [-T 200000] [-v]
```

- `<root_dir>`: 処理対象のサブディレクトリを含むルートディレクトリ。
- `-N/--compare-target-num`: 各ファイルに対して比較するファイルペアの最大数（デフォルトは10）。
- `-T/--threshold`: 動画を重複とみなすためのDTW距離の閾値（デフォルトは200000）。
- `-v/--verbose`: 処理の詳細な手順を表示します。

例:

```bash
python apply_compare_and_cleanup_to_all.py /path/to/root -N 5 -T 150000 -v
```

## アルゴリズム概要

### 1. 音声抽出

各動画ファイルから `ffmpeg` を使用して音声トラックを抽出します。抽出された音声は、さらなる分析と比較のために使用されます。

### 2. MFCC計算

音声トラックからメル周波数ケプストラム係数 (MFCC) を計算します。MFCCは、音声認識や音響処理で広く使用されている手法で、音の短時間パワースペクトルを表現します。

### 3. Dynamic Time Warping (DTW)

DTWアルゴリズムを使用して、2つの音声トラックのMFCCを比較します。DTWは、2つの系列間の最適な整列を見つけ、それらの類似度を表す距離スコアを計算します。DTW距離が小さいほど、類似度が高いことを示します。

### 4. 重複検出とクリーンアップ

2つの動画ファイル間のDTW距離が指定された閾値以下の場合、それらは重複しているとみなされます。その後、2つのファイルの作成日時を比較し、新しいファイル（および対応する `.vtt` ファイルが存在する場合）は `duplicate` ディレクトリに移動されます。

## 環境変数

キャッシュファイルが保存されるディレクトリを指定するために `COMPARE_CACHE` 環境変数を設定できます。設定されていない場合、デフォルトのディレクトリ `/tmp` が使用されます。

例 (Linux/MacOS):

```bash
export COMPARE_CACHE=/path/to/cache
```

例 (Windows):

```bash
set COMPARE_CACHE=C:\path	o\cache
```

## 貢献

問題がある場合や改善の提案がある場合は、GitHubでissueを作成するか、プルリクエストを提出してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 免責事項

このREADMEファイルおよび関連するスクリプトは、OpenAIのChatGPTの支援を受けて生成されました。正確性には注意を払っていますが、ユーザーは特定の環境でコードを使用する前に検証とテストを行う必要があります。このコードの使用による問題や損害について、OpenAIおよびモデルは責任を負いません。
