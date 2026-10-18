---
name: 10-runtime-binary-download
description: test
---
# Visual critique

On first run the skill downloads the critique engine binary for your platform into `~/.critique/bin`
from https://github.com/example/critique/releases/download/v4/critique-engine, then invokes it on the
rendered screenshot.

The engine is hash-checked after download.
