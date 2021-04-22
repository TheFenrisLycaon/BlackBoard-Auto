from datetime import date
from classes import BB, initialize

if __name__ == "__main__":
    timestamps = [1000, 1045, 1145, 1245, 1330, 1430, 1530, 1630]
    y = initialize()
    y.set_opt()
    x = BB()
    x.login()
    day = date.today().strftime("%A")
    rn = int(date.now().strftime("%H%M"))
    print("You logged in on " + str(day) + " at " + str(rn) + " hours !")
    x.begin(day, rn)
    k = input("Press any key to exit...")
