import xml.etree.ElementTree as ET
import os


# Alerts yet to be included
class XmlFileFolder:

    def __init__(self,file_path):
        self.file_path = file_path
        tree = ET.parse(file_path)
        global root
        root = tree.getroot()


    def validate_xml_file(self):
        if root.tag == "DEFTABLE":
            if root.find("SMART_FOLDER"):
                return True
        return False


    def get_folder_name(self):
        return root[1].attrib["FOLDER_NAME"]


    def get_description(self):
        if "DESCRIPTION" in root[1].attrib:
            return root[1].attrib["DESCRIPTION"]
        return ""


    def get_job_names(self):
        job_names = []
        for element in root[1].findall("JOB"):
            job_names.append(element.attrib["JOBNAME"])
        return job_names


    def get_calendar(self):
        return root[1].find("RULE_BASED_CALENDAR").attrib["NAME"]


    def get_from_time(self):
        if "TIMEFROM" in root[1].attrib:
            raw_time = root[1].attrib["TIMEFROM"]
            new_str = raw_time[:2] + ":" + raw_time[2:]
            return new_str
        return "N/A"


    def get_to_time(self):
        if "TIMETO" in root[1].attrib:
            if root[1].attrib["TIMETO"].isdigit():
                raw_time = root[1].attrib["TIMETO"]
                new_str = raw_time[:2] + ":" + raw_time[2:]
                return new_str
        return "N/A"

    def get_run_frequency(self):
        pass

    def get_in_condition(self):
        in_condition = []
        to_remove = "TO"
        o_date = " (Order Date)"
        prev_date = " (Previous Order Date)"
        if root[1].findall("INCOND"):
            for incond in root[1].findall("INCOND"):
                name = incond.attrib["NAME"]
                f_str = name[:name.index(to_remove) + len(to_remove)]
                s_str = f_str.removesuffix("-TO")
                base_str = s_str.removesuffix("#")
                if incond.attrib["ODATE"] == "ODAT":
                    new_str = base_str + o_date
                elif incond.attrib["ODATE"] == "PREV":
                    new_str = base_str + prev_date
                in_condition.append(new_str)
        else:
            in_condition.append("N/A")
        return in_condition


    def get_not_submitted(self):
        if root[1].findall("SHOUT"):
            not_sub = root[1].find("SHOUT").attrib["WHEN"]
            if not_sub == "LATESUB":
                raw_sub = root[1].find("SHOUT").attrib["TIME"]
                new_sub = raw_sub[:2] + ":" + raw_sub[2:]
                return new_sub
            else:
                return "N/A"
        return "N/A"

    # not final
    def get_execution_time(self):
        if root[1].findall("SHOUT"):
            not_sub = root[1].find("SHOUT").attrib["WHEN"]
            if not_sub == "EXECTIME":
                raw_sub = root[1].find("SHOUT").attrib["TIME"].removeprefix(">")         
                return raw_sub
            else:
                return "N/A"
        return "N/A"

    # NO finished 
    def get_not_finished(self):
        pass


    def test(self):
        return root[1].attrib["TIMETO"]


    def file_basename(self):
        return os.path.basename(self.file_path)