import os
import subprocess
import time
import random
import logging

def Mancala(players):
    global window_x,window_y,game_mode,current_player,in_hand,hand_pos,win_status,slots
    do_log = False
    if do_log:        
        LOG_FILENAME = "logfile.txt"
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode="w")
    
    #Variables
    window_x = 68
    window_y = 14
    game_mode = 0
    current_player = 1
    in_hand = 0
    hand_pos = 0
    win_status = 0
    slots = []
    for x in range(2):
        for y in range(6):
            slots.append(4)
        slots.append(0)

    #Functions:
    def msg(_input):
        if do_log:
            logging.debug(" : " + str(_input))
        else:
            pass
       
    def rgbme_new(rgbin): #Script to color text (New and simple)
            return ("\033[38;2;{};{};{}m".format(rgbin[0],rgbin[1],rgbin[2]))
        
    def drawbox(ammount):
        return (rgbme_new([17, 47, 75]) + "█"*ammount + rgbme_new([255,255,255]))

    def fix_nr(_input):
        if len(str(_input)) == 1:
            return ("0" + str(_input))
        else:
            return str(_input)

    def checkhand(pos_input):
        global hand_pos, in_hand
        if hand_pos == pos_input:
            return "[{}]".format(fix_nr(in_hand))
        else:
            return drawbox(4)

    def pickup(selected_input):
        if game_mode == 0:
            delay = 0
        else:
            delay = 0.5
        msg("---pickup()") 
        global in_hand,slots,hand_pos
        selected = selected_input
        if selected == 7 or selected == 14:
            print("Can not pick up from the Mancala")
            msg("Tried to pick up from Mancala") 
        else:
            if slots[selected-1] == 0:
                print("Selected block was empty")
                msg("Selected block was empty") 
            else:
                temp = slots[selected-1] + selected_input
                if in_hand == 0:
                    in_hand = slots[selected-1]
                    msg("picked up from slot : {}".format(selected-1)) 
                    slots[selected-1] = 0
                    msg("set slot {} to 0".format(selected-1)) 
                    render_screen()
                    time.sleep(delay)
                    for i in range(1,in_hand+1,1):
                        if selected+i > 14:
                            selected -= 14
                            msg("reduced selected by 14 cause it looped around") 
                        slots[(selected-1)+i] += 1
                        in_hand -= 1
                        msg("in hand reduced by one") 
                        hand_pos = selected + i
                        msg("hand pos updated") 
                        render_screen()
                        time.sleep(delay)
                    while temp > 14:
                        if temp > 14:
                            temp -= 14
                    msg("---pickup() END by return temp") 
                    return temp
                msg("---pickup() END by in_hand != 0 ") 

    def render_screen():
        if game_mode != 0:
            if (sum(slots) + in_hand) != 48:
                msg("Tried to render screen but (sum(slots) + in_hand) was {}".format((sum(slots) + in_hand))) 
                while True:
                    print("ERROR! : {}".format((sum(slots) + in_hand)))
            os.system('cls')
            print(drawbox(window_x))
            print(drawbox(8) + fix_nr(slots[12]) + drawbox(8) + fix_nr(slots[11]) + drawbox(8) + fix_nr(slots[10]) + drawbox(8) + fix_nr(slots[9]) + drawbox(8) + fix_nr(slots[8]) + drawbox(8) + fix_nr(slots[7]) + drawbox(8))
            print(drawbox(window_x))
            print(drawbox(7) + "(13)" + drawbox(6) + "(12)" + drawbox(6) + "(11)" + drawbox(6) + "(10)" + drawbox(6) + "(09)" + drawbox(6) + "(08)" + drawbox(7))
            
            print(drawbox(window_x))
            print(drawbox(7) + checkhand(13) + drawbox(6) + checkhand(12) + drawbox(6) + checkhand(11) + drawbox(6) + checkhand(10) + drawbox(6) + checkhand(9) + drawbox(6) + checkhand(8) + drawbox(7))
            print(drawbox(window_x))
                   
            print (drawbox(2) + fix_nr(slots[13]) + drawbox(2) + checkhand(14) + drawbox(48) + checkhand(7) + drawbox(2) + fix_nr(slots[6])  + drawbox(2))
             
            print(drawbox(window_x))
            print(drawbox(7) + checkhand(1) + drawbox(6) + checkhand(2) + drawbox(6) + checkhand(3) + drawbox(6) + checkhand(4) + drawbox(6) + checkhand(5) + drawbox(6) + checkhand(6) + drawbox(7))
            print(drawbox(window_x))
            
            print(drawbox(7) + "(01)" + drawbox(6) + "(02)" + drawbox(6) + "(03)" + drawbox(6) + "(04)" + drawbox(6) + "(05)" + drawbox(6) + "(06)" + drawbox(7))
            print(drawbox(window_x))
            print(drawbox(8) + fix_nr(slots[0]) + drawbox(8) + fix_nr(slots[1]) + drawbox(8) + fix_nr(slots[2]) + drawbox(8) + fix_nr(slots[3]) + drawbox(8) + fix_nr(slots[4]) + drawbox(8) + fix_nr(slots[5]) + drawbox(8))
            print(drawbox(window_x))
            
    def get_moves(to_render):
        global current_player
        moves = []
        offset = 0
        if current_player == 2:
            offset = 7 
        for x in range(0 + offset,6 + offset,1):
            if slots[x] != 0:
                moves.append(x +1)
        if to_render:       
            output = ""
            for x in moves:
                output = output + str(x) +  ", "    
            output = output[:-2]  
            return output
        else:
            return moves

    #INIT:                        
    os.system('mode con: cols={} lines={}'.format(window_x,window_y + 3)) #Set Resolution
    subprocess.call('', shell=True) #Fix Colors
    game_mode = players
    #int(input("1 or 2 players? : "))
    msg(str(game_mode))

    #Main Script:
    while win_status == 0:
        msg(str(slots))
        msg(str(in_hand))
        msg(str(sum(slots) + in_hand))

        temp = 0
        for x in range(0,6,1):
            temp = temp + int(slots[x])
        if temp == 0:
            win_status = 99
            break
            
      
        temp = 0
        for x in range(7,13,1):
            temp = temp + int(slots[x])
        if temp == 0:
            win_status = 99
            break
        
        #    12 11 10 9  8  7       
        # 13                   6   
        #    0  1  2  3  4  5                  
        hand_pos = 0        
        render_screen()     
        
        if win_status == 0:
            next_move = "NONE"
            while next_move == "NONE":
                try: 
                    if ((current_player == 2 and game_mode == 2) or current_player == 1) and game_mode != 0:
                        next_move = int(input("Player {}'s turn. Available moves : {}\n".format(current_player,get_moves(True))))
                    else:
                        if game_mode != 0:
                            print("Waiting for AI...")
                            time.sleep(random.uniform(0.5, 2))
                        next_move = get_moves(False)[(random.randint(0,(len(get_moves(False)) - 1)))]
                except:
                    render_screen()
                    next_move = "NONE"

            if (current_player == 1 and (next_move > 0 and next_move < 7)) or (current_player == 2 and (next_move > 6 and next_move < 14)):
                hand_pos = next_move
                render_screen()
                #time.sleep(0.5)
                landed_in = (pickup(next_move)-1)
                msg(str(landed_in) + " is Landed in")
                if current_player == 1:
                    if slots[landed_in] == 1 and (landed_in > -1 and landed_in < 6):
                        slots[6] = slots[landed_in] + slots[12 - landed_in] + slots[6]
                        slots[landed_in] = 0
                        slots[12 - landed_in] = 0                       
                    if landed_in == 6:
                        current_player = 1
                    else:
                        current_player = 2
                else:
                    if slots[landed_in] == 1 and (landed_in > 6 and landed_in < 13):
                        slots[13] = slots[landed_in] + slots[12 - landed_in] + slots[13]
                        slots[landed_in] = 0
                        slots[12 - landed_in] = 0                
                    if landed_in == 13:
                        current_player = 2
                    else:
                        current_player = 1                 
                msg(str(slots))
                render_screen()
     
    for y in range(0,6,1):  #Put all in P1's row in P1's Mancala
        slots[6] += int(slots[y])
        slots[y] = 0
    for y in range(7,13,1): #Put all in P2's row in P2's Mancala
        slots[13] += int(slots[y])
        slots[y] = 0


    if slots[6] > slots[13]: #Decide who wins
        win_status = 1
    else:
        win_status = 2

    if game_mode == 0: #Handle Win
        print(str(win_status) + " wins, " + str(slots[6] + slots[13] + in_hand) + "pieces")
    else:
        hand_pos = 0
        render_screen()
        if slots[6] + slots[13] == 48:
            x = input("Player {} wins!".format(win_status))
        else:
            x = input("Player {} wins, but total is : {}".format(win_status,slots[6] + slots[13]))

if __name__ == "__main__":
    os.system('mode con: cols={} lines={}'.format(68,14 + 3)) #Set Resolution
    Mancala(int(input("How many players? : ")))