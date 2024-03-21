from datetime import datetime
import os
import shutil
import re
import msvcrt
import config
import logging
import subprocess

#----------------------------Custom Exception classes-----------------------------------
class Error(Exception):
    pass
class fewer_than_five_DNX_zips_Exceptions(Error):
    pass
#---------------------------------------------------------------------------------------


#------------------------------------Logging--------------------------------------------
#Create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename=config.log_dir + datetime.now().strftime("DNX_%d%b%Y") + ".Log",
                    level = logging.DEBUG, format = LOG_FORMAT)
logger = logging.getLogger()
#---------------------------------------------------------------------------------------


#----------------------------Function declarations--------------------------------------
def get_latest_dnx_name():
    current_datetime = datetime.now()
    # contain date in this format "22Sep2021"
    current_date = current_datetime.strftime("%d%b%Y")    
    latest_DNX_name = "DNX_"+current_date
    return latest_DNX_name

def zip_latest_dnx():
 
    latest_DNX_name = get_latest_dnx_name()
    logger.info('-------------------------------------------------------------------------------------------------------')
    cmd = [config.seven_zip_exe_path, 'a', '-tzip', latest_DNX_name, '-mx5', config.to_be_zipped_dnx_dir]
    sp = subprocess.run(cmd, shell=True)
    logger.info(f'Archived DNX folder to {config.latest_zipped_DNX_location + latest_DNX_name + ".zip"} successfully!')
    print(f'Archived DNX folder to {config.latest_zipped_DNX_location + latest_DNX_name + ".zip"} successfully!')
  
def copy_to_DNX_zip():
    logger.info('Copying the latest DNX zip to DNX_zip folder.')
    print('Copying the latest DNX zip to DNX_zip folder.')
    print('This will take quite some time, you may come back later.')
    try:
        latest_DNX_name = get_latest_dnx_name() 
        shutil.copy(config.latest_zipped_DNX_location + latest_DNX_name+".zip", config.DNX_zip_folder)
        logger.info(f'Copied {config.latest_zipped_DNX_location + latest_DNX_name+".zip"} to {config.DNX_zip_folder} successfully!')
        print(f'Copied {config.latest_zipped_DNX_location + latest_DNX_name+".zip"} to {config.DNX_zip_folder} successfully!')
    except Exception:
        logger.info('Copy to DNX_zip failed!')
        logger.info(Exception)
        print('Copy to DNX_zip failed!')
        print(Exception)
    
def move_to_backup():
    try:
        
        latest_DNX_zip_file = config.latest_zipped_DNX_location + get_latest_dnx_name() + ".zip"
        
        #Check if the new backup folder 202Y exist on the first day of new year
        #If does not exist it will create before doing the backup to H drive.
        for drive in config.drives_to_check:
            if os.path.exists(drive + datetime.now().strftime('%Y/')):
                print(f"{drive + datetime.now().strftime('%Y/')} already exist, proceed to backup in {drive[0]} drive.")
                logger.info(f"{drive + datetime.now().strftime('%Y/')} already exist, proceed to backup in {drive[0]} drive.")
            else:
                print(f"{drive + datetime.now().strftime('%Y/')} does not exist, proceed to copy/create the directory.")
                logger.info(f"{drive + datetime.now().strftime('%Y/')} does not exist, proceed to copy/create the directory.") 
                
                ## Copy "yyyy" folder to E and G drives, then rename it to the current year.
                shutil.copytree(config.backup_template_folder_E, f"{drive[0] + config.backup_template_folder_before_renamed}")
                shutil.move(f"{drive[0] + config.backup_template_folder_before_renamed}", f"{drive[0] + config.backup_template_folder_renamed}")
                print("Folder is created.")
                logger.info("Folder is created.")           
                ##
            
            # if the monthly folder does not exist then create it first so it is available for the backup process later
            if not os.path.exists(drive + datetime.now().strftime("%Y/%m %b")):
                logger.info(f"{drive + datetime.now().strftime('%Y/%m %b')} does not exist, proceeding to create it.")
                print(f"{drive + datetime.now().strftime('%Y/%m %b')} does not exist, proceeding to create it.")
                os.makedirs(drive + datetime.now().strftime("%Y/%m %b"))
                logger.info("Created.")
                print("Created.")
                
            DNX_backup_dir = drive + datetime.now().strftime("%Y/%m %b/")        
            logger.info('Moving the latest DNX zip to the backup folder.')
            print('Moving the latest DNX zip to the backup folder.')
            print('It will only take a while.')
            shutil.copy(latest_DNX_zip_file, DNX_backup_dir)
            logger.info(f'Moved {latest_DNX_zip_file} to {DNX_backup_dir} successfully!')
            print(f'Moved {latest_DNX_zip_file} to {DNX_backup_dir} successfully!')
        os.remove(latest_DNX_zip_file)
        logger.info(f"Removed {latest_DNX_zip_file} as the backup to E and G drives completed.")
        print(f"Removed {latest_DNX_zip_file} as the backup to E and G drives completed.")
    except Exception as e:
        logger.info("Move to backup_DNX failed!")
        logger.info(e)
        print('Move to backup_DNX failed!')
        print(e)
    
def delete_oldest_zip():
    logger.info('Checking for oldest DNX zip for deletion.')
    print('Checking for oldest DNX zip for deletion.')
    all_DNX_zips = []
    for file in os.listdir(config.DNX_zip_folder):
        if os.path.isfile(config.DNX_zip_folder+file)==True and re.search("^DNX_.*zip$",file):
            all_DNX_zips.append(datetime.strptime(file[4:13], "%d%b%Y"))
    try:
        if len(all_DNX_zips) > 5:
            oldest_DNX_zip_name = "DNX_" + min(all_DNX_zips).strftime("%d%b%Y") + ".zip"
            os.remove(config.DNX_zip_folder + oldest_DNX_zip_name)
            msg = f"{oldest_DNX_zip_name} has been deleted."
            logger.info(msg)
            logger.info('-------------------------------------------------------------------------------------------------------')
            print(msg)
        else:
            raise fewer_than_five_DNX_zips_Exceptions
    except fewer_than_five_DNX_zips_Exceptions:
        msg = f"There were five or fewer DNX zips in {config.DNX_zip_folder}, so no DNX zip was deleted."
        print(msg)
        logger.info(msg)
        logger.info('-------------------------------------------------------------------------------------------------------')
        
def press_any_key_to_continue():
    print("\nEverything ended OK, press any key to close this.")
    msvcrt.getch()
    
#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("Please wait, this will take a while!")
    zip_latest_dnx()
    copy_to_DNX_zip()
    move_to_backup()
    delete_oldest_zip()
    press_any_key_to_continue()
    