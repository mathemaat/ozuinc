import xml.etree.ElementTree as ET


class OZUMember(object):

    DESCRIPTION_FORMAT = 'Contributie {} {}-{}'

    def __init__(self, mandaat_id, datum_handtekening, contributiebedrag, iban, ten_name_van, knsb_nummer, lidmaatschap):
        self.mandaat_id = mandaat_id
        self.datum_handtekening = datum_handtekening
        self.contributiebedrag = contributiebedrag
        self.iban = iban
        self.ten_name_van = ten_name_van
        self.knsb_nummer = knsb_nummer
        self.lidmaatschap = lidmaatschap

    def __repr__(self):
        return 'OZUMember({}, {}, {}, {}, {}, {})'.format(
            self.mandaat_id,
            self.datum_handtekening,
            self.contributie,
            self.iban,
            self.ten_name_van,
            self.knsb_nummer,
            self.lidmaatschap
        )

    def xml_insert_transaction(self, pmtInf, timestamp, season_start, season_end):
        # initialise the container element that represents the payment for a single member
        drctDbtTxInf = ET.SubElement(pmtInf, 'DrctDbtTxInf')
        # add the payment id
        pmtId = ET.SubElement(drctDbtTxInf, 'PmtId')
        endToEndId = ET.SubElement(pmtId, 'EndToEndId')
        endToEndId.text = '{}.{}'.format(timestamp.strftime('%Y%m%d'), self.knsb_nummer)
        # add the contribution amount
        instdAmt = ET.SubElement(drctDbtTxInf, 'InstdAmt')
        instdAmt.attrib['Ccy'] = 'EUR'
        instdAmt.text = '{0:.2f}'.format(self.contributiebedrag)
        # add mandate details
        drctDbtTx = ET.SubElement(drctDbtTxInf, 'DrctDbtTx')
        mndtRltdInf = ET.SubElement(drctDbtTx, 'MndtRltdInf')
        mndtId = ET.SubElement(mndtRltdInf, 'MndtId')
        mndtId.text = str(self.mandaat_id)
        dtOfSgntr = ET.SubElement(mndtRltdInf, 'DtOfSgntr')
        dtOfSgntr.text = self.datum_handtekening.isoformat()
        # add bank details (BIC)
        dbtrAgt = ET.SubElement(drctDbtTxInf, 'DbtrAgt')
        finInstnId = ET.SubElement(dbtrAgt, 'FinInstnId')
        bic = ET.SubElement(finInstnId, 'BIC')
        bic.text = self.iban.get_bic_code()
        # add debtor name
        dbtr = ET.SubElement(drctDbtTxInf, 'Dbtr')
        nm = ET.SubElement(dbtr, 'Nm')
        nm.text = self.ten_name_van
        # add bank details (account number)
        dbtrAcct = ET.SubElement(drctDbtTxInf, 'DbtrAcct')
        id = ET.SubElement(dbtrAcct, 'Id')
        iban = ET.SubElement(id, 'IBAN')
        iban.text = self.iban.value
        # add membership description
        rmtInf = ET.SubElement(drctDbtTxInf, 'RmtInf')
        ustrd = ET.SubElement(rmtInf, 'Ustrd')
        ustrd.text = self.DESCRIPTION_FORMAT.format(self.lidmaatschap.lower(), season_start, season_end)
