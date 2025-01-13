# RPG Maker VX Ace Archive Extractor

This script is a Python port of the [RPG Maker Decrypter](https://github.com/uuksu/RPGMakerDecrypter) project, specifically focusing on extracting contents from RPG Maker VX Ace archive files (*.rgss3a).

## About

The original RPG Maker Decrypter is a C# project that supports multiple RPG Maker versions (XP, VX, VX Ace, MV, MZ). This Python script is a simplified port that focuses solely on extracting RPG Maker VX Ace (*.rgss3a) archives while maintaining the same decryption logic and file handling approach.

## Usage

```bash
python3 rgss3a_extractor.py game.rgss3a
```

The script will:
1. Verify the input file format
2. Display archive statistics (total files, size, file types)
3. Extract all files to the './tmp' directory, maintaining the original directory structure
4. Show extraction progress

## Features

- Extracts all files from RPG Maker VX Ace archives
- Preserves original directory structure
- Shows detailed statistics about archive contents
- Displays real-time extraction progress
- Handles file decryption using the original algorithm

## Requirements

- Python 3.6 or higher
- No additional dependencies required

## License

The MIT License (MIT)

Copyright (c) 2024 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Credits

This script is based on the RPG Maker Decrypter project by [uuksu](https://github.com/uuksu). The original project and its encryption/decryption logic served as the foundation for this Python port.

## Example Output

```
Processing game.rgss3a...

Archive statistics:
Total files: 156
Total size: 24.53 MB

Found file types:
  .rvdata2: 98 files
  .png: 45 files
  .ogg: 12 files
  .txt: 1 files

Extracting files to tmp...
Progress: [156/156] 100.0% - Data/Weapons.rvdata2

Successfully extracted game.rgss3a to ./tmp directory
```
