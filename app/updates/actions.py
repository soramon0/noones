from django.contrib import messages


def accept_update(modeladmin, request, queryset):
    query = queryset.all()
    for q in query:
        # update only the ones that hasn't been accepted yet.
        if not q.accept:
            q.accept = True
            q.decline = None
            # TODO(karim): change default message
            q.message = "update has been accepted."
            q.save()
    modeladmin.message_user(
        request, "updates were successfully marked as accepted", messages.SUCCESS)


accept_update.short_description = "Mark selected update as accepted"
