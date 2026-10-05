"""Provide the `python -m btx_lib_list` entry point.

Runs `btx_lib_list.cli.main`, the function the console scripts run, so exit
codes and traceback handling are identical however the CLI is started.
"""

from __future__ import annotations

from . import cli

if __name__ == "__main__":
    raise SystemExit(cli.main())
