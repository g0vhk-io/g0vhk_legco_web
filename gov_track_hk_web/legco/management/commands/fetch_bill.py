import requests
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from legco.models import Bill,  BillCommittee, BillThirdReading, BillFirstReading, BillSecondReading
from lxml import etree
from datetime import *
from dateutil.parser import *
import md5


url = "http://app.legco.gov.hk/BillsDB/odata/Vbills?$format=json&$inlinecount=allpages&$filter=year(bill_gazette_date)%20ge%202010"


def parse_datetime(s):
    if s == '' or s is None:
        return datetime.min
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')

class Command(BaseCommand):
    help ='Fetch Bills'

    def add_arguments(self, parser):
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        r = requests.get(url)
        r.encoding = "utf-8"
        output = r.json()
        bill_dicts = output["value"]
        for bill_dict in bill_dicts:
            for k in bill_dict.keys():
                bill_dict[k] = (bill_dict[k] or "").strip()
            bill, created = Bill.objects.prefetch_related('first_reading').get_or_create(internal_key = bill_dict['internal_key'])
            bill.internal_key = bill_dict['internal_key']
            bill.ordinance_title_en  = bill_dict['ordinance_title_eng']
            bill.ordinance_title_ch  = bill_dict['ordinance_title_chi']
            bill.ordinance_content_url_en  = bill_dict['ordinance_content_url_eng']
            bill.ordinance_content_url_ch  = bill_dict['ordinance_content_url_chi']
            bill.bill_title_en  = bill_dict['bill_title_eng']
            bill.bill_title_ch  = bill_dict['bill_title_chi']
            bill.proposed_by_en  = bill_dict['proposed_by_eng']
            bill.proposed_by_ch  = bill_dict['proposed_by_chi']
            bill.bill_gazette_date  = parse_datetime(bill_dict['bill_gazette_date'])
            bill.bill_content_url_en  = bill_dict['bill_content_url_eng']
            bill.bill_content_url_ch   = bill_dict['bill_content_url_chi']
            bill.bill_gazette_date_2  = parse_datetime(bill_dict['bill_gazette_date_2'])
            bill.bill_content_url_2_en  = bill_dict['bill_content_url_2_eng']
            bill.bill_content_url_2_ch  = bill_dict['bill_content_url_2_chi']
            bill.bill_gazette_date_3  = parse_datetime(bill_dict['bill_gazette_date_3'])
            bill.bill_content_url_3_en  = bill_dict['bill_content_url_3_eng']
            bill.bill_content_url_3_ch  = bill_dict['bill_content_url_3_chi']
            bill.ordinance_gazette_date  = parse_datetime(bill_dict['ordinance_gazette_date'])
            bill.ordinance_year_number_en  = bill_dict['ordinance_year_number_eng']
            bill.ordinance_year_number_ch  = bill_dict['ordinance_year_number_chi']
            bill.ordinace_gazette_content_url_en  = bill_dict['ordinace_gazette_content_url_eng']
            bill.ordinance_gazette_content_url_ch  = bill_dict['ordinance_gazette_content_url_chi']
            bill.legco_brief_file_reference  = bill_dict['legco_brief_file_reference']
            bill.legco_brief_url_en  = bill_dict['legco_brief_url_eng']
            bill.legco_brief_url_ch  = bill_dict['legco_brief_url_chi']
            bill.additional_information_en  = bill_dict['additional_information_eng']
            bill.additional_information_ch  = bill_dict['additional_information_chi']
            bill.remarks_en  = bill_dict['remarks_eng']
            bill.remarks_ch  = bill_dict['remarks_chi']

            first_reading = bill.first_reading
            if first_reading is None:
                first_reading = BillFirstReading()
            first_reading.first_reading_date = parse_datetime(bill_dict['first_reading_date'])
            first_reading.first_reading_date_hansard_url_en = bill_dict['first_reading_date_hansard_url_eng']
            first_reading.first_reading_date_hansard_url_ch = bill_dict['first_reading_date_hansard_url_chi']
            first_reading.first_reading_date_2 = parse_datetime(bill_dict['first_reading_date_2'])
            first_reading.first_reading_date_2_hansard_url_en  = bill_dict['first_reading_date_2_hansard_url_eng']
            first_reading.first_reading_date_2_hansard_url_ch = bill_dict['first_reading_date_2_hansard_url_chi']
            first_reading.save()
            bill.first_reading = first_reading

            second_reading = bill.second_reading
            if second_reading is None:
                second_reading = BillSecondReading()

            second_reading.second_reading_date = parse_datetime(bill_dict['second_reading_date'])
            second_reading.second_reading_date_hansard_url_en  = bill_dict['second_reading_date_hansard_url_eng']
            second_reading.second_reading_date_hansard_url_ch = bill_dict['second_reading_date_hansard_url_chi']
            second_reading.second_reading_date_2 = parse_datetime(bill_dict['second_reading_date_2'])
            second_reading.second_reading_date_2_hansard_url_en = bill_dict['second_reading_date_2_hansard_url_eng']
            second_reading.second_reading_date_2_hansard_url_ch = bill_dict['second_reading_date_2_hansard_url_chi']
            second_reading.second_reading_date_3 = parse_datetime(bill_dict['second_reading_date_3'])
            second_reading.second_reading_date_3_hansard_url_en = bill_dict['second_reading_date_3_hansard_url_eng']
            second_reading.second_reading_date_3_hansard_url_ch = bill_dict['second_reading_date_3_hansard_url_chi']
            second_reading.second_reading_date_4 = parse_datetime(bill_dict['second_reading_date_4'])
            second_reading.second_reading_date_4_hansard_url_en = bill_dict['second_reading_date_4_hansard_url_eng']
            second_reading.second_reading_date_4_hansard_url_ch = bill_dict['second_reading_date_4_hansard_url_chi']
            second_reading.second_reading_date_5 = parse_datetime(bill_dict['second_reading_date_5'])
            second_reading.second_reading_date_5_hansard_url_en = bill_dict['second_reading_date_5_hansard_url_eng']
            second_reading.second_reading_date_5_hansard_url_ch = bill_dict['second_reading_date_5_hansard_url_chi']
            second_reading.save()

            bill.second_reading = second_reading

            third_reading = bill.third_reading
            if third_reading is None:
                third_reading = BillThirdReading()

            third_reading.third_reading_date = parse_datetime(bill_dict['third_reading_date'])
            third_reading.third_reading_date_hansard_url_en = bill_dict['third_reading_date_hansard_url_eng']
            third_reading.third_reading_date_hansard_url_chi = bill_dict['third_reading_date_hansard_url_chi']

            third_reading.save()
            bill.third_reading = third_reading

            committee = bill.committee
            if committee is None:
                committee = BillCommittee()

            committee.bills_committee_title_en = bill_dict['bills_committee_title_eng']
            committee.bills_committee_title_ch = bill_dict['bills_committee_title_chi']
            committee.bills_committee_url_en = bill_dict['bills_committee_url_eng']
            committee.bills_committee_url_ch = bill_dict['bills_committee_url_chi']
            committee.bills_committee_formation_date = parse_datetime(bill_dict['bills_committee_formation_date'])
            committee.bills_committee_report_url_en = bill_dict['bills_committee_report_url_eng']
            committee.bills_committee_report_url_ch = bill_dict['bills_committee_report_url_chi']
            committee.save()
            bill.committee = committee
            bill.save()
