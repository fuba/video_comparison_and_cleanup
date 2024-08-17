import os
import argparse
from lib.compare_and_cleanup import compare_and_cleanup, manage_cache

def apply_cleanup_to_all(root_dir, N, threshold, verbose=False):
    """ルートディレクトリ以下のすべてのサブディレクトリに対してcompare_and_cleanupを適用します。"""
    cache_base = os.environ.get("COMPARE_CACHE", "/tmp")

    for subdir, _, _ in os.walk(root_dir):
        print(f"Processing directory: {subdir}")
        compare_and_cleanup(subdir, N, threshold, verbose=verbose)
        manage_cache(cache_base)

def main():
    parser = argparse.ArgumentParser(description="Apply compare_and_cleanup to all subdirectories of a root directory.")
    parser.add_argument("root_dir", help="Root directory containing subdirectories to process")
    parser.add_argument("-N", "--compare-target-num", type=int, default=10, help="Number of closest file pairs to compare for each file")
    parser.add_argument("-T", "--threshold", type=float, default=200000, help="DTW distance threshold for considering videos as duplicates")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    
    apply_cleanup_to_all(args.root_dir, args.compare_target_num, args.threshold, verbose=args.verbose)

if __name__ == "__main__":
    main()
