import unittest
import sys
import os
from pathlib import Path
sys.path.insert(0, Path(os.path.abspath(__file__)).parents[1].as_posix().replace('/','\\'))


from EPOS.tools import PasswordStrength


class TestPasswordStrength(unittest.TestCase):

	def test_password_strength_pass(self):
		self.password = PasswordStrength('Bernice@124')
		self.assertEqual(self.password.validate(), True)

	def test_password_strength_fail(self):
		self.password = PasswordStrength('bernice@123')
		self.assertEqual(self.password.validate(), False)

	



if __name__ == '__main__':
	unittest.main()


