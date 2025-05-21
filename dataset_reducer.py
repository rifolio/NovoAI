import os
import argparse
import multiprocessing as mp
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(
        description="Efficiently delete files for selected base-names by scanning folders once each."
    )
    parser.add_argument(
        "--master", "-m", required=True,
        help="Path to the master filelist txt (e.g., images_filelist.txt)."
    )
    parser.add_argument(
        "--folders", "-f", nargs="+", required=True,
        help="List of folders to delete matching files from (e.g. images train test val)."
    )
    parser.add_argument(
        "--ratio", "-r", type=float, default=0.9,
        help="Fraction of entries to select/delete (default: 0.9 = 90%%)."
    )
    parser.add_argument(
        "--mode", "-d", choices=["first", "last"], default="first",
        help="Whether to select the first or last N%% entries from the master list."
    )
    parser.add_argument(
        "--workers", "-w", type=int, default=4,
        help="Number of parallel deletion workers (default: 4)."
    )
    return parser.parse_args()


def delete_entry(args):
    """
    Delete a single file entry: (folder_path, entry_name)
    """
    folder, entry = args
    try:
        os.remove(os.path.join(folder, entry))
        return 1
    except FileNotFoundError:
        return 0
    except Exception:
        return 0


def main():
    args = parse_args()

    # 1. Load master list and select base-names
    with open(args.master, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total = len(lines)
    k = int(total * args.ratio)
    if args.mode == 'first':
        selected_lines = lines[:k]
    else:
        selected_lines = lines[-k:]

    selected_set = {os.path.splitext(os.path.basename(p))[0] for p in selected_lines}

    print(f"Master entries: {total}")
    print(f"Selected {len(selected_set)} ({args.mode} {args.ratio*100:.0f}%%) base-names.")

    # 2. Define allowed extensions
    exts = {'.jpg', '.jpeg', '.png', '.xml'}

    # 3. Scan each folder once, collecting entries to delete
    tasks = []
    for folder in args.folders:
        print(f"Scanning '{folder}'...")
        # Using os.scandir for speed
        with os.scandir(folder) as it:
            for entry in tqdm(it, desc=f"Scanning {folder}"):
                if not entry.is_file():
                    continue
                base, ext = os.path.splitext(entry.name)
                if ext.lower() in exts and base in selected_set:
                    tasks.append((folder, entry.name))
    print(f"Total files queued for deletion: {len(tasks)} across {len(args.folders)} folders.")

    # 4. Parallel deletion
    if tasks:
        print(f"Deleting files with {args.workers} workers...")
        with mp.Pool(args.workers) as pool:
            # imap_unordered returns deletion results
            for _ in tqdm(pool.imap_unordered(delete_entry, tasks), total=len(tasks), desc="Deleting files"):  # noqa
                pass
    print("Deletion complete.")

if __name__ == '__main__':
    main()