
import os, sys, platform, subprocess

#archive handling
from zipfile import ZipFile
from datetime import datetime

backup_prefix = "backup_"

class backup_object:
    def __init__(self):
        #Local paths
        self.program_wd = sys.path[0]
        self.backups_path = os.path.join(self.program_wd, "backups")
        #Target dir paths
        self.target = None

    def set_target(self, target_path):
        print("Set backup taget to %s" % target_path)
        self.target = target_path

    def get_backups(self):
        if self.target:
            return subfiles(self.target)

    def parse_date(self, date):
        if date:
            try:
                date = remove_prefix(date, backup_prefix)
                date = date.strip(".zip")
                dates = date.split("-")
                ddmmyyyy = "{}/{}/{}".format(dates[1],dates[2],dates[0])
                return ddmmyyyy
            except Exception as e:
                return "unknown"

    def open_backups_folder(self):
        if self.target:
            open_folder_in_window(self.target)

    # def deletebackup(self,filetodelete):
    #     os.remove(filetodelete)
    #     self.printtoboth("\nDeleted backup {}\n".format(filetodelete))

    def makebackup(self):
        if self.target:
            if not os.path.isdir(self.backups_path):
                    os.mkdir(self.backups_path)

            files = subfiles(self.target)
            ziptime = date_str()
            newzipname = "{}{}.zip".format(backup_prefix,ziptime)
            newzip = os.path.join(self.backups_path,newzipname)

            with ZipFile(newzip, 'x') as backup:
                itt = 0
                while itt < len(files["location"]):
                    filename = files["filename"][itt]
                    backup.write(files["location"][itt],filename)
                    print("Archived - {}".format(filename))
                    itt += 1
                print("\nArchived {} files\n".format(itt))

            print("Backup {} complete".format(newzipname))

    def restorebackup(self, backup):
        if self.target:
            backup_file = os.path.join(self.program_wd,backup)
            if not os.path.isdir(backup_file):
                print("Not a vaild file to restore from")

            zip_file = backup_file

        with ZipFile(zip_file, 'r') as zipObj:
            zipObj.extractall(self.target)
            namelist = zipObj.namelist()
            print("files copied: \n {}".format(namelist))
            print("Copied {} files".format(len(namelist)))
            print("\nSucessfully restored backup {} to SD\n".format(zip_file))


def date_str():
    #returns the today string year, month, day, second
    return '{}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

def subfiles(path):
    filelist = {
        "location" : [],
        "filename" : [],
    }

    for root, dirs, files in os.walk(path):
        for name in files:
            filename = os.path.join(root, name)

            filelist["location"].append(filename)

            filename = remove_prefix(filename,path)

            filelist["filename"].append(filename)
    return filelist

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def open_folder_in_window(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])