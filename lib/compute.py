from keras.models import load_model
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import scipy as sc

model = load_model('stefan.h5')


def transform(originalValues):
    # the first line of "X_test_AE"
    return [[-2.83734569e+00,  9.83227741e-01,  2.73217562e-01, -4.78524696e-03,
             5.23113546e-02, -1.04610328e-03,  4.69188007e-02,  2.90218719e-02,
             1.25953972e-02, -3.60372131e-01,  9.00870408e-02,  7.19589387e-02,
             -7.79629676e-02, -3.79993916e-02,  1.02092528e-01, -3.35155292e-02,
             -1.48795630e-02,  1.97393418e-02, -1.22867991e-01,  4.32997898e-02,
             -1.42723225e-03, -9.13176842e-02,  1.81666606e-02, -4.26211488e-02,
             -4.27991657e-02,  4.06663542e-02,  4.96137126e-02, -4.97330536e-03,
             3.21861799e-02]]


def callModel(X):
    sc = StandardScaler()   # MinMaxScaler
    sc.fit(X)
    X_std = sc.transform(X)
    return model.predict(X_std)


def featurize(d):
    d["PerProviderAvg_InscClaimAmtReimbursed"] = d.groupby(
        'Provider')['InscClaimAmtReimbursed'].transform('mean')
    d["PerProviderAvg_DeductibleAmtPaid"] = d.groupby(
        'Provider')['DeductibleAmtPaid'].transform('mean')
    d["PerProviderAvg_IPAnnualReimbursementAmt"] = d.groupby(
        'Provider')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerProviderAvg_IPAnnualDeductibleAmt"] = d.groupby(
        'Provider')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerProviderAvg_OPAnnualReimbursementAmt"] = d.groupby(
        'Provider')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerProviderAvg_OPAnnualDeductibleAmt"] = d.groupby(
        'Provider')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerProviderAvg_Age"] = d.groupby('Provider')['Age'].transform('mean')
    d["PerProviderAvg_NoOfMonths_PartACov"] = d.groupby(
        'Provider')['NoOfMonths_PartACov'].transform('mean')
    d["PerProviderAvg_NoOfMonths_PartBCov"] = d.groupby(
        'Provider')['NoOfMonths_PartBCov'].transform('mean')
    d["PerProviderAvg_AdmitForDays"] = d.groupby(
        'Provider')['AdmitForDays'].transform('mean')

    # Grouping based on BeneID explains amounts involved per beneficiary.Reason to derive this feature is that one beneficiary
    # can go to multiple providers and can be involved in fraud cases
    d["PerBeneIDAvg_InscClaimAmtReimbursed"] = d.groupby(
        'BeneID')['InscClaimAmtReimbursed'].transform('mean')
    d["PerBeneIDAvg_DeductibleAmtPaid"] = d.groupby(
        'BeneID')['DeductibleAmtPaid'].transform('mean')
    d["PerBeneIDAvg_IPAnnualReimbursementAmt"] = d.groupby(
        'BeneID')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerBeneIDAvg_IPAnnualDeductibleAmt"] = d.groupby(
        'BeneID')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerBeneIDAvg_OPAnnualReimbursementAmt"] = d.groupby(
        'BeneID')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerBeneIDAvg_OPAnnualDeductibleAmt"] = d.groupby(
        'BeneID')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerBeneIDAvg_AdmitForDays"] = d.groupby(
        'BeneID')['AdmitForDays'].transform('mean')

    # Average features grouped by OtherPhysician.

    d["PerOtherPhysicianAvg_InscClaimAmtReimbursed"] = d.groupby(
        'OtherPhysician')['InscClaimAmtReimbursed'].transform('mean')
    d["PerOtherPhysicianAvg_DeductibleAmtPaid"] = d.groupby(
        'OtherPhysician')['DeductibleAmtPaid'].transform('mean')
    d["PerOtherPhysicianAvg_IPAnnualReimbursementAmt"] = d.groupby(
        'OtherPhysician')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerOtherPhysicianAvg_IPAnnualDeductibleAmt"] = d.groupby(
        'OtherPhysician')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerOtherPhysicianAvg_OPAnnualReimbursementAmt"] = d.groupby(
        'OtherPhysician')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerOtherPhysicianAvg_OPAnnualDeductibleAmt"] = d.groupby(
        'OtherPhysician')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerOtherPhysicianAvg_AdmitForDays"] = d.groupby(
        'OtherPhysician')['AdmitForDays'].transform('mean')

    # Average features grouped by OperatingPhysician

    d["PerOperatingPhysicianAvg_InscClaimAmtReimbursed"] = d.groupby(
        'OperatingPhysician')['InscClaimAmtReimbursed'].transform('mean')
    d["PerOperatingPhysicianAvg_DeductibleAmtPaid"] = d.groupby(
        'OperatingPhysician')['DeductibleAmtPaid'].transform('mean')
    d["PerOperatingPhysicianAvg_IPAnnualReimbursementAmt"] = d.groupby(
        'OperatingPhysician')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerOperatingPhysicianAvg_IPAnnualDeductibleAmt"] = d.groupby(
        'OperatingPhysician')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerOperatingPhysicianAvg_OPAnnualReimbursementAmt"] = d.groupby(
        'OperatingPhysician')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerOperatingPhysicianAvg_OPAnnualDeductibleAmt"] = d.groupby(
        'OperatingPhysician')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerOperatingPhysicianAvg_AdmitForDays"] = d.groupby(
        'OperatingPhysician')['AdmitForDays'].transform('mean')

    # Average features grouped by AttendingPhysician

    d["PerAttendingPhysicianAvg_InscClaimAmtReimbursed"] = d.groupby(
        'AttendingPhysician')['InscClaimAmtReimbursed'].transform('mean')
    d["PerAttendingPhysicianAvg_DeductibleAmtPaid"] = d.groupby(
        'AttendingPhysician')['DeductibleAmtPaid'].transform('mean')
    d["PerAttendingPhysicianAvg_IPAnnualReimbursementAmt"] = d.groupby(
        'AttendingPhysician')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerAttendingPhysicianAvg_IPAnnualDeductibleAmt"] = d.groupby(
        'AttendingPhysician')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerAttendingPhysicianAvg_OPAnnualReimbursementAmt"] = d.groupby(
        'AttendingPhysician')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerAttendingPhysicianAvg_OPAnnualDeductibleAmt"] = d.groupby(
        'AttendingPhysician')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerAttendingPhysicianAvg_AdmitForDays"] = d.groupby(
        'AttendingPhysician')['AdmitForDays'].transform('mean')

    # Average features grouped by DiagnosisGroupCode

    d["PerDiagnosisGroupCodeAvg_InscClaimAmtReimbursed"] = d.groupby(
        'DiagnosisGroupCode')['InscClaimAmtReimbursed'].transform('mean')
    d["PerDiagnosisGroupCodeAvg_DeductibleAmtPaid"] = d.groupby(
        'DiagnosisGroupCode')['DeductibleAmtPaid'].transform('mean')
    d["PerDiagnosisGroupCodeAvg_IPAnnualReimbursementAmt"] = d.groupby(
        'DiagnosisGroupCode')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerDiagnosisGroupCodeAvg_IPAnnualDeductibleAmt"] = d.groupby(
        'DiagnosisGroupCode')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerDiagnosisGroupCodeAvg_OPAnnualReimbursementAmt"] = d.groupby(
        'DiagnosisGroupCode')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerDiagnosisGroupCodeAvg_OPAnnualDeductibleAmt"] = d.groupby(
        'DiagnosisGroupCode')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerDiagnosisGroupCodeAvg_AdmitForDays"] = d.groupby(
        'DiagnosisGroupCode')['AdmitForDays'].transform('mean')
    # Average features grouped by ClmAdmitDiagnosisCode

    d["PerClmAdmitDiagnosisCodeAvg_InscClaimAmtReimbursed"] = d.groupby(
        'ClmAdmitDiagnosisCode')['InscClaimAmtReimbursed'].transform('mean')
    d["PerClmAdmitDiagnosisCodeAvg_DeductibleAmtPaid"] = d.groupby(
        'ClmAdmitDiagnosisCode')['DeductibleAmtPaid'].transform('mean')
    d["PerClmAdmitDiagnosisCodeAvg_IPAnnualReimbursementAmt"] = d.groupby(
        'ClmAdmitDiagnosisCode')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerClmAdmitDiagnosisCodeAvg_IPAnnualDeductibleAmt"] = d.groupby(
        'ClmAdmitDiagnosisCode')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerClmAdmitDiagnosisCodeAvg_OPAnnualReimbursementAmt"] = d.groupby(
        'ClmAdmitDiagnosisCode')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerClmAdmitDiagnosisCodeAvg_OPAnnualDeductibleAmt"] = d.groupby(
        'ClmAdmitDiagnosisCode')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerClmAdmitDiagnosisCodeAvg_AdmitForDays"] = d.groupby(
        'ClmAdmitDiagnosisCode')['AdmitForDays'].transform('mean')

    d["PerClmProcedureCode_1Avg_InscClaimAmtReimbursed"] = d.groupby(
        'ClmProcedureCode_1')['InscClaimAmtReimbursed'].transform('mean')
    d["PerClmProcedureCode_1Avg_DeductibleAmtPaid"] = d.groupby(
        'ClmProcedureCode_1')['DeductibleAmtPaid'].transform('mean')
    d["PerClmProcedureCode_1Avg_IPAnnualReimbursementAmt"] = d.groupby(
        'ClmProcedureCode_1')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerClmProcedureCode_1Avg_IPAnnualDeductibleAmt"] = d.groupby(
        'ClmProcedureCode_1')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerClmProcedureCode_1Avg_OPAnnualReimbursementAmt"] = d.groupby(
        'ClmProcedureCode_1')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerClmProcedureCode_1Avg_OPAnnualDeductibleAmt"] = d.groupby(
        'ClmProcedureCode_1')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerClmProcedureCode_1Avg_AdmitForDays"] = d.groupby(
        'ClmProcedureCode_1')['AdmitForDays'].transform('mean')
    # Average features grouped by ClmDiagnosisCode_2
    d["PerClmDiagnosisCode_2Avg_InscClaimAmtReimbursed"] = d.groupby(
        'ClmDiagnosisCode_2')['InscClaimAmtReimbursed'].transform('mean')
    d["PerClmDiagnosisCode_2Avg_DeductibleAmtPaid"] = d.groupby(
        'ClmDiagnosisCode_2')['DeductibleAmtPaid'].transform('mean')
    d["PerClmDiagnosisCode_2Avg_IPAnnualReimbursementAmt"] = d.groupby(
        'ClmDiagnosisCode_2')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerClmDiagnosisCode_2Avg_IPAnnualDeductibleAmt"] = d.groupby(
        'ClmDiagnosisCode_2')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerClmDiagnosisCode_2Avg_OPAnnualReimbursementAmt"] = d.groupby(
        'ClmDiagnosisCode_2')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerClmDiagnosisCode_2Avg_OPAnnualDeductibleAmt"] = d.groupby(
        'ClmDiagnosisCode_2')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerClmDiagnosisCode_2Avg_AdmitForDays"] = d.groupby(
        'ClmDiagnosisCode_2')['AdmitForDays'].transform('mean')
    # Average features grouped by ClmDiagnosisCode_3
    d["PerClmDiagnosisCode_3Avg_InscClaimAmtReimbursed"] = d.groupby(
        'ClmDiagnosisCode_3')['InscClaimAmtReimbursed'].transform('mean')
    d["PerClmDiagnosisCode_3Avg_DeductibleAmtPaid"] = d.groupby(
        'ClmDiagnosisCode_3')['DeductibleAmtPaid'].transform('mean')
    d["PerClmDiagnosisCode_3Avg_IPAnnualReimbursementAmt"] = d.groupby(
        'ClmDiagnosisCode_3')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerClmDiagnosisCode_3Avg_IPAnnualDeductibleAmt"] = d.groupby(
        'ClmDiagnosisCode_3')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerClmDiagnosisCode_3Avg_OPAnnualReimbursementAmt"] = d.groupby(
        'ClmDiagnosisCode_3')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerClmDiagnosisCode_3Avg_OPAnnualDeductibleAmt"] = d.groupby(
        'ClmDiagnosisCode_3')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerClmDiagnosisCode_3Avg_AdmitForDays"] = d.groupby(
        'ClmDiagnosisCode_3')['AdmitForDays'].transform('mean')
    # Average features grouped by ClmDiagnosisCode_4
    d["PerClmDiagnosisCode_4Avg_InscClaimAmtReimbursed"] = d.groupby(
        'ClmDiagnosisCode_4')['InscClaimAmtReimbursed'].transform('mean')
    d["PerClmDiagnosisCode_4Avg_DeductibleAmtPaid"] = d.groupby(
        'ClmDiagnosisCode_4')['DeductibleAmtPaid'].transform('mean')
    d["PerClmDiagnosisCode_4Avg_IPAnnualReimbursementAmt"] = d.groupby(
        'ClmDiagnosisCode_4')['IPAnnualReimbursementAmt'].transform('mean')
    d["PerClmDiagnosisCode_4Avg_IPAnnualDeductibleAmt"] = d.groupby(
        'ClmDiagnosisCode_4')['IPAnnualDeductibleAmt'].transform('mean')
    d["PerClmDiagnosisCode_4Avg_OPAnnualReimbursementAmt"] = d.groupby(
        'ClmDiagnosisCode_4')['OPAnnualReimbursementAmt'].transform('mean')
    d["PerClmDiagnosisCode_4Avg_OPAnnualDeductibleAmt"] = d.groupby(
        'ClmDiagnosisCode_4')['OPAnnualDeductibleAmt'].transform('mean')
    d["PerClmDiagnosisCode_4Avg_AdmitForDays"] = d.groupby(
        'ClmDiagnosisCode_4')['AdmitForDays'].transform('mean')
    # Average Feature based on grouping based on combinations of different variables
    d["ClmCount_Provider"] = d.groupby(
        ['Provider'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID"] = d.groupby(['Provider', 'BeneID'])[
        'ClaimID'].transform('count')
    d["ClmCount_Provider_AttendingPhysician"] = d.groupby(
        ['Provider', 'AttendingPhysician'])['ClaimID'].transform('count')
    d["ClmCount_Provider_OtherPhysician"] = d.groupby(
        ['Provider', 'OtherPhysician'])['ClaimID'].transform('count')
    d["ClmCount_Provider_OperatingPhysician"] = d.groupby(
        ['Provider', 'OperatingPhysician'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmAdmitDiagnosisCode"] = d.groupby(
        ['Provider', 'ClmAdmitDiagnosisCode'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmProcedureCode_1"] = d.groupby(
        ['Provider', 'ClmProcedureCode_1'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmProcedureCode_2"] = d.groupby(
        ['Provider', 'ClmProcedureCode_2'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmProcedureCode_3"] = d.groupby(
        ['Provider', 'ClmProcedureCode_3'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmProcedureCode_4"] = d.groupby(
        ['Provider', 'ClmProcedureCode_4'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmProcedureCode_5"] = d.groupby(
        ['Provider', 'ClmProcedureCode_5'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_1"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_1'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_2"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_2'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_3"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_3'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_4"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_4'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_5"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_5'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_6"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_6'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_7"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_7'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_8"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_8'])['ClaimID'].transform('count')
    d["ClmCount_Provider_ClmDiagnosisCode_9"] = d.groupby(
        ['Provider', 'ClmDiagnosisCode_9'])['ClaimID'].transform('count')
    d["ClmCount_Provider_DiagnosisGroupCode"] = d.groupby(
        ['Provider', 'DiagnosisGroupCode'])['ClaimID'].transform('count')

    d["ClmCount_Provider_BeneID_AttendingPhysician"] = d.groupby(
        ['Provider', 'BeneID', 'AttendingPhysician'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID_OtherPhysician"] = d.groupby(
        ['Provider', 'BeneID', 'OtherPhysician'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID_AttendingPhysician_ClmProcedureCode_1"] = d.groupby(
        ['Provider', 'BeneID', 'AttendingPhysician', 'ClmProcedureCode_1'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID_AttendingPhysician_ClmDiagnosisCode_1"] = d.groupby(
        ['Provider', 'BeneID', 'AttendingPhysician', 'ClmDiagnosisCode_1'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID_OperatingPhysician"] = d.groupby(
        ['Provider', 'BeneID', 'OperatingPhysician'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID_ClmProcedureCode_1"] = d.groupby(
        ['Provider', 'BeneID', 'ClmProcedureCode_1'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID_ClmDiagnosisCode_1"] = d.groupby(
        ['Provider', 'BeneID', 'ClmDiagnosisCode_1'])['ClaimID'].transform('count')
    d["ClmCount_Provider_BeneID_ClmDiagnosisCode_1_ClmProcedureCode_1"] = d.groupby(
        ['Provider', 'BeneID', 'ClmDiagnosisCode_1', 'ClmProcedureCode_1'])['ClaimID'].transform('count')
    return d
