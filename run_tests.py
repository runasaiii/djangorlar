#!/usr/bin/env python
"""Script to run tests and display output."""
import os
import sys
import subprocess

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.env.local')

# Run pytest
result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'apps/education/tests/', '-v', '--tb=short'],
    capture_output=False,
    text=True
)

sys.exit(result.returncode)

