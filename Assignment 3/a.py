#Â Decimals and Fractions are precise ways of calculating in Python.
#Â This is what I prefer in order to calculate necessities correctly.
from decimal import Decimal
from decimal import *
from fractions import Fraction

patients_data_list = []
keys = []

def patient_returner(name):
    if name in keys:
        i = keys.index(name)
        patient_data_list = patients_data_list[i]
        return i, patient_data_list
    else:
        return None, None

# How many tabs occupied by the given string?
def occupied_tabs(cell_string):
    length = len(cell_string)
    occupied_tabs = int(length / 4)
    return occupied_tabs

#Â name, disease, treatment fields occupy total of 2, 4, 4 tabs.
# Returns required tab counts for name, disease, treatment fields.
def calculate_tabs(name, disease, treatment):
    
    name_occupied_tabs = occupied_tabs(name)
    disease_occupied_tabs = occupied_tabs(disease)
    treatment_occupied_tabs = occupied_tabs(treatment)
    
    return (2 - name_occupied_tabs), (4 - disease_occupied_tabs), (4 - treatment_occupied_tabs)
    

def read_input():
    with open("doctors_aid_inputs.txt", "r") as inputs_file:
        input_lines = inputs_file.read().splitlines()
    return input_lines


def write_output(output_lines):
    with open("doctors_aid_outputs.txt", "w") as outputs_file:
        outputs_file.writelines(output_lines)


#Â "Hayriye, 0.999, Breast Cancer, 50/100000, Surgery, 0.40"
def create(line_string):
    patient_data_list = line_string.split(", ")
    patient_name = patient_data_list[0]
    
    i, p_data = patient_returner(patient_name)
    
    if p_data:
        return False
    else:
        patients_data_list.append(patient_data_list)
        keys.append(patient_name)
        return True


def remove(name):
    i, patient = patient_returner(name)
    
    if patient:
        patients_data_list.pop(i)
        keys.pop(i)
        return True
    else:
        return False


def probability(name):
    i, patient = patient_returner(name)
    
    if patient:
        diagnosis_accuracy = Decimal(patient[1])
        disease_incidence = Decimal(eval(patient[3]))
        
        TP = diagnosis_accuracy * disease_incidence
        FP = (1 - diagnosis_accuracy) * (1 - disease_incidence)
        probability = TP / (TP + FP)
        
        return Decimal(probability).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
    else:
        return False


def recommend(name):
    i, patient = patient_returner(name)
    
    if patient:
        disease_probability = probability(name)
        treatment_risk = patient[5]
        
        if float(disease_probability) >= float(treatment_risk):
            return True
        else:
            return False
    else:
        return -1
    
# Max Patient Name: "Hayriye"(7) / Max Disease Name:"Prostate Cancer"(15) / Max Treatment Name: "Targeted Therapy"(16)
# Patient Name Area (8) = 2 Tabs / Disease Name Area (16) = 4 Tabs / Treatment Name Area (16) = 4 Tabs
# Tabs are (4)
def printing_list():
    
    table = """Patient\tDiagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment
Name\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk
-------------------------------------------------------------------------
"""
    for patient in patients_data_list:
        name = patient[0]
        accuracy = float(patient[1]) * 100
        disease = patient[2]
        incidence = patient[3]
        treatment = patient[4]
        risk = str(int(float(patient[5]) * 100))
        
        tab1, tab2, tab3 = calculate_tabs(name, disease, treatment)
        tab1, tab2, tab3 = ("\t" * tab1), ("\t" * tab2), ("\t" * tab3)
        
        table += f'{name}{tab1}{accuracy:.2f}%\t\t{disease}{tab2}{incidence}\t{treatment}{tab3}{risk}%\n'
    
    return table


def command_checker(line):

    if line != "list":
        command, line_string = line.split(" ", maxsplit=1)[0], line.split(" ", maxsplit=1)[1]
    # Listing
    else:
        table = printing_list()
        return table
    
    
    # Creating
    if command == "create":
        iscreated = create(line_string)
        name = line_string.split(", ", maxsplit=1)[0]
        
        if iscreated:
            return "Patient {} is recorded.\n".format(name)
        else:
            return "Patient {} cannot be recorded due to duplication.\n".format(name)
      
    # Removing
    elif command == "remove":
        isremoved = remove(line_string)
        
        if isremoved:
            return "Patient {} is removed.\n".format(line_string)
        else:
            return "Patient {} cannot be removed due to absence.\n".format(line_string)
    
    # calculating Probability
    elif command == "probability":
        p = probability(line_string)
        
        if p:
            p = Fraction(p * 100)
            
            i, p_data = patient_returner(line_string)
            disease = p_data[2]
            
            if p.denominator == 1:
                return "Patient {} has a probability of {}% of having {}.\n".format(line_string, p, disease.lower())
            else:
                return "Patient {} has a probability of {}% of having {}.\n".format(line_string, round(float(p), 2), disease.lower())
                
        else:
            return "Probability for {} cannot be calculated due to absence.\n".format(line_string)
    
    # Giving Recommendation
    elif command == "recommendation":
        r = recommend(line_string)
        if r == -1:
            return "Recommendation for {} cannot be calculated due to absence.\n".format(line_string)
        elif r:
            return "System suggests {} to have the treatment.\n".format(line_string)
        else:
            return "System suggests {} NOT to have the treatment.\n".format(line_string)
    else:
        # This part is actually error handling. But out of scope now.
        return ""



# This is the Main script part.
input_file_lines = read_input()
output_file_lines = ""

for input_line in input_file_lines:
    output_file_lines += command_checker(input_line)
    
write_output(output_file_lines)
# Finish!
    
    