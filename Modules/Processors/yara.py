import subprocess
import requests
import os
from zipfile import ZipFile 
import sys
import codecs
import base64
import re
import json

def setup():
    pass

def generate_base64_permutations(input_string: str):
    encoded_variants = set()
    first_char_encoded = base64.b64encode(input_string[0].encode()).decode()[0]
    last_enc_char = base64.b64encode(("xx"+input_string[-1]).encode()).decode()[-1]
    # Try encoding with different alignments (adding leading bytes)
    for prefix_len in range(3):  # 0, 1, or 2 extra bytes before the string
        prefix = "X" * prefix_len  # Dummy prefix to shift encoding
        full_string = prefix + input_string
        
        # Encode in Base64
        encoded = base64.b64encode(full_string.encode()).decode()
        #trim extra leading characters
        encoded = encoded[prefix_len:]
        #trim padding
        encoded = encoded.rstrip("=")
        if not encoded.endswith(last_enc_char):
            encoded = encoded[:-1]

        if not encoded.startswith(first_char_encoded):
            encoded = encoded[1:]
        encoded_variants.add(encoded)
            
    return encoded_variants

def generate_yara_rule(string, rule_name='StringMatcher', output_path=None):
    """
    Generate a YARA rule that matches any of the provided strings.
    
    :param strings: List of strings to search for
    :param rule_name: Name of the YARA rule (default: 'StringMatcher')
    :param output_path: Optional path to save the YARA rule file
    :return: Generated YARA rule as a string
    """
    # Validate input
    if not string:
        raise ValueError("At least one string must be provided")
        
    # Construct YARA rule
    yara_rule = f"""rule {rule_name} {{
    meta:
        description = "Matches files containing {string} in various encodings (normal, ROT13, Base64(diferent permtations))"
        author = "Generated Script"
    
    strings:
        $normal = "{string}" ascii wide nocase
        $rot13 = "{codecs.encode(string, 'rot13')}" ascii wide nocase
{chr(10).join(f'        $b64_{i} = "{s}" ascii wide' for i, s in enumerate(generate_base64_permutations(string)))}
    
    condition:
        any of them
}}"""
    
    # Optionally write to file
    if output_path:
        with open(output_path, 'w') as f:
            f.write(yara_rule)
    
    return yara_rule

def generate_combined_yara_rule(strings,output_path=None):
    output=""
    
    for string in strings:
        name="StringMatcher_"+string.replace(" ","_")
        #replace any simbols that are not allowed in yara rule names with a regex
        name=re.sub(r"[^a-zA-Z0-9_]","_",name)
        output+=generate_yara_rule(string,rule_name=name)+"\n\n"

        # Optionally write to file
        if output_path:
            with open(output_path, 'w') as f:
                f.write(output)
    return output


def execute(config):
    setup()
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\yara_suspicious_tools.csv"):
        return()
    if not os.path.isfile("./Modules/tools/suspicious_tools.txt"):
        print("suspicious_tools.txt not found")
        return()
    generate_combined_yara_rule(open("./Modules/tools/suspicious_tools.txt").read().split("\n"),"./Modules/tools/yara/yara_rule.yar")
    extract_path=config["drive_path"]
    process = subprocess.Popen([r".\\Modules\\tools\\yara\\yr.exe", "scan",r"./Modules/tools/yara/yara_rule.yar",r"D:\Evidencies\testing\Test\SRVDC1_kape_2024-10-02T094353","-r","-o","json","-m","-w","--disable-console-logs"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    stdout, stderr = process.communicate()
    if stderr:
        raise(stderr)
    json_res=json.loads(stdout)
    out="rule,file,description\n"
    for match in json_res["matches"]:
        split_path=match["file"].split("\\")
        if split_path[-1] in ["$MFT","$J","$LogFile"]:
            continue
        if split_path[-1].endswith("CopyLog.csv"):
            continue
        if split_path[-2] in ["CSVs","JSONs","TXTs"]:
            continue
        if split_path[-2] in ["C","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"] and split_path[-1].split(".")[-1] in ["db","xlsx"]:
            continue
        out+=match["rule"]+","+match["file"]+",\""+match["meta"]["description"]+"\"\n"

    with open(extract_path+"\\JSONs\\yara.json", 'w') as f:
        json.dump(json_res, f, indent=4)
    with open(extract_path+"\\CSVs\\yara.csv", 'w') as f:
        f.write(out)

def get_dependencies():
    return([])

def get_outputs():
    return([("yara.csv","yara")])

def get_type():
    return("machine_module")

def get_name():
    return("yara")

def get_machine_type():
    return(["windows","linux","uac_linux","windows_live_response"])

def get_description():
    return("Executes the yara tool to search for known malicious strings")