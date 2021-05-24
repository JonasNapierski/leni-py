import datetime

class Debug:
    def print(msg, logfile=None):
        output_msg = f"[{str(datetime.datetime.now().isoformat())}] {str(msg)}"
        print(output_msg)
        if logfile == None:
            return

        try:
            with open(logfile, "a") as f:
                f.write(output_msg +"\n")
                f.close()
        except IOError as e:
            e.write()
