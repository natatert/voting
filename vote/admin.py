from django.contrib import admin
from .models import Character, Vote

# Register your models here.


class VoteAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        characters = Character.objects.all()
        if db_field.name == "character":
            for x in Vote.objects.all():
                characters = characters.exclude(pk__in=x.character.all())
            if not request.resolver_match.kwargs.get('object_id') is None:
                vote_id = request.resolver_match.kwargs.get('object_id')
                characters_selected = Vote.objects.get(id=vote_id).character.all()
                result = characters_selected | characters
            else:
                result = characters
            kwargs["queryset"] = result

        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Character)
admin.site.register(Vote, VoteAdmin)
