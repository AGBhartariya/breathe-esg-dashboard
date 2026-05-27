import csv
import io
import json

from datetime import datetime

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Company,
    ImportBatch,
    Activity,
    RawRecord,
    DataIssue,
    ReviewDecision,
    AuditEvent
)

from .serializers import (
    ActivitySerializer,
    ImportBatchSerializer,
    DataIssueSerializer
)


# =========================================================
# COLUMN ALIAS MAP
# =========================================================

COLUMN_ALIASES = {

    "activity_type": [
        "activity_type",
        "activity",
        "type",
        "category",
        "expense_type",
        "emission_type"
    ],

    "vendor": [
        "vendor",
        "supplier",
        "merchant",
        "provider",
        "company"
    ],

    "quantity": [
        "quantity",
        "qty",
        "usage",
        "consumption",
        "amount_used",
        "volume"
    ],

    "unit": [
        "unit",
        "uom",
        "measurement",
        "units"
    ],

    "amount": [
        "amount",
        "cost",
        "price",
        "expense",
        "value"
    ],

    "currency": [
        "currency",
        "currency_code",
        "money_type"
    ]
}


# =========================================================
# NORMALIZATION
# =========================================================

UNIT_CONVERSIONS = {

    "gallons": ("liters", 3.78541),

    "litres": ("liters", 1),

    "liters": ("liters", 1),

    "kwh": ("kwh", 1),

    "mwh": ("kwh", 1000),

    "kg": ("kg", 1),

    "tonnes": ("kg", 1000),

    "miles": ("km", 1.60934),

    "km": ("km", 1)
}


# =========================================================
# DETECT DELIMITER
# =========================================================

def detect_delimiter(text):

    possible = [",", ";", "\t", "|"]

    scores = {}

    for d in possible:

        scores[d] = text.count(d)

    return max(scores, key=scores.get)


# =========================================================
# FIND COLUMN
# =========================================================

def find_column(headers, target):

    aliases = COLUMN_ALIASES.get(target, [])

    normalized_headers = {

        h.lower().strip(): h

        for h in headers
    }

    for alias in aliases:

        alias = alias.lower().strip()

        if alias in normalized_headers:

            return normalized_headers[alias]

    for header in headers:

        h = header.lower().strip()

        for alias in aliases:

            if alias in h or h in alias:

                return header

    return None


# =========================================================
# NORMALIZE VALUE
# =========================================================

def normalize_quantity(quantity, unit):

    unit = str(unit).lower().strip()

    if unit in UNIT_CONVERSIONS:

        normalized_unit, factor = UNIT_CONVERSIONS[unit]

        return quantity * factor, normalized_unit

    return quantity, unit


# =========================================================
# FLAG SUSPICIOUS
# =========================================================

def detect_suspicious(activity):

    reasons = []

    if activity.quantity < 0:

        reasons.append("Negative quantity")

    if activity.quantity > 1000000:

        reasons.append("Extremely high quantity")

    if activity.amount < 0:

        reasons.append("Negative monetary amount")

    if not activity.vendor:

        reasons.append("Missing vendor")

    if not activity.activity_type:

        reasons.append("Missing activity type")

    return reasons


# =========================================================
# ACTIVITY LIST
# =========================================================

class ActivityListView(APIView):

    def get(self, request):

        activities = Activity.objects.all().order_by('-id')

        serializer = ActivitySerializer(

            activities,

            many=True
        )

        return Response(serializer.data)


# =========================================================
# BATCH LIST
# =========================================================

class BatchListView(APIView):

    def get(self, request):

        batches = ImportBatch.objects.all().order_by('-id')

        serializer = ImportBatchSerializer(

            batches,

            many=True
        )

        return Response(serializer.data)


# =========================================================
# ISSUES LIST
# =========================================================

class IssuesListView(APIView):

    def get(self, request):

        issues = DataIssue.objects.all().order_by('-id')

        serializer = DataIssueSerializer(

            issues,

            many=True
        )

        return Response(serializer.data)


# =========================================================
# FILE UPLOAD
# =========================================================

class UploadFileView(APIView):

    def post(self, request):

        try:

            uploaded_file = request.FILES.get('file')

            source_type = request.data.get(

                'source_type',

                'unknown'
            )

            company_name = request.data.get(

                'company',

                'Demo Company'
            )

            if not uploaded_file:

                return Response(

                    {

                        "error": "No file uploaded"
                    },

                    status=400
                )

            # =========================================
            # GET OR CREATE COMPANY
            # =========================================

            company, _ = Company.objects.get_or_create(

                name=company_name
            )

            # =========================================
            # CREATE BATCH
            # =========================================

            batch = ImportBatch.objects.create(

                company=company,

                source_type=source_type,

                source_file_name=uploaded_file.name,

                status='processing'
            )

            # =========================================
            # READ FILE SAFELY
            # =========================================

            raw_bytes = uploaded_file.read()

            decoded = None

            encodings = [

                'utf-8-sig',

                'utf-8',

                'latin-1',

                'cp1252'
            ]

            for enc in encodings:

                try:

                    decoded = raw_bytes.decode(enc)

                    break

                except:

                    continue

            if decoded is None:

                return Response(

                    {

                        "error": "Unable to decode file"
                    },

                    status=400
                )

            decoded = decoded.replace('\r\n', '\n')

            delimiter = detect_delimiter(decoded)

            csv_file = io.StringIO(decoded)

            reader = csv.DictReader(

                csv_file,

                delimiter=delimiter
            )

            headers = reader.fieldnames

            if not headers:

                return Response(

                    {

                        "error": "CSV headers missing"
                    },

                    status=400
                )

            # =========================================
            # FIND IMPORTANT COLUMNS
            # =========================================

            activity_col = find_column(

                headers,

                "activity_type"
            )

            vendor_col = find_column(

                headers,

                "vendor"
            )

            quantity_col = find_column(

                headers,

                "quantity"
            )

            unit_col = find_column(

                headers,

                "unit"
            )

            amount_col = find_column(

                headers,

                "amount"
            )

            currency_col = find_column(

                headers,

                "currency"
            )

            # =========================================
            # PROCESS ROWS
            # =========================================

            total_rows = 0
            success_rows = 0
            failed_rows = 0
            suspicious_rows = 0

            for raw_row in reader:

                total_rows += 1

                try:

                    raw_record = RawRecord.objects.create(

                        batch=batch,

                        raw_data=raw_row,

                        parse_status='parsed'
                    )

                    activity_type = str(

                        raw_row.get(activity_col, '')
                    ).strip()

                    vendor = str(

                        raw_row.get(vendor_col, '')
                    ).strip()

                    quantity_raw = str(

                        raw_row.get(quantity_col, '0')
                    ).strip()

                    unit = str(

                        raw_row.get(unit_col, '')
                    ).strip()

                    amount_raw = str(

                        raw_row.get(amount_col, '0')
                    ).strip()

                    currency = str(

                        raw_row.get(currency_col, 'USD')
                    ).strip()

                    try:

                        quantity = float(quantity_raw)

                    except:

                        quantity = 0

                    try:

                        amount = float(amount_raw)

                    except:

                        amount = 0

                    normalized_quantity, normalized_unit = normalize_quantity(

                        quantity,

                        unit
                    )

                    activity = Activity.objects.create(

                        company=company,

                        batch=batch,

                        source_type=source_type,

                        source_file_name=uploaded_file.name,

                        activity_type=activity_type,

                        vendor=vendor,

                        quantity=quantity,

                        unit=unit,

                        normalized_quantity=normalized_quantity,

                        normalized_unit=normalized_unit,

                        amount=amount,

                        currency=currency,

                        raw_payload=raw_row
                    )

                    raw_record.created_activity = activity

                    raw_record.save()

                    # =================================
                    # SUSPICIOUS DETECTION
                    # =================================

                    suspicious_reasons = detect_suspicious(activity)

                    if suspicious_reasons:

                        suspicious_rows += 1

                        activity.is_suspicious = True

                        activity.suspicious_reason = "; ".join(

                            suspicious_reasons
                        )

                        activity.save()

                        for reason in suspicious_reasons:

                            DataIssue.objects.create(

                                activity=activity,

                                batch=batch,

                                issue_type="Suspicious Data",

                                severity='high',

                                issue_message=reason,

                                suggested_fix="Review analyst input",

                                raw_data=raw_row
                            )

                            AuditEvent.objects.create(

                                activity=activity,

                                batch=batch,

                                event_type='issue_detected',

                                event_message=reason
                            )

                    AuditEvent.objects.create(

                        activity=activity,

                        batch=batch,

                        event_type='upload',

                        event_message='Activity uploaded'
                    )

                    success_rows += 1

                except Exception as e:

                    failed_rows += 1

                    RawRecord.objects.create(

                        batch=batch,

                        raw_data=raw_row,

                        parse_status='failed',

                        parsing_error=str(e)
                    )

            # =========================================
            # FINALIZE BATCH
            # =========================================

            batch.total_rows = total_rows

            batch.success_rows = success_rows

            batch.failed_rows = failed_rows

            batch.suspicious_rows = suspicious_rows

            batch.status = 'review_pending'

            batch.save()

            return Response({

                "message": "Upload successful",

                "batch_id": batch.id,

                "total_rows": total_rows,

                "success_rows": success_rows,

                "failed_rows": failed_rows,

                "suspicious_rows": suspicious_rows
            })

        except Exception as e:

            print(e)

            return Response(

                {

                    "error": str(e)
                },

                status=500
            )


# =========================================================
# APPROVE ACTIVITY
# =========================================================

class ApproveActivityView(APIView):

    def post(self, request, pk):

        try:

            activity = Activity.objects.get(id=pk)

            if activity.is_locked:

                return Response({

                    "error": "Activity already locked"
                })

            activity.review_status = 'approved'

            activity.is_locked = True

            activity.approved_at = timezone.now()

            activity.save()

            ReviewDecision.objects.create(

                activity=activity,

                decision='approved'
            )

            AuditEvent.objects.create(

                activity=activity,

                batch=activity.batch,

                event_type='approve',

                event_message='Activity approved'
            )

            return Response({

                "message": "Approved"
            })

        except Exception as e:

            return Response({

                "error": str(e)
            })


# =========================================================
# REJECT ACTIVITY
# =========================================================

class RejectActivityView(APIView):

    def post(self, request, pk):

        try:

            activity = Activity.objects.get(id=pk)

            if activity.is_locked:

                return Response({

                    "error": "Activity already locked"
                })

            activity.review_status = 'rejected'

            activity.save()

            ReviewDecision.objects.create(

                activity=activity,

                decision='rejected'
            )

            AuditEvent.objects.create(

                activity=activity,

                batch=activity.batch,

                event_type='reject',

                event_message='Activity rejected'
            )

            return Response({

                "message": "Rejected"
            })

        except Exception as e:

            return Response({

                "error": str(e)
            })