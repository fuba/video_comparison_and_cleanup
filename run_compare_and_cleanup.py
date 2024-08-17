import sys
import os
import argparse
from lib.compare_and_cleanup import compare_and_cleanup, manage_cache

def main():
    parser = argparse.ArgumentParser(description="Compare and clean up duplicate videos in a directory.")
    parser.add_argument("dir", help="Directory containing MP4 files")
    parser.add_argument("-N", "--compare-target-num", type=int, default=10, help="Number of closest file pairs to compare")
    parser.add_argument("-T", "--threshold", type=float, default=200000, help="DTW distance threshold for considering videos as duplicates")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    
    compare_and_cleanup(args.dir, args.compare_target_num, args.threshold, verbose=args.verbose)
    
    # キャッシュ管理も行う
    cache_base = os.environ.get("COMPARE_CACHE", "/tmp")
    manage_cache(cache_base)

if __name__ == "__main__":
    main()
