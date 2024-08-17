# Video Comparison and Cleanup Tool

This project provides a set of Python scripts and a library for comparing video files based on their audio tracks. The tool can be used to identify duplicate videos in a directory and automatically move duplicates to a separate directory.

## Features

- **Video Comparison**: Compare two video files based on their audio tracks using Mel-Frequency Cepstral Coefficients (MFCC) and Dynamic Time Warping (DTW) algorithms.
- **Duplicate Cleanup**: Automatically identify and move duplicate video files, along with their corresponding `.vtt` subtitle files, to a `duplicate` directory.
- **Flexible Configuration**: Configure the number of comparisons and the threshold for considering videos as duplicates.

## File Overview

- `lib/compare_and_cleanup.py`: 
  - A Python library that handles video comparison, cleanup, and cache management. It provides functions for comparing videos, managing cache files, and handling duplicate video cleanup.
  
- `lib/video_comparison.py`: 
  - A Python library for video comparison that extracts audio, generates MFCC, and calculates DTW distance. This library handles the core comparison logic.

- `apply_compare_and_cleanup_to_all.py`: 
  - A command-line script that applies the video comparison and cleanup process to all subdirectories of a specified root directory. It manages cache files and ensures that the number of cache files does not exceed a specified limit.

- `run_compare_and_cleanup.py`: 
  - A command-line script that compares and cleans up duplicate videos within a single directory. It uses the `lib/compare_and_cleanup.py` library to perform the necessary operations.

- `run_compare.py`: 
  - A command-line script for comparing two video files. It calculates the DTW distance between the audio tracks and outputs the result.

## Installation

Before using the scripts, ensure you have the necessary Python libraries installed. You can install them using `pip`:

```bash
pip install numpy scipy librosa pydub
```

Additionally, `ffmpeg` must be installed on your system. Follow the instructions below to install `ffmpeg`:

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

## Usage

### 1. Video Comparison

Use the `run_compare.py` script to compare two video files and output the DTW distance between their audio tracks.

```bash
python run_compare.py <video_file1> <video_file2>
```

Example:

```bash
python run_compare.py video1.mp4 video2.mp4
```

### 2. Directory Cleanup for a Single Directory

Use the `run_compare_and_cleanup.py` script to identify and move duplicate video files within a specified directory. The script also moves corresponding `.vtt` subtitle files if they exist.

```bash
python run_compare_and_cleanup.py <dir> [-N 10] [-T 200000] [-v]
```

- `<dir>`: The directory containing the video files to be compared.
- `-N/--compare-target-num`: The number of closest file pairs to compare for each file (default is 10).
- `-T/--threshold`: The DTW distance threshold for considering videos as duplicates (default is 200000).
- `-v/--verbose`: Enable verbose output to see detailed processing steps.

Example:

```bash
python run_compare_and_cleanup.py /path/to/videos -N 5 -T 150000 -v
```

### 3. Directory Cleanup for Multiple Directories

Use the `apply_compare_and_cleanup_to_all.py` script to apply the comparison and cleanup process to all subdirectories within a specified root directory.

```bash
python apply_compare_and_cleanup_to_all.py <root_dir> [-N 10] [-T 200000] [-v]
```

- `<root_dir>`: The root directory containing subdirectories to be processed.
- `-N/--compare-target-num`: The number of closest file pairs to compare for each file (default is 10).
- `-T/--threshold`: The DTW distance threshold for considering videos as duplicates (default is 200000).
- `-v/--verbose`: Enable verbose output to see detailed processing steps.

Example:

```bash
python apply_compare_and_cleanup_to_all.py /path/to/root -N 5 -T 150000 -v
```

## Algorithm Overview

### 1. Audio Extraction

For each video file, the audio track is extracted using `ffmpeg`. The extracted audio is used for further analysis and comparison.

### 2. MFCC Calculation

Mel-Frequency Cepstral Coefficients (MFCC) are computed from the audio track. MFCCs are widely used in audio processing and speech recognition to represent the short-term power spectrum of a sound.

### 3. Dynamic Time Warping (DTW)

The DTW algorithm is used to compare the MFCCs of two audio tracks. DTW finds the optimal alignment between the two sequences and calculates a distance score that represents their similarity. A lower DTW distance indicates higher similarity.

### 4. Duplicate Detection and Cleanup

If the DTW distance between two video files is below the specified threshold, they are considered duplicates. The script then compares the creation dates of the two files and moves the newer file (and its corresponding `.vtt` file, if it exists) to the `duplicate` directory.

## Environment Variables

You can set the `COMPARE_CACHE` environment variable to specify the directory where cache files are stored. If not set, the default directory `/tmp` is used.

Example (Linux/MacOS):

```bash
export COMPARE_CACHE=/path/to/cache
```

Example (Windows):

```bash
set COMPARE_CACHE=C:\path	o\cache
```

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This README file and the associated scripts were generated with the assistance of OpenAI's ChatGPT. While care has been taken to ensure accuracy, users should verify and test the code in their specific environment before use. OpenAI and the model bear no responsibility for any issues or damages resulting from the use of this code.
