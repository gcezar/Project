import RPi.GPIO as GPIO
import gps

PPS_PIN = 12

# Setup GPIO using board numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PPS_PIN, GPIO.IN)

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
 
while True:
    if GPIO.input(PPS_PIN):         
        try:
            report = session.next()
            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print report
            if report['class'] == 'TPV':
                if hasattr(report, 'time'):
                    print report.time
        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print "GPSD has terminated"
