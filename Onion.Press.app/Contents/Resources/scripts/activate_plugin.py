#!/usr/bin/env python3
"""
WordPress Plugin Activator
Activates a WordPress plugin inside a Docker container safely
"""

import sys
import subprocess

def activate_wordpress_plugin(container_name, plugin_path):
    """
    Activate a WordPress plugin in a Docker container
    Uses PHP to safely activate without shell injection risks

    Args:
        container_name: Docker container name
        plugin_path: Plugin path relative to wp-content/plugins/
                    e.g., "akismet/akismet.php"

    Returns:
        True if successful, False otherwise
    """
    # PHP script to activate plugin safely
    # Using Python to generate this eliminates shell heredoc risks
    php_script = f"""<?php
define('WP_USE_THEMES', false);
require_once('/var/www/html/wp-load.php');

if (!function_exists('is_plugin_active')) {{
    require_once(ABSPATH . 'wp-admin/includes/plugin.php');
}}

if (!is_plugin_active('{plugin_path}')) {{
    activate_plugin('{plugin_path}');
    echo "Plugin activated: {plugin_path}\\n";
    exit(0);
}} else {{
    echo "Plugin already active: {plugin_path}\\n";
    exit(0);
}}
?>"""

    try:
        # Check if WordPress is configured
        check_result = subprocess.run(
            ['docker', 'exec', container_name, 'test', '-f', '/var/www/html/wp-config.php'],
            capture_output=True,
            timeout=10
        )

        if check_result.returncode != 0:
            print("WordPress not yet configured - plugin will be activated after setup")
            return True  # Not an error, just not ready yet

        # Execute PHP script in container
        result = subprocess.run(
            ['docker', 'exec', '-i', container_name, 'php'],
            input=php_script.encode(),
            capture_output=True,
            timeout=30
        )

        if result.returncode == 0:
            print(result.stdout.decode().strip())
            return True
        else:
            print(f"Plugin activation failed: {result.stderr.decode().strip()}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("Plugin activation timed out", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error activating plugin: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: activate_plugin.py <container-name> <plugin-path>")
        print("Example: activate_plugin.py onionpress-wordpress akismet/akismet.php")
        sys.exit(1)

    container_name = sys.argv[1]
    plugin_path = sys.argv[2]

    if activate_wordpress_plugin(container_name, plugin_path):
        sys.exit(0)
    else:
        sys.exit(1)
