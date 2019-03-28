from saiqa.DAO.TestDAO import TestDAO
import .test.LoginTest as lt
import .test.RegisterTest as rt
import .test.QuestionTest as qt

# Setup database
testDAO = TestDAO()
testDAO.createData()

# Test Register
# Good Register
rtest = rt.testregister('TesteR','Te$!eR','Te$!eR')
assert rtest == 'Good registration'
# Password Mismatch
rtest = rt.testregister('TesteR','Te$!eR','Te$!aR')
assert rtest == 'Passwords do not match'
# Incorrect Username Format
rtest = rt.testregister('TeR','Te$!eR','Te$!eR')
assert rtest == 'Incorrect formatting'
# Incorrect Password Format 1
rtest = rt.testregister('TesteR','Te$!eR','Te$!er')
assert rtest == 'Incorrect formatting'
# Incorrect Password Format 2
rtest = rt.testregister('TesteR','Te$!eR','Te$tR')
assert rtest == 'Incorrect formatting'
# Bad Register
rtest = rt.testregister('','','')
assert rtest == 'Empty form'
# Duplicate User
rtest = rt.testregister('TesteR','Te$!eR','Te$!er')
assert rtest == 'Duplicate user'

# Test Login
# Good Login
ttest = lt.testlogin('TesteR','Te$!eR')
assert ttest.getusername() == 'TesteR'
# User Does not Exist
ttest = lt.testlogin('TesteRs','Te$!eRs')
assert rtest == 'User not found'
# Bad Login
ttest = lt.testlogin('','')
assert rtest == 'Bad Login'

# Random Fact Returned
qrtest = lt.testrandfact()
assert type(rtest) == type('Bad Login')

# Test Learning Module
# Correct Upload of Information
ltest = qt.testunderstand('Information is an important thing to test while making an application.  Certain information is more important than others.', 'Testing info', 4, 'TesteR')
print(ltest) # Checking output
assert ltest = True
# Clean upload of information
ltest = qt.testunderstand('This information (not important for further purposes) is for purposes of testing.  Information presented is not viable.', 'Testing info', 4, 'TesteR')
print(ltest) # Checking output
assert ltest = True
# Enter a non-digit for trust level
ltest = qt.testunderstand('This information (not important for further purposes) is for purposes of testing.  Information presented is not viable.', 'Testing info', 't', 'TesteR')
print(ltest) # Checking output
assert ltest = 'Not a number'
# Leave any field blank
ltest = qt.testunderstand('', 'Testing info', 't', 'TesteR')
print(ltest) # Checking output
assert ltest = 'Bad upload'

# Test Answering Module
# Ask a valid question
atest = qt.testanswer('What is information?', 'TesteR')
print(atest) # Check output due to unpredictable nature of DMN
# assert atest == 'Information is an important thing to test while making an application.'
# Ask a question about a semi-known subject
# Ask a valid question
atest = qt.testanswer('What is data?', 'TesteR')
print(atest) # Check output due to unpredictable nature of DMN
# assert atest == 'Information is an important thing to test while making an application.'
# Ask a question about an unknown subject
# Ask a valid question
atest = qt.testanswer('What is the Moon?', 'TesteR')
print(atest) # Check output due to unpredictable nature of DMN
assert atest == 'Could not find anything on the Moon'
# Ask for a random fact

# Destroy database
testDAO.destroyData()