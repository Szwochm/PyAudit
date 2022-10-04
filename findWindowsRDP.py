#! py -3

import wmi

def main():
    rval = 0  # Default: Check passes.
    timeframe =-1

    # Initialize WMI objects and query.
    wmi_o = wmi.WMI('.')
    wql = ("SELECT * FROM Win32_NTLogEvent WHERE Logfile="
           "'Security' AND EventCode='4624' AND EventType='10'")

    # Query WMI object.
    wql_r = wmi_o.query(wql)

    if len(wql_r):
        rval = -1  # Check fails.

    print("Results from event search...")
    print(wql)
    for entry in wql_r:
        print(entry)
        # Add logic for specified time frame

    return rval



if __name__ == '__main__':
    main()
