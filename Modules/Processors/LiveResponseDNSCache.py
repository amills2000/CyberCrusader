import os
import requests
from zipfile import ZipFile 
import subprocess
import re
import json

DNScodes = {
    "1": {
      "type": "A",
      "code": "1",
      "meaning": "a host address"
    },
    "2": {
      "type": "NS",
      "code": "2",
      "meaning": "an authoritative name server"
    },
    "3": {
      "type": "MD",
      "code": "3",
      "meaning": "a mail destination (OBSOLETE - use MX)"
    },
    "4": {
      "type": "MF",
      "code": "4",
      "meaning": "a mail forwarder (OBSOLETE - use MX)"
    },
    "5": {
      "type": "CNAME",
      "code": "5",
      "meaning": "the canonical name for an alias"
    },
    "6": {
      "type": "SOA",
      "code": "6",
      "meaning": "marks the start of a zone of authority"
    },
    "7": {
      "type": "MB",
      "code": "7",
      "meaning": "a mailbox domain name (EXPERIMENTAL)"
    },
    "8": {
      "type": "MG",
      "code": "8",
      "meaning": "a mail group member (EXPERIMENTAL)"
    },
    "9": {
      "type": "MR",
      "code": "9",
      "meaning": "a mail rename domain name (EXPERIMENTAL)"
    },
    "10": {
      "type": "NULL",
      "code": "10",
      "meaning": "a null RR (EXPERIMENTAL)"
    },
    "11": {
      "type": "WKS",
      "code": "11",
      "meaning": "a well known service description"
    },
    "12": {
      "type": "PTR",
      "code": "12",
      "meaning": "a domain name pointer"
    },
    "13": {
      "type": "HINFO",
      "code": "13",
      "meaning": "host information"
    },
    "14": {
      "type": "MINFO",
      "code": "14",
      "meaning": "mailbox or mail list information"
    },
    "15": {
      "type": "MX",
      "code": "15",
      "meaning": "mail exchange"
    },
    "16": {
      "type": "TXT",
      "code": "16",
      "meaning": "text strings"
    },
    "17": {
      "type": "RP",
      "code": "17",
      "meaning": "for Responsible Person"
    },
    "18": {
      "type": "AFSDB",
      "code": "18",
      "meaning": "for AFS Data Base location"
    },
    "19": {
      "type": "X25",
      "code": "19",
      "meaning": "for X.25 PSDN address"
    },
    "20": {
      "type": "ISDN",
      "code": "20",
      "meaning": "for ISDN address"
    },
    "21": {
      "type": "RT",
      "code": "21",
      "meaning": "for Route Through"
    },
    "22": {
      "type": "NSAP",
      "code": "22",
      "meaning": "for NSAP address, NSAP style A record (DEPRECATED)"
    },
    "23": {
      "type": "NSAP-PTR",
      "code": "23",
      "meaning": "for domain name pointer, NSAP style (DEPRECATED)"
    },
    "24": {
      "type": "SIG",
      "code": "24",
      "meaning": "for security signature"
    },
    "25": {
      "type": "KEY",
      "code": "25",
      "meaning": "for security key"
    },
    "26": {
      "type": "PX",
      "code": "26",
      "meaning": "X.400 mail mapping information"
    },
    "27": {
      "type": "GPOS",
      "code": "27",
      "meaning": "Geographical Position"
    },
    "28": {
      "type": "AAAA",
      "code": "28",
      "meaning": "IP6 Address"
    },
    "29": {
      "type": "LOC",
      "code": "29",
      "meaning": "Location Information"
    },
    "30": {
      "type": "NXT",
      "code": "30",
      "meaning": "Next Domain (OBSOLETE)"
    },
    "31": {
      "type": "EID",
      "code": "31",
      "meaning": "Endpoint Identifier"
    },
    "32": {
      "type": "NIMLOC",
      "code": "32",
      "meaning": "Nimrod Locator"
    },
    "33": {
      "type": "SRV",
      "code": "33",
      "meaning": "Server Selection"
    },
    "34": {
      "type": "ATMA",
      "code": "34",
      "meaning": "ATM Address"
    },
    "35": {
      "type": "NAPTR",
      "code": "35",
      "meaning": "Naming Authority Pointer"
    },
    "36": {
      "type": "KX",
      "code": "36",
      "meaning": "Key Exchanger"
    },
    "37": {
      "type": "CERT",
      "code": "37",
      "meaning": "CERT"
    },
    "38": {
      "type": "A6",
      "code": "38",
      "meaning": "A6 (OBSOLETE - use AAAA)"
    },
    "39": {
      "type": "DNAME",
      "code": "39",
      "meaning": "DNAME"
    },
    "40": {
      "type": "SINK",
      "code": "40",
      "meaning": "SINK"
    },
    "41": {
      "type": "OPT",
      "code": "41",
      "meaning": "OPT"
    },
    "42": {
      "type": "APL",
      "code": "42",
      "meaning": "APL"
    },
    "43": {
      "type": "DS",
      "code": "43",
      "meaning": "Delegation Signer"
    },
    "44": {
      "type": "SSHFP",
      "code": "44",
      "meaning": "SSH Key Fingerprint"
    },
    "45": {
      "type": "IPSECKEY",
      "code": "45",
      "meaning": "IPSECKEY"
    },
    "46": {
      "type": "RRSIG",
      "code": "46",
      "meaning": "RRSIG"
    },
    "47": {
      "type": "NSEC",
      "code": "47",
      "meaning": "NSEC"
    },
    "48": {
      "type": "DNSKEY",
      "code": "48",
      "meaning": "DNSKEY"
    },
    "49": {
      "type": "DHCID",
      "code": "49",
      "meaning": "DHCID"
    },
    "50": {
      "type": "NSEC3",
      "code": "50",
      "meaning": "NSEC3"
    },
    "51": {
      "type": "NSEC3PARAM",
      "code": "51",
      "meaning": "NSEC3PARAM"
    },
    "52": {
      "type": "TLSA",
      "code": "52",
      "meaning": "TLSA"
    },
    "53": {
      "type": "SMIMEA",
      "code": "53",
      "meaning": "S/MIME cert association"
    },
    "54": {
      "type": "Unassigned",
      "code": "54",
      "meaning": ""
    },
    "55": {
      "type": "HIP",
      "code": "55",
      "meaning": "Host Identity Protocol"
    },
    "56": {
      "type": "NINFO",
      "code": "56",
      "meaning": "NINFO"
    },
    "57": {
      "type": "RKEY",
      "code": "57",
      "meaning": "RKEY"
    },
    "58": {
      "type": "TALINK",
      "code": "58",
      "meaning": "Trust Anchor LINK"
    },
    "59": {
      "type": "CDS",
      "code": "59",
      "meaning": "Child DS"
    },
    "60": {
      "type": "CDNSKEY",
      "code": "60",
      "meaning": "DNSKEY(s) the Child wants reflected in DS"
    },
    "61": {
      "type": "OPENPGPKEY",
      "code": "61",
      "meaning": "OpenPGP Key"
    },
    "62": {
      "type": "CSYNC",
      "code": "62",
      "meaning": "Child-To-Parent Synchronization"
    },
    "63": {
      "type": "ZONEMD",
      "code": "63",
      "meaning": "Message Digest Over Zone Data"
    },
    "64": {
      "type": "SVCB",
      "code": "64",
      "meaning": "General-purpose service binding"
    },
    "65": {
      "type": "HTTPS",
      "code": "65",
      "meaning": "SVCB-compatible type for use with HTTP"
    },
    "99": {
      "type": "SPF",
      "code": "99",
      "meaning": ""
    },
    "100": {
      "type": "UINFO",
      "code": "100",
      "meaning": ""
    },
    "101": {
      "type": "UID",
      "code": "101",
      "meaning": ""
    },
    "102": {
      "type": "GID",
      "code": "102",
      "meaning": ""
    },
    "103": {
      "type": "UNSPEC",
      "code": "103",
      "meaning": ""
    },
    "104": {
      "type": "NID",
      "code": "104",
      "meaning": ""
    },
    "105": {
      "type": "L32",
      "code": "105",
      "meaning": ""
    },
    "106": {
      "type": "L64",
      "code": "106",
      "meaning": ""
    },
    "107": {
      "type": "LP",
      "code": "107",
      "meaning": ""
    },
    "108": {
      "type": "EUI48",
      "code": "108",
      "meaning": "an EUI-48 address"
    },
    "109": {
      "type": "EUI64",
      "code": "109",
      "meaning": "an EUI-64 address"
    },
    "249": {
      "type": "TKEY",
      "code": "249",
      "meaning": "Transaction Key"
    },
    "250": {
      "type": "TSIG",
      "code": "250",
      "meaning": "Transaction Signature"
    },
    "251": {
      "type": "IXFR",
      "code": "251",
      "meaning": "incremental transfer"
    },
    "252": {
      "type": "AXFR",
      "code": "252",
      "meaning": "transfer of an entire zone"
    },
    "253": {
      "type": "MAILB",
      "code": "253",
      "meaning": "mailbox-related RRs (MB, MG or MR)"
    },
    "254": {
      "type": "MAILA",
      "code": "254",
      "meaning": "mail agent RRs (OBSOLETE - see MX)"
    },
    "255": {
      "type": "*",
      "code": "255",
      "meaning": "A request for some or all records the server has available"
    },
    "256": {
      "type": "URI",
      "code": "256",
      "meaning": "URI"
    },
    "257": {
      "type": "CAA",
      "code": "257",
      "meaning": "Certification Authority Restriction"
    },
    "258": {
      "type": "AVC",
      "code": "258",
      "meaning": "Application Visibility and Control"
    },
    "259": {
      "type": "DOA",
      "code": "259",
      "meaning": "Digital Object Architecture"
    },
    "260": {
      "type": "AMTRELAY",
      "code": "260",
      "meaning": "Automatic Multicast Tunneling Relay"
    },
    "261": {
      "type": "RESINFO",
      "code": "261",
      "meaning": "Resolver Information as Key/Value Pairs"
    },
    "32768": {
      "type": "TA",
      "code": "32768",
      "meaning": "DNSSEC Trust Authorities"
    },
    "32769": {
      "type": "DLV",
      "code": "32769",
      "meaning": "DNSSEC Lookaside Validation (OBSOLETE)"
    },
    "65535": {
      "type": "Reserved",
      "code": "65535",
      "meaning": ""
    }
  }

lang = {
    "en":{
        "first_line":"Windows IP Configuration"
    },
    "ca":{
        "first_line":"Configuración IP de Windows"
        ""
    },
    "es":{
        "first_line":"Configuración IP de Windows"
    }
}


def execute(config):
    if not os.path.exists(config["DrivePath"]+"\\dns_cache.txt"):
        return()
    if os.path.exists(config["DrivePath"]+"\\CSVs\\dns_cache.csv"):
        return()
    dns_cache=[]
    cache={}
    with open(config["DrivePath"]+"\\dns_cache.txt","r",encoding="utf-16") as f:
        previous_line=""
        reg={}
        while True:
            line=f.readline()
            if not line:
                break
            if len(line.strip())==0:
                continue
            #search for delimiters
            match=None
            match=re.match(r'^\s{4}([-]+)$',line)
            if match:
                if cache!={}:
                    dns_cache.append(cache)
                cache={"domain":previous_line}
            line=line.strip()
            result=re.match(r'^([^\.\r\n]+)[^:\r\n]+: +([^\r\n]+)$',line)
            if not result:
                previous_line=line
                continue
            #search for registry name
            if line.startswith("Nombre de registro"):
                if reg!={}:
                    if not (reg["Sección"] in cache):
                        cache[reg["Sección"]]=[]
                    cache[reg["Sección"]].append(reg)
                    reg={}
                reg[result.group(1).strip()]=result.group(2).strip()
            elif line.startswith("Record Name"):
                if reg!={}:
                    if not (reg["Section"] in cache):
                        cache[reg["Section"]]=[]
                    cache[reg["Section"]].append(reg)
                    reg={}
                reg[result.group(1).strip()]=result.group(2).strip()
            else:
                reg[result.group(1).strip()]=result.group(2).strip()
    #store json
    with open(config["DrivePath"]+"\\JSONs\\dns_cache.json","w",encoding="utf-16") as f:
        f.write(str(dns_cache))
    #store csv only domain and respuesta/response 
    out="domain,regname,regtype,response\n"
    for entry in dns_cache:
        for response in entry["respuesta"]:
            if response["Tipo de registro"] in DNScodes:
                response["Tipo de registro"]=DNScodes[response["Tipo de registro"]]["type"]
            if "Registro CNAME" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro CNAME"]+"\n"
            elif "Registro MX" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro MX"]+"\n"
            elif "Registro NS" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro NS"]+"\n"
            elif "Registro SOA" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro SOA"]+"\n"
            elif "Registro SRV" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro SRV"]+"\n"
            elif "Registro TXT" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro TXT"]+"\n"
            elif "Un registro (host)" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Un registro (host)"]+"\n"
            elif "Registro AAAA" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro AAAA"]+"\n"
            elif "Registro A" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro A"]+"\n"
            elif "Registro PTR" in response:
                out+=entry["domain"]+","+response["Nombre de registro"]+","+response["Tipo de registro"]+","+response["Registro PTR"]+"\n"

    with open(config["DrivePath"]+"\\CSVs\\dns_cache.csv","w",encoding="utf-16") as f:
        f.write(out)
                

            

def get_dependencies():
    return([])

def get_outputs():
    return([])

def get_type():
    return("machine_module")

def get_name():
    return("LiveResponseDNSCache")

def get_machine_type():
    return("windows_live_response")

def get_description():
    return("Parses the DNSCahce file into a CSV file")


if __name__ == "__main__":
    config={"DrivePath":r"test path"}
    execute(config)