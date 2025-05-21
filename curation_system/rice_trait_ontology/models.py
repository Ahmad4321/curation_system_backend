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
        app_label = 'rice_trait_ontology'

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
        app_label = 'rice_trait_ontology'
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

class TraitExplaination(models.Model):
    id = models.AutoField(primary_key=True)
    sentence = models.TextField(db_column="sentence",max_length=255,null=True, blank=True)
    is_obsolete = models.TextField(db_column="is_obsolete",max_length=255,null=True, blank=True)
    is_a = models.TextField(db_column="is_a",max_length=255,null=True, blank=True)
    xref = models.TextField(db_column="xref",max_length=255,null=True, blank=True)
    synonym = models.TextField(db_column="synonym",max_length=255,null=True, blank=True)
    comment = models.TextField(db_column="comment",max_length=255,null=True, blank=True)
    name = models.TextField(db_column="name",max_length=255,null=True, blank=True)
    trait_ontology_id = models.TextField(db_column="trait_ontology_id",max_length=255,null=True, blank=True)

    class Meta:
        db_table = 'trait_explaination'
        app_label = 'rice_trait_ontology'
        indexes = [
            models.Index(fields=['id']),
        ]

class RiceAlteromeModelExternal(models.Model):

    # primary key
    id = models.AutoField(db_column="id",primary_key=True)
    Gene = models.CharField(db_column='Gene', max_length=100, db_index=True)
    EntrezID = models.CharField(db_column='EntrezID', max_length=100, db_index=True)
    NormalizedVariantsMention = models.CharField(db_column='NormalizedVariantsMention', max_length=100, db_index=True)
    NormalizedVariantsID = models.CharField(db_column='NormalizedVariantsID', max_length=100, db_index=True)
    NormalizedVariantsType = models.CharField(db_column='NormalizedVariantsType', max_length=100, db_index=True)
    AlterationsMention = models.CharField(db_column='AlterationsMention', max_length=100, db_index=True)
    AlterationsType = models.CharField(db_column='AlterationsType', max_length=100, db_index=True)
    GOMention = models.CharField(db_column='GOMention', max_length=100, db_index=True)
    GOTerm = models.CharField(db_column='GOTerm', max_length=100, db_index=True)
    GOAncestor = models.CharField(db_column='GOAncestor', max_length=100, db_index=True)
    TOMention = models.CharField(db_column='TOMention', max_length=100, db_index=True)
    TOTerm = models.CharField(db_column='TOTerm', max_length=100, db_index=True)
    TOAncestor = models.CharField(db_column='TOAncestor', max_length=100, db_index=True)
    MeshMention = models.CharField(db_column='MeshMention', max_length=100, db_index=True)
    MeshTerm = models.CharField(db_column='MeshTerm', max_length=100, db_index=True)
    UnNormTerm = models.CharField(db_column='UnNormTerm', max_length=100, db_index=True)
    IncludeEvents = models.CharField(db_column='IncludeEvents', max_length=10)
    Events = models.CharField(db_column='Events', max_length=500)
    PMID = models.CharField(db_column='PMID', max_length=15)
    Title = models.CharField(db_column='Title', max_length=100)
    Doi = models.CharField(db_column='Doi', max_length=10)
    Sentence = models.CharField(db_column='Sentence', max_length=1000)
    RichSentence = models.CharField(db_column='RichSentence', max_length=3000)
    Journal = models.CharField(db_column='Journal', max_length=100)
    Year = models.CharField(db_column='Year', max_length=10, db_index=True)

    class Meta:
        managed = False
        db_table = 'RiceAlteromeModel'
        app_label = 'RiceAlterome'

    def __str__(self):
        return f'{self.PMID}-{self.Year}-{self.Gene}'
    

class RiceAlteromePubannotationData(models.Model):
    id = models.AutoField(db_column="id",primary_key=True)
    alterome_GoTerm = models.CharField(db_column='alterome_GoTerm', max_length=100, db_index=True,null=True)
    alterome_Gene = models.CharField(db_column='alterome_Gene', max_length=100, db_index=True,null=True)
    alterome_PMID = models.CharField(db_column='alterome_PMID', max_length=15,null=True)
    alterome_RichSentence = models.CharField(db_column='alterome_RichSentence', max_length=3000,null=True)
    alterome_sentence = models.CharField(db_column='alterome_sentence', max_length=1000,null=True)
    alterome_title = models.CharField(db_column='alterome_title', max_length=100,null=True)
    alterome_trait_name = models.CharField(db_column='alterome_trait_name', max_length=100, db_index=True,null=True)
    alterome_TOTerm = models.CharField(db_column='alterome_TOTerm', max_length=100, db_index=True,null=True)
    pubannotation_target = models.TextField(db_column="pubannotation_target",null=True)
    pubannotation_text = models.TextField(db_column="pubannotation_text",null=True)
    pubannotation_source_db = models.TextField(db_column="pubannotation_source_db",null=True)
    pubannotation_project_name = models.TextField(db_column="pubannotation_project_name",null=True)
    pubannotation_tracks = models.TextField(db_column="pubannotation_tracks",null=True)

    class Meta:
        managed = True
        db_table = 'rice_alterome_pubannotationData'
        app_label = 'rice_trait_ontology'
        indexes = [
            models.Index(fields=['id']),
        ]

        