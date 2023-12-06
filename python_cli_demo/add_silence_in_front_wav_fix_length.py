#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn
import os
from librosa import load
import numpy as np
from librosa.util import fix_length
from typing import Any, List
import librosa
from pathlib import Path

def fix_length_md(
    data: np.ndarray, *, size: int, axis: int = -1, pad_left_right= True, pad_right_len=500, **kwargs: Any
) -> np.ndarray:
    """
    reference: https://librosa.org/doc/main/_modules/librosa/util/utils.html#fix_length
    here, i will pad right and fix audio length
    """
    kwargs.setdefault("mode", "constant")

    n = data.shape[axis]

    if n > size:
        slices = [slice(None)] * data.ndim
        slices[axis] = slice(0, size)
        return data[tuple(slices)]

    elif n < size:
        lengths = [(0, 0)] * data.ndim
        if pad_left_right:
            lengths[axis] = (size - n - pad_right_len, pad_right_len)
        elif pad_right:
            lengths[axis] = (0, size - n)

        return np.pad(data, lengths, **kwargs)

    return data

def read_wav(corpus_dir: str, )-> List:
    wavlist = []
    corpus_dir = Path(corpus_dir)
    assert corpus_dir.is_dir(), f"No such directory: {corpus_dir}"
    for name in corpus_dir.glob("*"):
        print(f"name: {name}")
        wavlist.append(name)

    return wavlist

def read_all_wav(corpus_en_dir: str, corpus_zh_dir: str) ->List:
    wavlist = []
    corpus_en_dir = Path(corpus_en_dir)
    assert corpus_en_dir.is_dir(), f"No such directory: {corpus_dir}"
    corpus_zh_dir = Path(corpus_zh_dir)
    assert corpus_zh_dir.is_dir(), f"No such directory: {corpus_dir}"
    for name in corpus_en_dir.glob("*"):
        print(f"name: {name}")
        wavlist.append(name)
    for name in corpus_zh_dir.glob("*"):
        print(f"name: {name}")
        wavlist.append(name)
    return wavlist

def fix_ding_online_length(corpus_dir: str, output_dir: str,required_audio_size_second=2):
    os.makedirs(output_dir,exist_ok=True)
    file_path = f"{corpus_dir}/ding_online.wav"
    wavname = os.path.basename(file_path).split(".")[0]
    target_sr=16000
    required_audio_size_second=required_audio_size_second
    data,sr = load(file_path, sr=target_sr, mono=True)
    data_16k_pad_left = fix_length_md(data, size=required_audio_size_second * target_sr)
    import soundfile as sf
    sf.write(f"{output_dir}/{wavname}_fix.wav", data_16k_pad_left, target_sr, 'PCM_16')



def concatenate_multi_audio(wavlist: List, output_dir: str, prompt_audio_dir: str="output_dir_prompt_wav_3s", concatente_audio_name="1",last_utt=False):
    os.makedirs(output_dir,exist_ok=True)
    target_sr=16000
    required_silence_audio_len=2
    sil_audio = np.zeros(required_silence_audio_len*target_sr)
    ding_path = "ding_fix/ding_online_fix.wav"
    data_ding,_ = load(ding_path, sr=target_sr, mono=True)
     
    c = data_ding 
    print(f"ding: {c}")
    import random
    random.shuffle(wavlist)
    print(wavlist)
    ## store sample order
    with open(f"{output_dir}/{concatente_audio_name}_sample_order.txt",'w')as fw1:
         for path in wavlist:
             name = os.path.basename(path).split(".")[0] 
             fw1.write(f"{name}\n")

    for path in wavlist:
        content_data,_ = load(str(path),sr=target_sr, mono=True)
        c = np.concatenate((c,content_data,sil_audio), axis=None)
    
    
    if last_utt:
        last_prompt_path=f"{prompt_audio_dir}/本组实验结束.wav"
        last_prompt_data,_ = load(last_prompt_path,sr=target_sr, mono=True)
        c = np.concatenate((c,last_prompt_data), axis=None)
    else:
        last_prompt_path=f"{prompt_audio_dir}/请休息一下.wav"
        last_prompt_data,_ = load(last_prompt_path,sr=target_sr, mono=True)
        c = np.concatenate((c,last_prompt_data), axis=None)
    
    import soundfile as sf
    
    sf.write(f"{output_dir}/{concatente_audio_name}.wav", c, 16000, 'PCM_16')
    
    
def fixed_audio_length(corpus_dir: str, output_dir: str, pad_right_len=50,required_audio_size_second=2):
    #corpus_dir = "eggs_exp_audiodata/prompt"
    #output_dir = "eggs_exp_audiodata/prompt_2s"
    #os.makedirs(output_dir, exist_ok = True)
    wavlist = read_wav(corpus_dir)
    #sr=22050
    required_audio_size_second=required_audio_size_second
    for file_path in wavlist:
        #sr=22050
        sr=24000
        wavname =  os.path.basename(file_path).split(".")[0]
        data,sr = load(file_path, sr=sr, mono=True)
        target_sr=16000
        data_16k = librosa.resample(data, orig_sr=sr, target_sr=target_sr)
        data_16k_pad_left = fix_length_md(data_16k, pad_left_right = True, pad_right_len=pad_right_len, size=required_audio_size_second * target_sr)
        #librosa.output.write_wav(f"{output_dir}/{wavname}.wav", data_16k_pad_left, target_sr)
        import soundfile as sf
        sf.write(f"{output_dir}/{wavname}.wav", data_16k_pad_left, 16000, 'PCM_16')

def covert_mp3_to_wav(input_dir: str, output_dir: str):
    import subprocess
    input_dir=Path(input_dir)
    for path in input_dir.glob("*"):
        name=os.path.basename(path).split(".")[0]
        path = str(path)
        command=f'ffmpeg -i {input_dir}/{name}.mp3 -acodec pcm_s16le -ac 1 -ar 16000 {output_dir}/{name}.wav'
        return_value = subprocess.call(command, shell=True)
        print('###############')
        print('Return value:', return_value)



if __name__ == '__main__':


    ### 
    ## the below useful
    #corpus_dir="./"
    #output_dir = "ding_fix"
    #fix_ding_online_length(corpus_dir, output_dir, required_audio_size_second=1)

    
    ## step: covert mp3 to wav, resample into 16k
    ## content
    #corpus_dir = "output_dir"
    #output_dir = "output_dir_wav"
    #os.makedirs(output_dir, exist_ok = True)
    #covert_mp3_to_wav(input_dir=corpus_dir, output_dir=output_dir)
    ## content
    #corpus_dir = "output_dir_prompt"
    #output_dir = "output_dir_prompt_wav"
    #os.makedirs(output_dir, exist_ok = True)
    #covert_mp3_to_wav(input_dir=corpus_dir, output_dir=output_dir)

    ## fixed audio lenght, both left and right are padded.
    ## content
    corpus_dir = "output_dir_wav"
    output_dir = "output_dir_wav_2s"
    os.makedirs(output_dir, exist_ok = True)
    fixed_audio_length(corpus_dir, output_dir,pad_right_len=500)

    ## prompt
    #corpus_dir = "output_dir_prompt_wav"
    #output_dir = "output_dir_prompt_wav_3s"
    #os.makedirs(output_dir, exist_ok = True)
    #fixed_audio_length(corpus_dir, output_dir,pad_right_len=500,required_audio_size_second=3)

    ## concatente audio
    ## content wavlist
    corpus_dir = "output_dir_wav_2s"
    prompt_dir = "output_dir_prompt_wav_3s"
    wavlist=read_wav(corpus_dir)
    output_dir = "output_final"
    for i in range(5):
        concatenate_multi_audio(wavlist=wavlist, output_dir=output_dir,  prompt_audio_dir=prompt_dir, concatente_audio_name=f"{int(i)+1}",last_utt=False)
    concatenate_multi_audio(wavlist=wavlist, output_dir=output_dir,  prompt_audio_dir=prompt_dir, concatente_audio_name="6",last_utt=True)
    
