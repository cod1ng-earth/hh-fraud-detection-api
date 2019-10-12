# -*- coding: utf-8 -*-
"""Cleaning_Feature_engineering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cyB8vww3lA0GhABA0mGJluHjfA0VnY5u
"""

from scipy import stats
import pickle
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os

#import scipy as sc
#import seaborn as sns
#import matplotlib.pyplot as plt
# To check data distributions and correlations
#import pandas_profiling as profile

import warnings     # for supressing a warning when importing large files
warnings.filterwarnings("ignore")
# Load Train Dataset


#Train=pd.read_csv("gdrive/My Drive/Healthhackathon19/data/Train-1542865627584.csv")
#Train_Beneficiarydata=pd.read_csv("gdrive/My Drive/Healthhackathon19/data/Train_Beneficiarydata-1542865627584.csv")
#Train_Inpatientdata=pd.read_csv("gdrive/My Drive/Healthhackathon19/data/Train_Inpatientdata-1542865627584.csv")
#Train_Outpatientdata=pd.read_csv("gdrive/My Drive/Healthhackathon19/data/Train_Outpatientdata-1542865627584.csv")

# BENEFICIARY DATA
# Replacing 2 with 0 for chronic conditions ,that means chroniv condition No is 0 and yes is 1

def transform(ClaimData):
    ClaimData = pd.DataFrame(ClaimData)
    ClaimData = ClaimData.replace({'ChronicCond_Alzheimer': 2, 'ChronicCond_Heartfailure': 2, 'ChronicCond_KidneyDisease': 2,
                                   'ChronicCond_Cancer': 2, 'ChronicCond_ObstrPulmonary': 2, 'ChronicCond_Depression': 2,
                                   'ChronicCond_Diabetes': 2, 'ChronicCond_IschemicHeart': 2, 'ChronicCond_Osteoporasis': 2,
                                   'ChronicCond_rheumatoidarthritis': 2, 'ChronicCond_stroke': 2}, 0)

    ClaimData = ClaimData.replace({'RenalDiseaseIndicator': 'Y'}, 1)
# Lets Create Age column to the dataset
    return ClaimData

    ClaimData['DOB'] = pd.to_datetime(
        ClaimData['DOB'], format='%Y-%m-%d')
    ClaimData['DOD'] = pd.to_datetime(
        ClaimData['DOD'], format='%Y-%m-%d', errors='ignore')
    ClaimData['Age'] = round(
        ((ClaimData['DOD'] - ClaimData['DOB']).dt.days)/365)


# As we see that last DOD value is 2009-12-01 ,which means Beneficiary Details data is of year 2009.
# so we will calculate age of other benficiaries for year 2009.

    ClaimData.Age.fillna(round(((pd.to_datetime('2009-12-01', format='%Y-%m-%d') - Train_Beneficiarydata['DOB']).dt.days)/365),
                         inplace=True)


# Lets create a new variable 'WhetherDead' with flag 1 means Dead and 0 means not Dead

    ClaimData.loc[Train_Beneficiarydata.DOD.isna(), 'WhetherDead'] = 0
    ClaimData.loc[Train_Beneficiarydata.DOD.notna(), 'WhetherDead'] = 1

    return ClaimData


# INPATIENT/OUTPATIENT
# As patient can be admitted for only for 1 day,we will add 1 to the difference of Discharge Date and Admission Date

    Train_Inpatientdata['AdmissionDt'] = pd.to_datetime(
        Train_Inpatientdata['AdmissionDt'], format='%Y-%m-%d')
    Train_Inpatientdata['DischargeDt'] = pd.to_datetime(
        Train_Inpatientdata['DischargeDt'], format='%Y-%m-%d')
    Train_Inpatientdata['AdmitForDays'] = (
        (Train_Inpatientdata['DischargeDt'] - Train_Inpatientdata['AdmissionDt']).dt.days)+1

    Key_Column_To_Merge_Outpatient = Train_Outpatientdata.columns
    # Lets make union of Inpatienta and outpatient data .
    # We will use all keys in outpatient data as we want to make union and dont want duplicate columns from both tables.

    Train_Allpatientdata = pd.merge(Train_Outpatientdata, Train_Inpatientdata,
                                    left_on=['BeneID', 'ClaimID', 'ClaimStartDt', 'ClaimEndDt', 'Provider',
                                             'InscClaimAmtReimbursed', 'AttendingPhysician', 'OperatingPhysician',
                                             'OtherPhysician', 'ClmDiagnosisCode_1', 'ClmDiagnosisCode_2',
                                             'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5',
                                             'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7', 'ClmDiagnosisCode_8',
                                             'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10', 'ClmProcedureCode_1',
                                             'ClmProcedureCode_2', 'ClmProcedureCode_3', 'ClmProcedureCode_4',
                                             'ClmProcedureCode_5', 'ClmProcedureCode_6', 'DeductibleAmtPaid',
                                             'ClmAdmitDiagnosisCode'],
                                    right_on=['BeneID', 'ClaimID', 'ClaimStartDt', 'ClaimEndDt', 'Provider',
                                              'InscClaimAmtReimbursed', 'AttendingPhysician', 'OperatingPhysician',
                                              'OtherPhysician', 'ClmDiagnosisCode_1', 'ClmDiagnosisCode_2',
                                              'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5',
                                              'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7', 'ClmDiagnosisCode_8',
                                              'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10', 'ClmProcedureCode_1',
                                              'ClmProcedureCode_2', 'ClmProcedureCode_3', 'ClmProcedureCode_4',
                                              'ClmProcedureCode_5', 'ClmProcedureCode_6', 'DeductibleAmtPaid',
                                              'ClmAdmitDiagnosisCode'], how='outer')

    # Lets merge All patient data with beneficiary details data based on 'BeneID' as joining key for inner join
    Train_AllPatientDetailsdata = pd.merge(
        Train_Allpatientdata, Train_Beneficiarydata, left_on='BeneID', right_on='BeneID', how='inner')

    # Lets merge patient data with fradulent providers details data with "Provider" as joining key for inner join

    Train_ProviderWithPatientDetailsdata = pd.merge(
        Train, Train_AllPatientDetailsdata, on='Provider')

    Train_ProviderWithPatientDetailsdata.head()

    """#Feature Engineering"""

    Train_ProviderWithPatientDetailsdata["PerProviderAvg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_Age"] = Train_ProviderWithPatientDetailsdata.groupby('Provider')[
        'Age'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_NoOfMonths_PartACov"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['NoOfMonths_PartACov'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_NoOfMonths_PartBCov"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['NoOfMonths_PartBCov'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerProviderAvg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'Provider')['AdmitForDays'].transform('mean')

    # Grouping based on BeneID explains amounts involved per beneficiary.Reason to derive this feature is that one beneficiary
    # can go to multiple providers and can be involved in fraud cases
    Train_ProviderWithPatientDetailsdata["PerBeneIDAvg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'BeneID')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerBeneIDAvg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'BeneID')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerBeneIDAvg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'BeneID')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerBeneIDAvg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'BeneID')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerBeneIDAvg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'BeneID')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerBeneIDAvg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'BeneID')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerBeneIDAvg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby('BeneID')[
        'AdmitForDays'].transform('mean')

    # Average features grouped by OtherPhysician.

    Train_ProviderWithPatientDetailsdata["PerOtherPhysicianAvg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OtherPhysician')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOtherPhysicianAvg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OtherPhysician')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOtherPhysicianAvg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OtherPhysician')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOtherPhysicianAvg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OtherPhysician')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOtherPhysicianAvg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OtherPhysician')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOtherPhysicianAvg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OtherPhysician')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOtherPhysicianAvg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OtherPhysician')['AdmitForDays'].transform('mean')

    # Average features grouped by OperatingPhysician

    Train_ProviderWithPatientDetailsdata["PerOperatingPhysicianAvg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OperatingPhysician')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOperatingPhysicianAvg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OperatingPhysician')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOperatingPhysicianAvg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OperatingPhysician')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOperatingPhysicianAvg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OperatingPhysician')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOperatingPhysicianAvg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OperatingPhysician')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOperatingPhysicianAvg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OperatingPhysician')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerOperatingPhysicianAvg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'OperatingPhysician')['AdmitForDays'].transform('mean')

    # Average features grouped by AttendingPhysician

    Train_ProviderWithPatientDetailsdata["PerAttendingPhysicianAvg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'AttendingPhysician')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerAttendingPhysicianAvg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'AttendingPhysician')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerAttendingPhysicianAvg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'AttendingPhysician')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerAttendingPhysicianAvg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'AttendingPhysician')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerAttendingPhysicianAvg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'AttendingPhysician')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerAttendingPhysicianAvg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'AttendingPhysician')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerAttendingPhysicianAvg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'AttendingPhysician')['AdmitForDays'].transform('mean')

    # Average features grouped by DiagnosisGroupCode

    Train_ProviderWithPatientDetailsdata["PerDiagnosisGroupCodeAvg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'DiagnosisGroupCode')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerDiagnosisGroupCodeAvg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'DiagnosisGroupCode')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerDiagnosisGroupCodeAvg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'DiagnosisGroupCode')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerDiagnosisGroupCodeAvg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'DiagnosisGroupCode')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerDiagnosisGroupCodeAvg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'DiagnosisGroupCode')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerDiagnosisGroupCodeAvg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'DiagnosisGroupCode')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerDiagnosisGroupCodeAvg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'DiagnosisGroupCode')['AdmitForDays'].transform('mean')

    # Average features grouped by ClmAdmitDiagnosisCode

    Train_ProviderWithPatientDetailsdata["PerClmAdmitDiagnosisCodeAvg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmAdmitDiagnosisCode')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmAdmitDiagnosisCodeAvg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmAdmitDiagnosisCode')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmAdmitDiagnosisCodeAvg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmAdmitDiagnosisCode')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmAdmitDiagnosisCodeAvg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmAdmitDiagnosisCode')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmAdmitDiagnosisCodeAvg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmAdmitDiagnosisCode')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmAdmitDiagnosisCodeAvg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmAdmitDiagnosisCode')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmAdmitDiagnosisCodeAvg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmAdmitDiagnosisCode')['AdmitForDays'].transform('mean')

    Train_ProviderWithPatientDetailsdata["PerClmProcedureCode_1Avg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmProcedureCode_1')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmProcedureCode_1Avg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmProcedureCode_1')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmProcedureCode_1Avg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmProcedureCode_1')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmProcedureCode_1Avg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmProcedureCode_1')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmProcedureCode_1Avg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmProcedureCode_1')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmProcedureCode_1Avg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmProcedureCode_1')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmProcedureCode_1Avg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmProcedureCode_1')['AdmitForDays'].transform('mean')

    # Average features grouped by ClmDiagnosisCode_2

    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_2Avg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_2')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_2Avg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_2')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_2Avg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_2')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_2Avg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_2')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_2Avg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_2')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_2Avg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_2')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_2Avg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_2')['AdmitForDays'].transform('mean')

    # Average features grouped by ClmDiagnosisCode_3

    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_3Avg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_3')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_3Avg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_3')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_3Avg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_3')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_3Avg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_3')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_3Avg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_3')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_3Avg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_3')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_3Avg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_3')['AdmitForDays'].transform('mean')

    # Average features grouped by ClmDiagnosisCode_4

    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_4Avg_InscClaimAmtReimbursed"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_4')['InscClaimAmtReimbursed'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_4Avg_DeductibleAmtPaid"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_4')['DeductibleAmtPaid'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_4Avg_IPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_4')['IPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_4Avg_IPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_4')['IPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_4Avg_OPAnnualReimbursementAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_4')['OPAnnualReimbursementAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_4Avg_OPAnnualDeductibleAmt"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_4')['OPAnnualDeductibleAmt'].transform('mean')
    Train_ProviderWithPatientDetailsdata["PerClmDiagnosisCode_4Avg_AdmitForDays"] = Train_ProviderWithPatientDetailsdata.groupby(
        'ClmDiagnosisCode_4')['AdmitForDays'].transform('mean')

    # Average Feature based on grouping based on combinations of different variables

    Train_ProviderWithPatientDetailsdata["ClmCount_Provider"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_AttendingPhysician"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'AttendingPhysician'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_OtherPhysician"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'OtherPhysician'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_OperatingPhysician"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'OperatingPhysician'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmAdmitDiagnosisCode"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmAdmitDiagnosisCode'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmProcedureCode_1"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmProcedureCode_1'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmProcedureCode_2"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmProcedureCode_2'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmProcedureCode_3"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmProcedureCode_3'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmProcedureCode_4"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmProcedureCode_4'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmProcedureCode_5"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmProcedureCode_5'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_1"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_1'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_2"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_2'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_3"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_3'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_4"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_4'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_5"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_5'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_6"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_6'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_7"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_7'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_8"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_8'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_ClmDiagnosisCode_9"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'ClmDiagnosisCode_9'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_DiagnosisGroupCode"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'DiagnosisGroupCode'])['ClaimID'].transform('count')

    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_AttendingPhysician"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'AttendingPhysician'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_OtherPhysician"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'OtherPhysician'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_AttendingPhysician_ClmProcedureCode_1"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'AttendingPhysician', 'ClmProcedureCode_1'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_AttendingPhysician_ClmDiagnosisCode_1"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'AttendingPhysician', 'ClmDiagnosisCode_1'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_OperatingPhysician"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'OperatingPhysician'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_ClmProcedureCode_1"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'ClmProcedureCode_1'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_ClmDiagnosisCode_1"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'ClmDiagnosisCode_1'])['ClaimID'].transform('count')
    Train_ProviderWithPatientDetailsdata["ClmCount_Provider_BeneID_ClmDiagnosisCode_1_ClmProcedureCode_1"] = Train_ProviderWithPatientDetailsdata.groupby(
        ['Provider', 'BeneID', 'ClmDiagnosisCode_1', 'ClmProcedureCode_1'])['ClaimID'].transform('count')

    Train_ProviderWithPatientDetailsdata.head()

    # Lets impute numeric columns with 0

    cols1 = Train_ProviderWithPatientDetailsdata.select_dtypes(
        [np.number]).columns
    cols2 = Train_ProviderWithPatientDetailsdata.select_dtypes(
        exclude=[np.number]).columns

    Train_ProviderWithPatientDetailsdata[cols1] = Train_ProviderWithPatientDetailsdata[cols1].fillna(
        value=0)

    # Lets remove unnecessary columns ,as we grouped based on these columns and derived maximum infromation from them.

    cols = Train_ProviderWithPatientDetailsdata.columns
    cols[:58]

    remove_these_columns = ['BeneID', 'ClaimID', 'ClaimStartDt', 'ClaimEndDt', 'AttendingPhysician',
                            'OperatingPhysician', 'OtherPhysician', 'ClmDiagnosisCode_1',
                            'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4',
                            'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7',
                            'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10',
                            'ClmProcedureCode_1', 'ClmProcedureCode_2', 'ClmProcedureCode_3',
                            'ClmProcedureCode_4', 'ClmProcedureCode_5', 'ClmProcedureCode_6',
                            'ClmAdmitDiagnosisCode', 'AdmissionDt',
                            'DischargeDt', 'DiagnosisGroupCode', 'DOB', 'DOD',
                            'State', 'County']

    Train_category_removed = Train_ProviderWithPatientDetailsdata.drop(
        axis=1, columns=remove_these_columns)

    # Lets Convert types of gender and race to categorical.

    Train_category_removed.Gender = Train_category_removed.Gender.astype(
        'category')
    Train_category_removed.Race = Train_category_removed.Race.astype(
        'category')

    # Lets create dummies for categorrical columns.

    Train_category_removed = pd.get_dummies(Train_category_removed, columns=[
                                            'Gender', 'Race'], drop_first=True)

    Train_category_removed.PotentialFraud.replace(
        ['Yes', 'No'], ['1', '0'], inplace=True)
    Train_category_removed.PotentialFraud = Train_category_removed.PotentialFraud.astype(
        'int64')

    """#Data Aggregation"""

    # Lets aggregate claims data to unique providers.

    Train_category_removed_groupedbyProv_PF = Train_category_removed.groupby(
        ['Provider', 'PotentialFraud'], as_index=False).agg('mean')