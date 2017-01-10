from functools import wraps
from django.contrib.contenttypes.models import ContentType
from vote.models import Vote


def instance_required(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if self.instance is None:
            error = "Can't call %s with a non-instance manager" % func.__name__
            raise TypeError(error)

        return func(self, *args, **kwargs)

    return inner


def add_field_to_objects(model, objects, user_id, vote_up_field='is_voted_up',
                         vote_down_field='is_voted_down'):
    content_type = ContentType.objects.get_for_model(model)
    object_ids = [r.id for r in objects]

    voted_object_ids = Vote.objects.filter(
        user_id=user_id,
        content_type=content_type,
        object_id__in=object_ids
    ).values_list("object_id", "action")

    for r in objects:
        setattr(r, vote_up_field, (r.pk, Vote.UP) in voted_object_ids)
        setattr(r, vote_down_field, (r.pk, Vote.DOWN) in voted_object_ids)

    return objects
