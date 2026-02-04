#!/usr/bin/env python3
"""
Activate WordPress plugin using WP-CLI
Usage: activate_plugin.py <container-name> <plugin-path>
"""

import sys
import subprocess
import os

def activate_plugin(container_name, plugin_path):
    """Activate WordPress plugin using WP-CLI in container"""

    print(f"Activating plugin: {plugin_path}")

    # Set up Docker environment
    docker_host = f"unix://{os.path.expanduser('~')}/.onion.press/colima/default/docker.sock"
    docker_config = f"{os.path.expanduser('~')}/.onion.press/docker-config"

    env = os.environ.copy()
    env['DOCKER_HOST'] = docker_host
    env['DOCKER_CONFIG'] = docker_config

    # Get docker binary path
    docker_bin = "/Applications/Onion.Press.app/Contents/Resources/bin/docker"
    if not os.path.exists(docker_bin):
        docker_bin = "docker"  # Fallback to system docker

    try:
        # Check if WordPress is configured (has database connection)
        check_cmd = [
            docker_bin, "exec", "-T", container_name,
            "wp", "core", "is-installed",
            "--allow-root"
        ]

        result = subprocess.run(
            check_cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print("WordPress not yet configured, plugin will activate after setup")
            return False

        # Activate the plugin
        activate_cmd = [
            docker_bin, "exec", "-T", container_name,
            "wp", "plugin", "activate", plugin_path,
            "--allow-root"
        ]

        result = subprocess.run(
            activate_cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"✓ Plugin activated: {plugin_path}")
            if result.stdout:
                print(result.stdout.strip())
            return True
        else:
            print(f"Failed to activate plugin: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("Error: Command timed out")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: activate_plugin.py <container-name> <plugin-path>")
        sys.exit(1)

    container_name = sys.argv[1]
    plugin_path = sys.argv[2]

    success = activate_plugin(container_name, plugin_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
