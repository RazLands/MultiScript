# $language = "python"
# $interface = "1.0"
import csv


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        str = "Input Site Name"
        self.run_button.clicked.connect(self.open_edit_dialog(str))

    def open_edit_dialog(self, str):
        input_text = QInputDialog.getText(self, "Input Dialog", str)



def connect(host, user, pswd):
    # Prompt for a password instead of embedding it in a script...
    passwd = crt.Dialog.Prompt("Enter password for " + host, "Login", "", True)
    # Build a command-line string to pass to the Connect method.
    cmd = "/SSH2 /L %s /PASSWORD %s /C 3DES /M MD5 %s" % (user, passwd, host)
    crt.Session.Connect(cmd)


# Read the AP list given in ap 'list.csv'
def ap_list():
    AP_list_file_path = 'N:\\Share\\Serv\\LocAndExFTR\\Local\\Global Wifi\\Global Wifi Team\\Team folders\\Raz\Multi Script\\ap list.csv'
    AP_list_file = open(AP_list_file_path, 'r')
    AP_list = list(csv.reader(AP_list_file))

    return AP_list


def create_ap_list_temp(site, tempfile_path, waitStrs):
    crt.Screen.Send("show wireless ap on " + site + chr(13))
    crt.Screen.WaitForString("\n")

    cli2file(tempfile_path, waitStrs)
    reader = read_temp_file(tempfile_path)

    AP_list = [reader[6][0]]
    i = 7
    while "AP" in str(reader[i][0])[0:3]:
        AP_list.append(reader[i][0])
        i += 1

    return AP_list


def create_ap_list(AP_list_file_path, tempfile_path, waitStrs):
    file = open(tempfile_path, "r+")
    # write_file = open(AP_list_file_path, "wb")
    ws = csv.writer()


# Switch-case replacement - List of the available commands for the CLI
def switch_case(str_num):
    swticher = {
        "1": "show version on ",
        "2": "show wireless ap on "

    }
    return swticher[str_num]


# Write temporary output of command performed (single element at a time)
def cli2file(tempfile_path, waitStrs):
    tempfile = open(tempfile_path, 'wb')

    worksheet = csv.writer(tempfile)

    row = 1
    while True:
        result = crt.Screen.WaitForStrings(waitStrs)  # Wait for the linefeed at the end of each line
        if result == 2:  # We saw the prompt, we're done.
            break

        # Cut the output data from current row on screen, from char 1 to 40
        screenrow = crt.Screen.CurrentRow - 1
        readline = crt.Screen.Get(screenrow, 1, screenrow, 300)

        # Split the line ( " " delimited) and put some fields into Excel
        items = readline.strip("*").strip("-").strip().split(" ")
        worksheet.writerow(items)

        row = row + 1

    tempfile.close()


# Write the final results to 'Results.csv'
def final2file(output, results_path):
    results = open(results_path, 'wb')
    worksheet = csv.writer(results)
    worksheet.writerow(output)


# Read the earlier saved data from 'temp.csv' file
def read_temp_file(tempfile_path):
    tempfile = open(tempfile_path, 'r')
    reader = list(csv.reader(tempfile))
    reader2 = csv.reader(tempfile)

    return reader
    # return reader2


# Check for APs serial numbers
def serial_number(AP, tempfile_path, waitStrs):
    crt.Screen.Send(switch_case("1") + AP + chr(9) + chr(13))
    crt.Screen.WaitForString("\n")

    cli2file(tempfile_path, waitStrs)

    reader = read_temp_file(tempfile_path)
    result = str(reader[7][4])

    return result


# Check which AP is RFDM, l2tpv3 tunnel status and fix "Idle" tunnel
def check_tunnel(site, tempfile_path, waitStrs):
    crt.Screen.Send(switch_case("2") + site + chr(13))
    crt.Screen.WaitForString("\n")

    cli2file(tempfile_path, waitStrs)

    reader = read_temp_file(tempfile_path)
    AP_list = [reader[6][0]]

    i = 7
    while "AP" in str(reader[i][0])[0:3]:
        AP_list.append(reader[i][0])
        i += 1

    for ap in AP_list:
        crt.Screen.Send("sh l2tpv3 tunnel-summary on " + ap + chr(13))
        cli2file(tempfile_path, waitStrs)
        reader = read_temp_file(tempfile_path)
        if ("Established" not in str(reader[4])) and ("Idle" not in str(reader[4])) and (
                "STANDBY" not in str(reader[4])):
            continue

        status = str(reader[4][52])
        if status == "Established":
            crt.Dialog.MessageBox("RFDM at {}  is: {} and tunnel is Established".format(site, ap))
            return ap
        elif status == "Idle":
            break
        elif status == "STANDBY":
            crt.Dialog.MessageBox("L2tpv3 tunnel is 'STANDBY'. Please check why")
            break
    # If tunnel status is 'Idle': Fix tunnel
    if status == "Idle":
        crt.Screen.Send("l2tpv3 tunnel all up on " + ap + chr(13))
        # crt.Screen.WaitForString("\n")
        crt.Screen.Send("sh l2tpv3 tunnel-summary on " + ap + chr(13))
        crt.Dialog.MessageBox("Idle tunnel fixed. {} is the RFDM".format(ap))


# Pull Smart RF report
def smart_rf(ftp_user, ftp_pwd, site):
    crt.Screen.Send(
        "Remote-debug copy-smart-rf-report rf-domain {} write ftp://{}:{}@10.110.65.41/".format(site, ftp_user,
                                                                                                ftp_pwd) + chr(13))


# Pull Tech Support
def tech_support(ftp_user, ftp_pwd, site):
    crt.Screen.Send(
        "remote-debug copy-techsupport rf-domain {} write ftp://{}:{}@10.110.65.41/"
        .format(site, ftp_user, ftp_pwd) + chr(13))


# Program's main body
#  Create an Excel compatible spreadsheet
# os.system("python 'N:\Share\Serv\LocAndExFTR\Local\Global Wifi\Global Wifi Team\Team folders\Raz\Multi Script\\test.py'")

host = "10.0.80.80"
user = "Razl"
pswd = "Motorola3691"
# connect(host, user, pswd)

tempfile_path = 'N:\Share\Serv\LocAndExFTR\Local\Global Wifi\Global Wifi Team\Team folders\Raz\Multi Script\\temp.csv'
results_path = 'N:\Share\Serv\LocAndExFTR\Local\Global Wifi\Global Wifi Team\Team folders\Raz\Multi Script\\results.csv'
rfdm_path = 'N:\Share\Serv\LocAndExFTR\Local\Global Wifi\Global Wifi Team\Team folders\Raz\Multi Script\\RFDM.txt'
tempfile = open(tempfile_path, 'wb')
rfdm_file = open(rfdm_path, 'r')
rfdm_list = rfdm_file.read()
output = []
waitStrs = ["\n", "60#"]
AP_list = ap_list()  # Call the function to get the AP list from 'ap list.csv'

crt.Screen.Synchronous = True  # Start CRT session

# Send the initial command to run and wait for the first linefeed
# Script menu:
options = ["0", "q", "Q", "1", "2", "3", "4", "4+5"]
command_num = "0"
# try:
while True:
    command_num = str(crt.Dialog.Prompt("Enter Command:\n"
                                        "0/q - Exit Script\n"
                                        "1 - Create AP List (ap list.csv)\n"
                                        "2 - Check AP(s) serial number (from ap_list.csv)\n"
                                        "3 - Check for tunnel status\n"
                                        "4 - Pull Smart-RF report from site\n"
                                        "5 - Pull Tech Support file from site\n"
                                        "4+5 - Pull both Smart-RF and Tech Support"
                                        , "Multi Script By Raz Landsberger"))
    if command_num in options: break

# Exit script
if command_num == "0" or command_num.lower() == "q":
    pass

# Make AP List
elif command_num == "1":
    AP_list_file_path = 'N:\\Share\\Serv\\LocAndExFTR\\Local\\Global Wifi\\Global Wifi Team\\Team folders\\Raz\Multi Script\\ap list.csv'
    AP_list = open(AP_list_file_path, 'wb')
    site = str(crt.Dialog.Prompt("Enter site (Exp: AMERAR06):"))
    output = create_ap_list(site, tempfile_path, waitStrs)

# Serial number
elif command_num == "2":
    for AP in AP_list:
        result = serial_number(str(AP)[2:8], tempfile_path, waitStrs)
        output.append(result)

# Check tunnel
elif command_num == "3":
    site = str(crt.Dialog.Prompt("Enter site (Exp: AMERAR06):"))
    result = check_tunnel(site, tempfile_path, waitStrs)
    output.append(result)

# Smart RF
elif command_num == "4":
    while True:
        site = str(crt.Dialog.Prompt("***Make sure 3CDeamon is open in Secondary GLOBAL***\n\n"
                                     "Enter site (Exp: AMERAR06):"))
        if site in rfdm_list and site.isupper(): break
    ftp_user = str(crt.Dialog.Prompt("Enter FTP username"))
    ftp_pwd = str(crt.Dialog.Prompt("Enter FTP password"))
    smart_rf(ftp_user, ftp_pwd, site)

# Tech Support
elif command_num == "5":
    while True:
        site = str(crt.Dialog.Prompt("***Make sure 3CDeamon is open in Secondary GLOBAL***\n\n"
                                     "Enter site (Exp: AMERAR06):"))
        if site in rfdm_list and site.isupper(): break
    ftp_user = str(crt.Dialog.Prompt("Enter FTP username"))
    ftp_pwd = str(crt.Dialog.Prompt("Enter FTP password"))
    tech_support(ftp_user, ftp_pwd, site)

# Smart RF + Tech Support
elif command_num == "4+5":
    while True:
        site = str(crt.Dialog.Prompt("***Make sure 3CDeamon is open in Secondary GLOBAL***\n\n"
                                     "Enter site (Exp: AMERAR06):"))
        if site in rfdm_list and site.isupper(): break
    ftp_user = str(crt.Dialog.Prompt("Enter FTP username"))
    ftp_pwd = str(crt.Dialog.Prompt("Enter FTP password"))
    smart_rf(ftp_user, ftp_pwd, site)
    tech_support(ftp_user, ftp_pwd, site)

# else:
#     crt.Dialog.MessageBox("Please Choose an Option From The List")
# finally:
# Close csv file and CRT session
tempfile.close()
crt.Screen.Synchronous = False  # End CRT session

final2file(output, results_path)  # Call function to write the final results to results.csv
crt.Screen.Clear()
crt.Dialog.MessageBox("Script has DONE. Check Results.csv for results")
