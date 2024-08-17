import sys
import os
from lib.compare_and_cleanup import compare_videos

def print_usage():
    print("Usage: python run_compare.py <video_file1> <video_file2>")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()

    video_file1 = sys.argv[1]
    video_file2 = sys.argv[2]

    # 環境変数 COMPARE_CACHE からキャッシュディレクトリを取得、指定がない場合は /tmp を使用
    cache_base = os.environ.get("COMPARE_CACHE", "/tmp")
    
    # compare_videos関数を呼び出してDTW距離を取得
    dtw_distance = compare_videos(video_file1, video_file2, cache_base)
    
    if dtw_distance is None:
        print(f"Error: DTW distance could not be calculated for {video_file1} and {video_file2}.", file=sys.stderr)
        sys.exit(1)

    # 結果を出力
    print(f"DTW distance between {video_file1} and {video_file2} is {dtw_distance:.2f}")
