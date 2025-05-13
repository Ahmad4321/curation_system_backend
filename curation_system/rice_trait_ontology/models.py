from django.db import models

from django.contrib.auth.models import User  # default auth_user table

class RTOdata(models.Model):
    TAG = models.TextField()
    LEVEL = models.TextField(db_column='"LEVEL"')  # Avoid keyword conflict
    CNAME = models.TextField()
    ENAME = models.TextField()
    TOID = models.TextField()
    PARENTID = models.IntegerField(null=True, blank=True)

    # Additional evidence fields
    pubAnnotation_evidence = models.TextField(null=True, blank=True)
    llm_evidence = models.TextField(null=True, blank=True)
    rice_alterome_evidence = models.IntegerField(null=True, blank=True)

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
        db_table = 'RTOdata'

class TraitEvaluation(models.Model):
    evaluation = models.TextField()
    trait = models.ForeignKey(
        RTOdata, on_delete=models.CASCADE,
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
            models.Index(fields=['id', 'trait']),
        ]
