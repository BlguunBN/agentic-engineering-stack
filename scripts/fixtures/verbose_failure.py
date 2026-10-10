"""Deterministic failing output fixture for compression-preservation checks."""

import sys

for index in range(30):
    print(f"diagnostic line {index:02d}: setup detail retained for reproduction")
print("Traceback (most recent call last):")
print("  File 'fixture.py', line 30, in run")
print("AssertionError: deliberate regression sample")
sys.exit(1)
