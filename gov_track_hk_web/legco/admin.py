from django.contrib import admin
from legco.models import Party, Individual, Council, Constituency,  Meeting, Motion, VoteSummary, IndividualVote, Vote, NewsArticle
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

