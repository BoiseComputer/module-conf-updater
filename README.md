# module-conf-updater

A script that adds newly added configuration options after a module update.

## Overview

**module-conf-updater** is a Python script designed to help you keep your configuration files up-to-date when upgrading to new versions of software modules. It automatically detects configuration options that have been introduced in an updated version and ensures they are added to your existing configuration file—without overwriting your custom settings.

This tool is particularly useful for system administrators and developers who regularly update modules and need a reliable way to merge new default options into their custom configuration files.

---

## Features

- **Automatic Detection of New Options**  
  Compares your existing configuration file with the updated module’s default config and identifies any new configuration options.

- **Non-Destructive Updates**  
  Only new or missing options are appended to your config file. Existing user settings remain unchanged.

- **Customizable File Paths**  
  Supports specifying the paths to your current config file and the new version’s default config.

- **Side-by-Side Comparison**  
  Optionally outputs a comparison of the old and new config files for review.

- **Backup Creation**  
  Automatically creates a backup of your original configuration before making changes.

- **Command-Line Interface**  
  Simple to use from the command line with clear arguments and help output.

- **Python 3 Compatible**  
  Written in pure Python and compatible with modern Python versions.

---

## How It Works

1. **Input Files**:  
   You provide the path to your existing configuration file (your current settings) and the updated default configuration file from the new module version.

2. **Comparison**:  
   The script parses both files, comparing section-by-section and option-by-option to find any settings present in the new default that are missing in your configuration.

3. **Update**:  
   Missing options are appended to the relevant sections of your config file, with comments indicating they are newly added.

4. **Backup**:  
   Before making any changes, a backup of your original configuration is created in the same directory.

5. **Output**:  
   The updated configuration file is ready to use, with all new options included and your custom settings preserved.

---

## Usage

```bash
python3 module-conf-updater.py \
  --current path/to/your/config.conf \
  --updated path/to/new/default.conf \
  [--output path/to/updated/config.conf] \
  [--backup] \
  [--diff]
```

**Arguments:**

- `--current` (required): Path to your existing configuration file.
- `--updated` (required): Path to the new version’s default configuration file.
- `--output` (optional): Path to write the updated configuration file. Defaults to overwriting the original.
- `--backup` (optional): Create a backup of your original config before updating.
- `--diff` (optional): Output a diff/summary of changes made.

**Example:**

```bash
python3 module-conf-updater.py --current /etc/myapp/config.conf --updated ./defaults/config.conf --backup --diff
```

---

## Requirements

- Python 3.x

No additional dependencies are required.


Advanced Usage
Customizing Section and Option Handling
Selective Section Updates:
If you want to update only specific sections, you can modify the script to accept a list of target sections. This helps when only a subset of the configuration file is relevant for updates.

Option Value Preservation:
By default, the script preserves your current option values and only inserts missing options from the default config. If you want to force-update specific options to their new defaults, you may adjust the merging logic (see script internals below).

Integration with Automation Tools
Pre/Post Hooks:
Integrate the script into your CI/CD pipeline or as a pre/post-install hook to automate configuration management during deployments or module upgrades.

Batch Processing:
Use shell scripting to run the updater across multiple config pairs in one step:

bash
for dir in $(ls /etc/myapps); do
  python3 module-conf-updater.py --current /etc/myapps/$dir/config.conf --updated ./defaults/config.conf --backup
done
Output Customization
Change Markers:
Newly added options are marked with comments. You can customize the marker string or format by adjusting the script’s comment generation logic if you want to comply with your organization’s standards.

Verbose Logging:
Run the script with a --verbose flag (if implemented) for detailed output about each change applied and every option added.

Script Internals
Configuration File Parsing
ConfigParser:
The script uses Python’s built-in configparser module to read and manipulate .ini-style configuration files.
Each section is handled as a dictionary of key-value pairs.
Comments and the order of entries are preserved where possible.
Comparison Algorithm
Load Both Files:
Reads the current config and the updated default config into separate data structures.
Section Walk:
Iterates through each section in the updated default config.
Option Comparison:
For each section, checks if the section exists in the current config.
If not, the section (with all its options) is added.
If yes, compares each option—if an option is missing, it is appended with a comment.
Preservation:
Existing options and their values remain unchanged.
Backup and Atomic Writes
Backups:
If --backup is specified, the script copies your original configuration file to config.conf.bak before making changes.

Atomic Writes:
The script writes changes to a temporary file and then moves it to the target location to avoid partial writes in case of errors.

Error Handling
Syntax Validation:
The script checks for syntax errors in both the current and new configuration files before proceeding.

Merge Conflicts:
If a section or option cannot be cleanly merged, the script logs the issue and skips the problematic entry, ensuring the rest of the file is still updated.

Extending the Script
Support for Other Formats:
The script is currently tailored for .ini files. To handle YAML, JSON, or XML configs, consider modularizing the parser logic for easy extension.

Unit Testing:
Tests can be added with pytest or similar frameworks. Test cases should cover merging, backup creation, error handling, and edge cases (e.g., duplicate options).
---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

---

## License

This project is licensed under the MIT License.

---

**Note:**  
Please review the script and test on non-production files before use to ensure compatibility with your specific configuration format and workflow.
