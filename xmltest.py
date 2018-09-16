import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET

document = ET.Element('Document')
document.attrib['xmlns'] = 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.02'
cstmrDrctDbtInitn = ET.SubElement(document, 'CstmrDrctDbtInitn')

# group header
grpHdr = ET.SubElement(cstmrDrctDbtInitn, 'GrpHdr')

msgId = ET.SubElement(grpHdr, 'MsgId')
msgId.text = '20171019'
creDtTm = ET.SubElement(grpHdr, 'CreDtTm')
creDtTm.text = '2017-10-19T18:31:19'
nbOfTxs = ET.SubElement(grpHdr, 'NbOfTxs')
nbOfTxs.text = '22'
ctrlSum = ET.SubElement(grpHdr, 'CtrlSum')
ctrlSum.text = '1961.00'
InitgPty = ET.SubElement(grpHdr, 'InitgPty')
Nm = ET.SubElement(InitgPty, 'Nm')
Nm.text = 'Schaakclub Oud Zuylen Utrecht'

# payment information
pmtInf = ET.SubElement(cstmrDrctDbtInitn, 'PmtInf')

pmtInfId = ET.SubElement(pmtInf, 'PmtInfId')
pmtInfId.text = '20171019'
PmtMtd = ET.SubElement(pmtInf, 'PmtMtd')
PmtMtd.text = 'DD'
nbOfTxs = ET.SubElement(pmtInf, 'NbOfTxs')
nbOfTxs.text = '22'
ctrlSum = ET.SubElement(pmtInf, 'CtrlSum')
ctrlSum.text = '1961.00'
PmtTpInf = ET.SubElement(pmtInf, 'PmtTpInf')
SvcLvl = ET.SubElement(PmtTpInf, 'SvcLvl')
Cd = ET.SubElement(SvcLvl, 'Cd')
Cd.text = 'SEPA'
LclInstrm = ET.SubElement(PmtTpInf, 'LclInstrm')
Cd = ET.SubElement(LclInstrm, 'Cd')
Cd.text = 'CORE'
SeqTp = ET.SubElement(PmtTpInf, 'SeqTp')
SeqTp.text = 'FRST'
ReqdColltnDt = ET.SubElement(pmtInf, 'ReqdColltnDt')
ReqdColltnDt.text = '2017-10-19'
Cdtr = ET.SubElement(pmtInf, 'Cdtr')
Nm = ET.SubElement(Cdtr, 'Nm')
Nm.text = 'Schaakclub Oud Zuylen Utrecht'
CdtrAcct = ET.SubElement(pmtInf, 'CdtrAcct')
Id = ET.SubElement(CdtrAcct, 'Id')
IBAN = ET.SubElement(Id, 'IBAN')
IBAN.text = 'NL54INGB0003517238'
CdtrAgt = ET.SubElement(pmtInf, 'CdtrAgt')
FinInstnId = ET.SubElement(CdtrAgt, 'FinInstnId')
BIC = ET.SubElement(FinInstnId, 'BIC')
BIC.text = 'INGBNL2A'
ChrgBr = ET.SubElement(pmtInf, 'ChrgBr')
ChrgBr.text = 'SLEV'
CdtrSchmeId = ET.SubElement(pmtInf, 'CdtrSchmeId')
Nm = ET.SubElement(CdtrSchmeId, 'Nm')
Nm.text = 'Schaakclub Oud Zuylen Utrecht'
Id = ET.SubElement(CdtrSchmeId, 'Id')
PrvtId = ET.SubElement(Id, 'PrvtId')
Othr = ET.SubElement(PrvtId, 'Othr')
Id = ET.SubElement(Othr, 'Id')
Id.text = 'NL29ZZZ404791530000'
SchmeNm = ET.SubElement(Othr, 'SchmeNm')
Prtry = ET.SubElement(SchmeNm, 'Prtry')
Prtry.text = 'SEPA'

tree = ET.ElementTree(document)
tree.write('test.xml', encoding='utf-8', xml_declaration=True)

xml = xml.dom.minidom.parse('test.xml')
xml = xml.toprettyxml()
xml = xml.replace('\t', '  ')

file = open('test.xml', 'w')
file.write(xml)
file.close()
