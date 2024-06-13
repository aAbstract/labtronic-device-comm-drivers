#!/bin/bash

alias bbld='python ./scripts/build.py elf_dbg'
alias lbld='python ./scripts/build.py driver_so'
alias qrn='python ./scripts/build.py elf_dbg && build/main && rm build/main'
