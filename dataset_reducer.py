import os
import argparse
import multiprocessing as mp
from tqdm import tqdm
import shutil

def parse_args():
    parser = argparse.ArgumentParser(
        description="Copy a selected fraction of files (by base-name) from default train/val/test or custom source folders into an output directory."
    )
    parser.add_argument(
        "--master", "-m", required=True,
        help="Path to the master filelist txt (one path per line)."
    )
    parser.add_argument(
        "--folders", "-f", nargs="+",
        help="Optional list of source folders to scan. If omitted, defaults to train, val and test under master’s folder."
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Path to the output folder where selected files will be copied."
    )
    parser.add_argument(
        "--ratio", "-r", type=float, default=0.3,
        help="Fraction of entries to select and copy (default: 0.3 = 30%%)."
    )
    parser.add_argument(
        "--mode", "-d", choices=["first", "last"], default="first",
        help="Whether to select the first or last N%% entries from the master list."
    )
    parser.add_argument(
        "--workers", "-w", type=int, default=4,
        help="Number of parallel workers for copying (default: 4)."
    )
    return parser.parse_args()


def copy_entry(args):
    src_folder, filename, dst_folder = args
    src_path = os.path.join(src_folder, filename)
    dst_path = os.path.join(dst_folder, filename)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    try:
        shutil.copy2(src_path, dst_path)
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False


def main():
    args = parse_args()

    # 1. Determine source folders
    if args.folders:
        folders = args.folders
    else:
        base_dir = os.path.dirname(os.path.abspath(args.master))
        folders = [os.path.join(base_dir, sub) for sub in ("train", "val", "test")]
    print("Using folders:", folders)

    # 2. Load master list and pick selected base-names
    with open(args.master, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    total = len(lines)
    k = int(total * args.ratio)

    if args.mode == 'first':
        chosen = lines[:k]
    else:
        chosen = lines[-k:]

    selected = {os.path.splitext(os.path.basename(p))[0] for p in chosen}
    print(f"Master entries: {total}")
    print(f"Copying {len(selected)} ({args.mode} {args.ratio*100:.0f}%) base-names.")

    # 3. Extensions to include
    exts = {'.jpg', '.jpeg', '.png', '.xml'}

    # 4. Collect tasks: only copy if base-name is in selected
    tasks = []
    for folder in folders:
        print(f"Scanning '{folder}'...")
        with os.scandir(folder) as it:
            for entry in tqdm(it, desc=f"Scanning {os.path.basename(folder)}"):
                if not entry.is_file():
                    continue
                base, ext = os.path.splitext(entry.name)
                if ext.lower() in exts and base in selected:
                    tasks.append((folder, entry.name, args.output))

    print(f"Total files queued for copy: {len(tasks)}")

    # 5. Parallel copy
    if tasks:
        print(f"Copying files with {args.workers} workers...")
        with mp.Pool(args.workers) as pool:
            for _ in tqdm(pool.imap_unordered(copy_entry, tasks),
                          total=len(tasks), desc="Copying"):
                pass

    print("Copy complete.")


if __name__ == '__main__':
    main()
