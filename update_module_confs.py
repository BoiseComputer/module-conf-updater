import os
import shutil

def find_modules(folder):
    dist_files = []
    for file in os.listdir(folder):
        if file.endswith('.conf.dist'):
            dist_files.append(file)
    return sorted(dist_files)

def prompt_module_selection(dist_files):
    print("Found the following modules:")
    for idx, fname in enumerate(dist_files, 1):
        print(f"  {idx}. {fname}")
    print("\nOptions:")
    print("  A: Update all modules")
    print("  B: Select modules individually")
    choice = input("Select an option (A/B): ").strip().lower()
    selected = []
    if choice == "a":
        selected = dist_files
    elif choice == "b":
        nums = input("Enter numbers of modules to update (comma-separated): ").strip()
        indices = [int(x)-1 for x in nums.split(",") if x.strip().isdigit() and 0 < int(x) <= len(dist_files)]
        selected = [dist_files[i] for i in indices]
    else:
        print("Invalid selection, exiting.")
    return selected

def backup_file(filepath):
    bakpath = filepath + ".bak"
    shutil.copy2(filepath, bakpath)
    print(f"  Backup created: {bakpath}")

def parse_conf(filepath):
    # Returns a dict of key: (line, [preceding_comments])
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()
    conf = {}
    comments = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            comments.append(line)
            continue
        if "=" in stripped:
            key = stripped.split("=")[0].strip()
            conf[key] = (line, comments.copy())
            comments.clear()
    return conf

def find_missing_keys(dist_conf, user_conf):
    missing = {}
    for key, (line, comments) in dist_conf.items():
        if key not in user_conf:
            missing[key] = (line, comments)
    return missing

def update_conf(dist_path, conf_path):
    if not os.path.exists(conf_path):
        print(f"  User config {conf_path} does not exist, skipping.")
        return
    backup_file(conf_path)
    dist_conf = parse_conf(dist_path)
    user_conf = parse_conf(conf_path)
    missing = find_missing_keys(dist_conf, user_conf)
    if not missing:
        print("  No new config options to add.")
        return
    
    with open(conf_path, "a", encoding="utf-8") as f:
        for key, (line, comments) in missing.items():
            print("\n" + "".join(comments if comments else []) + line, end="")
            add = input(f"  Add {key} to config? (Y/n): ").strip().lower()
            if add in ("", "y", "yes"):
                if comments:
                    f.writelines(comments)
                f.write(line)
                print(f"    Added {key}.")
            else:
                print(f"    Skipped {key}.")

def main(modules_dir):
    dist_files = find_modules(modules_dir)
    if not dist_files:
        print("No .conf.dist files found in the specified folder.")
        return
    selected = prompt_module_selection(dist_files)
    if not selected:
        print("No modules selected. Exiting.")
        return
    for dist_fname in selected:
        module = dist_fname[:-5]  # Removes ".dist"
        conf_fname = module  # e.g., mod_x.conf
        dist_path = os.path.join(modules_dir, dist_fname)
        conf_path = os.path.join(modules_dir, conf_fname)
        print(f"\nProcessing {conf_fname} ...")
        update_conf(dist_path, conf_path)

if __name__ == "__main__":
    print("AzerothCore Module Config Updater")
    print("---------------------------------")
    folder = input("Enter the path to your modules folder (default: .): ").strip()
    if not folder:
        folder = "."
    if not os.path.isdir(folder):
        print("Provided path is not a valid directory.")
    else:
        main(folder)
