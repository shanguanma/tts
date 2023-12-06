#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn
from pathlib import Path
import os
from tts2 import transferMsTTSData, get_SSML
from tts import mainSeq,get_SSML
import asyncio

if __name__=="__main__":
    input_dir="input_dir"
    output_dir="output_dir"
    os.makedirs(output_dir, exist_ok = True)
    input_dir = Path(input_dir)
    for path in input_dir.glob("*"):
        path = str(path)
        print(path)
        name = os.path.basename(path).split(".")[0]
        ssml=get_SSML(path)
        asyncio.get_event_loop().run_until_complete(mainSeq(ssml, f"{output_dir}/{name}"))
        #transferMsTTSData(ssml,f"{output_dir}/{name}")
