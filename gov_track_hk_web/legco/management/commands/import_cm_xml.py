from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from legco.models import Meeting, Vote, Motion, Individual, IndividualVote, VoteSummary
from lxml import etree
from datetime import *
from dateutil.parser import *
import md5

def parse_date(s):
    for fmt in ["%d/%m/%Y","%d-%m-%Y"]:
        try:
            return datetime.strptime(s, fmt)
        except:
            pass
    raise Exception("failed to parse %s." % (s))

def parse_time(s):
    return datetime.strptime(s or "00:00:00", "%H:%M:%S")

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)
        parser.add_argument('--url', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = options['file']
        url = options['url']
        s = open(file_path, 'rb').read()
        doc = etree.XML(s)
        individuals = Individual.objects.all()

        for meeting_node in doc.xpath('//meeting'):
            with transaction.atomic():
                meeting = Meeting()
                meeting.date = parse_date(meeting_node.attrib['start-date'])
                meeting.meeting_type = meeting_node.attrib['type']
                meeting.source_url = url
                meeting.key =  str(md5.new(url).hexdigest())
                meeting.save()
                for vote_node in meeting_node.xpath('./vote'):
                    motion = Motion()
                    motion.name_en = vote_node.xpath('motion-en')[0].text or ""
                    motion.name_ch = vote_node.xpath('motion-ch')[0].text
                    if len(vote_node.xpath('mover-en')) > 0:
                        motion.mover_en = vote_node.xpath('mover-en')[0].text
                        motion.mover_ch = vote_node.xpath('mover-ch')[0].text
                        motion.mover_type = vote_node.xpath('mover-type')[0].text
                    else:
                        motion.mover_en = ""
                        motion.mover_ch = ""
                        motion.mover_type = ""
                    motion.save()
                    vote = Vote()
                    vote.meeting = meeting
                    vote.date = parse_date(vote_node.xpath('vote-date')[0].text)
                    vote.time = parse_time(vote_node.xpath('vote-time')[0].text)
                    vote.vote_number = int(vote_node.attrib['number'])
                    vote.separate = vote_node.xpath('vote-separate-mechanism')[0].text == "Yes"
                    vote.motion = motion
                    vote.save()
                    possible_summary_tags = ['overall','functional-constituency','geographical-constituency']
                    summary_types = ['OVER', 'FUNC', 'GEOG']
                    for summary_node in vote_node.xpath('vote-summary')[0].xpath('*'):
                        summary = VoteSummary()
                        summary.vote = vote
                        summary.summary_type = summary_types[possible_summary_tags.index(summary_node.tag)]
                        summary.present_count = int(summary_node.xpath('present-count')[0].text or 0)
                        summary.vote_count = int(summary_node.xpath('vote-count')[0].text or 0)
                        summary.yes_count =  int(summary_node.xpath('yes-count')[0].text or 0)
                        summary.no_count = int(summary_node.xpath('no-count')[0].text or 0)
                        summary.abstain_count = int(summary_node.xpath('abstain-count')[0].text or 0)
                        summary.result = summary_node.xpath('result')[0].text
                        summary.save()
                    for individual_vote_node in vote_node.xpath('./individual-votes/member'):
                        name_ch = individual_vote_node.attrib['name-ch']

                    for individual_vote_node in vote_node.xpath('./individual-votes/member'):
                        name_ch = individual_vote_node.attrib['name-ch']
                        name_en = individual_vote_node.attrib['name-en']
                        target_individual = None
                        for individual in individuals:
                            if individual.name_ch == name_ch or individual.name_en == name_en:
                                target_individual = individual
                                break
                        if target_individual is None:
                            raise Exception("Individual not found " + name_ch)
                        individual_vote = IndividualVote()
                        individual_vote.result = individual_vote_node.xpath('vote')[0].text.upper()
                        individual_vote.individual = target_individual
                        individual_vote.vote = vote
                        individual_vote.save()
                #Saving Records
                meeting.save()
                print("Done" + str(meeting))

