# Chess TCN Python

## Overview
**Chess TCN Python** is a Python package that provides functionality to encode and decode TCN, a move format used by **Chess.com**. This package is ideal for developers looking to work with TCN in Python applications.

## What is TCN?
TCN is a format used by **Chess.com** to transmit move lists in its JSON API. A typical endpoint for retrieving a game’s move list is:
```
https://www.chess.com/callback/live/game/{gameId}
```
This endpoint returns a `moveList` field containing a TCN string.

## Features
- Decode TCN strings into PGN (Portable Game Notation).
- Encode PGN back into TCN format.

## Installation
To install the package, use `pip`:
```bash
pip install chess-tcn
```

## Usage
Here’s a quick example of how to use the package:

```python
from chess_tcn import decode_tcn, encode_tcn, tcn_to_pgn, pgn_to_tcn

# Example TCN string (e.g. from Chess.com live‐game API)
tcn_string = "mC0Kgv7Tbq5Qlt9IqHT7cM1TMFWOHs2MFwZRfm6Eeg"

# Decode TCN to a list of move dicts
moves = decode_tcn(tcn_string)
print("Decoded moves (dicts):", moves)

# Re-encode that move list back into a TCN string
reencoded_tcn = encode_tcn(moves)
print("Re-encoded TCN string:", reencoded_tcn)

# Convert the TCN string directly to a PGN move-text string
pgn_text = tcn_to_pgn(tcn_string)
print("PGN move-text:", pgn_text)

# Convert a PGN move-text string back into TCN
roundtrip_tcn = pgn_to_tcn(pgn_text)
print("TCN from PGN:", roundtrip_tcn)
```

## API Reference
For complete details on usage, check out the [documentation](https://chess-tcn.github.io/docs).

## License
This project is licensed under the MIT License. See below for full text.
```
MIT License

Copyright (c) 2021-2025 chess-tcn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
