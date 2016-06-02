#!/usr/bin/python -u

import os
import sys
import time
import boto.ec2
import urllib2

try:
	# Connect to EC2...
	region = urllib2.urlopen("http://169.254.169.254/latest/meta-data/placement/availability-zone").readline().rstrip('abcde')
	print "Connecting to EC2 (%s)" % region
	ec2 = boto.ec2.connect_to_region(region)

except Exception, e:
	print "EC2 data gathering failed: %s" % e
	sys.exit(1)


# Get security groups
groups = ec2.get_all_security_groups()

for group in groups:
    print "\t%s:" % group.name
    for rule in group.rules:
        print "\t\t%s\t%s\t%s\t%s" % (rule.ip_protocol, rule.from_port, rule.to_port, rule.grants)

