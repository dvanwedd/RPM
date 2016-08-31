#!/usr/bin/python
import os,sys,time


##Defining variables/Functions
deploylist = []
HOME = os.getenv('HOME')
FILES = HOME+'/rpmbuild/FILES'
FILESclean = HOME+'/rpmbuild/FILES/*'
specpath = HOME+'/rpmbuild/SPECS/'
builddir = HOME+'/rpmbuild/BUILD/'
attr = "attr(0644,root,root) "
fldr = "%dir /"
bldrt = " %{buildroot}/"
mkdir = "mkdir -p -m 0755 "
installf = "install -m 0755 "
fileLocation = HOME+'/rpmbuild/FILES'
SOURCES = HOME+'/rpmbuild/SOURCES/'
groupList = {'1':'Amusements/Games','2':'Amusements/Graphics',
'3':'Applications/Archiving','4':'Applications/Communications',
'5':'Applications/Databases','6':'Applications/Editors',
'7':'Applications/Emulators','8':'Applications/Engineering',
'9':'Applications/Files','10':'Applications/Internet',
'11':'Applications/Multimedia','12':'Applications/Productivity',
'13':'Applications/Publishing','14':'Applications/System',
'15':'Applications/Text','16':'Development/Debuggers',
'17':'Development/Languages','18':'Development/Libraries',
'19':'Development/System','20':'Development/Tools',
'21':'Documentation','22':'System Environment/Base',
'23':'System Environment/Daemons','24':'System Environment/Kernel',
'25':'System Environment/Libraries','26':'System Environment/Shells',
'27':'User Interface/Desktops','28':'User Interface/X',
'29':'User Interface/X Hardware Support',
'X':'EXIT'}
#######################################################################################


##Program Modules
def drcreatePrep():
	print 'Verifying program requirements...\n\n'
	time.sleep(1)
	fldCheck = os.path.isdir(FILES)
	try:
		if	os.path.exists(fileLocation) == 'False':
			os.mkdir(fileLocation)
	except OSError:
		print 'No Folder...\n'

def notesSection():
	print '\nIf you havn\'t already done so, please create a tarball (filename.tar.gz) and move it to %s \n' % SOURCES

def installSectionMkdir():
	target.write('%install\nrm -rf %{buildroot}\n# mkdir - make directories\n')
	ch1 = os.walk(fileLocation)
	for dirname, dirnames, filenames in ch1:
		for subdirname in dirnames:
			d1 = os.path.join(dirname,subdirname)
			sp = d1.split('/')
			count = 0
			while (count < 6):
				sp.pop(0)
				count = count + 1
				newList = '/'.join(sp)
			target.write('mkdir -p %{buildroot}'+'/'+newList+'\n')

def installSectionInstall():
	target.write('# install - copy files and set attributes: \n')
	ch1 = os.walk(fileLocation)
	for dirname, dirnames, filenames in ch1:
		for filename in filenames:
			f2 = os.path.join(dirname,filename)
			sp = f2.split('/')
			count = 0
			while (count < 6):
				sp.pop(0)
				count = count + 1
				newList = '/'.join(sp)
			target.write('install -m 0644 '+f2+' %{buildroot}/'+newList+'\n')

def installSectionFilesDir():
	target.write('# Files section, what do we install and how we keep track of it\n%files\n# %defattr - Default Attributes (file_perm, user, group, dir_perm):\n')
	target.write('%defattr(0644,root,root,0755)\n')
	ch1 = os.walk(fileLocation)
	for dirname, dirnames, filenames in ch1:
		for subdirname in dirnames:
			d1 = os.path.join(dirname,subdirname)
			sp = d1.split('/')
			count = 0
			while (count < 6):
				sp.pop(0)
				count = count + 1
				newList = '/'.join(sp)
			target.write('/'+newList+'\n')

def installSectionFilesAttr():
	target.write('# %config directive is used to flag the file as being a configuration file.\n')
	target.write('%defattr(0644,root,root,0755)\n')
	ch1 = os.walk(fileLocation)
	for dirname, dirnames, filenames in ch1:
		for filename in filenames:
			f2 = os.path.join(dirname,filename)
			sp = f2.split('/')
			count = 0
			while (count < 6):
				sp.pop(0)
				count = count + 1
				newList = '/'.join(sp)
			target.write('/'+newList+'\n')

def welcomeMessage():
	print "\nWelcome to Danny V's RPM generator\n\n"


##Make sure input is a number

def checkIfNumber(x):
	try:
		return int(x)
	except Exception:
		return x

######################
welcomeMessage()
drcreatePrep()
notesSection()
######################



name = raw_input("############\nPlease name your RPM... ie... if your tar.gz is name example.tar.gz..  Enter example.... \n ")
print name


version = raw_input("############\nWhat is the version number?...\n ")
print version


try:
	release = raw_input("############\nWhat is the release number?...\tIf none, just press ENTER \n")
	n = int(release)
	print '%d' %n
except ValueError:
	print "%s is not a number..."%release

nameFinal = name+'-'+version+'.'+release+'.'+'tar.gz'
nameVR = name+'-'+version+'.'+release

os.system('tar xzvf $HOME/rpmbuild/SOURCES/'+nameFinal)
PATH = os.system('cd $HOME/rpmbuild/FILES;tar zxvf '+SOURCES+nameFinal)


###Iterate through GroupList and show it in Human-Readable Order
for keys,group in enumerate(sorted(groupList.iteritems(), key = lambda(k, v): checkIfNumber(k) )):
	eachKey, eachValue = group
	if keys % 2 == 1 and keys != 0:
		print '%s:) %s\t \n%s:) %s'%(prevKey, preValue, eachKey, eachValue)
	prevKey = eachKey
	preValue = eachValue
while True:
	groupChoice = raw_input('> ')
	if groupChoice == 'x' or groupChoice == 'X':
		print 'GoodBye...'
		exit(0)
	elif groupChoice in groupList:
		group = groupList[groupChoice]
		print group
		break
	else:
		print 'Error in option choice...'


##Get Build Architecture
barch = raw_input("############\nWhat's the build? ie.. x86_64 i386 i586 noarch ... Press ENTER for noarch\n")
print barch


summary = raw_input("############\nEnter any summary information about this RPM...(Required) \n")
print summary


vendor = raw_input("############\nWho is the vendor? \n")
print vendor


##This is where we create and write our SPEC file
target = open(specpath+name+'-'+version+'.'+release+'.spec', 'a')
targetPath = specpath+name+'-'+version+'.'+release+'.spec'

target.write('%define name '+name+'\n')
target.write('%define version '+version+'\n')
target.write('%define release '+release+'\n')
target.write('Summary:\t '+summary+'\n')
target.write('Name:\t'+'         '+'%{name}\n')
target.write('Version:\t'+' '+'%{version}\n')
target.write('Release:\t'+' '+'%{release}\n')
target.write('License:\t GPL\n')
target.write('Group:\t '+'         '+group+'\n')
target.write('BuildArch:\t '+barch+'\n')
target.write('BuildRoot:\t %{_builddir}/%{name}-root\n')
target.write('Vendor:\t '+'         '+vendor+'\n')
target.write('Source0:\t'+nameFinal+'\n')
target.write('%description\n'+summary+'\n')

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
target.write('%prep\n%setup -q\n')

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
target.write('%build\n\n')

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
installSectionMkdir()
installSectionInstall()

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
target.write('%pre\n(\n\techo "Pre Install Section:"\n) > /var/tmp/%{name}-%{version}-%{release}-install.pre.log 2>&1\n')

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
target.write('%post\n(\n\techo "Post Install Section:"\n) > /var/tmp/%{name}-%{version}-%{release}-install.post.log 2>&1\n')

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
target.write('%preun\n(\n\techo "Pre Uninstall Section:"\n) > /var/tmp/%{name}-%{version}-%{release}-uninstall.pre.log 2>&1\n')

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
target.write('%postun\n(\n\techo "Post Uninstall Section:"\n) > /var/tmp/%{name}-%{version}-%{release}-uninstall.post.log 2>&1\n')

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
installSectionFilesDir()
installSectionFilesAttr()

target.write('#-----------------------------------------------------------------------------------------------------------------------------------------#\n')
target.write('%clean\nrm -rf %{buildroot}\nrm -rf '+FILESclean+'\n')
target.close()


#print 'Building RPM....\n'
#time.sleep(0.5)
#os.system('rpmbuild -ba '+targetPath)

