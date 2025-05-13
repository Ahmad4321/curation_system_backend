from django.db import models

from django.contrib.auth.models import User  # default auth_user table

class rtoData(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.TextField(db_column='tag')
    level = models.TextField(db_column='level')  # Avoid keyword conflict
    cname = models.TextField(db_column='cname')
    ename = models.TextField(db_column='ename')
    toid = models.TextField(db_column='toid')
    parent_id = models.IntegerField(null=True, blank=True)

    # Additional evidence fields
    pubAnnotation_evidence = models.TextField(null=True, blank=True)
    llm_evidence = models.TextField(null=True, blank=True)
    rice_alterome_evidence = models.TextField(null=True, blank=True)

    # Audit fields (linked to auth_user)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='rtodata_created'
    )
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='rtodata_updated'
    )

    class Meta:
        db_table = 'rto_data'

class TraitEvaluation(models.Model):
    id = models.AutoField(primary_key=True)
    evaluation = models.TextField(max_length=255)
    trait_id = models.ForeignKey(
        rtoData, on_delete=models.CASCADE,
        db_column='trait_id', related_name='trait_evaluations'
    )
    expert_name = models.TextField(null=True, blank=True)

    # Audit fields (linked to auth_user)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='traiteval_created'
    )
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='traiteval_updated'
    )

    class Meta:
        db_table = 'trait_evaluation'
        indexes = [
            models.Index(fields=['id', 'trait_id']),
        ]


class CustomUser(models.Model):
    pass

AUTH_USER_MODEL = 'users.CustomUser'