import os
import json
import hashlib
import subprocess
import numpy as np
import librosa
import gzip
from scipy.spatial.distance import cdist
from pydub import AudioSegment

def get_cache_directory(file_path, cache_base):
    # ファイルのハッシュ値を使って一意のディレクトリを生成
    file_hash = hashlib.md5(file_path.encode('utf-8')).hexdigest()
    return os.path.join(cache_base, file_hash)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_audio_from_video(video_file_path, cache_dir):
    ensure_directory_exists(cache_dir)
    
    # 音声ファイルのパスを生成
    audio_file_path = os.path.join(cache_dir, "audio.aac")
    
    if not os.path.exists(audio_file_path):
        # FFmpegを使用して音声を抽出
        command = ['ffmpeg', '-i', video_file_path, '-vn', '-acodec', 'copy', audio_file_path]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return audio_file_path

def generate_mfcc(audio_file_path, cache_dir, n_mfcc=8, sr=8000, duration=None):
    mfcc_cache_file = os.path.join(cache_dir, "mfcc_cache.json.gz")

    # キャッシュファイルが存在する場合、キャッシュを読み込む
    if os.path.exists(mfcc_cache_file):
        with gzip.open(mfcc_cache_file, 'rt') as f:
            mfcc = np.array(json.load(f))
        return mfcc

    # キャッシュがない場合、音声ファイルを処理
    audio = AudioSegment.from_file(audio_file_path)
    samples = np.array(audio.get_array_of_samples()).astype(float)
    
    # ダウンサンプリングを適用
    samples = librosa.resample(samples, orig_sr=audio.frame_rate, target_sr=sr)
    
    # 音声データの長さを制限
    if duration:
        samples = samples[:int(sr * duration)]
    
    # MFCCの計算
    mfcc = librosa.feature.mfcc(y=samples, sr=sr, n_mfcc=n_mfcc)

    # キャッシュファイルに保存
    with gzip.open(mfcc_cache_file, 'wt') as f:
        json.dump(mfcc.tolist(), f)

    return mfcc

def calculate_dtw_distance(mfcc1, mfcc2):
    # MFCCの距離行列を計算
    distance_matrix = cdist(mfcc1.T, mfcc2.T, metric='euclidean')
    # DTWの計算
    dtw_distance, _ = librosa.sequence.dtw(C=distance_matrix)
    
    return dtw_distance[-1, -1]

def compress_cache_file(file_path):
    with open(file_path, 'rb') as f_in:
        with gzip.open(file_path + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)
    os.remove(file_path)  # オリジナルファイルを削除

def cleanup_and_compress_cache(cache_dir):
    for root, _, files in os.walk(cache_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not file_path.endswith(".gz"):
                compress_cache_file(file_path)
    
def delete_audio_file(audio_file_path):
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

def compare_videos(video_file1, video_file2, cache_base):
    try:
        # キャッシュディレクトリを取得
        cache_dir1 = get_cache_directory(video_file1, cache_base)
        cache_dir2 = get_cache_directory(video_file2, cache_base)
        
        # 音声ファイルを抽出
        audio_file1 = os.path.join(cache_dir1, "audio.aac")
        audio_file2 = os.path.join(cache_dir2, "audio.aac")

        if not os.path.exists(os.path.join(cache_dir1, "mfcc_cache.json.gz")):
            audio_file1 = extract_audio_from_video(video_file1, cache_dir1)

        if not os.path.exists(os.path.join(cache_dir2, "mfcc_cache.json.gz")):
            audio_file2 = extract_audio_from_video(video_file2, cache_dir2)

        # MFCCを生成 (ダウンサンプリングと次元削減)
        mfcc1 = generate_mfcc(audio_file1, cache_dir1, n_mfcc=8, sr=8000, duration=600)  # 10分の音声を使用
        mfcc2 = generate_mfcc(audio_file2, cache_dir2, n_mfcc=8, sr=8000, duration=600)

        if mfcc1 is not None and mfcc2 is not None:
            # DTW距離を計算
            dtw_distance = calculate_dtw_distance(mfcc1, mfcc2)
            
            # AACファイルを削除
            delete_audio_file(audio_file1)
            delete_audio_file(audio_file2)
            
            # キャッシュをGzip圧縮
            cleanup_and_compress_cache(cache_dir1)
            cleanup_and_compress_cache(cache_dir2)
            
            return dtw_distance  # DTW距離を返す
        else:
            raise ValueError("Failed to generate MFCCs.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)  # 標準エラー出力にエラーメッセージを出力
        return None  # エラーが発生した場合、Noneを返す
