from rest_framework import serializers

from .models import (
    Company,
    ImportBatch,
    Activity,
    RawRecord,
    DataIssue,
    ReviewDecision,
    AuditEvent
)


# ==========================================
# COMPANY
# ==========================================

class CompanySerializer(serializers.ModelSerializer):

    class Meta:

        model = Company

        fields = '__all__'


# ==========================================
# IMPORT BATCH
# ==========================================

class ImportBatchSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(

        source='company.name',

        read_only=True
    )

    class Meta:

        model = ImportBatch

        fields = '__all__'


# ==========================================
# ACTIVITY
# ==========================================

class ActivitySerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(

        source='company.name',

        read_only=True
    )

    batch_id = serializers.IntegerField(

        source='batch.id',

        read_only=True
    )

    class Meta:

        model = Activity

        fields = '__all__'


# ==========================================
# RAW RECORD
# ==========================================

class RawRecordSerializer(serializers.ModelSerializer):

    class Meta:

        model = RawRecord

        fields = '__all__'


# ==========================================
# DATA ISSUE
# ==========================================

class DataIssueSerializer(serializers.ModelSerializer):

    class Meta:

        model = DataIssue

        fields = '__all__'


# ==========================================
# REVIEW DECISION
# ==========================================

class ReviewDecisionSerializer(serializers.ModelSerializer):

    class Meta:

        model = ReviewDecision

        fields = '__all__'


# ==========================================
# AUDIT EVENT
# ==========================================

class AuditEventSerializer(serializers.ModelSerializer):

    class Meta:

        model = AuditEvent

        fields = '__all__'