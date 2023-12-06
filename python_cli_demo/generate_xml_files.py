#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn



import os
if __name__ == "__main__":

    xml_file="SSML.xml"
    xml_list= []
    with open(xml_file,'r')as f:
        for i, line in enumerate(f):
            xml_list.append(line)
    ## content
    #input="./en_zh.txt"
    #input_dir="input_dir"

    ## prompt
    input="./prompt.txt"
    input_dir="input_dir_prompt"
    os.makedirs(f"{input_dir}",exist_ok=True)
    with open(input,'r')as f:
        for line in f:
            name = line.strip()
            with open(f"{input_dir}/{name}.xml",'w')as fw:
                 top=" ".join(xml_list[:3])
                 tail =' '.join(xml_list[-3:])
                 fw.write(f"{top} {name}\n{tail}")

