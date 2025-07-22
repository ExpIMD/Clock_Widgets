import clock_simulator as cs

try: # interactive part of the project
    index: int = int(input("Choose a clock category:\n0. Round clock\n1. Round clock with pendulum\n2. Digital clock\n"))
    match index:
        case 0:
            a = cs.round_clock()
            a.run()
        case 1:
            a = cs.pendulum_clock()
            a.run()
        case 2:
            a = cs.digital_clock()
            a.run()
        case _:
            print("Unknown number. Restart the program")
except ValueError:
    print("Invalid literal for input. Restart the program")