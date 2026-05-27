from django.db import models


# ==========================================
# COMPANY MODEL
# ==========================================

class Company(models.Model):

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name


# ==========================================
# IMPORT BATCH MODEL
# ==========================================

class ImportBatch(models.Model):

    STATUS_CHOICES = [

        ('processing', 'Processing'),

        ('review_pending', 'Review Pending'),

        ('approved', 'Approved'),

        ('locked', 'Locked')
    ]

    company = models.ForeignKey(

        Company,

        on_delete=models.CASCADE,

        related_name='batches'
    )

    source_type = models.CharField(max_length=100)

    source_file_name = models.CharField(max_length=255)

    total_rows = models.IntegerField(default=0)

    success_rows = models.IntegerField(default=0)

    failed_rows = models.IntegerField(default=0)

    suspicious_rows = models.IntegerField(default=0)

    status = models.CharField(

        max_length=30,

        choices=STATUS_CHOICES,

        default='processing'
    )

    is_locked = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    approved_at = models.DateTimeField(

        null=True,

        blank=True
    )

    def __str__(self):

        return f"Batch #{self.id} - {self.source_file_name}"


# ==========================================
# ACTIVITY MODEL
# ==========================================

class Activity(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),

        ('approved', 'Approved'),

        ('rejected', 'Rejected')
    ]

    company = models.ForeignKey(

        Company,

        on_delete=models.CASCADE,

        related_name='activities'
    )

    batch = models.ForeignKey(

        ImportBatch,

        on_delete=models.CASCADE,

        related_name='activities',

        null=True,

        blank=True
    )

    source_type = models.CharField(max_length=100)

    source_file_name = models.CharField(

        max_length=255,

        blank=True
    )

    activity_type = models.CharField(max_length=255)

    vendor = models.CharField(max_length=255)

    quantity = models.FloatField(default=0)

    unit = models.CharField(max_length=100)

    normalized_quantity = models.FloatField(default=0)

    normalized_unit = models.CharField(

        max_length=100,

        blank=True
    )

    amount = models.FloatField(default=0)

    currency = models.CharField(

        max_length=20,

        default='USD'
    )

    review_status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='pending'
    )

    is_locked = models.BooleanField(default=False)

    approved_at = models.DateTimeField(

        null=True,

        blank=True
    )

    is_suspicious = models.BooleanField(default=False)

    suspicious_reason = models.TextField(blank=True)

    raw_payload = models.JSONField(

        null=True,

        blank=True
    )

    uploaded_at = models.DateTimeField(

        auto_now_add=True
    )

    updated_at = models.DateTimeField(

        auto_now=True
    )

    def __str__(self):

        return f'{self.activity_type} - {self.vendor}'


# ==========================================
# RAW RECORD MODEL
# ==========================================

class RawRecord(models.Model):

    PARSE_STATUS = [

        ('parsed', 'Parsed'),

        ('failed', 'Failed')
    ]

    batch = models.ForeignKey(

        ImportBatch,

        on_delete=models.CASCADE,

        related_name='raw_records'
    )

    raw_data = models.JSONField()

    parse_status = models.CharField(

        max_length=20,

        choices=PARSE_STATUS,

        default='parsed'
    )

    parsing_error = models.TextField(blank=True)

    created_activity = models.ForeignKey(

        Activity,

        on_delete=models.SET_NULL,

        null=True,

        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"RawRecord #{self.id}"


# ==========================================
# DATA ISSUE MODEL
# ==========================================

class DataIssue(models.Model):

    ISSUE_SEVERITY = [

        ('low', 'Low'),

        ('medium', 'Medium'),

        ('high', 'High')
    ]

    activity = models.ForeignKey(

        Activity,

        on_delete=models.CASCADE,

        null=True,

        blank=True
    )

    batch = models.ForeignKey(

        ImportBatch,

        on_delete=models.CASCADE,

        null=True,

        blank=True
    )

    issue_type = models.CharField(max_length=255)

    severity = models.CharField(

        max_length=20,

        choices=ISSUE_SEVERITY,

        default='medium'
    )

    issue_message = models.TextField()

    suggested_fix = models.TextField(blank=True)

    raw_data = models.JSONField(

        null=True,

        blank=True
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return self.issue_message


# ==========================================
# REVIEW DECISION MODEL
# ==========================================

class ReviewDecision(models.Model):

    DECISION_CHOICES = [

        ('approved', 'Approved'),

        ('rejected', 'Rejected')
    ]

    activity = models.ForeignKey(

        Activity,

        on_delete=models.CASCADE,

        related_name='review_decisions'
    )

    decision = models.CharField(

        max_length=20,

        choices=DECISION_CHOICES
    )

    reviewer_notes = models.TextField(blank=True)

    decided_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.activity.id} - {self.decision}"


# ==========================================
# AUDIT EVENT MODEL
# ==========================================

class AuditEvent(models.Model):

    EVENT_TYPES = [

        ('upload', 'Upload'),

        ('approve', 'Approve'),

        ('reject', 'Reject'),

        ('lock', 'Lock'),

        ('issue_detected', 'Issue Detected')
    ]

    activity = models.ForeignKey(

        Activity,

        on_delete=models.CASCADE,

        null=True,

        blank=True
    )

    batch = models.ForeignKey(

        ImportBatch,

        on_delete=models.CASCADE,

        null=True,

        blank=True
    )

    event_type = models.CharField(

        max_length=50,

        choices=EVENT_TYPES
    )

    event_message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.event_type