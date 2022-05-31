import os
import sys
# for moving files
import shutil
# For logging
import logging
# config file parser
from configparser import ConfigParser
from datetime import datetime
#xlsx
import xlsxwriter
# table
from tabulate import tabulate
# Parsing
from docx_file_job import DocxFileJob
from docx_file_folder import DocxFileFolder
from xml_file_job import XmlFileJob
from xml_file_folder import XmlFileFolder


class ValidateFolder():

    def __init__(self,dir_to_validate):
        self.xml_path = []
        self.docx_path = []
        self.dir_to_validate = dir_to_validate


    def absolute_paths(self):
        raw_folder_files = os.listdir(self.dir_to_validate)
        abs_path_files = []
        for path in raw_folder_files:
            full_path = os.path.join(self.dir_to_validate,path)
            abs_path_files.append(full_path)
        return abs_path_files


    def validate_dir_files(self):
        folder_files = self.absolute_paths()
        if folder_files:
            for files in folder_files:
                if files.endswith(".xml"):
                    self.xml_path.append(files)
                if files.endswith(".docx"):
                    self.docx_path.append(files)
            if len(self.xml_path) != 0 and len(self.docx_path) != 0:
                if len(self.xml_path) == len(self.docx_path):
                    if all(item in raw_paths(self.xml_path) for item in raw_paths(self.docx_path)):
                        logger("folder","info","Files are ready to be validated")
                        return True
                    else:
                        print("Error Occurred, some files does not have a matching workload document")
                        logger("folder","error","Error Occurred, some files does not have a matching workload document")
                        return False
                else:
                    print("Error Occurred, number of files do not match")
                    logger("folder","error","Error Occurred, number of files do not match")
                    return False
            else:
                print("Error Occurred, No valid files inside directory")
                logger("folder","error","Error Occurred, No valid files inside directory")
                return False
        else:
            print("Error Occured, there are no files in the directory")
            logger("folder","error","Error Occurred, there are no files in the directory")
            return False

    def validate_folder_files(self):
        res_list = []
        logger("folder","info","Setting up the folder files")
        for xml_path in self.xml_path:
            for docx_path in self.docx_path:
                xml_base = os.path.basename(xml_path).removesuffix(".xml")
                if xml_base in docx_path:
                    xml = XmlFileFolder(xml_path)
                    xml_basename = xml.file_basename()
                    docx = DocxFileFolder(docx_path)
                    docx_basename = docx.file_basename()
                    try:
                        if xml.validate_xml_file() and docx.validate_docx_file():
                            # Not Finished not included
                            validations = {"Folder Name" : compare(xml.get_folder_name(),docx.get_folder_name()),
                                           "Description" : compare(xml.get_description(),docx.get_description()),
                                           "Job Names" : check_list(xml.get_job_names(),docx.get_job_names()),
                                           "Calendar" : compare(xml.get_calendar(),docx.get_calendar()),
                                           "From Time" : compare(xml.get_from_time(),docx.get_from_time()),
                                           "To Time" : compare(xml.get_to_time(),docx.get_to_time()),
                                           "Prerequisites" : check_list(xml.get_in_condition(),docx.get_in_condition()),
                                           "Not Submitted By" : compare(xml.get_not_submitted(),docx.get_not_submitted()),
                                           "Execution Time" : compare(xml.get_execution_time(),docx.get_execution_time())}
                            temp_list = []
                            for key,value in validations.items():
                                res = key + " : " + str(value)
                                temp_list.append(res)
                            parsed_values = "\n".join(temp_list)
                            if all(validations.values()):
                                val = (xml_basename,docx_basename,parsed_values,"Values Match")
                            else:
                                val = (xml_basename,docx_basename,parsed_values,"Contains Discrepancies")
                        else:
                            logger("folder","warning",f"Error occurred: {xml_basename} and {docx_basename}, Please Check file format")
                            val = (xml_basename,docx_basename,"Invalid Format","Invalid Format")
                    except TypeError:
                        logger("folder","warning",f"Type Error occurred: {xml_basename} and {docx_basename}, Please Check file format")
                        val = (xml_basename,docx_basename,"Invalid Format","Invalid Format")
                    except IndexError:
                        logger("folder","warning",f"Index Error occurred: {xml_basename} and {docx_basename}, Please Check file format")
                        val = (xml_basename,docx_basename,"Invalid Format","Invalid Format")
                    res_list.append(val)
        logger("folder","info","Validation Complete")
        return res_list

    def get_xml_files(self):
        return self.xml_path


    def get_docx_files(self):
        return self.docx_path


    def get_dir(self):
        return self.dir_to_validate


    def get_all_files(self):
        all_files = self.xml_path + self.docx_path
        return all_files



class ValidateJob():

    def __init__(self,dir_to_validate,parameter):
        self.xml_path = []
        self.docx_path = []
        self.dir_to_validate = dir_to_validate
        self.param = parameter


    def absolute_paths(self):
        raw_folder_files = os.listdir(self.dir_to_validate)
        abs_path_files = []
        for path in raw_folder_files:
            full_path = os.path.join(self.dir_to_validate,path)
            abs_path_files.append(full_path)
        return abs_path_files


    def validate_dir_files(self):
        folder_files = self.absolute_paths()
        if folder_files:
            for files in folder_files:
                if files.endswith(".xml"):
                    self.xml_path.append(files)
                if files.endswith(".docx"):
                    self.docx_path.append(files)
            if len(self.xml_path) != 0 and len(self.docx_path) != 0:
                if len(self.xml_path) == len(self.docx_path):
                    if all(item in raw_paths(self.xml_path) for item in raw_paths(self.docx_path)):
                        logger("job","info","Files are ready to be validated")
                        return True
                    else:
                        print("Error Occurred, some files does not have a matching workload document")
                        logger("job","error","Error Occurred, some files does not have a matching workload document")
                        return False
                else:
                    print("Error Occurred, number of files do not match")
                    logger("job","error","Error Occurred, number of files do not match")
                    return False
            else:
                print("Error Occurred, No valid files inside the directory")
                logger("job","error","Error Occurred, No valid files inside the directory")
                return False
        else:
            print("Error Occurred, there are no files in the directory")
            logger("job","error","Error Occurred, there are no files in the directory")
            return False


    def validate_job_files(self):
        res_list = []
        logger("job","info","Setting up the folder files")
        for xml_path in self.xml_path:
            for docx_path in self.docx_path:
                xml_base = os.path.basename(xml_path).removesuffix(".xml")
                if xml_base in docx_path:
                    xml = XmlFileJob(xml_path)
                    xml_basename = xml.file_basename()
                    docx = DocxFileJob(docx_path)
                    docx_basename = docx.file_basename()
                    try:
                        if xml.validate_xml_file() and docx.validate_docx_file():
                            # Not Finished not included
                            validations = {"Job Name" : compare(xml.get_job_name(),docx.get_job_name()),
                                          "Folder Name" : compare(xml.get_folder_name(),docx.get_folder_name()),
                                          "Description" : compare(xml.get_description(),docx.get_description()),
                                          "Calendar" : compare(xml.get_calendar(),docx.get_calendar()),
                                          "From Time" : compare(xml.get_from_time(),docx.get_from_time()),
                                          "To Time" : compare(xml.get_to_time(),docx.get_to_time()),
                                          "Cyclic" : compare(xml.get_cyclic(),docx.get_cyclic()),
                                          "Prerequisites" : check_list(xml.get_in_condition(),docx.get_in_condition()),
                                          "Not Submitted By" : compare(xml.get_not_submitted(),docx.get_not_submitted()),
                                          "Execution Time" : compare(xml.get_execution_time(),docx.get_execution_time())}
                            if self.param == "prod":
                                validations["CMD Script(PRD)"] = compare(xml.get_command_prd(),docx.get_command_prd())
                                validations["Parameters(PRD)"] = compare(xml.get_param_prd(),docx.get_param_prd())
                                if compare(xml.get_prd_nodeid(),docx.get_prd_hostgroup()) or compare(xml.get_prd_nodeid(),docx.get_prd_hostname()):
                                    validations["PRD"] = True
                                else:
                                    validations["PRD"] = False
                            elif self.param == "dev":
                                validations["CMD Script(NON-PRD)"] = compare(xml.get_command_nonprd(),docx.get_command_nonprd())
                                validations["Parameters(NON-PRD)"] = compare(xml.get_param_nonprd(),docx.get_param_nonprd())
                                if compare(xml.get_nonprd_nodeid(),docx.get_nonprd_hostgroup()) or compare(xml.get_nonprd_nodeid(),docx.get_nonprd_hostname()):
                                    validations["NON-PRD"] = True
                                else:
                                    validations["NON-PRD"] = False
                            temp_list = []
                            for key,value in validations.items():
                                res = key + " : " + str(value)
                                temp_list.append(res)
                            parsed_values = "\n".join(temp_list)
                            if all(validations.values()):
                                val = (xml_basename,docx_basename,parsed_values,"Values Match")
                            else:
                                val = (xml_basename,docx_basename,parsed_values,"Contains Discrepancies")
                        else:
                            logger("job","warning",f"Error occurred: {xml_basename} and {docx_basename}, Please Check file format")
                            val = (xml_basename,docx_basename,"Invalid Format","Invalid Format")
                    except TypeError:
                        logger("job","warning",f"Type Error occurred: {xml_basename} and {docx_basename}, Please Check file format")
                        val = (xml_basename,docx_basename,"Invalid Format","Invalid Format")
                    except IndexError:
                        logger("job","warning",f"Index Error occurred: {xml_basename} and {docx_basename}, Please Check file format")
                        val = (xml_basename,docx_basename,"Invalid Format","Invalid Format")
                    res_list.append(val)
        logger("job","info","Validation Complete")
        return res_list


    def get_xml_files(self):
        return self.xml_path


    def get_docx_files(self):
        return self.docx_path


    def get_dir(self):
        return self.dir_to_validate

    def get_all_files(self):
        all_files = self.xml_path + self.docx_path
        return all_files


# Global Functions
def compare(xml_value,doc_value):
    if xml_value == doc_value:
        return True
    return False


def check_list(xml_list,docx_list):
    if all(item in xml_list for item in docx_list):
        return True
    return False


def raw_paths(list_box):
    raw_filename_list = []
    for paths in list_box:
        basename = os.path.basename(paths)
        file_split = basename.split(".")
        raw_filename_list.append(file_split[0])
    return raw_filename_list


def save(file_dnt,file_type,directory,save_list):
    if file_type == "folder":
        logger("folder","info","Creating file")
        file_name = "CM_Validation_Folder - " + file_dnt
    elif file_type == "job":
        logger("folder","info","Creating file")
        file_name = "CM_Validation_Job - " + file_dnt
    fin_name = directory +"/"+ file_name + ".xlsx"
    out_workbook = xlsxwriter.Workbook(fin_name)
    out_sheet = out_workbook.add_worksheet()

    out_sheet.write("A1","Xml File")
    out_sheet.write("B1","Docx File")
    out_sheet.write("C1","Result")
    out_sheet.write("D1","Remarks")

    for ind,item in enumerate(save_list):
        out_sheet.write(ind+1, 0,item[0])
        out_sheet.write(ind+1, 1,item[1])
        out_sheet.write(ind+1, 2,item[2])
        out_sheet.write(ind+1, 3,item[3])
    out_workbook.close()
    print(f"File saved at {fin_name}")
    print()


def logger(val_type,level,msg):
    if val_type == "folder":
        log_folder_path = config_paths["folder_logs"]
        logging.basicConfig(level=logging.DEBUG,
                        format="{asctime} {levelname:<8} {message}",
                        style="{",
                        filename=log_folder_path + date_time + "Folder_logs.log",
                        filemode="w")
    elif val_type == "job":
        log_job_path = config_paths["job_logs"]
        logging.basicConfig(level=logging.DEBUG,
                        format="{asctime} {levelname:<8} {message}",
                        style="{",
                        filename=log_job_path + date_time + "Job_logs.log",
                        filemode="w")

    if level == "info":
        logging.info(msg)
    elif level == "warning":
        logging.warning(msg)
    elif level == "error":
        logging.error(msg)


def check_parameter():
    try:
        parameter = sys.argv[1].lower()
        if parameter == "prod":
            return "prod"
        elif parameter == "dev":
            return "dev"
        else:
            return "invalid"
    except IndexError:
        return "folder"

def check_config(file_path):
    try:
        config = ConfigParser()
        config.read(file_path)
        bol = True
        dic_path = {"folder_files" : config["folder"]["files"],
                    "folder_archive" : config["folder"]["archive"],
                    "folder_excel" : config["folder"]["excel"],
                    "folder_logs" : config["folder"]["logs"],

                    "job_files" : config["job"]["files"],
                    "job_archive" : config["job"]["archive"],
                    "job_excel" : config["job"]["excel"],
                    "job_logs" : config["job"]["logs"]}

        for key,path in dic_path.items():
            if not os.path.exists(path):
                print(path)
                print(key,"has an invalid path")
                bol = False
            else:
                bol = True
            if not bol:
                break
        return bol,dic_path
    except FileNotFoundError:
        print("Config file not found")
        return False
    except IOError:
        print("Config file cannot be accessed")
        return False
    except KeyError:
        print("Config file not found")
        return False


def move_to_archive(file_list,destination_path):
    for files in file_list:
        shutil.move(files,destination_path)
    print()
    print("Files has been moved to archive folder")

def display_result(result_list):
    headers = ["XML Files","Docx Files","Result","Remarks"]
    return tabulate(result_list,headers=headers)


# Main
if __name__ == "__main__":
    config_file = "cm_validation_config.ini"
    try:
        if check_config(config_file)[0]:
            config_paths = check_config(config_file)[1]
        else:
            print("Exiting automation..")
            quit()
    except TypeError:
        print("Error in accessing config file")
        quit()

    script_param = check_parameter()
    now = datetime.now()
    date_time = now.strftime("%m%d%Y%H%M%S")

    if script_param == "folder":
        print()
        print("Validating: Folders")
        folder_dir_path = config_paths["folder_files"]

        folder_validate = ValidateFolder(folder_dir_path)
        if folder_validate.validate_dir_files():
            print()
            directory_path = folder_validate.get_dir()
            validation = folder_validate.validate_folder_files()
            logger("folder","info","\n" + display_result(validation))
            save(date_time,"folder",config_paths["folder_excel"],validation)
            logger("folder","info","Folder Validation Result has been saved")
            move_to_archive(folder_validate.get_all_files(),config_paths["folder_archive"])
            logger("folder","info","Folder Files has been moved to archive")
            logger("folder","info","Done Thank you!")
        print("Done, Thank you!")

    elif script_param == "prod" or script_param == "dev":
        print()
        print("Validating: Jobs")
        job_dir_path = config_paths["job_files"]

        job_validate = ValidateJob(job_dir_path,script_param)
        if job_validate.validate_dir_files():
            print()
            directory_path = job_validate.get_dir()
            validation = job_validate.validate_job_files()
            logger("job","info","\n\n" + display_result(validation))
            save(date_time,"job",config_paths["job_excel"],validation)
            logger("job","info","Job Validation Result has been saved")
            move_to_archive(job_validate.get_all_files(),config_paths["job_archive"])
            logger("job","info","Job Files has been moved to archive")
            logger("job","info","Done Thank you!")
        print("Done, Thank you!")
    else:
        print()
        print("Invalid Parameter!")
        quit()
