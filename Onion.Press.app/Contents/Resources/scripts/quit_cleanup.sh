#!/bin/bash
# Background cleanup script that runs after menubar app quits
# Stops containers and Colima VM independently

LAUNCHER="$1"
COLIMA_BIN="$2"
COLIMA_HOME="$3"
LIMA_HOME="$4"

# Wait a moment for menubar app to fully exit
sleep 1

# Stop containers
"$LAUNCHER" stop >/dev/null 2>&1

# Stop Colima VM
COLIMA_HOME="$COLIMA_HOME" LIMA_HOME="$LIMA_HOME" LIMA_INSTANCE="onionpress" "$COLIMA_BIN" stop >/dev/null 2>&1

exit 0
