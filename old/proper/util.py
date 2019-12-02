#-*- coding: utf-8 -*-
import datetime
import os.path
from xml.etree import ElementTree

def generateTimeBaseFileName(orginal_file_name):
    nowMicrotime = datetime.datetime.now()
    newFileNameExcludeExtension = nowMicrotime.strftime('%Y%m%d%H%M%S%f')
    
    orgFileNameInfo = os.path.splitext(orginal_file_name)
    
    return str(newFileNameExcludeExtension) + orgFileNameInfo[1]

def parsePCInfoXML(xml):
    tree = ElementTree.parse(xml)
    root = tree.getroot()

    # 스캔타임
    scan_time = root.find("./COMPUTER/ScanTime").text

    # 동작중인 OS
    os = root.find("./COMPUTER/Property[Entry='Operating System']/Description").text

    # 서비스팩(윈도우에 한해서) - IE10 설치는 반드시 Windows 7 Service Pack 1이 설치되어 있어야 한다.
    # 이 정보는 None 값을 가질 수 있다.
    service_pack = root.find("./COMPUTER/Property[Entry='Service Pack']/Description")
    if service_pack:
        service_pack = service_pack.text
    else:
        service_pack = ""

    # USB 지원버전
    usb_support_ver = root.find("./COMPUTER/SubNodes/MOBO/Property[Entry='USB Version Supported']/Description").text

    # 시스템 제조사
    manufacture = root.find("./COMPUTER/SubNodes/MOBO/SubNode/SubNode/Property[Entry='System Manufacturer']/Description").text

    # 제품이름
    product_name = root.find("./COMPUTER/SubNodes/MOBO/SubNode/SubNode/Property[Entry='Product Name']/Description").text

    # 제품번호
    product_serial = root.find("./COMPUTER/SubNodes/MOBO/SubNode/SubNode/Property[Entry='Product Serial Number']/Description").text

    # 프로세서 고유 명칭
    cpu_name = root.find("./COMPUTER/SubNodes/MOBO/SubNode/SubNode/Property[Entry='Processor Version']/Description").text

    # 전체 메모리 크기
    memory_size = root.find("./COMPUTER/SubNodes/MEMORY/Property[Entry='Total Memory Size']/Description").text

    # 비디오 칩셋 이름
    video_chip = root.find("./COMPUTER/SubNodes/VIDEO/SubNode/NodeName").text

    # HDD 명
    hdd_name = root.find("./COMPUTER/SubNodes/DRIVES/SubNode[NodeName='IDE Drives']/SubNode/NodeName").text

    # HDD Serial
    hdd_serial = root.find("./COMPUTER/SubNodes/DRIVES/SubNode[NodeName='IDE Drives']/SubNode/Property[Entry='Drive Serial Number']/Description").text

    # HDD 용량
    hdd_capacity = root.find("./COMPUTER/SubNodes/DRIVES/SubNode[NodeName='IDE Drives']/SubNode/Property[Entry='Drive Capacity']/Description").text

    # Lan Card Mac Address
    mac_addr = root.find("./COMPUTER/SubNodes/NETWORK/SubNode/Property[Entry='MAC Address']/Description").text

    return {
        "scan_time": scan_time,
        "os": os,
        "service_pack": service_pack,
        "usb_support_ver": usb_support_ver,
        "manufacture": manufacture,
        "product_name": product_name,
        "product_serial": product_serial,
        "cpu_name": cpu_name,
        "memory_size": memory_size,
        "video_chip": video_chip,
        "hdd_name": hdd_name,
        "hdd_serial": hdd_serial,
        "hdd_capacity": hdd_capacity,
        "mac_addr": mac_addr
    }

def parseMonitorInfoXML(xml):
    # 6층 김정태 온라인 외주 작업자처럼 모니터는 자기 모니터를 사용하는 경우도 있다.
    # 이는 모니터 정보가 존재하지 않을수도 있다는 거다.

    tree = ElementTree.parse(xml)
    root = tree.getroot()

    # 빈 객체(모니터 정보에 대한) - 모니터는 최대 2대 일 수 있다.
    info = []

    # 모니터 노드가 파일에 있는지 확인한다. 모니터는 최대 2대 일 수 있다.(노트북은 조금 더 예외가 필요하겠지만)
    if root.find("./COMPUTER/SubNodes/MONITOR"):
        monitors = root.findall("./COMPUTER/SubNodes/MONITOR/SubNode")
        for monitor in  monitors:
            monitor_detail = {
                "product_name": monitor.find("./Property[Entry='Monitor Name (Manuf)']/Description").text,
                "make_date": monitor.find("./Property[Entry='Date Of Manufacture']/Description").text,
                "product_serial": monitor.find("./Property[Entry='Serial Number']/Description").text
            }
            info.append(monitor_detail)

    return info

def makeAssetCode(seq):
    return "%s-%d" % ("SCK_ASSET", seq)