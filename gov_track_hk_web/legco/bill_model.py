from django.db import models
from datetime import datetime
from dirtyfields import DirtyFieldsMixin
#

class BillThirdReading(DirtyFieldsMixin, models.Model):
    third_reading_date = models.DateTimeField(auto_now_add=True)
    third_reading_date_hansard_url_en = models.CharField(max_length=512)
    third_reading_date_hansard_url_ch = models.CharField(max_length=512)


class BillFirstReading(DirtyFieldsMixin, models.Model):
    first_reading_date = models.DateTimeField(auto_now_add=True)
    first_reading_date_hansard_url_en = models.CharField(max_length=512)
    first_reading_date_hansard_url_ch = models.CharField(max_length=512)
    first_reading_date_2 = models.DateTimeField(auto_now_add=True)
    first_reading_date_2_hansard_url_en = models.CharField(max_length=512)
    first_reading_date_2_hansard_url_ch = models.CharField(max_length= 512)


class BillSecondReading(DirtyFieldsMixin, models.Model):
    second_reading_date = models.DateTimeField(auto_now_add=True)
    second_reading_date_hansard_url_en = models.CharField(max_length=512)
    second_reading_date_hansard_url_ch = models.CharField(max_length=512)
    second_reading_date_2 = models.DateTimeField(auto_now_add=True)
    second_reading_date_2_hansard_url_en = models.CharField(max_length=512)
    second_reading_date_2_hansard_url_ch = models.CharField(max_length=512)
    second_reading_date_3 = models.DateTimeField(auto_now_add=True)
    second_reading_date_3_hansard_url_en = models.CharField(max_length=512)
    second_reading_date_3_hansard_url_ch = models.CharField(max_length=512)
    second_reading_date_4 = models.DateTimeField(auto_now_add=True)
    second_reading_date_4_hansard_url_en = models.CharField(max_length=512)
    second_reading_date_4_hansard_url_ch = models.CharField(max_length=512)
    second_reading_date_5 =  models.DateTimeField(auto_now_add=True)
    second_reading_date_5_hansard_url_en = models.CharField(max_length=512)
    second_reading_date_5_hansard_url_ch = models.CharField(max_length=512)


class BillCommittee(DirtyFieldsMixin, models.Model):
    bills_committee_title_en = models.CharField(max_length=512)
    bills_committee_title_ch = models.CharField(max_length=512)
    bills_committee_url_en = models.CharField(max_length=512)
    bills_committee_url_ch = models.CharField(max_length=512)
    bills_committee_formation_date = models.DateTimeField(auto_now_add=True)
    bills_committee_report_url_en = models.CharField(max_length=512)
    bills_committee_report_url_ch = models.CharField(max_length=512)

class Bill(DirtyFieldsMixin, models.Model):
    committee = models.ForeignKey(BillCommittee, null=True, blank=True)
    first_reading = models.ForeignKey(BillFirstReading, null=True, blank=True)
    second_reading = models.ForeignKey(BillSecondReading, null=True, blank=True)
    third_reading = models.ForeignKey(BillThirdReading, null=True, blank=True)
    internal_key = models.CharField(max_length=100, unique=True)
    ordinance_title_en = models.CharField(max_length=512)
    ordinance_title_ch = models.CharField(max_length=512)
    ordinance_content_url_en = models.CharField(max_length=512)
    ordinance_content_url_ch = models.CharField(max_length=512)
    bill_title_en = models.CharField(max_length=512)
    bill_title_ch = models.CharField(max_length=512)
    proposed_by_en = models.CharField(max_length=512)
    proposed_by_ch = models.CharField(max_length=512)
    bill_gazette_date = models.DateTimeField(auto_now_add=True)
    bill_content_url_en = models.CharField(max_length=512)
    bill_content_url_ch  = models.CharField(max_length=512)
    bill_gazette_date_2 = models.DateTimeField(auto_now_add=True)
    bill_content_url_2_en = models.CharField(max_length=512)
    bill_content_url_2_ch = models.CharField(max_length=512)
    bill_gazette_date_3 = models.DateTimeField(auto_now_add=True)
    bill_content_url_3_en = models.CharField(max_length=512)
    bill_content_url_3_ch = models.CharField(max_length=512)
    ordinance_gazette_date = models.DateTimeField(auto_now_add=True)
    ordinance_year_number_en = models.CharField(max_length=512)
    ordinance_year_number_ch = models.CharField(max_length=512)
    ordinace_gazette_content_url_en = models.CharField(max_length=512)
    ordinance_gazette_content_url_ch = models.CharField(max_length=512)
    legco_brief_file_reference = models.CharField(max_length=512)
    legco_brief_url_en = models.CharField(max_length=512)
    legco_brief_url_ch = models.CharField(max_length=512)
    additional_information_en = models.CharField(max_length=512)
    additional_information_ch = models.CharField(max_length=512)
    remarks_en = models.CharField(max_length=512)
    remarks_ch = models.CharField(max_length=512)
