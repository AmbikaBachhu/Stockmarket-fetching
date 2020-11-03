from nsetools import Nse
import time
import urllib.request
import urllib.error

data_top = {}
lsave = time.time()
nse = Nse()
top = nse.get_top_gainers()


def autoSave():
    global lsave
    curr_time = time.time()
    if (curr_time >= lsave):
        with open('top', 'a+') as f:
            f.write(str(data_top))
        lsave = time.time()
        print("AutoSaved at : " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lsave)))


def main():
    t_list = top

    try:
        while (True):
            print("Starting get_quote for ", t_list)
            autoSave()
            print("Taking a nap!")
            time.sleep(10)
            print("\n\n")
    except Exception as e:
        print(e)
    finally:
        with open('top', 'a+') as f:
            f.write(str(data_top))

main()




