from marshmallow import Schema, fields

class PatientMedicalHistoryInsertRequest(Schema):
    hist_patient_id = fields.Int(required=True)
    hist_primary_complaint = fields.String(required=False)
    hist_onset_date = fields.Date(required=False)
    hist_related_trauma = fields.Boolean(required=False)
    hist_current_treatment = fields.String(required=False)
    hist_notes = fields.String(required=False)
    user_created = fields.String(required=True)

class PatientMedicalHistoryUpdateRequest(Schema):
    hist_id = fields.Int(required=True)
    hist_patient_id = fields.Int(required=True)
    hist_primary_complaint = fields.String(required=False)
    hist_onset_date = fields.Date(required=False)
    hist_related_trauma = fields.Boolean(required=False)
    hist_current_treatment = fields.String(required=False)
    hist_notes = fields.String(required=False)
    user_modified = fields.String(required=True)