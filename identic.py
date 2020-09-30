#Safa Burak Altunel
#2017400207


import argparse
import os
import hashlib

def encrypt_string(hash_string): #hash function
	if type(hash_string) == bytes:
		sha_signature = hashlib.sha256(hash_string).hexdigest()
	else:
		sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
	return sha_signature

def get_size(start_path): #returns size of the given directory
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def bubbleSort(arr): 
    n = len(arr) 
  
    # Traverse through all array elements 
    for i in range(n): 
  
        # Last i elements are already in place 
        for j in range(0, n-i-1): 
  
            # traverse the array from 0 to n-i-1 
            # Swap if the element found is greater 
            # than the next element 
            if arr[j][0] == arr[j+1][0] and arr[j][1] > arr[j+1][1] : 
                arr[j], arr[j+1] = arr[j+1], arr[j]

#parsing inputs
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-f", action = "store_true")
group.add_argument("-d",action = "store_true")
parser.add_argument("-c",action = "store_true")
parser.add_argument("-n",action = "store_true")
parser.add_argument("-cn",action = "store_true")
parser.add_argument("-s",action = "store_true")
parser.add_argument("dirs",nargs = '*', default = [os.getcwd()])
args = parser.parse_args()

# dictionaries which store the duplicates
fileContentsDict = {}
fileNamesDict = {}
fileNamesAndContentsDict = {}

dirContentPathDict = {}
dirNamePathDict = {}
dirNameAndContentPathDict = {}

dirContentsDict = {}
dirNamesDict = {}
dirNamesAndContentsDict = {}


for klasor in args.dirs: #iterating over input directories
	for (root,directories,files) in os.walk(klasor, topdown = False):
		root = os.path.abspath(root)
		temp = os.path.split(root)
		nameOfCurrentDir = temp[1]
		dirContentsList = []
		dirNamesList = []
		dirNamesAndContentsList = []
		for file in files: #iterating over files and hashing (contents), (names) and (names and contents).
			with open(os.path.join(root,file),"rb") as fi:
				content = fi.read()
			contentHash = encrypt_string(content)
			if contentHash in fileContentsDict:
				fileContentsDict[contentHash].add(os.path.join(root,file))
			else:
				fileContentsDict[contentHash] = {os.path.join(root,file)}

			nameHash = encrypt_string(file)
			if nameHash in fileNamesDict:
				fileNamesDict[nameHash].add(os.path.join(root,file))
			else:
				fileNamesDict[nameHash] = {os.path.join(root,file)}

			nameAndContentHash = encrypt_string(nameHash + contentHash)
			if nameAndContentHash in fileNamesAndContentsDict:
				fileNamesAndContentsDict[nameAndContentHash].add(os.path.join(root,file))
			else:
				fileNamesAndContentsDict[nameAndContentHash] = {os.path.join(root,file)}

			dirNamesAndContentsList.append(nameAndContentHash)
			dirContentsList.append(contentHash)
			dirNamesList.append(nameHash)
		for dirr in directories: #iterating over subdirectories and getting calculated hashes.
			dirContentsList.append(dirContentPathDict[os.path.join(root,dirr)])
			dirNamesList.append(dirNamePathDict[os.path.join(root,dirr)])
			dirNamesAndContentsList.append(dirNameAndContentPathDict[os.path.join(root,dirr)])


		dirContentsList.sort()
		dirNamesList.sort()
		dirNamesAndContentsList.sort()


		#adding roots of the content duplicates to the same dictionary key
		s = ""
		for myHash in dirContentsList:
			s += myHash
		dirContentHash = encrypt_string(s)
		if dirContentHash in dirContentsDict:
			dirContentsDict[dirContentHash].add(root)
		else:
			dirContentsDict[dirContentHash] = {root}
		dirContentPathDict[root] = dirContentHash


		#adding roots of the name duplicates to the same dictionary key
		s = ""
		for myHash in dirNamesList:
			s += myHash
		dirNameHash = encrypt_string(encrypt_string(nameOfCurrentDir) + s)
		if dirNameHash in dirNamesDict:
			dirNamesDict[dirNameHash].add(root)
		else:
			dirNamesDict[dirNameHash] = {root}
		dirNamePathDict[root] = dirNameHash


		#adding roots of the name and content duplicates to the same dictionary key
		s = ""
		for myHash in dirNamesAndContentsList:
			s += myHash
		dirNameAndContentHash = encrypt_string(encrypt_string(nameOfCurrentDir) + s)
		if dirNameAndContentHash in dirNamesAndContentsDict:
			dirNamesAndContentsDict[dirNameAndContentHash].add(root)
		else:
			dirNamesAndContentsDict[dirNameAndContentHash] = {root}
		dirNameAndContentPathDict[root] = dirNameAndContentHash


if args.d: #look for identical directories
	if args.n: #look for identical directory names
		ans = []
		for key in dirNamesDict:
			if len(dirNamesDict[key]) > 1:
				list = []
				for paths in dirNamesDict[key]:
					list.append(paths)
				list.sort()
				ans.append(list)
		ans.sort()
		for list in ans:
			for path in list:
				print(path)
			print("")
	elif args.cn: #look for identical directory names and contents
		if args.s: #printing size
			ans = []
			for key in dirNamesAndContentsDict:
				if len(dirNamesAndContentsDict[key]) > 1:
					list = []
					for paths in dirNamesAndContentsDict[key]:
						list.append(paths)
					list.sort()
					dir_size = 0
					for d in dirNamesAndContentsDict[key]:
						dir_size = get_size(d)
						break 
					list.insert(0,dir_size)
					ans.append(list)
			ans.sort(reverse = True)
			bubbleSort(ans)
			for list in ans:
				for i in range(1,len(list)):
					print(list[i],end = "\t")
					print(list[0])
				print("")
		else: #not printing size
			ans = []
			for key in dirNamesAndContentsDict:
				if len(dirNamesAndContentsDict[key]) > 1:
					list = []
					for paths in dirNamesAndContentsDict[key]:
						list.append(paths)
					list.sort()
					ans.append(list)
			ans.sort()
			for list in ans:
				for path in list:
					print(path)
				print("")

	else: #look for identical directory contents
		if args.s: #printing size
			ans = []
			for key in dirContentsDict:
				if len(dirContentsDict[key]) > 1:
					list = []
					for paths in dirContentsDict[key]:
						list.append(paths)
					list.sort()
					dir_size = 0
					for d in dirContentsDict[key]:
						dir_size = get_size(d)
						break 
					list.insert(0,dir_size)
					ans.append(list)
			ans.sort(reverse = True)
			bubbleSort(ans)
			for list in ans:
				for i in range(1,len(list)):
					print(list[i],end = "\t")
					print(list[0])
				print("")
		else: #not printing size
			ans = []
			for key in dirContentsDict:
				if len(dirContentsDict[key]) > 1:
					list = []
					for paths in dirContentsDict[key]:
						list.append(paths)
					list.sort()
					ans.append(list)
			ans.sort()
			for list in ans:
				for path in list:
					print(path)
				print("")
else: #look for identical files
	if args.n: #look for identical file names		
		ans = []
		for key in fileNamesDict:
			if len(fileNamesDict[key]) > 1:
				list = []
				for paths in fileNamesDict[key]:
					list.append(paths)
				list.sort()
				ans.append(list)
		ans.sort()
		for list in ans:
			for path in list:
				print(path)
			print("")
	elif args.cn: #look for identical file names and contents
		if args.s: #printing size
			ans = []
			for key in fileNamesAndContentsDict:
				if len(fileNamesAndContentsDict[key]) > 1:
					list = []
					for paths in fileNamesAndContentsDict[key]:
						list.append(paths)
					list.sort()
					file_size = 0
					for fil in fileNamesAndContentsDict[key]:
						file_size = os.stat(fil).st_size
						break

					list.insert(0,file_size)
					ans.append(list)
			ans.sort(reverse = True)
			bubbleSort(ans)
			for list in ans:
				for i in range(1,len(list)):
					print(list[i],end = "\t")
					print(list[0])
				print("")
		else: #not printing size
			ans = []
			for key in fileNamesAndContentsDict:
				if len(fileNamesAndContentsDict[key]) > 1:
					list = []
					for paths in fileNamesAndContentsDict[key]:
						list.append(paths)
					list.sort()
					ans.append(list)
			ans.sort()
			for list in ans:
				for path in list:
					print(path)
				print("")
	else: #look for identical file contents
		if args.s: #printing size
			ans = []
			for key in fileContentsDict:
				if len(fileContentsDict[key]) > 1:
					list = []
					for paths in fileContentsDict[key]:
						list.append(paths)
					list.sort()
					file_size = 0
					for fil in fileContentsDict[key]:
						file_size = os.stat(fil).st_size
						break
					list.insert(0,file_size)
					ans.append(list)
			ans.sort(reverse = True)
			bubbleSort(ans)
			for list in ans:
				for i in range(1,len(list)):
					print("{}\t{}".format(list[i],list[0]))
				print("")
		else: #not printing size
			ans = []
			for key in fileContentsDict:
				if len(fileContentsDict[key]) > 1:
					list = []
					for paths in fileContentsDict[key]:
						list.append(paths)
					list.sort()
					ans.append(list)
			ans.sort()
			for list in ans:
				for path in list:
					print(path)
				print("")