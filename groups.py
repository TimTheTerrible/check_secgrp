import os
import sys 
import time
import boto.ec2
import urllib2
region = urllib2.urlopen("http://169.254.169.254/latest/meta-data/placement/availability-zone").readline().rstrip('abcde')
ec2 = boto.ec2.connect_to_region(region)
groups = ec2.get_all_security_groups()
