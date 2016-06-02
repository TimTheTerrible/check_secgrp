#!/usr/bin/python -u

import os
import sys
import time
import boto.ec2
import urllib2

# check_secgrp.py - a nagios check to look for open security groups in AWS
#
# 2014-12-28 - Tim Currie
#
# In order for it to work, it needs to be run on an AWS instance which has an
# IAM role containing the "ec2:describe*" permission. Alternatively, if you 
# create a ~/.boto file and put a set of AWS secret keys in it, the boto 
# library will authenticate using those. Note that if you go the IAM route,
# you'll get security groups for the region/datacenter/vpc where the node 
# lives. If you use keys, you'll get the security groups for the EC2 account
# wherein those credentials are valid. This produces confusing results, so
# consider yourself warned.
#

NAGIOS_OK=0
NAGIOS_WARN=1
NAGIOS_CRIT=2
NAGIOS_FAIL=3

result = NAGIOS_OK

message = "No open security groups found"

try:
    # Connect to EC2...
    region = urllib2.urlopen("http://169.254.169.254/latest/meta-data/placement/availability-zone").readline().rstrip('abcde')
    ec2 = boto.ec2.connect_to_region(region)

except Exception, e:
    print "EC2 data gathering failed: %s" % e
    sys.exit(NAGIOS_FAIL)


# Get security groups
groups = ec2.get_all_security_groups()

badgroups = []
for group in groups:
    for rule in group.rules:
        for grant in rule.grants:
            # Flag any rule that allows internet access (0.0.0.0/0) to any tcp/udp port besides web (80/443)...
            if ( grant.cidr_ip == "0.0.0.0/0"
                and (rule.ip_protocol == "tcp" or rule.ip_protocol == "udp")
                and (rule.from_port != 443 and rule.from_port != 80)):
                if group.name not in badgroups:
                    badgroups.append(group.name)

if badgroups:
    message = "WARNING Open Security Groups: " + ", ".join(badgroups)
    result = NAGIOS_WARN

print message

sys.exit(result)

