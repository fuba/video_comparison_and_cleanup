import os
import shutil
import difflib
import sys
from lib.video_comparison import compare_videos

def get_file_pairs(dir_path, N, verbose=False):
    """指定されたディレクトリ内の各ファイルに対して、名前の編集距離が近い最大N件のペアを返します。"""
    files = [f for f in os.listdir(dir_path) if f.endswith(".mp4")]
    pairs = []

    for i in range(len(files)):
        distances = []
        for j in range(len(files)):
            if i != j:
                file1 = files[i]
                file2 = files[j]
                ratio = difflib.SequenceMatcher(None, file1, file2).ratio()
                distances.append((file1, file2, ratio))
        
        # 類似度の高い順にソートして上位 N ペアを選択
        distances.sort(key=lambda x: x[2], reverse=True)
        selected_pairs = distances[:N]
        pairs.extend(selected_pairs)
    
    if verbose:
        print(f"Identified {len(pairs)} file pairs for comparison.")
    
    return pairs

def move_file_to_duplicate_dir(file_path, duplicate_dir, verbose=False):
    """ファイルを重複ディレクトリに移動し、対応する .vtt ファイルがあればそれも移動します。"""
    ensure_directory_exists(duplicate_dir)
    destination = os.path.join(duplicate_dir, os.path.basename(file_path))
    shutil.move(file_path, destination)
    if verbose:
        print(f"Moved {file_path} to {destination}")

    # 対応する .vtt ファイルも移動
    vtt_file_path = os.path.splitext(file_path)[0] + ".vtt"
    if os.path.exists(vtt_file_path):
        vtt_destination = os.path.join(duplicate_dir, os.path.basename(vtt_file_path))
        shutil.move(vtt_file_path, vtt_destination)
        if verbose:
            print(f"Moved {vtt_file_path} to {vtt_destination}")

def ensure_directory_exists(directory):
    """ディレクトリが存在しない場合は作成します。"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def manage_cache(cache_base, max_cache_files=20000, files_to_remove=10000):
    """キャッシュディレクトリのファイル数を管理し、必要に応じて古いファイルを削除します。"""
    cache_files = []
    for root, _, files in os.walk(cache_base):
        for file in files:
            full_path = os.path.join(root, file)
            cache_files.append(full_path)

    if len(cache_files) > max_cache_files:
        # キャッシュファイルを最終アクセス時間でソート
        cache_files.sort(key=lambda x: os.path.getatime(x))
        files_to_delete = cache_files[:files_to_remove]

        for file in files_to_delete:
            os.remove(file)
            print(f"Deleted cache file: {file}")

def compare_and_cleanup(dir_path, N, threshold, verbose=False):
    duplicate_dir = os.path.join(dir_path, "duplicate")
    cache_base = os.environ.get("COMPARE_CACHE", "/tmp")

    # ファイルペアのリストを取得
    file_pairs = get_file_pairs(dir_path, N, verbose=verbose)

    for idx, (file1, file2, _) in enumerate(file_pairs):
        file1_path = os.path.join(dir_path, file1)
        file2_path = os.path.join(dir_path, file2)

        # 移動済みのファイルをチェック
        if not os.path.exists(file1_path) or not os.path.exists(file2_path):
            if verbose:
                print(f"Skipping comparison for {file1} and {file2} because one or both files no longer exist.")
            continue

        if verbose:
            print(f"Comparing {file1} and {file2} ({idx + 1}/{len(file_pairs)})")

        # 動画を比較してDTW距離を取得
        dtw_distance = compare_videos(file1_path, file2_path, cache_base)
        
        if dtw_distance is None:
            print(f"Error: DTW distance could not be calculated for {file1} and {file2}.", file=sys.stderr)
            continue
        
        if dtw_distance <= threshold:
            if verbose:
                print(f"DTW distance between {file1} and {file2} is {dtw_distance:.2f}, below threshold {threshold:.2f}. Marking as duplicate.")
            # ファイルの作成日時を比較して、古い方を残す
            file1_ctime = os.path.getctime(file1_path)
            file2_ctime = os.path.getctime(file2_path)
            
            if file1_ctime < file2_ctime:
                move_file_to_duplicate_dir(file2_path, duplicate_dir, verbose=verbose)
            else:
                move_file_to_duplicate_dir(file1_path, duplicate_dir, verbose=verbose)
        elif verbose:
            print(f"DTW distance between {file1} and {file2} is {dtw_distance:.2f}, above threshold {threshold:.2f}. No action taken.")
