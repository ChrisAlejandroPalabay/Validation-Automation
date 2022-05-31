import unittest
from xml_file_folder import XmlFileFolder as xff
# from docx_file_folder import DocxFileFolder as dff

xml = xff(r"C:\Users\chris.a.palabay\Documents\Python\CM Validation Automation\Workspace_1.xml")
class TestDocxFolder(unittest.TestCase):

    def test_validate_xml_file(self):
        res = xml.validate_xml_file()
        return self.assertTrue(res)

    def test_get_folder_name(self):
        res = xml.get_folder_name()
        return self.assertEqual(res,"RDL-EDW-Sqoop-MasterVendor")

    def test_get_desc(self):
        res = xml.get_description()
        return self.assertEqual(res,"This folder will perform the processing of Master Vendor files into RDL.")

    def test_get_job_names(self):
        res = xml.get_job_names()
        return self.assertIn("rdl_process_mdm_mastervendor",res)

    def test_get_calendar(self):
        res = xml.get_calendar()
        return self.assertEqual(res,"BASE")

    def test_get_fromtime(self):
        res = xml.get_from_time()
        return self.assertEqual(res,"20:00")

    def test_get_totime(self):
        res = xml.get_to_time()
        return self.assertEqual(res,"N/A")

    # def test_get_runfrequency(self):
    #     res = xml.get_run_frequency()
    #     return self.assertEqual(res,"Daily at 8:00 PM PT")

    def test_get_incondition(self):
        res = xml.get_in_condition()
        return self.assertIn("N/A",res)

    def test_get_notsubmitted(self):
        res = xml.get_not_submitted()
        return self.assertEqual(res,"N/A")

    def test_get_exectime(self):
        res = xml.get_execution_time()
        return self.assertEqual(res,"N/A")

    # def test_get_notfinby(self):
    #     res = xml.get_not_finished()
    #     return self.assertEqual(res,"N/A")


if __name__ == "__main__":
    unittest.main()
