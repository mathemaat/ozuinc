import xml.dom.minidom
import xml.etree.ElementTree as ET

from datetime import datetime

from classes.Iban import Iban


class OZUIncasso(object):

    NAME = 'Schaakclub Oud Zuylen Utrecht'
    IBAN = Iban.parse_from_string('NL54INGB0003517238')
    CREDITOR_ID = 'NL29ZZZ404791530000'

    XML_TMP_FILE = 'tmp.xml'

    def __init__(self, members):
        self.members = members

    @staticmethod
    def get_season():
        now = datetime.now()
        # assume the new season starts in September
        if now.month <= 8:
            return now.year - 1, now.year
        else:
            return now.year, now.year + 1

    def generate_incasso(self, timestamp):
        # create the document element
        document = ET.Element('Document')
        document.attrib['xmlns'] = 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.02'
        # create the element that will contain the incasso data
        cstmrDrctDbtInitn = ET.SubElement(document, 'CstmrDrctDbtInitn')
        # insert the header
        self.xml_insert_header(cstmrDrctDbtInitn, timestamp)
        # initialise payment information, including payment details and transactions
        pmtInf = ET.SubElement(cstmrDrctDbtInitn, 'PmtInf')
        self.xml_insert_payment_details(pmtInf, timestamp)
        self.xml_insert_transactions(pmtInf, timestamp)
        # create the xml-document itself
        tree = ET.ElementTree(document)
        tree.write(self.XML_TMP_FILE, encoding='utf-8', xml_declaration=True)
        # pretty print the xml data
        xmldata = xml.dom.minidom.parse(self.XML_TMP_FILE)
        xmldata = xmldata.toprettyxml()
        xmldata = xmldata.replace('\t', '  ')
        # recreate the xml-document
        file = open(self.XML_TMP_FILE, 'w')
        file.write(xmldata)
        file.close()

    def xml_insert_header(self, element, timestamp):
        grpHdr = ET.SubElement(element, 'GrpHdr')
        # add message id
        msgId = ET.SubElement(grpHdr, 'MsgId')
        msgId.text = timestamp.strftime('%Y%m%d')
        # add time
        creDtTm = ET.SubElement(grpHdr, 'CreDtTm')
        creDtTm.text = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        # add number of transactions
        nbOfTxs = ET.SubElement(grpHdr, 'NbOfTxs')
        nbOfTxs.text = str(self.get_transaction_count())
        # add total sum
        ctrlSum = ET.SubElement(grpHdr, 'CtrlSum')
        ctrlSum.text = '{0:.2f}'.format(self.get_total_sum())
        # add club name
        InitgPty = ET.SubElement(grpHdr, 'InitgPty')
        Nm = ET.SubElement(InitgPty, 'Nm')
        Nm.text = self.NAME

    def xml_insert_payment_details(self, pmtInf, timestamp):
        # add id
        pmtInfId = ET.SubElement(pmtInf, 'PmtInfId')
        pmtInfId.text = timestamp.strftime('%Y%m%d')
        # add payment method
        PmtMtd = ET.SubElement(pmtInf, 'PmtMtd')
        PmtMtd.text = 'DD'
        # add number of transactions
        nbOfTxs = ET.SubElement(pmtInf, 'NbOfTxs')
        nbOfTxs.text = str(self.get_transaction_count())
        # add total sum
        ctrlSum = ET.SubElement(pmtInf, 'CtrlSum')
        ctrlSum.text = '{0:.2f}'.format(self.get_total_sum())
        # add SEPA keywords
        PmtTpInf = ET.SubElement(pmtInf, 'PmtTpInf')
        SvcLvl = ET.SubElement(PmtTpInf, 'SvcLvl')
        Cd = ET.SubElement(SvcLvl, 'Cd')
        Cd.text = 'SEPA'
        LclInstrm = ET.SubElement(PmtTpInf, 'LclInstrm')
        Cd = ET.SubElement(LclInstrm, 'Cd')
        Cd.text = 'CORE'
        SeqTp = ET.SubElement(PmtTpInf, 'SeqTp')
        SeqTp.text = 'FRST'
        # add incasso date
        ReqdColltnDt = ET.SubElement(pmtInf, 'ReqdColltnDt')
        ReqdColltnDt.text = timestamp.strftime('%Y-%m-%d')
        # add creditor name
        Cdtr = ET.SubElement(pmtInf, 'Cdtr')
        Nm = ET.SubElement(Cdtr, 'Nm')
        Nm.text = 'Schaakclub Oud Zuylen Utrecht'
        # add account number
        CdtrAcct = ET.SubElement(pmtInf, 'CdtrAcct')
        Id = ET.SubElement(CdtrAcct, 'Id')
        IBAN = ET.SubElement(Id, 'IBAN')
        IBAN.text = self.IBAN.value
        # add BIC code
        CdtrAgt = ET.SubElement(pmtInf, 'CdtrAgt')
        FinInstnId = ET.SubElement(CdtrAgt, 'FinInstnId')
        BIC = ET.SubElement(FinInstnId, 'BIC')
        BIC.text = self.IBAN.get_bic_code()
        # add SEPA keywords
        ChrgBr = ET.SubElement(pmtInf, 'ChrgBr')
        ChrgBr.text = 'SLEV'
        # add creditor details, such as name and id
        CdtrSchmeId = ET.SubElement(pmtInf, 'CdtrSchmeId')
        Nm = ET.SubElement(CdtrSchmeId, 'Nm')
        Nm.text = self.NAME
        Id = ET.SubElement(CdtrSchmeId, 'Id')
        PrvtId = ET.SubElement(Id, 'PrvtId')
        Othr = ET.SubElement(PrvtId, 'Othr')
        Id = ET.SubElement(Othr, 'Id')
        Id.text = self.CREDITOR_ID
        SchmeNm = ET.SubElement(Othr, 'SchmeNm')
        Prtry = ET.SubElement(SchmeNm, 'Prtry')
        Prtry.text = 'SEPA'

    def xml_insert_transactions(self, element, timestamp):
        start, end = OZUIncasso.get_season()
        for member in self.members:
            member.xml_insert_transaction(element, timestamp, start, end)

    def get_transaction_count(self):
        return len(self.members)

    def get_total_sum(self):
        return sum([member.contributiebedrag for member in self.members])
