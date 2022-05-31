import unittest
from xml_file_job import XmlFileJob as xfj


xml_job = xfj(r"C:\Users\chris.a.palabay\Documents\Python\CM Validation Automation\Workspace_1.xml")
class TestXmlJob(unittest.TestCase):

    def test_validation(self):
        res = xml_job.validate_xml_file()
        return self.assertTrue(res)

    def test_validate_file(self):
        res = xml_job.validate_xml_file()
        return self.assertTrue(res)

    def test_get_jobname(self):
        res = xml_job.get_job_name()
        return self.assertEqual(res,"rdl_process_mdm_mastervendor")

    def test_get_foldername(self):
        res = xml_job.get_folder_name()
        return self.assertEqual(res,"RDL-EDW-Sqoop-MasterVendor")

    def test_get_desc(self):
        res = xml_job.get_description()
        return self.assertEqual(res,"Performs both conversion and ingestion of Master Vendor XML files in RDL")

    def test_cmd_prd(self):
        res = xml_job.get_command_prd()
        return self.assertEqual(res,"/app/hadoop/rdl/script/rdlwkld_wrapper.ksh")

    def test_cmd_nonprod(self):
        res = xml_job.get_command_nonprd()
        return self.assertEqual(res,"/app/hadoop/rdl/script/rdlwkld_wrapper.ksh")

    # def test_get_param(self):
    #     res = xml_job.get_parameters()
    #     return self.assertIn("rdl_process_master_vendor.bash",res)

    def test_get_prd_nodeid(self):
        res = xml_job.get_prd_nodeid()
        return self.assertEqual(res,"rdldb")

    def test_prd_runas(self):
        res = xml_job.get_prd_runas()
        return self.assertEqual(res,"rdlwkld")

    def test_get_nonprd_nodeid(self):
        res = xml_job.get_nonprd_nodeid()
        return self.assertEqual(res,"rdldb")

    def test_nonprd_runas(self):
        res = xml_job.get_nonprd_runas()
        return self.assertEqual(res,"rdlwkld")

    def test_get_calendar(self):
        res = xml_job.get_calendar()
        return self.assertEqual(res,"BASE")

    def test_get_from_time(self):
        res = xml_job.get_from_time()
        return self.assertEqual(res,"N/A")

    def test_get_to_time(self):
        res = xml_job.get_to_time()
        return self.assertEqual(res,"N/A")

    def test_get_cyclic(self):
        res = xml_job.get_cyclic()
        return self.assertEqual(res,"N/A")

    # def test_get_run_frequency(self):
    #     res = xml_job.get_run_frequency()
    #     return self.assertEqual(res,"Daily")

    def test_get_incondition(self):
        res = xml_job.get_in_condition()
        return self.assertIn("N/A",res)

    def test_not_sub(self):
        res = xml_job.get_not_submitted()
        return self.assertEqual(res,"N/A")

    def test_exec_time(self):
        res = xml_job.get_execution_time()
        return self.assertEqual(res,"030")

    # def test_not_finby(self):
    #     res = xml_job.get_not_finished()
    #     return self.assertEqual(res,"N/A")



if __name__ == "__main__":
    unittest.main()
