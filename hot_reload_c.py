import time
import sys
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class CFileSystemEventHandler(FileSystemEventHandler):
  last_update = 0

  def on_modified(self, event):
    event_path = event.src_path.replace("\\", "/")
    if not event_path == FILE_PATH:
      return
    
    current_time = time.time()
    if not (current_time - self.last_update) > 1:
      return
    
    self.last_update = current_time
    print("Change Made!")
    compile_run_file()

def compile_run_file():
  subprocess.run(["cls"], shell=True)
  out_path = TEMP_DIR + "/" + FILE_NAME[0]
  
  try:
    subprocess.run(["gcc", FILE_PATH, "-o", out_path], check=True)
  except subprocess.CalledProcessError:
    print("Error in Compile")
    return
  
  run_command = out_path
  try:
    subprocess.run(run_command)
    footer_text()
  except:
    print("Runtime Error!")
  
def welcome_text():
  subprocess.run("cls", shell=True)
  print("Tracking changes on:", PATH_TO_FILE)
  print("File: ", FILE_NAME[0]+"."+FILE_NAME[1])

def footer_text():
  print("\n\n------------->")
  print("Waiting for changes /")

def remove_temp_dir():
  shutil.rmtree(TEMP_DIR)

def get_file_path_interactive():
  path = input("Enter File Path: ")
  sys.argv.append(path)

def process_input() -> str:
  if not len(sys.argv) > 1:
    print("File to watch not specified!")
    get_file_path_interactive()
  return sys.argv[1]

def check_file_exist(path_to_file: str):
  path_to_file = str(path_to_file).replace("\"", "")
  if not (os.path.isfile(path_to_file)):
    print("File does not exist!", path_to_file)
    exit()
  return path_to_file

def check_temp_dir_exist():
  if not os.path.isdir(TEMP_DIR):
    os.mkdir(TEMP_DIR)
  return

def set_temp_dir_path() -> str:
  current_path_file = sys.argv[0].replace("\\", "/").split("/")
  current_path = "/".join(current_path_file[:-1])
  current_path += "/"+(TEMP_DIR_NAME)
  return current_path

def startup():
  global FILE_PATH, FILE_NAME, PATH_TO_FILE, TEMP_DIR

  TEMP_DIR = set_temp_dir_path()
  check_temp_dir_exist()
  FILE_PATH = check_file_exist(process_input())

  FILE_PATH = FILE_PATH.replace("\\", "/")
  path_split = FILE_PATH.split("/")
  FILE_NAME = path_split[-1].split(".")
  PATH_TO_FILE = "/".join(path_split[:-1])

def main_loop():
  startup()
  event_handler = CFileSystemEventHandler()
  observer = Observer()
  observer.schedule(event_handler, PATH_TO_FILE)
  
  welcome_text()
  observer.start()
  footer_text()

  try:
    while (1):
      time.sleep(1)
  except KeyboardInterrupt:
    print("Ending Watch!")
    observer.stop()
    remove_temp_dir()
    exit()

TEMP_DIR = ""
TEMP_DIR_NAME = "h_reload"

FILE_PATH = ""
FILE_NAME = ""
PATH_TO_FILE = ""

print (sys.argv[0])
main_loop()