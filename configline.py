#!/usr/bin/python
from xml.dom import minidom

###
# Parses sip.conf entries to generate the sip-basic.cfg registrations.
# It's expecting an entry like the one below where:
# * The extension is in the brackets
# * The first line after the extension is a COMMENTED mac address for the phone / user.
# * The next line is the secret
# * The last line is the CID.
##
# Example
##
# [111](l3office)
# ;0004f2f957f9
# secret=shoonfa9s3k
# callerid="Conference Phone" <111>
###
server = '192.168.10.9'
site="l3atl"

fp = open('reg.list')
for line in fp:
	buff = line.strip()
	if buff.startswith("["):
		extension = line[1:4]
		buff = fp.next()
		mac = buff[1:].strip()
		buff = fp.next().split("=")
		secret = buff[1].strip()

		
		xmldoc = minidom.parse('reg-basic.cfg')
		itemlist = xmldoc.getElementsByTagName('reg')
		for s in itemlist:
			s.attributes['reg.1.address'] = '%s@%s' % (extension,server)
			s.attributes['reg.1.auth.password'] = secret
			s.attributes['reg.1.auth.userId'] = extension
			s.attributes['reg.1.label'] = extension
			# s.attributes['reg.1.outboundProxy.address']

		output = xmldoc.toxml()
		xp = open(mac,'w')
		xp.write(output)
		xp.close()

		xmldoc = minidom.parse('000000000000.cfg')
		app = xmldoc.getElementsByTagName('APPLICATION')

		# Assemble config file list
		files = ['site.cfg', 'sip-interop.cfg', 'features.cfg', 'sip-basic.cfg', 'reg-advanced.cfg']
		paths = []

		for f in files:
			path = "%s/%s" % (site,f)
			paths.append(path)

		# Add the last one.
		config = "%s/%s" % (site,mac)
		paths.append(config)

		setting = ", ".join(paths)
		print app
		for a in app:
			a.attributes['CONFIG_FILES'] = setting

		output =  xmldoc.toxml()

		cp = open(mac+".cfg","w")
		cp.write(output)
		cp.close()

fp.close()