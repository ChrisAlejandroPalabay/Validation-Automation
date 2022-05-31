import xml.etree.ElementTree as ET
import os


# Alerts yet to be included
class XmlFileJob:

    # root[1] == Element(SMART_FOLDER)

    def __init__(self,file_path) -> None:
        self.file_path = file_path
        tree = ET.parse(file_path)
        global root
        root = tree.getroot()


    def validate_xml_file(self):
        if root.tag == "DEFTABLE":
            if root.find("SMART_FOLDER"):
                return True
        return False


    def get_job_name(self):
        return root[1].find("JOB").attrib["JOBNAME"]


    def get_folder_name(self):
        return root[1].attrib["FOLDER_NAME"]


    def get_description(self):
        if "DESCRIPTION" in root[1].find("JOB").attrib:
            return root[1].find("JOB").attrib["DESCRIPTION"]
        return ""


    def get_command_prd(self):
        if "CMDLINE" in root[1].find("JOB").attrib:
            raw_cmd = root[1].find("JOB").attrib["CMDLINE"]
            if '"' in raw_cmd:
                f_split = raw_cmd.split(" ")
                return f_split[0]
            return raw_cmd
        return "N/A"


    def get_command_nonprd(self):
        # Assuming that prd and non-prd will have the same value
        return self.get_command_prd()


    def __get_parameters(self):
        params = []
        if "CMDLINE" in root[1].find("JOB").attrib:
            raw_cmd = root[1].find("JOB").attrib["CMDLINE"]
            if '"' in raw_cmd:
                f_str = raw_cmd.split(" ")
                new_str = f_str[1].removeprefix('"').removesuffix('"')
                params.append(new_str)
            else:
                params.append("N/A")
        else:
            params.append("N/A")
        return params


    def get_param_prd(self):
        return self.__get_parameters()[0]

    def get_param_nonprd(self):
        return self.__get_parameters()[0]

    # NODEID = Host Group
    def get_prd_nodeid(self):
        return root[1].find("JOB").attrib["NODEID"]

    # RUNS_AS = Run As
    def get_prd_runas(self):
        return root[1].find("JOB").attrib["RUN_AS"]

    # NODEID = Host Group
    # Assuming prd values = non-prd values
    def get_nonprd_nodeid(self):
        return self.get_prd_nodeid()

    # RUNS_AS = Run As
    # Assuming prd values = non-prd values
    def get_nonprd_runas(self):
        return self.get_prd_runas()


    def get_calendar(self):
        return root[1].find("JOB").find("RULE_BASED_CALENDARS").attrib["NAME"]


    def get_from_time(self):
        if "TIMEFROM" in root[1].find("JOB").attrib:
            raw_time = root[1].find("JOB").attrib["TIMEFROM"]
            new_str = raw_time[:2] + ":" + raw_time[2:]
            return new_str
        return "N/A"


    def get_to_time(self):
        if "TIMETO" in root[1].find("JOB").attrib:
            raw_time = root[1].find("JOB").attrib["TIMETO"]
            new_str = raw_time[:2] + ":" + raw_time[2:]
            return new_str
        return "N/A"


    def get_cyclic(self):
        if "CYCLIC" in root[1].find("JOB").attrib:
            cyclic_val = root[1].find("JOB").attrib["CYCLIC"]
            if cyclic_val == 0 or cyclic_val == "0":
                return "N/A"
            else:
                return cyclic_val
        else:
            return "N/A"

    # To follow
    def get_run_frequency(self):
        pass


    def get_in_condition(self):
        in_condition = []
        to_remove = "TO"
        o_date = " (Order Date)"
        prev_date = " (Previous Order Date)"
        if root[1].find("JOB").findall("INCOND"):
            for incond in root[1].find("JOB").findall("INCOND"):
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
        if root[1].find("JOB").findall("SHOUT"):
            not_sub = root[1].find("JOB").find("SHOUT").attrib["WHEN"]
            if not_sub == "LATESUB":
                raw_sub = root[1].find("JOB").find("SHOUT").attrib["TIME"]
                new_sub = raw_sub[:2] + ":" + raw_sub[2:]
                return new_sub
            else:
                return "N/A"
        return "N/A"


    # not final
    def get_execution_time(self):
        if root[1].find("JOB").findall("SHOUT"):
            not_sub = root[1].find("JOB").find("SHOUT").attrib["WHEN"]
            if not_sub == "EXECTIME":
                raw_sub = root[1].find("JOB").find("SHOUT").attrib["TIME"].removeprefix(">")
                # new_sub = raw_sub[:2] + ":" + raw_sub[2:]
                return raw_sub
            else:
                return "N/A"
        return "N/A"


    def get_not_finished(self):
        pass


    def file_basename(self):
        return os.path.basename(self.file_path)
