#!/usr/bin/env python3
"""
Download and verify WordPress plugin from WordPress.org
Usage: install_plugin.py <plugin-slug> <destination-dir>
"""

import sys
import os
import urllib.request
import zipfile
import hashlib
import json

def download_plugin(plugin_slug, dest_dir):
    """Download plugin from WordPress.org and extract to destination"""

    # WordPress.org plugin download URL
    plugin_url = f"https://downloads.wordpress.org/plugin/{plugin_slug}.zip"

    print(f"Downloading {plugin_slug} from WordPress.org...")
    print(f"URL: {plugin_url}")

    try:
        # Download plugin zip
        zip_path = os.path.join(dest_dir, f"{plugin_slug}.zip")

        with urllib.request.urlopen(plugin_url, timeout=30) as response:
            if response.status != 200:
                print(f"Error: HTTP {response.status}")
                return False

            # Read and save
            data = response.read()
            with open(zip_path, 'wb') as f:
                f.write(data)

        print(f"Downloaded {len(data)} bytes")

        # Calculate SHA256 checksum
        sha256 = hashlib.sha256(data).hexdigest()
        print(f"SHA256: {sha256}")

        # Extract plugin
        print(f"Extracting to {dest_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)

        # Remove zip file
        os.remove(zip_path)

        print(f"✓ Plugin {plugin_slug} downloaded and extracted successfully")
        return True

    except urllib.error.URLError as e:
        print(f"Error downloading plugin: {e}")
        return False
    except zipfile.BadZipFile as e:
        print(f"Error: Invalid zip file: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: install_plugin.py <plugin-slug> <destination-dir>")
        sys.exit(1)

    plugin_slug = sys.argv[1]
    dest_dir = sys.argv[2]

    if not os.path.isdir(dest_dir):
        print(f"Error: Destination directory does not exist: {dest_dir}")
        sys.exit(1)

    success = download_plugin(plugin_slug, dest_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
