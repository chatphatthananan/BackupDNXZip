from datetime import datetime


#Directory of latest DNX folder to be zipped
to_be_zipped_dnx_dir = 'C:/Evogenius/Evogenius Reporting/DNX/'

#Location of latest zipped DNX folder
latest_zipped_DNX_location = "C:/SGTAM_DP/Working Project/BackupDNXZip/"

#Location of DNX_zip folder that stores 5 latest DNXs
DNX_zip_folder = "D:/05. Data Production/DNX Zip/"

#Location of DNX backup root folder
backup_root_dir_E = "E:/DNX backup/"
backup_root_dir_G = "F:/DNX backup/"
drives_to_check = [backup_root_dir_E, backup_root_dir_G]

#Python log folder (same location as folder with latest DNX)
log_dir = "C:/SGTAM_DP/Working Project/BackupDNXZip/Log/"

#7zip.exe path on the PC
seven_zip_exe_path = "C:/Program Files/7-Zip/7z.exe"

#Template folder for backup in E drive
backup_template_folder_E = 'E:/DNX backup/DO_NOT_DELETE/yyyy'

#location that backup template folder is coppied to, DRIVE CHARACTER WAS INTENTIONAL LEFT OUT
backup_template_folder_before_renamed = ':/DNX backup/yyyy'


#location of the backup folder that has been renamed.
backup_template_folder_renamed = f":/DNX backup/{datetime.now().strftime('%Y/')}"
