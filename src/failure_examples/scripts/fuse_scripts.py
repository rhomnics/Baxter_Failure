#!/usr/bin/env python
import argparse
import sys
import json
import rospy


def main():
	arg_fmt = argparse.RawDescriptionHelpFormatter
	parser  = argparse.ArgumentParser(formatter_class=arg_fmt, description=main.__doc__)
	required = parser.add_argument_group('required arguments')
	required.add_argument('-f', '--file', dest='file1', required=True, help='the file name to record to')
	required.add_argument('-g', '--gile', dest='file2', required=True, help='the file name to record to')
	required.add_argument('-j', '--jile', dest='file3', required=True, help='the file name to record to')

	args = parser.parse_args(rospy.myargv()[1:])
	source_file1 = open(args.file1, 'rb').read()
	waypoints1=json.loads(source_file1)

	source_file2 = open(args.file2, 'rb').read()
	waypoints2=json.loads(source_file2)	

	waypoints2.extend(waypoints1)

	with open(args.file3, 'wb') as f:
		f.write(json.dumps(waypoints1))
    #parser = argparse.ArgumentParser(formatter_class=arg_fmt, description=main.__doc__)
    #required = parser.add_argument_group('required arguments')

	# required.add_argument('-f', '--file', dest='file1', required=True, help='the file name to record to')

 #    required.add_argument('-g', '--gile', dest='file2', required=True, help='the file name to record to')

	# required.add_argument('-h', '--hile', dest='file3', required=True, help='the file name to record to')


    
	# args = parser.parse_args(rospy.myargv()[1:])

	# source_file1 = open(args.file1, 'rb').read()
	# waypoints1=json.loads(source_file1)

	# source_file2 = open(args.file2, 'rb').read()
	# waypoints2=json.loads(source_file2)																																																																																																																							source_file2 = open(args.file2, 'rb').read()


	# waypoints2.extend(waypoints1)

	# with open(args.file3, 'wb') as f:
	# 	f.write(json.dumps(waypoints1))

if __name__ == '__main__':
    main()