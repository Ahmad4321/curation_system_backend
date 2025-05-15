from django.db import models

from django.contrib.auth.models import User  # default auth_user table


class rtoData(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.TextField(db_column='tag')
    level = models.TextField(db_column='level')  # Avoid keyword conflict
    cname = models.TextField(db_column='cname')
    ename = models.TextField(db_column='ename')
    toid = models.TextField(db_column='toid',max_length=255)
    parent_id = models.IntegerField(db_column="parentId",null=True, blank=True)

    # Additional evidence fields
    pubAnnotation_evidence = models.TextField(db_column="pubAnnotation_evidence",null=True, blank=True)
    llm_evidence = models.TextField(db_column="llm_evidence",null=True, blank=True)
    rice_alterome_evidence = models.TextField(db_column="rice_alterome_evidence",null=True, blank=True)

    # Audit fields (linked to auth_user)
    created_at = models.DateTimeField(db_column="created_at",auto_now_add=True,null=True)
    updated_at = models.DateTimeField(db_column="updated_at",auto_now=True,null=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='rtodata_created',db_column="created_by"
    )
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='rtodata_updated',db_column="updated_by"
    )

    class Meta:
        db_table = 'rto_data'

class TraitEvaluation(models.Model):
    id = models.AutoField(primary_key=True)
    evaluation = models.TextField(db_column="evaluation",max_length=255)
    trait_id = models.ForeignKey(
        rtoData, on_delete=models.CASCADE,
        db_column='trait_id', related_name='trait_evaluations'
    )
    expert_name = models.TextField(db_column="expert_name",null=True, blank=True)

    # Audit fields (linked to auth_user)
    created_at = models.DateTimeField(db_column="created_at",auto_now_add=True,null=True)
    updated_at = models.DateTimeField(db_column="updated_at",auto_now=True,null=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,related_name='traiteval_created',db_column="created_by")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,related_name='traiteval_updated',db_column="updated_by")

    class Meta:
        db_table = 'trait_evaluation'
        indexes = [
            models.Index(fields=['id', 'trait_id']),
        ]


class ActionPerformed(models.Model):
    id = models.AutoField(db_column="id",primary_key=True)
    action_name = models.TextField(db_column="action_name",max_length=255)
    action_code = models.TextField(db_column="action_code",max_length=255)
    performed_by = models.TextField(db_column="performed_by",max_length=255)
    trait_name = models.TextField(db_column="trait_name",max_length=255)
    is_active = models.BooleanField(db_column="is_active",default=False)
    is_resolved = models.BooleanField(db_column="is_resolved",default=False)
    trait_id = models.ForeignKey(
        rtoData, on_delete=models.CASCADE,null=True,
        db_column='trait_id', related_name='actionperformed_trait'
    )
    trait_reference = models.TextField(db_column="trait_reference",null=True, blank=True)
    new_rice_alterome_evidence = models.TextField(db_column="new_rice_alterome_evidence",null=True, blank=True)
    new_pubAnnotation_evidence = models.TextField(db_column="new_pubAnnotation_evidence",null=True, blank=True)
    new_llm_evidence = models.TextField(db_column="new_llm_evidence",null=True, blank=True)
    
    # Avoid keyword conflict
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='actionperformed_created'
    )
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='actionperformed_updated'
    )

    class Meta:
        db_table = 'action_performed'
        # Avoid keyword conflict        
        indexes = [
            models.Index(fields=['id']),
        ]

class CustomUser(models.Model):
    pass

AUTH_USER_MODEL = 'users.CustomUser'