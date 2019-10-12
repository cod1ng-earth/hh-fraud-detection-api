from flask import g
import pandas as pd


def query_db(query, args=(), one=False):
    cur = g.db.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]

    # cur.connection.close()
    return (r[0] if r else None) if one else r


def all_claims(providerId):
    sql = """
    Select * from (
                SELECT BeneID,
                        ClaimID,
                        ClaimStartDt,
                        ClaimEndDt,
                        Provider,
                        InscClaimAmtReimbursed,
                        AttendingPhysician,
                        OperatingPhysician,
                        OtherPhysician,
                        ClmDiagnosisCode_1,
                        ClmDiagnosisCode_2,
                        ClmDiagnosisCode_3,
                        ClmDiagnosisCode_4,
                        ClmDiagnosisCode_5,
                        ClmDiagnosisCode_6,
                        ClmDiagnosisCode_7,
                        ClmDiagnosisCode_8,
                        ClmDiagnosisCode_9,
                        ClmDiagnosisCode_10,
                        ClmProcedureCode_1,
                        ClmProcedureCode_2,
                        ClmProcedureCode_3,
                        ClmProcedureCode_4,
                        ClmProcedureCode_5,
                        ClmProcedureCode_6,
                        DeductibleAmtPaid,
                        ClmAdmitDiagnosisCode,
                        DiagnosisGroupCode,
                        AdmissionDt,
                        DischargeDt
                from Inpatient
                where Provider = ?
                UNION
                select BeneID,
                        ClaimID,
                        ClaimStartDt,
                        ClaimEndDt,
                        Provider,
                        InscClaimAmtReimbursed,
                        AttendingPhysician,
                        OperatingPhysician,
                        OtherPhysician,
                        ClmDiagnosisCode_1,
                        ClmDiagnosisCode_2,
                        ClmDiagnosisCode_3,
                        ClmDiagnosisCode_4,
                        ClmDiagnosisCode_5,
                        ClmDiagnosisCode_6,
                        ClmDiagnosisCode_7,
                        ClmDiagnosisCode_8,
                        ClmDiagnosisCode_9,
                        ClmDiagnosisCode_10,
                        ClmProcedureCode_1,
                        ClmProcedureCode_2,
                        ClmProcedureCode_3,
                        ClmProcedureCode_4,
                        ClmProcedureCode_5,
                        ClmProcedureCode_6,
                        DeductibleAmtPaid,
                        ClmAdmitDiagnosisCode,
                        "NA" as DiagnosisGroupCode,
                        "NA" as AdmissionDt,
                        "NA" as DischargeDt
                from Outpatient
                where Provider = ?
            ) q left join Beneficiary b on b.BeneID = q.BeneID
    ;
    """
    return query_db(sql, (providerId, providerId))


def all_claims_x(providerId):
    sql = """
    Select * from (
                SELECT BeneID,
                        ClaimID,
                        ClaimStartDt,
                        ClaimEndDt,
                        Provider,
                        InscClaimAmtReimbursed,
                        AttendingPhysician,
                        OperatingPhysician,
                        OtherPhysician,
                        ClmDiagnosisCode_1,
                        ClmDiagnosisCode_2,
                        ClmDiagnosisCode_3,
                        ClmDiagnosisCode_4,
                        ClmDiagnosisCode_5,
                        ClmDiagnosisCode_6,
                        ClmDiagnosisCode_7,
                        ClmDiagnosisCode_8,
                        ClmDiagnosisCode_9,
                        ClmDiagnosisCode_10,
                        ClmProcedureCode_1,
                        ClmProcedureCode_2,
                        ClmProcedureCode_3,
                        ClmProcedureCode_4,
                        ClmProcedureCode_5,
                        ClmProcedureCode_6,
                        DeductibleAmtPaid,
                        ClmAdmitDiagnosisCode,
                        DiagnosisGroupCode,
                        AdmissionDt,
                        DischargeDt
                from Inpatient
                where Provider IN (?,?)
                UNION
                select BeneID,
                        ClaimID,
                        ClaimStartDt,
                        ClaimEndDt,
                        Provider,
                        InscClaimAmtReimbursed,
                        AttendingPhysician,
                        OperatingPhysician,
                        OtherPhysician,
                        ClmDiagnosisCode_1,
                        ClmDiagnosisCode_2,
                        ClmDiagnosisCode_3,
                        ClmDiagnosisCode_4,
                        ClmDiagnosisCode_5,
                        ClmDiagnosisCode_6,
                        ClmDiagnosisCode_7,
                        ClmDiagnosisCode_8,
                        ClmDiagnosisCode_9,
                        ClmDiagnosisCode_10,
                        ClmProcedureCode_1,
                        ClmProcedureCode_2,
                        ClmProcedureCode_3,
                        ClmProcedureCode_4,
                        ClmProcedureCode_5,
                        ClmProcedureCode_6,
                        DeductibleAmtPaid,
                        ClmAdmitDiagnosisCode,
                        "NA" as DiagnosisGroupCode,
                        "NA" as AdmissionDt,
                        "NA" as DischargeDt
                from Outpatient
                where Provider IN (?,?)
            ) q left join Beneficiary b on b.BeneID = q.BeneID
    ;
    """
    return query_db(sql, ("PRV51001", providerId, "PRV51001", providerId))
