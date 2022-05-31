import unittest
from docx_file_folder import DocxFileFolder as dff

docx = dff(r"C:\Users\chris.a.palabay\Documents\Python\CM Validation Automation\RDL-EDW-Sqoop-MasterVendor.docx")
class TestDocxFolder(unittest.TestCase):

    def test_validate_docx_file(self):
        res = docx.validate_docx_file()
        return self.assertTrue(res)

    def test_get_folder_name(self):
        res = docx.get_folder_name()
        return self.assertEqual(res,"RDL-EDW-Sqoop-MasterVendor")

    def test_get_desc(self):
        res = docx.get_description()
        return self.assertEqual(res,"This folder will perform the processing of Master Vendor files into RDL.")

    def test_get_job_names(self):
        res = docx.get_job_names()
        return self.assertIn("rdl_process_mdm_mastervendor",res)

    def test_get_calendar(self):
        res = docx.get_calendar()
        return self.assertEqual(res,"BASE")

    def test_get_fromtime(self):
        res = docx.get_from_time()
        return self.assertEqual(res,"20:00")

    def test_get_totime(self):
        res = docx.get_to_time()
        return self.assertEqual(res,"N/A")

    def test_get_runfrequency(self):
        res = docx.get_run_frequency()
        return self.assertEqual(res,"Daily at 8:00 PM PT")

    def test_get_incondition(self):
        res = docx.get_in_condition()
        return self.assertIn("N/A",res)

    def test_get_notsubmitted(self):
        res = docx.get_not_submitted()
        return self.assertEqual(res,"N/A")

    def test_get_exectime(self):
        res = docx.get_execution_time()
        return self.assertEqual(res,"N/A")

    def test_get_notfinby(self):
        res = docx.get_not_finished()
        return self.assertEqual(res,"N/A")


if __name__ == "__main__":
    unittest.main()
