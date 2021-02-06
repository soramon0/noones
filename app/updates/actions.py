from django.contrib import messages


def accept_update(modeladmin, request, queryset):
    query = queryset.all()
    for q in query:
        # update only the ones that hasn't been accepted yet.
        if not q.accept:
            # TODO(kairm): may have to check for q.dirty here
            q.accept = True
            q.decline = None
            # TODO(karim): change default message
            q.message = "update has been accepted."
            q.save()
            modeladmin.message_user(
                request,
                "update(s) were successfully marked accepted",
                messages.SUCCESS
            )


accept_update.short_description = "Mark selected update(s) as accepted"
