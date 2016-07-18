from django.contrib import admin
from legco.models import Party, Individual, Council, Constituency,  Meeting, Motion, VoteSummary, IndividualVote, Vote, NewsArticle
from legco.models import Bill,  BillCommittee, BillThirdReading, BillFirstReading, BillSecondReading
from legco.models import Question
admin.site.register(Party)
admin.site.register(Vote)
admin.site.register(Individual)
admin.site.register(Council)
admin.site.register(Constituency)
admin.site.register(Motion)
admin.site.register(Meeting)
admin.site.register(VoteSummary)
admin.site.register(IndividualVote)
admin.site.register(NewsArticle)
admin.site.register(Bill)
admin.site.register(BillCommittee)
admin.site.register(BillThirdReading)
admin.site.register(BillFirstReading)
admin.site.register(BillSecondReading)
admin.site.register(Question)
