from datetime import date, datetime
from classes import BB, initialize


if __name__ == "__main__":
    y = initialize()
    x = BB()
    x.login()
    day = date.today().strftime("%A")
    rn = int(datetime.now().strftime("%H%M"))
    print("You logged in on " + str(day) + " at " + str(rn) + " hours !")
    x.gettingStarted()

    comp = './Data/.setupComp'

    with open(comp, 'w') as fileIn:
        fileIn.write('Welcome to future !!!')
    input("Press Enter to exit.")
    x.bye()
